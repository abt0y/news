import os
from datetime import datetime

# Base structure definition
STRUCTURE = {
    "articles": {},
    "knowledge": {
        "ai": ["overview.md", "llms.md", "agents.md", "research.md"],
        "cybersecurity": ["overview.md", "threats.md", "vulnerabilities.md", "tools.md"],
        "hardware": ["overview.md", "chips.md", "gpus.md", "architectures.md"],
        "science": ["overview.md", "ai_research.md", "math_ai.md"],
        "creative": ["overview.md", "ai_music.md", "ai_art.md", "tools.md"],
        "meta": ["sources.md", "glossary.md", "taxonomy.md"]
    },
    "summaries": {
        "daily": [],
        "weekly": [],
        "monthly": []
    },
    "embeddings": ["articles.json", "knowledge.json"],
    ".github/workflows": ["daily-news.yml"]
}

ROOT_FILES = [
    "index.html",
    "generate_news.py",
    "requirements.txt",
    "today_llm.txt",
    "llms.txt"
]


def create_file(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("")


def create_structure(base_path="."):
    # Root files
    for file in ROOT_FILES:
        create_file(os.path.join(base_path, file))

    # Structured folders
    for folder, content in STRUCTURE.items():
        folder_path = os.path.join(base_path, folder)

        if isinstance(content, dict):
            for subfolder, files in content.items():
                sub_path = os.path.join(folder_path, subfolder)
                os.makedirs(sub_path, exist_ok=True)

                for file in files:
                    create_file(os.path.join(sub_path, file))

        elif isinstance(content, list):
            os.makedirs(folder_path, exist_ok=True)
            for file in content:
                create_file(os.path.join(folder_path, file))

        else:
            os.makedirs(folder_path, exist_ok=True)

    # Create today's article folder
    today = datetime.utcnow().strftime("%Y-%m-%d")
    os.makedirs(os.path.join(base_path, "articles", today), exist_ok=True)

    print("✅ LLM Wiki structure created successfully.")


if __name__ == "__main__":
    create_structure()