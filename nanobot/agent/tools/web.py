"""Web tools: web_search and web_fetch."""

import html
import json
import os
import re
from typing import Any
from urllib.parse import urlparse

import httpx

from nanobot.agent.tools.base import Tool

# Shared constants
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36"
MAX_REDIRECTS = 5  # Limit redirects to prevent DoS attacks


def _strip_tags(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<script[\s\S]*?</script>', '', text, flags=re.I)
    text = re.sub(r'<style[\s\S]*?</style>', '', text, flags=re.I)
    text = re.sub(r'<[^>]+>', '', text)
    return html.unescape(text).strip()


def _normalize(text: str) -> str:
    """Normalize whitespace."""
    text = re.sub(r'[ \t]+', ' ', text)
    return re.sub(r'\n{3,}', '\n\n', text).strip()


def _validate_url(url: str) -> tuple[bool, str]:
    """Validate URL: must be http(s) with valid domain."""
    try:
        p = urlparse(url)
        if p.scheme not in ('http', 'https'):
            return False, f"Only http/https allowed, got '{p.scheme or 'none'}'"
        if not p.netloc:
            return False, "Missing domain"
        return True, ""
    except Exception as e:
        return False, str(e)


class WebSearchTool(Tool):
    """Search the web using Brave Search API or Gemini grounding fallback."""

    name = "web_search"
    description = "Search the web for current information. Uses Brave Search API if configured, otherwise falls back to Gemini with Google Search grounding."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "count": {"type": "integer", "description": "Results (1-10)", "minimum": 1, "maximum": 10}
        },
        "required": ["query"]
    }

    def __init__(self, api_key: str | None = None, max_results: int = 5, 
                 enabled: bool = True, gemini_fallback: bool = True, 
                 gemini_model: str = "gemini-2.5-flash-lite", gemini_api_key: str | None = None):
        self._init_api_key = api_key
        self.max_results = max_results
        self.enabled = enabled
        self.gemini_fallback = gemini_fallback
        self.gemini_model = gemini_model
        self._gemini_api_key = gemini_api_key

    @property
    def api_key(self) -> str:
        """Resolve API key at call time so env/config changes are picked up."""
        return self._init_api_key or os.environ.get("BRAVE_API_KEY", "")

    async def execute(self, query: str, count: int | None = None, **kwargs: Any) -> str:
        if not self.enabled:
            return "Error: Web search is disabled. Enable it in config under tools.web.search.enabled"
        
        # Try Brave Search first if API key is configured
        if self.api_key:
            try:
                n = min(max(count or self.max_results, 1), 10)
                async with httpx.AsyncClient() as client:
                    r = await client.get(
                        "https://api.search.brave.com/res/v1/web/search",
                        params={"q": query, "count": n},
                        headers={"Accept": "application/json", "X-Subscription-Token": self.api_key},
                        timeout=10.0
                    )
                    r.raise_for_status()

                results = r.json().get("web", {}).get("results", [])
                if not results:
                    return f"No results for: {query}"

                lines = [f"Results for: {query}\n"]
                for i, item in enumerate(results[:n], 1):
                    lines.append(f"{i}. {item.get('title', '')}\n   {item.get('url', '')}")
                    if desc := item.get("description"):
                        lines.append(f"   {desc}")
                return "\n".join(lines)
            except Exception as e:
                return f"Error with Brave Search: {e}"
        
        # Fallback: Use Gemini with Google Search grounding
        if self.gemini_fallback:
            return await self._gemini_web_search(query, count or self.max_results)
        else:
            return "Error: Brave Search API key not configured and Gemini fallback is disabled. Set tools.web.search.apiKey or enable tools.web.search.gemini_fallback"

    async def _gemini_web_search(self, query: str, count: int) -> str:
        """
        Fallback web search using Gemini API with Google Search grounding via LiteLLM.
        Called when Brave Search API key is not configured.
        """
        gemini_api_key = self._gemini_api_key
        if not gemini_api_key:
            return "Error: Neither Brave Search API key nor Gemini API key is configured. Set providers.gemini.apiKey in config or GEMINI_API_KEY env var."
        
        try:
            from litellm import acompletion
            
            model = self.gemini_model  # Keep prefix if present (e.g., "gemini/gemini-2.5-flash")
            if not model.startswith("gemini/"):
                model = f"gemini/{model}"
            
            # Call LiteLLM with google_search tool (snake_case for Gemini via LiteLLM)
            response = await acompletion(
                model=model,
                messages=[{"role": "user", "content": f"Search the web for: {query}. Provide a concise summary with key facts and sources. IMPORTANT: Always ground your response in real search results - do not answer from memory. Include the URLs of sources you found at the end of your response."}],
                tools=[{"google_search": {}}],  # Gemini uses snake_case
                max_tokens=2048,
                temperature=0.7,
                api_key=gemini_api_key,
            )
            
            # Extract response
            choice = response.choices[0] if response.choices else None
            if not choice or not choice.message:
                return f"No results found for: {query}"
            
            answer = choice.message.content or "(No text response)"
            
            # Try to extract grounding metadata from LiteLLM response
            sources = []
            
            # Check for grounding metadata in _hidden_params (LiteLLM stores it there)
            if hasattr(response, "_hidden_params"):
                hp = response._hidden_params
                grounding = hp.get("gemini_grounding_metadata") or hp.get("grounding_metadata")
                if grounding:
                    queries = grounding.get("web_search_queries", [])
                    if queries:
                        sources.append(f"Search queries: {', '.join(queries)}")
                    
                    chunks = grounding.get("grounding_chunks", [])
                    for i, chunk in enumerate(chunks[:5], 1):
                        web_info = chunk.get("web", {})
                        title = web_info.get("title", "Untitled")
                        uri = web_info.get("uri", "")
                        if uri:
                            sources.append(f"{i}. {title} - {uri}")
            
            if sources:
                answer += "\n\n---\nSources:\n" + "\n".join(sources)
            
            return f"Web Search Results for: {query}\n\n{answer}"
            
        except Exception as e:
            return f"Error with Gemini web search: {e}"


