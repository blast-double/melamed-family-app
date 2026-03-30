# Production RAG Guide

> A comprehensive guide to building production-grade RAG systems. This guide is designed to be reusable across any project that implements retrieval-augmented generation.

**Last Updated**: January 2026
**Sources**: Ragie.ai engineering blog, production implementations

---

## Table of Contents
1. [RAG Architecture Overview](#1-rag-architecture-overview)
2. [Document Ingestion Pipeline](#2-document-ingestion-pipeline)
3. [Retrieval Strategies](#3-retrieval-strategies)
4. [Generation & Hallucination Prevention](#4-generation--hallucination-prevention)
5. [Agentic RAG](#5-agentic-rag)
6. [Production Considerations](#6-production-considerations)
7. [Quick Reference Checklist](#7-quick-reference-rag-improvement-checklist)

---

## 1. RAG Architecture Overview

### What RAG Solves
Large Language Models have knowledge cutoffs and can hallucinate. RAG (Retrieval-Augmented Generation) grounds LLM responses in your actual data by:
1. **Retrieving** relevant context from your knowledge base
2. **Augmenting** the prompt with that context
3. **Generating** responses based on retrieved facts

### Core Components

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Knowledge  │────▶│  Retriever  │────▶│  Generator  │
│    Base     │     │             │     │    (LLM)    │
└─────────────┘     └─────────────┘     └─────────────┘
     │                    │                    │
     ▼                    ▼                    ▼
  Documents           Embeddings           Response
  Chunks              Similarity           + Citations
  Metadata            Reranking
```

| Component | Role |
|-----------|------|
| **Knowledge Base** | Indexed documents stored in a vector database |
| **Retriever** | Converts queries to embeddings, performs similarity search |
| **Generator** | LLM that synthesizes retrieved context with user query |

---

## 2. Document Ingestion Pipeline

### 2.1 Document Processing

**Step 1: Extraction**
```python
def extract_document(file_path: str) -> ExtractedDocument:
    if file_path.endswith('.pdf'):
        # Native PDF text extraction
        text = extract_pdf_text(file_path)

        # Fallback to OCR for scanned documents
        if is_scanned(text):
            text = run_ocr(file_path)

        # Extract form fields (fillable PDFs)
        form_fields = extract_form_fields(file_path)

    return ExtractedDocument(text=text, form_fields=form_fields)
```

**Best Practices**:
- Detect document type (native PDF vs scanned) and route accordingly
- Extract structured data (forms, tables) separately from prose
- Preserve metadata: page numbers, section headers, timestamps

### 2.2 Chunking Strategies

**The Problem**: LLMs have context limits. Documents must be split into chunks that:
- Fit within embedding model limits (typically 512-8192 tokens)
- Preserve semantic coherence
- Maintain context for accurate retrieval

#### Strategy 1: Fixed-Size Chunking
```python
# Simple but can break mid-sentence
chunks = split_by_tokens(text, max_tokens=500, overlap=50)
```
| Pros | Cons |
|------|------|
| Simple, predictable | Breaks logical units, loses context |

#### Strategy 2: Semantic Chunking
*Recommended for narrative content (blogs, FAQs, articles)*

```python
def semantic_chunk(text: str) -> list[str]:
    # Split on paragraphs, then merge to target size
    paragraphs = text.split('\n\n')
    chunks = []
    current = []

    for para in paragraphs:
        if token_count(current) + token_count(para) > MAX_TOKENS:
            chunks.append('\n\n'.join(current))
            current = [para]
        else:
            current.append(para)

    return chunks
```
| Pros | Cons |
|------|------|
| Preserves paragraph coherence | Variable chunk sizes |

#### Strategy 3: Hierarchical Chunking
*Recommended for structured documents (contracts, leases, legal documents, specifications)*

```python
def hierarchical_chunk(document: Document) -> list[Chunk]:
    chunks = []

    for section in document.sections:
        # Keep section header with content
        chunk = Chunk(
            text=f"{section.header}\n{section.content}",
            metadata={
                "section_title": section.header,
                "section_number": section.number,
                "page_range": section.pages
            }
        )

        # Split large sections, preserving header
        if token_count(chunk.text) > MAX_TOKENS:
            sub_chunks = split_with_header(chunk)
            chunks.extend(sub_chunks)
        else:
            chunks.append(chunk)

    return chunks
```
| Pros | Cons |
|------|------|
| Maintains document structure, better for Q&A | Requires document structure detection |

#### Strategy 4: Table-Aware Chunking
*Critical for tabular data (spreadsheets, fee schedules, matrices)*

```python
def chunk_with_tables(text: str) -> list[Chunk]:
    tables = detect_tables(text)

    for table in tables:
        if fits_in_chunk(table):
            yield TableChunk(headers=table.headers, rows=table.rows)
        else:
            # Split by rows, repeat headers
            for row_batch in batch_rows(table.rows, max_rows=10):
                yield TableChunk(
                    headers=table.headers,  # Always include headers
                    rows=row_batch
                )
```

**Example: Why table chunking matters**
```
Bad chunking (header lost):
  Chunk 1: "| Month | Rent | Due Date |"
  Chunk 2: "| Jan | $2,500 | 1st |"  ← What do these columns mean?

Good chunking (header preserved):
  Chunk 1: "| Month | Rent | Due Date |\n| Jan | $2,500 | 1st |"
  Chunk 2: "| Month | Rent | Due Date |\n| Mar | $2,600 | 1st |"  ← Headers repeated
```

### 2.3 Embedding Generation

**Choosing an Embedding Model**:

| Model | Dimensions | Best For |
|-------|------------|----------|
| OpenAI text-embedding-3-small | 1536 | General purpose, cost-effective |
| OpenAI text-embedding-3-large | 3072 | High accuracy, document summaries |
| Cohere embed-v3 | 1024 | Multilingual |
| Open-source (e5-large) | 1024 | Self-hosted, no API costs |

**Best Practices**:
- Use larger dimensions for document summaries (semantic density)
- Use smaller dimensions for chunks (speed, cost)
- Normalize embeddings for cosine similarity
- Batch embedding calls for efficiency

```python
def embed_chunks(chunks: list[Chunk], model: str = "text-embedding-3-small"):
    batches = batch(chunks, size=100)  # Max 2048 per call for OpenAI

    embeddings = []
    for batch in batches:
        response = openai.embeddings.create(
            input=[c.text for c in batch],
            model=model
        )
        embeddings.extend([e.embedding for e in response.data])

    return embeddings
```

---

## 3. Retrieval Strategies

### 3.1 Basic Vector Search

```python
def search(query: str, top_k: int = 10) -> list[Chunk]:
    query_embedding = embed(query)

    results = vector_db.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    return results
```

**Limitations**:
- Pure semantic similarity may miss keyword matches
- Domain jargon may not embed well
- No understanding of query intent

### 3.2 Hybrid Search (Recommended)

Combine vector similarity with keyword/BM25 search:

```python
def hybrid_search(query: str, top_k: int = 10) -> list[Chunk]:
    # Vector search
    vector_results = vector_db.query(embed(query), top_k=top_k*2)

    # Keyword search (BM25 or full-text)
    keyword_results = text_search(query, top_k=top_k*2)

    # Reciprocal Rank Fusion
    combined = reciprocal_rank_fusion(
        [vector_results, keyword_results],
        k=60  # RRF constant
    )

    return combined[:top_k]
```

**Example**:
- Query: "What is the late fee?"
- Vector search finds: sections about "penalties", "charges", "delinquent payments"
- Keyword search finds: exact matches for "late fee"
- Hybrid combines both for better recall

### 3.3 Cross-Encoder Reranking

Initial retrieval is fast but imprecise. Reranking improves precision:

```python
def search_with_rerank(query: str, top_k: int = 5) -> list[Chunk]:
    # Step 1: Fast retrieval (over-fetch)
    candidates = hybrid_search(query, top_k=20)

    # Step 2: Precise reranking
    reranked = rerank(query, candidates)

    return reranked[:top_k]

def rerank(query: str, chunks: list[Chunk]) -> list[Chunk]:
    # Option A: Cross-encoder model
    scores = cross_encoder.predict([(query, c.text) for c in chunks])

    # Option B: LLM-based reranking
    prompt = f"""
    Rate each passage's relevance to the query (0-10).
    Query: {query}

    Passages:
    {format_passages(chunks)}

    Return: [{{"index": 0, "score": 8.5}}, ...]
    """
    scores = llm.generate(prompt)

    return sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
```

**Why Reranking Works**:
| Stage | Question Being Asked |
|-------|---------------------|
| Initial retrieval | "Does this chunk contain similar words?" |
| Reranking | "Does this chunk actually answer the question?" |

**Example**:
- Query: "Can I have a dog?"
- Chunk A: "Pets are allowed with a $500 deposit" → **High rerank score**
- Chunk B: "The property has a dog park nearby" → **Low rerank score** (mentions dogs but doesn't answer)

**Benchmarks** (from Ragie):
- 124% improvement in precision with reranking enabled
- 16% reduction in hallucinations
- Trade-off: ~200-500ms latency increase

### 3.4 Query Decomposition

Complex queries should be broken into sub-queries:

```python
def decompose_query(query: str) -> list[str]:
    prompt = f"""
    Break this complex question into simpler sub-questions:
    Query: {query}

    Return JSON array of sub-questions.
    """

    return llm.generate(prompt)

# Example
query = "Compare the late fee policy and security deposit terms"
sub_queries = decompose_query(query)
# ["What is the late fee policy?", "What are the security deposit terms?"]

# Search each sub-query, merge results
results = []
for sq in sub_queries:
    results.extend(search_with_rerank(sq, top_k=3))
```

### 3.5 Two-Tiered Retrieval

For large document collections or multi-document scenarios:

```
Tier 1: Document Selection (coarse)
  └─ Search document summaries
  └─ Identify which documents are relevant

Tier 2: Chunk Retrieval (fine)
  └─ Search chunks within selected documents
  └─ Apply reranking
```

```python
def two_tier_search(query: str, top_k: int = 5) -> list[Chunk]:
    # Tier 1: Find relevant documents
    relevant_docs = search_summaries(query, top_k=3)

    # Tier 2: Search within those documents
    chunks = search_chunks(
        query,
        filter={"document_id": {"$in": [d.id for d in relevant_docs]}},
        max_per_document=3  # Diversify results
    )

    return rerank(query, chunks)[:top_k]
```

**Use Case**: Multi-document portfolios
- User asks: "What's the rent for the Market St property?"
- Tier 1: Summary search identifies the Market St lease
- Tier 2: Chunk search finds rent terms within that specific lease

---

## 4. Generation & Hallucination Prevention

### 4.1 Context-Grounded Generation

```python
def generate_answer(query: str, context: list[Chunk]) -> Answer:
    prompt = f"""
    Answer the question using ONLY the provided context.
    If the answer is not in the context, say "I don't have information about that."

    Context:
    {format_context(context)}

    Question: {query}

    Answer with citations in format: [Source: page X, section Y]
    """

    response = llm.generate(prompt)
    return parse_answer_with_citations(response)
```

### 4.2 Self-Evaluation Pass

Verify that generated answers are supported by sources:

```python
def generate_with_verification(query: str, context: list[Chunk]) -> Answer:
    # Generate initial answer
    answer = generate_answer(query, context)

    # Verify each claim
    verification_prompt = f"""
    Verify if this answer is supported by the source text.

    Answer: {answer.text}
    Sources: {answer.citations}

    For each claim in the answer:
    1. Is it explicitly stated in the sources?
    2. Is it a reasonable inference?
    3. Is it unsupported/hallucinated?

    Return: {{
      "verified": bool,
      "confidence": 0-1,
      "unsupported_claims": ["..."],
      "corrections": "..."
    }}
    """

    verification = llm.generate(verification_prompt)

    if not verification.verified:
        return generate_answer(query, context, strict=True)

    return answer
```

### 4.3 Citation Requirements

Always require and display citations:

```python
@dataclass
class Citation:
    document_id: str
    page_number: int
    section_title: str
    snippet: str  # Exact quote

@dataclass
class Answer:
    text: str
    citations: list[Citation]
    confidence: float
```

**UI Display Example**:
> "The late fee is $50 after a 5-day grace period."
> *[Source: Lease Agreement, Page 3, Section 4: Late Payments]*

---

## 5. Agentic RAG

### 5.1 When to Use Agentic RAG

| Basic RAG | Agentic RAG |
|-----------|-------------|
| Single retrieval → single generation | Multi-step reasoning with retrieval at each step |

**Use Agentic RAG when**:
- Questions require information from multiple sources
- Complex reasoning is needed
- Initial retrieval may be insufficient
- Follow-up queries depend on initial results

### 5.2 Agent Architecture

```python
class RAGAgent:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLM()
        self.memory = []

    def answer(self, query: str, max_steps: int = 5) -> Answer:
        for step in range(max_steps):
            action = self.plan(query, self.memory)

            if action.type == "search":
                results = self.retriever.search(action.query)
                self.memory.append(("search", action.query, results))

            elif action.type == "refine_search":
                refined = self.llm.rewrite_query(action.original, action.feedback)
                results = self.retriever.search(refined)
                self.memory.append(("refined_search", refined, results))

            elif action.type == "answer":
                return self.generate_answer(query, self.memory)

            elif action.type == "insufficient_info":
                return Answer(
                    text="I couldn't find sufficient information.",
                    confidence=0.0
                )

        return self.generate_best_effort(query, self.memory)
```

### 5.3 Agent Capabilities

**Query Rewriting**: Improve retrieval with better queries
```python
# Original: "pet policy"
# Rewritten: "Are pets allowed? What is the pet deposit and monthly pet rent?"
```

**Chunk Expansion**: Fetch surrounding context
```python
def expand_chunk(chunk: Chunk, window: int = 1) -> str:
    neighbors = get_adjacent_chunks(chunk.id, window=window)
    return combine_chunks([*neighbors.before, chunk, *neighbors.after])
```

**Self-Reflection**: Evaluate retrieval quality
```python
def evaluate_retrieval(query: str, chunks: list[Chunk]) -> RetrievalQuality:
    prompt = f"""
    Evaluate if these retrieved chunks can answer the query.

    Query: {query}
    Chunks: {format_chunks(chunks)}

    Return:
    - sufficient: bool
    - missing_info: list
    - suggested_queries: list
    """
    return llm.generate(prompt)
```

---

## 6. Production Considerations

### 6.1 Performance Optimization

**Caching**:
```python
@cache(ttl=3600)
def embed(text: str) -> list[float]:
    return embedding_model.embed(text)

@cache(ttl=300, key=lambda q, k: f"{hash(q)}:{k}")
def search(query: str, top_k: int) -> list[Chunk]:
    ...
```

**Index Optimization**:
- Use HNSW indexes for approximate nearest neighbor (faster)
- Shard large indexes across multiple nodes
- Use metadata filtering before vector search

### 6.2 Cost Management

| Component | Cost Driver | Optimization |
|-----------|-------------|--------------|
| Embeddings | Tokens embedded | Cache, batch, smaller models |
| Vector DB | Storage + queries | Prune old data, optimize indexes |
| LLM (retrieval) | Reranking calls | Cache, limit candidates |
| LLM (generation) | Output tokens | Concise prompts, streaming |

**Cost-Aware Retrieval**:
```python
def cost_aware_search(query: str, budget: str = "low") -> list[Chunk]:
    if budget == "low":
        return vector_search(query, top_k=5)
    elif budget == "medium":
        candidates = hybrid_search(query, top_k=10)
        return lightweight_rerank(query, candidates)[:5]
    elif budget == "high":
        candidates = hybrid_search(query, top_k=20)
        return cross_encoder_rerank(query, candidates)[:5]
```

### 6.3 Evaluation & Monitoring

**Metrics to Track**:
- Retrieval precision/recall
- Answer accuracy
- Hallucination rate
- Latency (p50, p95, p99)
- Cost per query

**Evaluation Framework**:
```python
def evaluate_rag_system(test_set: list[TestCase]) -> Metrics:
    results = []

    for case in test_set:
        chunks = search(case.query)
        retrieval_recall = compute_recall(chunks, case.relevant_chunks)

        answer = generate(case.query, chunks)
        correctness = judge_answer(answer, case.expected_answer)
        hallucination_score = detect_hallucinations(answer, chunks)

        results.append({
            "retrieval_recall": retrieval_recall,
            "answer_correctness": correctness,
            "hallucination_score": hallucination_score
        })

    return aggregate_metrics(results)
```

### 6.4 Security

**Data Protection**:
- Encrypt embeddings at rest
- TLS for all API calls
- PII detection and redaction before embedding

**Access Control**:
```python
def search_with_access_control(query: str, user: User) -> list[Chunk]:
    allowed_docs = get_user_permissions(user.id)
    return search(
        query,
        filter={"document_id": {"$in": allowed_docs}}
    )
```

**Audit Logging**:
```python
def log_rag_interaction(user_id: str, query: str, chunks: list, answer: str):
    audit_log.write({
        "timestamp": now(),
        "user_id": user_id,
        "query": query,
        "retrieved_chunk_ids": [c.id for c in chunks],
        "answer_hash": hash(answer),
        "latency_ms": elapsed_ms
    })
```

---

## 7. Quick Reference: RAG Improvement Checklist

### Chunking
- [ ] Use semantic/hierarchical chunking for structured documents
- [ ] Preserve table headers when splitting tables
- [ ] Include section titles in chunk metadata
- [ ] Overlap chunks for context continuity

### Retrieval
- [ ] Implement hybrid search (vector + keyword)
- [ ] Add cross-encoder reranking
- [ ] Use query decomposition for complex queries
- [ ] Implement two-tiered retrieval for multi-document scenarios

### Generation
- [ ] Ground all answers in retrieved context
- [ ] Require citations for all factual claims
- [ ] Add self-evaluation pass to catch hallucinations
- [ ] Handle "insufficient information" gracefully

### Production
- [ ] Cache embeddings and search results
- [ ] Implement access control filtering
- [ ] Monitor retrieval quality and hallucination rates
- [ ] Set up cost tracking and budgets

---

## References

- [Ragie: How We Built Agentic Retrieval](https://www.ragie.ai/blog/how-we-built-agentic-retrieval-at-ragie)
- [Ragie: Our Approach to Table Chunking](https://www.ragie.ai/blog/our-approach-to-table-chunking)
- [Ragie: Advanced RAG with Document Summarization](https://www.ragie.ai/blog/advanced-rag-with-document-summarization)
- [Ragie: The Architect's Guide to Production RAG](https://www.ragie.ai/blog/the-architects-guide-to-production-rag-navigating-challenges-and-building-scalable-ai)
- [Ragie: Multimodal RAG for Audio and Video](https://www.ragie.ai/blog/how-we-built-multimodal-rag-for-audio-and-video)
- [Ragie: Build Smarter AI Apps and Reduce Hallucinations](https://www.ragie.ai/blog/build-smarter-ai-apps-and-reduce-hallucinations-with-rag)
