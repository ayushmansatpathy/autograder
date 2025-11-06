from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Run the server with this command from backend/: 
# uvicorn app.main:app --reload
@app.get("/")
def read_root():
    return {"Hello": "World"}