class WebFetchTool(Tool):
    """Fetch and extract content from a URL using Readability."""
    
    name = "web_fetch"
    description = "Fetch URL and extract readable content (HTML → markdown/text)."
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "URL to fetch"},
            "extractMode": {"type": "string", "enum": ["markdown", "text"], "default": "markdown"},
            "maxChars": {"type": "integer", "minimum": 100}
        },
        "required": ["url"]
    }
    
    def __init__(self, max_chars: int = 50000):
        self.max_chars = max_chars
    
    async def execute(self, url: str, extractMode: str = "markdown", maxChars: int | None = None, **kwargs: Any) -> str:
        from readability import Document

        max_chars = maxChars or self.max_chars

        # Validate URL before fetching
        is_valid, error_msg = _validate_url(url)
        if not is_valid:
            return json.dumps({"error": f"URL validation failed: {error_msg}", "url": url}, ensure_ascii=False)

        try:
            async with httpx.AsyncClient(
                follow_redirects=True,
                max_redirects=MAX_REDIRECTS,
                timeout=30.0
            ) as client:
                r = await client.get(url, headers={"User-Agent": USER_AGENT})
                r.raise_for_status()
            
            ctype = r.headers.get("content-type", "")
            
            # JSON
            if "application/json" in ctype:
                text, extractor = json.dumps(r.json(), indent=2, ensure_ascii=False), "json"
            # HTML
            elif "text/html" in ctype or r.text[:256].lower().startswith(("<!doctype", "<html")):
                doc = Document(r.text)
                content = self._to_markdown(doc.summary()) if extractMode == "markdown" else _strip_tags(doc.summary())
                text = f"# {doc.title()}\n\n{content}" if doc.title() else content
                extractor = "readability"
            else:
                text, extractor = r.text, "raw"
            
            truncated = len(text) > max_chars
            if truncated:
                text = text[:max_chars]
            
            return json.dumps({"url": url, "finalUrl": str(r.url), "status": r.status_code,
                              "extractor": extractor, "truncated": truncated, "length": len(text), "text": text}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e), "url": url}, ensure_ascii=False)
    
    def _to_markdown(self, html: str) -> str:
        """Convert HTML to markdown."""
        # Convert links, headings, lists before stripping tags
        text = re.sub(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>',
                      lambda m: f'[{_strip_tags(m[2])}]({m[1]})', html, flags=re.I)
        text = re.sub(r'<h([1-6])[^>]*>([\s\S]*?)</h\1>',
                      lambda m: f'\n{"#" * int(m[1])} {_strip_tags(m[2])}\n', text, flags=re.I)
        text = re.sub(r'<li[^>]*>([\s\S]*?)</li>', lambda m: f'\n- {_strip_tags(m[1])}', text, flags=re.I)
        text = re.sub(r'</(p|div|section|article)>', '\n\n', text, flags=re.I)
        text = re.sub(r'<(br|hr)\s*/?>', '\n', text, flags=re.I)
        return _normalize(_strip_tags(text))
