from fastapi import APIRouter, UploadFile, File
from ..models.request import EmbedRubricRequest, QueryRequest, EmbedTextRequest
from ..models.response import QueryResponse
from ..services.embeddings import (
    extract_text_from_pdf,
    embed_doc,
    retrieve_top_vectors,
    ask_llm,
)
from ..db.pinecone_client import pc

router = APIRouter()


@router.post("/upload-rubric")
async def upload_and_store_doc(request, file: UploadFile = File(...)):
    file_bytes = await file.read()  # TODO: Store file on S3, filename on some DB
    extracted_text = extract_text_from_pdf(file_bytes)
    doc_embeddings = embed_doc(extracted_text, file.filename)
    pc.upsert_vectors(doc_embeddings, request.user_id)
    return {"message": "Rubric uploaded successfully"}


@router.post("/upload-text")
async def upload_text(request):
    extracted_text = request.text
    doc_embeddings = embed_doc(extracted_text, request.filename)
    pc.upsert_vectors(doc_embeddings, request.user_id)
    return {"message": "Rubric uploaded successfully"}


@router.post("/grade-answer")
async def grade_answer(request):
    query_response = retrieve_top_vectors(request.user_id, request.question)
    top_vectors = query_response["matches"]
    texts = [vector["metadata"]["text"] for vector in top_vectors]
    context = "\n".join(texts)
    answer = ask_llm(request.question, request.student_response, context)
    return {"response": answer}


question = "What are the 3 pillars of Object Oriented Programming?"
answer = "The 3 pillars are encapsulation, recursion , and threading."
query_response = retrieve_top_vectors(
    "12345test", "What are the 3 pillars of Object Oriented Programming?"
)
top_vectors = query_response["matches"]
texts = [vector["metadata"]["text"] for vector in top_vectors]
context = "\n".join(texts)
answer = ask_llm(question, answer, context)
print(answer)
