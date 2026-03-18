Local-RAG-Explorer: Privacy-First AI Document Assistant

A high-performance Retrieval-Augmented Generation (RAG) system engineered for local execution on resource-constrained hardware. This project focuses on eliminating cloud dependencies by utilizing small-parameter models and an event-driven context management system to provide 100% private, factual document analysis.
Hardware and Environment (Validated Specs)

    Host Processor: AMD Ryzen 5 4600G (6 Cores / 12 Threads)

    Environment: VirtualBox (Ubuntu 22.04 LTS Guest)

    Memory Allocation: 4GB RAM (Total System RAM)

    Inference Engine: Ollama (Local API)

    Language Model: Qwen2.5-1.5B (Quantized 4-bit)

Core Engineering Features
1. Modular System Architecture

The project follows a decoupled design to separate concerns between document processing and the AI inference loop:

    brain_tools.py: Acts as the "Peripheral Driver" module, containing optimized parsers for various file formats and the text-chunking logic.

    ragQnA.py: The "Main Control Unit" that manages the user interface, the conversation state, and the background monitoring thread.

2. Multi-Format Protocol Decoding

The system supports high-density text extraction from multiple document types without manual conversion:

    Standard: .txt and .md (Markdown)

    Binary/Rich Text: .pdf (via pypdf) and .docx (via python-docx)

3. The Live Sentry (Interrupt-Driven Updates)

Utilizing the Watchdog library, the system implements an event-driven background thread that monitors the filesystem for changes. It functions similarly to a hardware interrupt:

    Full Synchronization: Triggers a context refresh on File Created, Modified, Deleted, and Moved events.

    Non-Blocking Execution: The Sentry runs on a separate thread, ensuring that the main AI inference remains responsive during directory updates.

4. Sliding-Window Chunking

To maintain semantic integrity within the model's context window, data is processed using a sliding-window strategy:

    Chunk Size: 800 characters.

    Overlap: 150 characters.

    Logic: Prevents the loss of critical information that often occurs at hard-coded boundaries in long documents.

5. Deterministic Memory & Attribution

    FIFO Memory Buffer: Implements a First-In, First-Out rolling history to maintain conversational context without exceeding token limits.

    Source Attribution: Forces the LLM to prepend answers with source metadata (Filename and Part Number), eliminating hallucinations and providing 100% auditability.

Installation

    Install the required system dependencies:
    Bash

    pip install ollama watchdog pypdf python-docx

    Download the optimized 1.5B model:
    Bash

    ollama pull qwen2.5:1.5b

    Initialize the workspace:
    Bash

    mkdir brainSpace

Usage

    Populate the brainSpace directory with your technical documents (PDFs, Manuals, Notes).

    Launch the application:
    Bash

    python3 ragQnA.py

    The system will load all documents into RAM and enter an interactive CLI mode. Any subsequent changes to the files in brainSpace will be detected and integrated automatically by the Sentry thread.Local-RAG-Explorer: Privacy-First AI Document Assistant

A high-efficiency Retrieval-Augmented Generation (RAG) system designed to run on consumer-grade hardware. This project demonstrates how to feed high-density context into a small-parameter LLM to provide 100% factual, localized answers without relying on cloud APIs or external data processing.
Hardware & Environment (Tested Specs)

    Host CPU: AMD Ryzen 5 4600G (6 Cores / 12 Threads)

    Virtualization: VirtualBox (Ubuntu 22.04+ Guest)

    Memory Allocation: 4GB RAM

    AI Model: Qwen2.5-1.5B (Quantized 4-bit via Ollama)# Local-RAG-Explorer: Privacy-First AI Document Assistant

A lightweight Retrieval-Augmented Generation (RAG) system built to run on consumer-grade hardware. This project demonstrates how to bypass web-scraping restrictions and feed high-density context into a small-parameter LLM (0.5B) to provide 100% factual, localized answers without cloud APIs.

---

## Hardware & Environment (Tested Specs)
- **Host CPU:** AMD Ryzen 5 4600G (6 Cores / 12 Threads)
- **Virtualization:** VirtualBox (Ubuntu 22.04+ Guest)
- **Memory Allocation:** 4GB RAM 
- **AI Model:** Qwen2.5-1.5B (Inference via Ollama)

