# Daily AI & Tech News Aggregator

## Overview
Automated RSS aggregator that:
- Collects 47 feeds
- Filters today's AI/tech-related articles
- Generates:
  - `index.html`
  - Markdown archive
  - `today_llm.txt`

Runs daily via GitHub Actions at **00:00 UTC (~07:00 Vietnam time)**.

---

## Setup

### 1. Clone repo
```bash
git clone <repo>
cd repo

## LLM Wiki Knowledge Structure

This project follows a knowledge organization approach inspired by Andrej Karpathy's "LLM Wiki" concept.

### Structure Overview
/
├── index.html
├── generate_news.py
├── requirements.txt
├── today_llm.txt
├── llms.txt
│
├── articles/
│   └── YYYY-MM-DD/
│       └── *.md
│
├── knowledge/
│   ├── ai/
│   │   ├── overview.md
│   │   ├── llms.md
│   │   ├── agents.md
│   │   └── research.md
│   │
│   ├── cybersecurity/
│   │   ├── overview.md
│   │   ├── threats.md
│   │   ├── vulnerabilities.md
│   │   └── tools.md
│   │
│   ├── hardware/
│   │   ├── overview.md
│   │   ├── chips.md
│   │   ├── gpus.md
│   │   └── architectures.md
│   │
│   ├── science/
│   │   ├── overview.md
│   │   ├── ai_research.md
│   │   └── math_ai.md
│   │
│   ├── creative/
│   │   ├── overview.md
│   │   ├── ai_music.md
│   │   ├── ai_art.md
│   │   └── tools.md
│   │
│   └── meta/
│       ├── sources.md
│       ├── glossary.md
│       └── taxonomy.md
│
├── summaries/
│   ├── daily/
│   │   └── YYYY-MM-DD.md
│   ├── weekly/
│   │   └── YYYY-WW.md
│   └── monthly/
│       └── YYYY-MM.md
│
├── embeddings/
│   ├── articles.json
│   └── knowledge.json
│
└── .github/
    └── workflows/
        └── daily-news.yml


### Purpose

- Optimized for **LLM ingestion**
- Enables **semantic retrieval & embeddings**
- Clean separation of:
  - Raw data (`articles/`)
  - Structured knowledge (`knowledge/`)
  - Summaries (`summaries/`)
  - Agent-readable index (`llms.txt`)

---

## Auto-Generate Structure

Run:

```bash
python create_structure.py

This will generate:

All folders
Empty markdown files
Agent-readable structure
llms.txt

Acts like robots.txt but for AI agents:

Lists important files
Entry point for parsing knowledge
Future Extensions
Vector embeddings (FAISS / Chroma)
Auto-linking between notes
AI summarization pipelines
Knowledge graph generation




License

MIT