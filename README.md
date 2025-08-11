# Event GPT

**Event GPT** is an AI-powered event recommendation system for Germany, designed to fetch the latest events from public APIs, analyze community discussions, and provide intelligent, context-aware recommendations through a conversational interface.

## Tech Stack
- **Python** – core data processing
- **Sentence Transformers** – embeddings
- **ChromaDB** – vector storage
- **Streamlit** – interactive UI
- **APScheduler / cron** – periodic data updates
- **Docker** – deployment

---

## Installation
```bash
# Clone the repository
git clone https://github.com/<your-username>/event-gpt.git
cd event-gpt

# Create a virtual environment
python -m venv event-gpt
source venv/bin/activate   # on Windows: venv\Scripts\activate

# Install dependencies (will update later)
pip install -r requirements.txt
