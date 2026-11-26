# FarmDoc System Architecture

## Online Engine

1. Farmer question
2. Language normalization
3. BM25, BGE and E5 retrieval
4. Reciprocal Rank Fusion
5. LambdaRank reranking
6. Evidence selection
7. Quality and safety screening
8. FarmDoc response

## Edge Engine

1. Farmer question
2. Language normalization
3. Local BGE encoder
4. INT8 document index
5. Local agricultural knowledge base
6. Evidence extraction
7. Quality and safety screening
8. FarmDoc response

## Automatic Connectivity Handling

When the remote service is available, FarmDoc uses advanced retrieval.

When the remote service is unavailable, the locally installed application uses the CPU edge engine and displays Edge.

Remote availability is checked at startup and when a question is submitted.

A remote-only browser session cannot perform inference after losing connectivity.

## Experimental Components

AfriBERTa: agricultural intent classification.

Qwen: FP16, INT8 and INT4 generation experiments.

Neither is required by the default extractive response engine.
