# Agricultural-RAG-SLMe

**Agricultural Retrieval-Augmented Generation System for Resource-Constrained Environments**

**Featuring FarmDoc — an agricultural information assistant powered by Agricultural-RAG-SLMe**

## 1. Project Overview

Agricultural-RAG-SLMe is a research and engineering project investigating how Retrieval-Augmented Generation (RAG), natural language processing, retrieval optimization, small language models and edge intelligence can improve access to agricultural information in resource-constrained environments.

The project focuses on smallholder farmers, subsistence farmers and agricultural stakeholders who may face limited access to agricultural extension services, reliable internet connectivity, electricity and high-performance computing resources.

The system combines agricultural document retrieval, query understanding, machine-learning-based ranking and evidence screening to provide relevant agricultural information with supporting references.

**FarmDoc** is the user-facing application developed to demonstrate the research system. It offers a conversational interface, supports English and experimental Nigerian Pidgin input, and can fall back to a locally installed CPU-based retrieval engine when its remote service becomes unavailable.

**Project status:** Functional research prototype, version 0.1.0. Independent agronomic validation, physical offline deployment testing and permanent hosting remain outstanding.

## 2. Problem Statement

Farmers often need timely information about crop diseases, soil fertility, pest management, irrigation and changing environmental conditions.

However, agricultural information may be difficult to find, expressed in unfamiliar technical language or dependent on continuous internet connectivity.

Conventional cloud-based AI applications also present challenges in communities with limited internet access or computing resources.

Agricultural-RAG-SLMe investigates whether efficient retrieval, evidence-grounded responses and compressed local inference can reduce these barriers.

## 3. Project Objectives

The project aims to:

1. Build and organize a searchable agricultural knowledge base.
2. Develop efficient sparse, dense and hybrid retrieval systems.
3. Understand agricultural context, including crops, symptoms, environmental conditions and farmer intent.
4. Optimize document ranking using machine learning.
5. Produce responses grounded in retrieved agricultural evidence.
6. Provide traceable supporting document references.
7. Investigate lightweight models, quantization and offline edge inference.
8. Evaluate retrieval effectiveness, response behaviour and computational efficiency.
9. Demonstrate the research through FarmDoc.

## 4. Introducing FarmDoc

**FarmDoc — Powered by Agricultural RAG SLMe**

FarmDoc is an agricultural information assistant designed to make the research accessible through a simple web interface.

Its prototype capabilities include:

- Agricultural questions in English and experimental Nigerian Pidgin.
- Retrieval of relevant information from an agricultural knowledge base.
- Supporting document references.
- Clarification when evidence is insufficient or a question is ambiguous.
- Safety screening for selected high-risk requests.
- Automatic remote-to-local fallback in the installed application.
- Local CPU inference using compressed document embeddings.

When the remote service is unavailable, the locally installed application uses its edge inference engine and displays an **Edge** indicator.

**Important:** Opening only the remotely hosted FarmDoc website does not provide offline inference. Offline operation requires a locally installed engine and its model assets.

## 5. System Architecture

Agricultural-RAG-SLMe implements two primary inference pathways.

### Online Retrieval Pipeline

Farmer Question → Query Normalization → BM25 + BGE + E5 Retrieval → Reciprocal Rank Fusion → LambdaRank Reranking → Evidence Selection → Quality Screening → Evidence-Grounded Response

### Edge Retrieval Pipeline

Farmer Question → Query Normalization → Local BGE Encoder → INT8 Document Index → Evidence Extraction → Quality Screening → Response with References

The project also investigates AfriBERTa for agricultural intent classification and Qwen under FP16, INT8 and INT4 quantization.

These remain experimental components. The current default application uses screened, extractive evidence responses rather than unrestricted language-model generation.

## 6. Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Experimentation | Google Colab, Kaggle |
| Sparse retrieval | BM25 |
| Dense retrieval | Sentence Transformers, BGE, E5 |
| Hybrid retrieval | Reciprocal Rank Fusion |
| Ranking optimization | LightGBM LambdaRank |
| Language experiments | AfriBERTa, Qwen, Hugging Face Transformers |
| Machine learning | PyTorch, scikit-learn |
| Model optimization | FP16, INT8, INT4 |
| Data processing | Pandas, NumPy |
| User interface | Gradio |
| Edge inference | Locally packaged BGE encoder and compressed document index |
| Version control | GitHub |

FAISS and SQLite were considered in the initial design but are not necessary components of the currently demonstrated inference pipeline.

