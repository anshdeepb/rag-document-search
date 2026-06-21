# RAG Document Search System

## Overview

This project is a Retrieval-Augmented Generation (RAG) system designed to answer questions from a collection of technical documents. The system combines semantic search, query rewriting, reranking, and large language models to provide accurate, context-grounded responses.

Unlike a traditional chatbot, the system retrieves relevant information from a document corpus before generating an answer, reducing hallucinations and improving factual accuracy.

## Features

* PDF document ingestion and processing
* Text chunking using LangChain
* Embedding generation using OpenAI embeddings
* Vector storage and retrieval with Pinecone
* Query rewriting for improved retrieval performance
* Semantic search over document collections
* Cohere reranking for improved result relevance
* Context-grounded answer generation using OpenAI models
* Support for comparison, definition, and explanatory questions

## Architecture

```text
User Query
    ↓
Query Rewriter (OpenAI)
    ↓
Embedding Search (Pinecone)
    ↓
Top-K Retrieved Chunks
    ↓
Cohere Rerank
    ↓
Context Assembly
    ↓
OpenAI Response Generation
    ↓
Final Answer
```

## Motivation

Traditional vector search systems often struggle when users phrase questions indirectly.

For example:

* "What is dynamic programming?" → usually retrieves relevant content.
* "Which is better, greedy algorithms or dynamic programming?" → may fail because the retrieval query does not closely match document wording.

To address this problem, the system includes a query rewriting stage that transforms user questions into retrieval-optimized search queries before searching the vector database.

## Technology Stack

### Backend

* Python

### Retrieval & Vector Search

* Pinecone
* OpenAI Embeddings

### Language Models

* OpenAI GPT-4o Mini

### Reranking

* Cohere Rerank

### Document Processing

* LangChain
* PDF processing libraries

## Workflow

### 1. Document Ingestion

Documents are loaded from PDF files and converted into text.

### 2. Chunking

Large documents are split into smaller chunks to improve retrieval quality and embedding performance.

### 3. Embedding Generation

Each chunk is converted into a vector embedding using OpenAI embedding models.

### 4. Vector Storage

Embeddings are stored in Pinecone for efficient similarity search.

### 5. Query Rewriting

User questions are transformed into retrieval-friendly search queries to improve recall.

Example:

**User Question**

```text
Which is better, greedy algorithms or dynamic programming?
```

**Generated Search Queries**

```text
greedy algorithm vs dynamic programming
differences between greedy and dynamic programming
advantages of greedy algorithms
advantages of dynamic programming
when to use greedy vs dynamic programming
```

### 6. Retrieval

Relevant document chunks are retrieved from Pinecone.

### 7. Reranking

Retrieved chunks are reranked using Cohere to prioritize the most relevant context.

### 8. Answer Generation

The highest-ranked chunks are provided to an OpenAI model, which generates a grounded response using only the retrieved information.

## Example Use Cases

* Educational document search
* Technical knowledge bases
* Course material assistants
* Research document exploration
* Internal company documentation search

## Future Improvements

* Hybrid search (vector + keyword search)
* Metadata filtering
* Source citation generation
* Multi-document reasoning
* Agentic query planning
* Evaluation benchmark suite
* Web interface deployment
* Cloud deployment using AWS

## Project Goals

The primary goal of this project is to explore modern information retrieval techniques and build a production-style RAG pipeline that combines:

* Semantic search
* Query understanding
* Retrieval optimization
* Reranking
* Grounded language generation

This project demonstrates practical applications of large language models, vector databases, and retrieval systems in real-world software engineering workflows.
