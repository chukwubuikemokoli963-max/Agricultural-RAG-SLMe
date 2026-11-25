# Agricultural-RAG-SLMe

## Agricultural Retrieval-Augmented Generation System for Resource-Constrained Environments

### 1. Project Overview

Agricultural-RAG-SLMe is an AI-powered agricultural knowledge assistant designed to help farmers and 
agricultural stakeholders access reliable agricultural information.

The system combines information retrieval, natural language processing, and local language models to retrieve
relevant agricultural knowledge and generate evidence-grounded responses.

the major objective is to support offline operation and deployment in resource-constrained 
environments where reliable internet connectivity, electricity, and computing resources may be limited.

### 2. Project Objectives

- Build a credible and searchable agricultural knowledge base.
- Develop an efficient hybrid retrieval system.
- Incorporate agricultural context such as crops, pests, diseases, symptoms, and farmer intent.
- Generate answers grounded in retrieved agricultural documents.
- Provide references to the sources supporting generated answers.
- Investigate lightweight models and offline deployment.
- Evaluate retrieval accuracy, answer quality, and computational efficiency.

### 3. Proposed System Architecture

Agricultural Knowledge Sources  
→ Document Processing  
→ Metadata Extraction  
→ Knowledge Storage  
→ Query Understanding  
→ Hybrid Retrieval  
→ Candidate Ranking  
→ Evidence Selection  
→ Local Language Model  
→ Grounded Agricultural Response

### 4. Technology Stack

The initial proposed technologies include:

- Python
- Google Colab
- Sentence Transformers
- BM25
- FAISS
- SQLite
- LightGBM
- Hugging Face Transformers
- PyTorch

### 5. Development Roadmap

| Phase | Description | Status |
|---|---|---|
| 0 | Project setup and architecture 
| 1 | Agricultural data collection 
| 2 | Document processing and preparation 
| 3 | Baseline retrieval 
| 4 | Dense and hybrid retrieval 
| 5 | Agricultural query understanding 
| 6 | Ranking optimisation 
| 7 | RAG answer generation 
| 8 | System evaluation 
| 9 | Offline and edge deployment 