## 7. Agricultural Knowledge Base

The current benchmark contains:

| Dataset component | Records |
|---|---:|
| Agricultural documents | 695 |
| Training queries | 308 |
| Unlabelled test queries | 200 |
| Relevance judgements | 4,194 |

The corpus includes synthetic agricultural documents and associated metadata.

Organization names appearing in source fields do not necessarily indicate verified publications or endorsement by those organizations.

The dataset supports prototype development and retrieval benchmarking. Its provenance, licensing and agronomic accuracy require further verification before production use or redistribution.

## 8. Research Results

### Retrieval Performance

| Retrieval method | nDCG@5 |
|---|---:|
| BM25 | 0.4608 |
| Hybrid RRF | 0.7731 |
| E5 | 0.8081 |
| BGE | 0.8209 |
| LambdaRank | **0.8565** |

The optimized LambdaRank pipeline achieved an approximately **85.87% relative improvement in nDCG@5** over BM25 on the Phase 7 evaluation split.

Additional retrieval results include:

- LambdaRank MRR@5: 0.9444.
- Candidate Recall@100: 0.9872.
- CPU INT8 retrieval latency: approximately 40.36 milliseconds.
- Embedding storage reduction: approximately 74.74% compared with FP32.

### FarmDoc System Evaluation

The final functional evaluation tested 30 questions on each of the online and edge engines.

| Metric | Online engine | Edge engine |
|---|---:|---:|
| Functional test pass rate | 100% | 100% |
| Agricultural evidence coverage | 75.00% | 58.33% |
| Citation integrity checks | 100% | 100% |
| Guardrail test pass rate | 100% | 100% |
| Mean agricultural response latency | 0.2673 s | 1.5311 s |

These results describe the tested prototype's retrieval and software behaviour. They do not establish 100% factual accuracy or agricultural safety.

The evaluation includes synthetic language variants and previously used development questions.

## 9. Development Roadmap

| Phase | Development activity |
|---|---|
| 0 | Project setup and architecture |
| 1 | Dataset preparation |
| 2 | BM25 baseline |
| 3 | Dense retrieval |
| 4 | Hybrid retrieval |
| 5 | Basic RAG generation |
| 6 | Farmer language understanding |
| 7 | Advanced retrieval optimization |
| 8 | Evidence-grounded responses and safety screening |
| 9 | Model optimization and edge intelligence |
| 10 | FarmDoc application |
| 11 | Final system evaluation and packaging |

Completing these development milestones does not imply that the application has been independently validated or deployed on every intended platform.

## 10. Repository Organization

- `data/` — Agricultural datasets and language experiments.
- `docs/` — System architecture, methodology and dataset provenance.
- `evaluation/` — Retrieval benchmarks, final evaluation and performance charts.
- `farmdoc/` — FarmDoc source code, UI and application instructions.
- `notebooks/` — Research experiments and model development notebooks when integrated.
- `requirements.txt` — Research environment dependencies.

The application release package contains the local model assets and compressed document index; these are not included in the lightweight GitHub source update.

## 11. Running FarmDoc

Download and extract the FarmDoc application release package.

On Windows:

1. Run `install_windows.bat` while connected to the internet.
2. Run `start_windows.bat`.
3. Access `http://127.0.0.1:7860`.

The installed application is designed to execute local inference without relying on the remote API.

Physical internet-disconnection testing on the target device is still required.

## 12. Current Limitations and Future Research

The most important remaining activities are:

- Independently validate agricultural responses with agronomists or agricultural extension officers.
- Expand the evidence base using verified agricultural publications.
- Improve the generalization of Nigerian Pidgin and informal farmer-language understanding.
- Improve coverage and relevance for difficult agricultural questions.
- Validate the local application under actual internet disconnection.
- Establish reproducible deployment on additional low-resource devices.
- Investigate native smartphone inference and deployment.
- Establish permanent online hosting.

Qwen model quantization achieved substantial memory savings, but generated responses did not pass the project's strict evidence-screening benchmark. Reliable constrained generation remains future research.

## 13. Research and Safety Disclaimer

Agricultural-RAG-SLMe and FarmDoc are research prototypes.

Their responses are for informational purposes and are not substitutes for professional agricultural diagnosis, localized field inspection or qualified agricultural extension advice.

Recommendations involving pesticides, fertilizer rates, irrigation or crop treatment must be verified for local conditions.

## 14. Project Repository

https://github.com/chukwubuikemokoli963-max/Agricultural-RAG-SLMe
