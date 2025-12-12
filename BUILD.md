# BUILD.md

## Overview
This project is an AI-assisted autograder that uses a Retrieval-Augmented Generation (RAG) pipeline.  
The backend is a FastAPI service that ingests rubric or context text into a Pinecone vector index and uses a local LLM (via Ollama) to generate rubric-grounded grading feedback.  
The frontend is a Next.js application that communicates with the backend API.

---

## Prerequisites
- Python **3.11+**
- Node.js **18+**
- Ollama installed (for local LLM inference)
- A Pinecone account and API key

---

## Repository Structure
- `backend/` — FastAPI backend service and tests  
- `frontend/` — Next.js frontend application  

---

## Environment Variables
Create a `.env` file at the project root **or** inside the `backend/` directory.

Minimum required:
```
PINECONE_API_KEY=your_pinecone_api_key_here
```

Notes:
- The Pinecone index name is defined in `backend/app/db/pinecone_client.py` as `rubric-embeddings`.
- The backend will automatically create the index if it does not already exist.

---

## Dependencies

### Backend dependencies (Python)
Backend dependencies are defined in:
- `backend/requirements.txt`

Install them with:
```
pip install -r backend/requirements.txt
```

To verify installed packages:
```
pip freeze
```

---

### Frontend dependencies (Node / Next.js)
Frontend dependencies are defined in:
- `frontend/package.json`

Install them with:
```
cd frontend
npm install
```

To list installed packages:
```
npm ls --depth=0
```

---

## Backend Setup (FastAPI)

### 1. Create and activate virtual environment
From the project root:
```
python3.11 -m venv .venv
source .venv/bin/activate
```

### 2. Install backend dependencies
```
pip install -r backend/requirements.txt
```

### 3. Run the backend server
```
cd backend
uvicorn app.main:app --reload --port 8000
```

Backend will be available at:
```
http://127.0.0.1:8000
```

---

## Ollama Setup (Local LLM)

### 1. Pull the model
```
ollama pull llama3
```

Ollama runs locally at:
```
http://127.0.0.1:11434
```

If `ollama serve` reports that the address is already in use, Ollama is already running.

---

## Frontend Setup (Next.js)

### 1. Install frontend dependencies
```
cd frontend
npm install
```

### 2. Start the frontend development server
```
npm run dev
```

Frontend will be available at:
```
http://localhost:3000
```

---

## Testing

### Backend unit and integration tests
**Start the backend first** in a separate terminal:
```
cd backend
uvicorn app.main:app --reload --port 8000
```

Then run tests:
```
cd backend
pytest -v
```

---

## Evaluation and Benchmarks

### Latency evaluation
Measures end-to-end grading latency:
```
cd backend
../.venv/bin/python -m tests.eval_latency
```

---

### Load testing (concurrent users)
Simulates multiple simultaneous grading requests:
```
cd backend
../.venv/bin/python -m tests.load_test --n 2
../.venv/bin/python -m tests.load_test --n 5
../.venv/bin/python -m tests.load_test --n 10
../.venv/bin/python -m tests.load_test --n 20
```

---

## Troubleshooting

### Pinecone 401 Unauthorized
- Verify the API key in `.env`
- Restart the backend after updating `.env`
- Ensure the key belongs to the correct Pinecone project

### Tests cannot connect to backend
- Ensure the backend is running on port 8000
- Verify with:
```
curl http://127.0.0.1:8000/
```

### Python module not found after installation
You may be using system Python instead of the virtual environment.  
Run scripts using the virtual environment’s Python:
```
../.venv/bin/python -m tests.eval_latency
```
