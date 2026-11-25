# System Architecture

## 1. Overview

Agricultural-RAG-SLMe is a retrieval-augmented generation system designed to provide reliable agricultural 
information.

## 2. Processing Pipeline

1. Data collection – Gather trusted agricultural documents.
2. Document processing – Extract, clean and split documents.
3. Knowledge storage – Store processed documents and metadata.
4. Query understanding – Identify crops, diseases, symptoms and user intent.
5. Retrieval – Retrieve relevant information using BM25 and dense search.
6. Ranking – Rank retrieved documents by relevance.
7. Answer generation – Generate answers using retrieved evidence.
8. Evaluation – Measure retrieval accuracy and answer reliability.

## 3. Proposed Architecture

Agricultural Documents
→ Document Processing
→ Knowledge Base
→ User Query
→ Query Understanding
→ Hybrid Retrieval
→ Ranking
→ Evidence Selection
→ Language Model
→ Grounded Answer with Sources

## 4. Design Priorities

- Low computational requirements.
- Reliable agricultural sources.
- Explainable answers with citations.
- Offline deployment capability.
- Reproducible experiments.
