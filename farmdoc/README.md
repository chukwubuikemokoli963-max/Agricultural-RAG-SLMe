# FarmDoc

Powered by Agricultural RAG SLMe

## Overview

FarmDoc is a resource-aware agricultural
information research prototype.

## Installation on Windows

1. Install a compatible Python version.
2. Extract the FarmDoc ZIP package.
3. Run install_windows.bat while connected
   to the internet.
4. Run start_windows.bat.

Alternatively:

python -m pip install -r requirements.txt
python app.py

Open:

http://127.0.0.1:7860

## Automatic connectivity handling

FarmDoc attempts to use its remote advanced
retrieval engine when available.

If the remote engine is unavailable, FarmDoc
uses its installed CPU edge engine and displays
the Edge indicator.

Remote availability is checked when the app
starts and when a question is submitted.

The temporary Kaggle/Gradio remote URL can
expire. Update remote_url in farmdoc_config.json
when a replacement endpoint is available.

Questions are transmitted to the remote server
when remote inference is available.

## Offline operation

The local application includes:

- BGE embedding model
- INT8 document embeddings
- 695 agricultural benchmark documents
- Language normalization rules
- Extractive evidence engine
- FarmDoc graphical interface

Internet access is not required for local
model inference after dependencies are installed.

## Limitations

The corpus contains synthetic benchmark
documents and has not been independently
validated for agricultural accuracy.

FarmDoc is not a confirmed crop diagnostic
system or a substitute for agricultural
extension services.

Mobile browser access to the remote demo
does not provide native offline mobile inference.

Review dataset and model redistribution
licenses before public distribution.
