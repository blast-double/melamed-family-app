*Last Edited: 2026-03-25 14:30*

# Tavily Comprehensive Guide

> Tavily is a search engine optimized for LLMs and AI agents. It handles searching, scraping, filtering, and extracting relevant information from the web — designed specifically for agentic workflows, not human browsing.

---

## Table of Contents

1. [Overview](#overview)
2. [Core Endpoints](#core-endpoints)
   - [Search](#1-search)
   - [Extract](#2-extract)
   - [Crawl](#3-crawl)
   - [Map](#4-map)
   - [Research](#5-research)
3. [Python SDK](#python-sdk)
4. [MCP Server](#mcp-server)
5. [Agent Skills](#agent-skills)
6. [Use Cases](#use-cases)
7. [LangChain Integration](#langchain-integration)
8. [Anthropic Integration](#anthropic-integration)
9. [Best Practices](#best-practices)
10. [Pricing & Rate Limits](#pricing--rate-limits)

---

## Overview

**What Tavily Does**: Unlike traditional search APIs (Serp, Google) that return links to potentially-related articles, Tavily returns **optimized, extracted content** ready for LLM consumption. It handles:

- Web search with agent-optimized results
- Content extraction from URLs
- Website crawling with semantic filtering
- Site structure mapping
- AI-powered deep research with cited reports

**Key Advantages**:
- Results are pre-filtered and ranked for relevance to the query
- Content is extracted and cleaned (no raw HTML)
- Supports `include_answer` for short LLM-generated answers (great for agent-to-agent communication)
- Custom fields like `context` and token limits for optimal LLM context sizing
- Async support for parallel queries

**Base URL**: `https://api.tavily.com`
**Auth**: Bearer token (`Authorization: Bearer tvly-YOUR_API_KEY`)

---

## Core Endpoints

### 1. Search

**`POST /search`** — Web search with agent-optimized results.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` (required) | `str` | — | The search query (keep under 400 chars) |
| `search_depth` | `enum` | `basic` | `ultra-fast` → `fast` → `basic` → `advanced` (latency vs relevance tradeoff) |
| `topic` | `enum` | `general` | `general` or `news` (news includes `published_date` metadata) |
| `max_results` | `int` | `5` | Number of results to return |
| `include_answer` | `bool/enum` | `false` | `true`, `basic`, or `advanced` — returns a short LLM-generated answer |
| `include_raw_content` | `bool` | `false` | Returns full extracted page content per result |
| `include_images` | `bool` | `false` | Returns query-related images |
| `include_image_descriptions` | `bool` | `false` | Includes descriptions with images |
| `include_domains` | `list[str]` | `[]` | Restrict to specific domains |
| `exclude_domains` | `list[str]` | `[]` | Exclude specific domains |
| `time_range` | `enum` | `null` | `day`, `week`, `month`, `year` |
| `start_date` | `str` | `""` | Filter results after date (`YYYY-MM-DD`) |
| `end_date` | `str` | `""` | Filter results before date (`YYYY-MM-DD`) |
| `country` | `str` | `""` | Boost results from a country (full name, not ISO code) |
| `auto_parameters` | `bool` | `false` | Auto-configure params based on query intent |
| `exact_match` | `bool` | `false` | Only return results containing exact quoted phrases |

#### Response Schema

```json
{
  "query": "string",
  "answer": "string (if include_answer=true)",
  "results": [
    {
      "title": "string",
      "url": "string",
      "content": "string (snippet)",
      "raw_content": "string (if include_raw_content=true)",
      "score": 0.99,
      "published_date": "string (if topic=news)"
    }
  ],
  "images": [
    {
      "url": "string",
      "description": "string (if include_image_descriptions=true)"
    }
  ],
  "response_time": 1.23
}
```

#### Python SDK

```python
from tavily import TavilyClient

client = TavilyClient(api_key="tvly-YOUR_API_KEY")

# Basic search
response = client.search("Who is Leo Messi?")

# Advanced search with filters
response = client.search(
    query="AI regulations 2026",
    search_depth="advanced",
    topic="news",
    max_results=10,
    include_answer=True,
    time_range="month",
    include_domains=["reuters.com", "bloomberg.com"]
)

# Exact match for specific names/phrases
response = client.search(
    query='"John Smith" CEO Acme Corp',
    exact_match=True
)
```

#### Search Depth Guide

| Depth | Latency | Use Case |
|-------|---------|----------|
| `ultra-fast` | Lowest | Simple factual queries, latency-critical apps |
| `fast` | Low | High relevance with optimized latency |
| `basic` | Medium | General queries (default) |
| `advanced` | Highest | Complex queries, higher quality results, 2 credits |

---

### 2. Extract

**`POST /extract`** — Extract clean content from one or more URLs.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `urls` (required) | `str` or `list[str]` | — | URL(s) to extract content from |
| `query` | `str` | `""` | Rerank extracted chunks by relevance to this query |
| `chunks_per_source` | `int` | `3` | Number of content chunks per URL |
| `extract_depth` | `enum` | `basic` | `basic` or `advanced` (advanced for tables, structured data, protected sites) |
| `format` | `enum` | `markdown` | `markdown` or `text` |
| `include_images` | `bool` | `false` | Include images from pages |

#### Response Schema

```json
{
  "results": [
    {
      "url": "string",
      "raw_content": "string (extracted content)",
      "images": ["string"]
    }
  ],
  "failed_results": [
    {
      "url": "string",
      "error": "string"
    }
  ],
  "response_time": 1.23
}
```

#### Python SDK

```python
# Basic extraction
response = client.extract("https://example.com/article")

# Multi-URL with query reranking
response = client.extract(
    urls=[
        "https://example.com/page1",
        "https://example.com/page2"
    ],
    query="machine learning applications in healthcare",
    chunks_per_source=3,
    extract_depth="advanced"
)
```

#### When to Use `extract_depth=advanced`

- LinkedIn profiles and protected sites
- Pages with tables and structured data
- Embedded content and media
- Complex page layouts

---

### 3. Crawl

**`POST /crawl`** — Crawl a website starting from a URL, extracting content with semantic filtering.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` (required) | `str` | — | Root URL to begin crawling |
| `instructions` | `str` | `""` | Natural language instructions for what to extract (doubles credit cost) |
| `max_depth` | `int` | `1` | How many levels deep to crawl (1-5) |
| `max_breadth` | `int` | `20` | Max links to follow per page |
| `limit` | `int` | `50` | Total max pages to crawl |
| `select_paths` | `list[str]` | `[]` | Regex patterns for URL paths to include |
| `select_domains` | `list[str]` | `[]` | Regex patterns for domains to include |
| `exclude_paths` | `list[str]` | `[]` | Regex patterns for URL paths to exclude |
| `exclude_domains` | `list[str]` | `[]` | Regex patterns for domains to exclude |
| `extract_depth` | `enum` | `basic` | `basic` or `advanced` |
| `format` | `enum` | `markdown` | `markdown` or `text` |
| `chunks_per_source` | `int` | `3` | Content chunks per page |
| `allow_external` | `bool` | `true` | Whether to include external links |
| `include_favicon` | `bool` | `false` | Include favicon URLs |

#### Response Schema

```json
{
  "base_url": "string",
  "results": [
    {
      "url": "string",
      "raw_content": "string",
      "images": ["string"]
    }
  ],
  "failed_results": [],
  "response_time": 9.14,
  "usage": { "credits": 5 },
  "request_id": "string"
}
```

#### Python SDK

```python
# Crawl with semantic instructions
response = client.crawl(
    url="https://docs.example.com",
    max_depth=3,
    limit=50,
    instructions="Find all pages about authentication and API keys"
)

# Targeted crawl with path filters
response = client.crawl(
    url="https://example.com",
    max_depth=2,
    select_paths=["/docs/.*", "/api/v1.*"],
    exclude_paths=["/private/.*", "/admin/.*"],
    extract_depth="advanced"
)
```

---

### 4. Map

**`POST /map`** — Discover and list all URLs on a website (sitemap generation).

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` (required) | `str` | — | Root URL to begin mapping |
| `instructions` | `str` | `""` | Natural language filter for URL discovery (doubles credit cost) |
| `max_depth` | `int` | `1` | How deep to explore (1-5) |
| `max_breadth` | `int` | `20` | Max links per page |
| `limit` | `int` | `50` | Total max links to process |
| `select_paths` | `list[str]` | `[]` | Regex patterns for paths to include |
| `select_domains` | `list[str]` | `[]` | Regex patterns for domains |
| `allow_external` | `bool` | `true` | Include external links |

#### Response Schema

```json
{
  "base_url": "string",
  "results": ["url1", "url2", "..."],
  "response_time": 1.23,
  "usage": { "credits": 1 },
  "request_id": "string"
}
```

#### Python SDK

```python
# Map a site's structure
response = client.map(
    url="https://docs.example.com",
    max_depth=2,
    limit=30,
    instructions="Find pages about citrus fruits"
)

for url in response["results"]:
    print(url)
```

#### Map → Crawl Pattern

Use Map to discover URLs, then Crawl to extract content from the interesting ones:

```python
# Step 1: Discover the site structure
sitemap = client.map(url="https://docs.example.com", max_depth=2)

# Step 2: Filter URLs of interest
api_docs = [url for url in sitemap["results"] if "/api/" in url]

# Step 3: Extract content from those URLs
for url in api_docs:
    content = client.extract(urls=[url], extract_depth="advanced")
```

---

### 5. Research

**`POST /research`** — AI-powered comprehensive research that produces a cited report.

This is the most powerful endpoint. It orchestrates multiple searches, extractions, and analysis steps to produce a full research report with citations.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` (required) | `str` | — | The research task or question |
| `model` | `enum` | `auto` | `mini` (narrow/fast), `pro` (comprehensive/multi-agent), `auto` |
| `citation_format` | `enum` | `numbered` | `numbered`, `mla`, `apa`, `chicago` |
| `output_schema` | `object` | `null` | JSON Schema to structure the output |
| `max_results` | `int` | — | Control the breadth of research |

#### Response Schema

```json
{
  "request_id": "string",
  "created_at": "2025-01-15T10:30:00Z",
  "status": "completed",
  "input": "string",
  "model": "mini",
  "output": "string (the full research report with citations)",
  "sources": [
    {
      "url": "string",
      "title": "string"
    }
  ],
  "response_time": 45.2
}
```

#### Model Selection Guide

| Model | Best For | Credit Range |
|-------|----------|-------------|
| `pro` | Comprehensive, multi-agent research for complex, multi-domain topics | 15–250 credits |
| `mini` | Targeted, efficient research for narrow or well-scoped questions | 4–110 credits |
| `auto` | When unsure how complex the research will be | Varies |

#### Python SDK

```python
# Basic research
response = client.research(
    input="What are the latest developments in AI agents?",
    model="mini"
)
print(response["output"])

# Structured output research
response = client.research(
    input="Research Acme Corp's 2026 outlook",
    model="pro",
    output_schema={
        "properties": {
            "company": {"type": "string", "description": "Company name"},
            "market_position": {"type": "string", "description": "Current market position"},
            "key_metrics": {
                "type": "array",
                "description": "Key performance metrics",
                "items": {"type": "string"}
            },
            "competitors": {
                "type": "array",
                "description": "Main competitors",
                "items": {"type": "string"}
            },
            "outlook": {"type": "string", "description": "2026 outlook analysis"}
        },
        "required": ["company", "market_position"]
    }
)
```

#### Research Prompting Tips

- Be specific about what you want: company overview, competitive analysis, financial data
- Include context the model should already know to avoid redundant research
- Use `output_schema` for programmatic consumption of results
- Break very broad topics into focused research tasks

**Example Prompts**:
```
"Research the company ____ and its 2026 outlook. Provide a brief overview
of the company, its products, services, and market position."

"Conduct a competitive analysis of ____ in 2026. Identify their main
competitors, compare market positioning, and analyze key differentiators."

"We're evaluating Notion as a potential partner. We already know they
primarily serve SMB and mid-market teams. Research Notion's 2026 outlook,
including market position, growth risks, and where a partnership could
be most valuable. Include citations."
```

---

## Python SDK

### Installation

```bash
pip install tavily-python
```

### Client Instantiation

```python
from tavily import TavilyClient

# Synchronous client
client = TavilyClient(api_key="tvly-YOUR_API_KEY")

# Or use environment variable TAVILY_API_KEY
client = TavilyClient()

# With project tracking
client = TavilyClient(api_key="tvly-YOUR_API_KEY", project_id="my-project")
```

### Async Client

```python
from tavily import AsyncTavilyClient

async_client = AsyncTavilyClient(api_key="tvly-YOUR_API_KEY")

# All methods are the same, just await them
response = await async_client.search("query")
response = await async_client.extract(urls=["..."])
response = await async_client.crawl(url="...")
response = await async_client.map(url="...")
response = await async_client.research(input="...")
```

### Proxy Support

```python
client = TavilyClient(api_key="tvly-YOUR_API_KEY", proxies={
    "http": "http://proxy:8080",
    "https": "https://proxy:8080"
})
```

### SDK Methods Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `client.search(query, ...)` | `/search` | Web search |
| `client.extract(urls, ...)` | `/extract` | Content extraction |
| `client.crawl(url, ...)` | `/crawl` | Website crawling |
| `client.map(url, ...)` | `/map` | URL discovery |
| `client.research(input, ...)` | `/research` | Deep research reports |

### Hybrid RAG (Advanced)

The SDK includes a `TavilyHybridClient` for combining Tavily search with MongoDB vector search:

```python
from tavily import TavilyHybridClient

hybrid_client = TavilyHybridClient(
    api_key="tvly-YOUR_API_KEY",
    db_provider="mongodb",
    collection=mongo_collection,
    index="vector_index",
    embeddings_model="cohere",
    cohere_api_key="..."
)

# Search combines web + local vector results
results = hybrid_client.search("query")
```

---

## MCP Server

Tavily provides an MCP (Model Context Protocol) server for direct integration with AI assistants like Claude.

### Remote MCP (Recommended)

URL: `https://mcp.tavily.com/mcp?tavilyApiKey=tvly-YOUR_API_KEY`

Supports OAuth authentication as an alternative to API key in URL.

### Local Installation

```json
{
  "mcpServers": {
    "tavily-mcp": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@latest"],
      "env": {
        "TAVILY_API_KEY": "tvly-YOUR_API_KEY"
      }
    }
  }
}
```

### MCP Default Parameters

Configure default search behavior for all MCP requests:

```json
{
  "mcpServers": {
    "tavily-mcp": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@latest"],
      "env": {
        "TAVILY_API_KEY": "your-api-key",
        "DEFAULT_PARAMETERS": "{\"include_images\": true, \"max_results\": 15, \"search_depth\": \"advanced\"}"
      }
    }
  }
}
```

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `tavily_search` | Web search with all search parameters |
| `tavily_extract` | Extract content from URLs |
| `tavily_crawl` | Crawl websites with semantic filtering |
| `tavily_map` | Discover site structure |
| `tavily_research` | Deep AI-powered research |
| `tavily_skill` | Search library/API documentation |

---

## Agent Skills

Tavily provides official skills for AI coding agents (Claude Code, etc.) that define best practices for using each endpoint.

### Installation

```bash
# Install the skills CLI
curl -fsSL https://skills.sh | bash

# Add all skills
npx skills add tavily-ai/skills --all

# Add a specific skill
npx skills add tavily-ai/skills --skill tavily-search
```

### Available Skills

| Skill | Description |
|-------|-------------|
| `tavily-search` | Web search with agent-optimized results |
| `tavily-extract` | Extract clean markdown/text from URLs |
| `tavily-crawl` | Crawl a website and extract content with semantic filtering |
| `tavily-map` | Discover and list all URLs on a website |
| `tavily-research` | AI-powered research that produces a cited report |
| `tavily-best-practices` | Reference docs for building production-ready integrations |

### Usage

Skills can be invoked automatically (by natural language) or explicitly:

```
# Automatic
"Search for the latest news on AI regulations"
"Crawl the Stripe API docs and save them locally"
"Research the competitive landscape for AI coding assistants"

# Explicit
/tavily-search current React best practices
/tavily-extract https://example.com/docs
/tavily-crawl https://docs.stripe.com
/tavily-research AI agent frameworks and save to report.json
/tavily-best-practices
```

---

## Use Cases

### 1. Chat Agent
Build conversational agents with real-time web search. Tavily provides compact `content` snippets for low-latency multi-turn chat, with source URLs for citations.

**Key pattern**: Use LangChain integration for intelligent routing — the agent decides when to search, extract, or crawl based on conversation context.

### 2. Data Enrichment
Enrich spreadsheets and datasets with web data. Upload a CSV with entities (companies, people, products), define columns to fill, and Tavily searches + extracts the data.

**Key pattern**: Parallel async searches per row, extract specific data points, export as CSV.

### 3. Company Research (→ Topic Research)
Deep-dive research on any company or topic. This is Tavily's most popular use case.

**Key pattern**: Multiple focused sub-queries → aggregate results → LLM synthesis with citations.

**Repurposing for Topic Research**: The company researcher pattern generalizes to any topic. Replace company-specific queries with topic-specific ones:

```python
# Company research queries
queries = [
    f"What does {company} do?",
    f"{company} financial performance 2026",
    f"{company} competitors",
    f"{company} recent news"
]

# Topic research queries (same pattern)
queries = [
    f"What is {topic}?",
    f"{topic} current state 2026",
    f"{topic} key players and frameworks",
    f"{topic} recent developments",
    f"{topic} best practices and pitfalls"
]

# Execute in parallel
import asyncio
from tavily import AsyncTavilyClient

async def research_topic(topic: str):
    client = AsyncTavilyClient()
    queries = [...]  # topic-specific queries
    tasks = [client.search(q, search_depth="advanced", max_results=5) for q in queries]
    results = await asyncio.gather(*tasks)
    return results
```

### 4. Crawl to RAG
Turn any website into a searchable knowledge base:
1. **Crawl** a website with Tavily's crawl endpoint
2. **Embed** extracted content into a vector store (MongoDB Atlas, etc.)
3. **Query** with a conversational agent that does semantic search over the crawled data

### 5. Meeting Prep
Automated pre-meeting research:
1. Connect to Google Calendar via MCP
2. Extract meeting attendees
3. Search for attendee profiles and company info
4. Generate meeting prep briefing

### 6. RAG Evaluation
Generate evaluation datasets for RAG systems:
1. Generate domain-specific search queries
2. Use Tavily to gather current web content
3. Generate Q&A pairs from the content
4. Save as evaluation dataset for LLM-as-a-Judge evaluation

### 7. Market Research
Portfolio analysis and market insights:
- Use `topic="news"` and `topic="finance"` parameters
- Parallel searches per ticker symbol
- Automated report generation with source citations

---

## LangChain Integration

The official `langchain-tavily` package provides Search, Extract, Map, and Crawl as LangChain tools.

```bash
pip install -U langchain-tavily
```

> **Note**: The older `langchain_community.tools.tavily_search.tool` is deprecated. Use `langchain-tavily` instead.

```python
from langchain_tavily import TavilySearch, TavilyExtract, TavilyMap, TavilyCrawl

# Search tool
search = TavilySearch(
    max_results=10,
    topic="general",
    api_key="tvly-YOUR_API_KEY"
)

# Extract tool
extract = TavilyExtract(
    extract_depth="advanced",
    api_key="tvly-YOUR_API_KEY"
)

# Map tool
map_tool = TavilyMap()

# Crawl tool
crawl = TavilyCrawl()

# Use with an agent
from langchain.agents import create_react_agent
tools = [search, extract, map_tool, crawl]
```

---

## Anthropic Integration

Use Tavily as a tool with Claude's tool calling:

```python
import os
import json
from anthropic import Anthropic
from tavily import TavilyClient

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

# Define Tavily as a tool for Claude
tools = [
    {
        "name": "tavily_search",
        "description": "Search the web for current information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "search_depth": {
                    "type": "string",
                    "enum": ["basic", "advanced"],
                    "description": "Search depth"
                },
                "max_results": {"type": "integer", "description": "Max results"},
                "include_answer": {"type": "boolean", "description": "Include answer"}
            },
            "required": ["query"]
        }
    }
]

# In your tool execution handler
def handle_tool_call(tool_name, tool_input):
    if tool_name == "tavily_search":
        return tavily_client.search(**tool_input)
```

---

## Best Practices

### Search Best Practices

1. **Keep queries under 400 characters** — think agent search query, not LLM prompt
2. **Break complex queries into sub-queries**:
   ```python
   # Instead of one massive query:
   queries = [
       "Competitors of company ABC",
       "Financial performance of company ABC",
       "Recent developments of company ABC"
   ]
   ```
3. **Use `search_depth` wisely**: `basic` for most queries, `advanced` only when quality matters more than speed
4. **Filter by date** for time-sensitive information: `time_range="week"` or `start_date`/`end_date`
5. **Use `topic="news"`** for news-specific queries (adds `published_date` to results)
6. **Domain filtering**: `include_domains` for trusted sources, `exclude_domains` for noise
7. **Score-based filtering**: Filter results by `score` field for higher precision
8. **Use `auto_parameters=true`** to let Tavily auto-configure based on query intent

### Extract Best Practices

1. **Use `query` parameter** to rerank chunks by relevance — don't extract blindly
2. **`extract_depth="advanced"`** for LinkedIn, protected sites, tables, structured data
3. **Two-step pattern**: Search to find URLs → Extract to get full content
4. **`chunks_per_source`**: Increase for long documents, decrease for focused extraction

### Crawl Best Practices

1. **Start conservative**: `max_depth=1, max_breadth=20` then expand
2. **Use `instructions`** for semantic filtering (costs 2x credits but much more relevant)
3. **Set `limit`** to prevent runaway crawls
4. **Use `select_paths` / `exclude_paths`** for known URL patterns
5. **Watch depth vs performance**: depth increases latency exponentially

### Research Best Practices

1. **Be specific** in your research prompt — include context you already know
2. **Use `output_schema`** for structured, programmatic output
3. **Choose the right model**: `mini` for focused questions, `pro` for comprehensive analysis
4. **Include what you already know** to avoid redundant research

---

## Pricing & Rate Limits

### Pricing Plans

| Plan | Credits/Month | Price/Month | Per Credit |
|------|--------------|-------------|------------|
| **Researcher** (Free) | 1,000 | Free | — |
| **Project** | 4,000 | $30 | $0.0075 |
| **Bootstrap** | 15,000 | $100 | $0.0067 |
| **Startup** | 38,000 | $220 | $0.0058 |
| **Growth** | 100,000 | $500 | $0.005 |
| **Pay as you go** | Per usage | — | $0.008 |
| **Enterprise** | Custom | Custom | Custom |

### Credit Costs per Endpoint

| Endpoint | Basic | Advanced/With Instructions |
|----------|-------|---------------------------|
| **Search** | 1 credit | 2 credits (`search_depth=advanced`) |
| **Extract** | 1 credit per URL | 2 credits per URL (`extract_depth=advanced`) |
| **Map** | 1 credit per 10 pages | 2 credits per 10 pages (with `instructions`) |
| **Crawl** | 1 credit per 10 pages | 2 credits per 10 pages (with `instructions`) |
| **Research (mini)** | 4–110 credits | — |
| **Research (pro)** | 15–250 credits | — |

### Rate Limits

| Endpoint | Development | Production |
|----------|------------|------------|
| **Search/Extract** | 100 RPM | 1,000 RPM |
| **Crawl** | 100 RPM | 100 RPM |
| **Research** | 20 RPM | 20 RPM |
| **Usage** | 10 per 10 min | 10 per 10 min |

Rate limit exceeded returns `429 Too Many Requests` with a `retry-after` header.

---

## Integration Ecosystem

Tavily integrates with the following platforms:

| Category | Integrations |
|----------|-------------|
| **AI Frameworks** | LangChain, LlamaIndex, Pydantic AI, CrewAI, Agno, Google ADK |
| **LLM Providers** | Anthropic (Claude), OpenAI, Vercel AI SDK |
| **No-Code** | n8n, Make, Zapier, Langflow, Dify, FlowiseAI, StackAI, Tines |
| **Cloud** | Azure, Snowflake, Databricks, Amazon Bedrock AgentCore |
| **Agent Builders** | OpenAI Agent Builder, Composio |

---

## Quick Reference: Choosing the Right Endpoint

| I want to... | Use | Example |
|--------------|-----|---------|
| Find current information on a topic | **Search** | `client.search("latest AI news")` |
| Get content from a specific URL | **Extract** | `client.extract("https://...")` |
| Get content from an entire website | **Crawl** | `client.crawl(url="https://docs.example.com")` |
| See all pages on a website | **Map** | `client.map(url="https://example.com")` |
| Get a comprehensive research report | **Research** | `client.research(input="Analyze XYZ market")` |
| Find docs for a library/API | **Skill** (MCP) | `tavily_skill(query="celery beat periodic tasks")` |

---

## Common Patterns for Our Pipeline

### Pattern 1: Topic Research (adapted from Company Research)

```python
import asyncio
from tavily import AsyncTavilyClient

async def research_topic(topic: str, subtopics: list[str]) -> dict:
    """Research a topic using parallel sub-queries."""
    client = AsyncTavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    # Generate focused queries per subtopic
    queries = [f"{topic}: {subtopic}" for subtopic in subtopics]

    # Execute all searches in parallel
    tasks = [
        client.search(q, search_depth="advanced", max_results=5)
        for q in queries
    ]
    results = await asyncio.gather(*tasks)

    # Aggregate results
    all_sources = []
    for result in results:
        for r in result.get("results", []):
            all_sources.append({
                "title": r["title"],
                "url": r["url"],
                "content": r["content"],
                "score": r["score"]
            })

    return {
        "topic": topic,
        "sources": sorted(all_sources, key=lambda x: x["score"], reverse=True)
    }
```

### Pattern 2: Search → Extract Pipeline

```python
async def deep_search(query: str) -> list[dict]:
    """Search for relevant pages, then extract full content from top results."""
    client = AsyncTavilyClient()

    # Step 1: Search for relevant URLs
    search_results = await client.search(
        query=query,
        search_depth="advanced",
        max_results=10
    )

    # Step 2: Filter by score
    top_urls = [
        r["url"] for r in search_results["results"]
        if r["score"] > 0.7
    ]

    # Step 3: Extract full content from top results
    if top_urls:
        extracted = await client.extract(
            urls=top_urls,
            query=query,
            extract_depth="advanced"
        )
        return extracted["results"]

    return []
```

### Pattern 3: Crawl Documentation Site

```python
async def crawl_docs(docs_url: str, focus: str) -> list[dict]:
    """Crawl a documentation site focused on a specific topic."""
    client = AsyncTavilyClient()

    # Step 1: Map the site structure
    sitemap = await client.map(url=docs_url, max_depth=2, limit=100)

    # Step 2: Crawl with semantic instructions
    results = await client.crawl(
        url=docs_url,
        max_depth=2,
        limit=30,
        instructions=f"Find all pages about {focus}",
        extract_depth="advanced"
    )

    return results["results"]
```
