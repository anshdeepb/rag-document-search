# RAG Document Search

A retrieval-augmented generation (RAG) system that answers questions over technical PDF documents with page-level citations. The retrieval pipeline is also exposed as a **Model Context Protocol (MCP) server**, so AI agents such as Claude Code, Claude Desktop, and Cursor can search the indexed documents as a tool.

## Features

- **Multi-query retrieval:** an LLM rewrites each question into several search queries; each is searched separately and the results are merged and deduplicated
- **Cohere reranking** against the user's original question
- **Cited answers:** every passage carries its source file and page number, and generated answers cite pages
- **MCP server:** a read-only `search_documents` tool that agents can call to retrieve cited passages
- **Page-aware chunking:** ~800-character chunks with overlap, split at sentence boundaries and never crossing page boundaries, so citations stay accurate
- **Fast startup:** ingestion is a separate, explicit step; querying connects to the existing index without re-processing documents

## Architecture

```text
            ┌──────────────┐        ┌──────────────────────┐
            │  CLI         │        │  MCP host            │
            │  (main.py)   │        │  (Claude, Cursor…)   │
            └──────┬───────┘        └──────────┬───────────┘
                   │                           │ stdio
                   │                ┌──────────▼───────────┐
                   │                │  MCP server          │
                   │                │  (mcp_server.py)     │
                   │                └──────────┬───────────┘
                   ▼                           ▼
            ┌─────────────────────────────────────────────┐
            │  Query pipeline (generation/)               │
            │  1. Rewrite question into search queries    │
            │  2. Embed each query                        │
            │  3. Search Pinecone, merge + deduplicate    │
            │  4. Rerank against the original question    │
            │  5. Generate a cited answer (CLI only)      │
            └──────────────────────┬──────────────────────┘
                                   │
                         Pinecone vector index
                                   ▲
            ┌──────────────────────┴──────────────────────┐
            │  Ingestion (run manually)                   │
            │  PDF → clean → chunk → embed → upsert       │
            └─────────────────────────────────────────────┘
```

The CLI and the MCP server share the same pipeline modules, so there is a single implementation of retrieval.

## How Retrieval Works

| Stage | Implementation | Why |
|---|---|---|
| Query rewriting | `gpt-4o-mini` produces 2–5 search queries (the original question is always included) | Indirect or comparative questions often don't match document wording |
| Embedding | OpenAI `text-embedding-3-small`, all queries in one request | One API call per question |
| Search | Pinecone top-k per query; results merged by chunk id, keeping the best score | Broader recall without duplicate passages |
| Reranking | Cohere `rerank-v3.5` against the **original** question | Rewritten queries help recall; the user's wording is the best target for precision |
| Generation | `gpt-4o-mini` with source/page-labelled context; low-relevance chunks filtered out | Grounded answers with page citations |

## MCP Server

`app/mcp_server.py` exposes the retrieval pipeline to MCP-compatible agents over stdio.

| Tool | Input | Returns |
|---|---|---|
| `search_documents` | `query` (string), `top_n` (1–10, default 5) | Top reranked passages with `text`, `source`, `page`, `chunk_id`, `relevance_score` |

The tool returns passages rather than a generated answer: the calling agent is already an LLM, so giving it the source text lets it reason over the evidence and cite pages directly.

### Connecting an agent

Add the server to your MCP host's configuration. For Claude Code, create a `.mcp.json` in the project root (keep it out of version control, since it contains local paths):

```json
{
  "mcpServers": {
    "rag-docs": {
      "command": "/absolute/path/to/rag-document-search/.venv/bin/python",
      "args": ["/absolute/path/to/rag-document-search/app/mcp_server.py"]
    }
  }
}
```

Claude Desktop uses the same `mcpServers` block in `claude_desktop_config.json`.

## Tech Stack

| Area | Tools |
|---|---|
| Language | Python 3.11+ |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector database | Pinecone (serverless) |
| Reranking | Cohere `rerank-v3.5` |
| Query rewriting & generation | OpenAI `gpt-4o-mini` |
| Document processing | pypdf, NLTK, LangChain text splitters |
| Agent integration | MCP Python SDK |

## Project Structure

```text
app/
├── main.py                  # CLI: optional ingestion, then interactive Q&A
├── mcp_server.py            # MCP server exposing search_documents
├── chunking.py              # Page-bounded, sentence-aware chunking
├── embeddings.py            # OpenAI client and batch embedding
├── ingestion/               # PDF loading and text cleaning
├── vectorstore/             # Pinecone index management and upserts
└── generation/              # Query rewriting, retrieval, reranking, prompting, generation
```

## Getting Started

### Prerequisites
- Python 3.11 or newer
- API keys for OpenAI, Pinecone, and Cohere

### Installation

```bash
git clone https://github.com/anshdeepb/rag-document-search.git
cd rag-document-search
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Virtual environments store absolute paths. If you move the project folder, delete `.venv` and recreate it.

### Configuration

Copy the example environment file and add your keys:

```bash
cp .env.example .env
```

```text
OPENAI_API_KEY=
PINECONE_API_KEY=
COHERE_API_KEY=
```

### Add documents

Place PDF files in `data/`. Source documents are not included in this repository.

### Ingest

```bash
cd app
python main.py      # answer "yes" to ingest
```

Ingestion creates the Pinecone index if it doesn't exist. If you change chunking or chunk ids, delete the index first; existing vectors with old ids are not overwritten.

### Ask questions

```bash
cd app
python main.py      # answer "no" to skip ingestion
```

## Security & Privacy

- **Secrets:** API keys are read from `.env`, which is gitignored and must never be committed. `.env.example` lists variable names only.
- **Least privilege:** use project-scoped API keys with spending limits or prepaid credits where providers support them.
- **Read-only MCP surface:** the MCP server exposes search only. Ingestion and index writes are deliberately not available to agents, and `top_n` is bounded.
- **No network listener:** the server communicates over stdio with the host process that launched it; it opens no ports.
- **Minimal disclosure:** results include file names, not filesystem paths. Keys and source code are never sent to the agent, only tool results.
- **Logging:** the server logs to stderr only (stdout carries the MCP protocol); passage contents are not logged.
- **Third-party data flow:** document text and queries are sent to OpenAI, Pinecone, and Cohere, and tool results are sent to the MCP host's model provider. Don't index confidential documents unless that is acceptable under those providers' terms.
- **Trusted content only:** retrieved text is placed into LLM prompts. Index only documents you trust, since untrusted documents could carry prompt-injection text.
- **Dependencies:** versions are pinned in `requirements.txt`; apply security updates promptly.

## Limitations

- Page numbers are PDF page indices, which may differ from the page numbers printed in a book.
- Chunks do not span pages, so content that continues across a page break is split.
- Sentence splitting uses NLTK's English models.
- The MCP server is intended for local use; a remote deployment would require authentication, rate limiting, and TLS.

## Roadmap

- Evaluation suite: a hand-labelled question set with retrieval recall@k and Ragas answer-quality metrics
- `ask_documents` MCP tool returning a generated, cited answer
- Hybrid search (vector + keyword)
- Metadata filtering by document and section
- Web interface

## License

Copyright © 2026 Anshdeep Bhachoo. All rights reserved. This is proprietary software; see [LICENSE](LICENSE) for terms.
