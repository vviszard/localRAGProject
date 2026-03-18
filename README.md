Local-RAG-Explorer: Privacy-First AI Document Assistant

A high-performance Retrieval-Augmented Generation (RAG) system engineered for local execution on resource-constrained hardware. This project focuses on eliminating cloud dependencies by utilizing small-parameter models and an event-driven context management system to provide 100% private, factual document analysis.
Hardware and Environment (Validated Specs)

    Host Processor: AMD Ryzen 5 4600G (6 Cores / 12 Threads)

    Environment: VirtualBox (Ubuntu 22.04 LTS Guest)

    Memory Allocation: 4GB RAM (Total System RAM)

    Inference Engine: Ollama (Local API)

    Language Model: Qwen2.5-1.5B (Quantized 4-bit)
System Requirements (Tested Specs)

    Processor: AMD Ryzen 5 4600G

    Setup: VirtualBox (running Ubuntu 22.04)

    Memory: 4GB RAM (Total)

    AI Engine: Ollama

    AI Model: Qwen2.5-1.5B (Compact version)

Key Features
1. Organized Code (Modular Design)

The project is split into two specialized parts to keep the code clean:

- brain_tools.py: The "worker" module. It handles reading different file types and breaking long text into smaller, readable pieces.

- ragQnA.py: The "brain" module. It manages the chat interface, remembers your conversation, and watches your files for changes.

2. Multi-File Support

No need to convert your files to text manually. The system automatically reads:

- Plain Text: .txt and .md (Markdown)

- Office Docs: .pdf and .docx (Word)

3. The "Live Sentry" (Auto-Update)

The system has a built-in "Sentry" that constantly watches your document folder.

- Instant Sync: If you add, edit, or delete a file, the AI updates its knowledge immediately.

- Background Work: The Sentry runs in the background so you can keep chatting while it updates.

4. Smart Text Chunking

To make sure the AI doesn't get overwhelmed by long documents, the system breaks text into 800-character "chunks."

- Context Overlap: Each chunk repeats a bit of the previous one (150 characters) so that sentences aren't cut in half and meaning isn't lost.

5. Fact-Checking & Memory

- Source Credits: The AI is required to tell you exactly which file it got its information from. This prevents the AI from "hallucinating" or making things up.

- Chat Memory: It remembers the last few things you said, so you can ask follow-up questions naturally.

Installation

    Install the necessary Python tools:
    Bash

    pip install ollama watchdog pypdf python-docx

    Download the AI model:
    Bash

    ollama pull qwen2.5:1.5b

    Create your document folder:
    Bash

    mkdir brainSpace

How to Use

    Drop your PDFs, Word docs, or Text files into the brainSpace folder.

    Start the program:
    Bash

    python3 ragQnA.py

    Type your questions into the terminal. If you update your files while the program is running, the AI will "learn" the new information automatically. 

---

## Hardware & Environment (Tested Specs)
- **Host CPU:** AMD Ryzen 5 4600G (6 Cores / 12 Threads)
- **Virtualization:** VirtualBox (Ubuntu 22.04+ Guest)
- **Memory Allocation:** 4GB RAM 
- **AI Model:** Qwen2.5-1.5B (Inference via Ollama)

