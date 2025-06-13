# AI Caregiver Recommender Demo

A simple proof-of-concept web application that recommends suitable caregivers for elderly patients based on their health conditions. Built using:

- **Django** (web framework)
- **LangChain & RAG** (retrieval-augmented generation)
- **FAISS** (vector search for caregiver profiles)
- **Hugging Face Transformers** (local LLM inference)
- **Pandas** (data loading from Excel/CSV)

---

## Features

- **Web form** to collect an elderly patient’s health condition.
- **Semantic search** of caregiver profiles to find the top matches.
- **LLM-generated recommendations** in clean bullet-list format.
- **Source profile display** for transparency.

---

## Prerequisites

- **Python 3.11.4** (recommended)  
- **pyenv** (optional, for managing Python versions)  
- Git  
- A GitHub account (for pushing the demo)  

---

## Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/<your-username>/caregiver_demo.git
   cd caregiver_demo
   ```

2. **Create and activate a virtual environment**  
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows PowerShell
   ```

3. **Install required packages**  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Generate dummy data** (for testing)  
   ```bash
   python generate_dummy.py
   # Creates caregivers.xlsx in the project root
   ```

5. **Run the Django development server**  
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
   Open [http://127.0.0.1:8000/recommender/](http://127.0.0.1:8000/recommender/) in your browser.

---

## Usage

1. Enter a description of the patient’s condition, e.g.:  
   > `75-year-old with chronic kidney disease and limited mobility`
2. Click **Get Recommendations**.
3. View a bullet list of recommended caregivers and see the source profiles used for matching.

---

## Project Structure

```
caregiver_demo/
├── caregiver_project/    # Django settings & URLs
├── recommender/          # Main app: views, templates, retriever, utils
│   ├── templates/
│   │   └── recommender/
│   │       └── recommend.html
│   ├── retriever.py      # RAG pipeline & get_recommendations()
│   ├── utils.py          # Data loading & FAISS vector store
│   └── generate_dummy.py # Script to create sample Excel data
├── venv/                 # Python virtual environment (ignored by Git)
├── requirements.txt
├── README.md             # This file
└── db.sqlite3            # SQLite database (for Django; ignored by Git)
```

---

## Next Steps

- Swap the GPT-2 placeholder with a more powerful local LLM (e.g., LLaMA or Mistral).  
- Persist the FAISS index for faster startup.  
- Add user accounts, recommendation history, and feedback loops.  
- Deploy to a production server (e.g., Docker + Gunicorn + Nginx).  

---

## License

This demo is released under the MIT License. See [LICENSE](LICENSE) for details.
