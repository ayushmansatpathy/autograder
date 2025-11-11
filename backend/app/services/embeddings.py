from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pymupdf
import uuid
from io import BytesIO
from ..db.pinecone_client import pc


model = SentenceTransformer("all-MiniLM-L6-v2")
llm = OllamaLLM(model="llama3", temperature=0) # change to one instance

def extract_text_from_pdf(file_bytes):
    # Open the PDF from file bytes
    doc = pymupdf.open(stream=BytesIO(file_bytes), filetype="pdf")
    
    # Extract text from all pages and join them into a single string
    extracted_text = "\n".join(page.get_text() for page in doc)
    
    return extracted_text

def embed_doc(doc_text, doc_name):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,  # Adjust based on LLM or embedding model limits
        chunk_overlap=50,  # Small overlap for context continuity
        length_function=len,
    )
    chunks = text_splitter.split_text(doc_text)

    embeddings = []
    for idx, chunk in enumerate(chunks):
        embedding = model.encode(chunk)
        embeddings.append({
            "id": str(uuid.uuid4()),  # Generate a unique ID for each chunk
            "values": embedding,  # Change from "embedding" to "value"
            "metadata": {
                "chunk_index": idx,
                "text": chunk,
                "source_file": doc_name
            }
        })

    return embeddings

def retrieve_top_vectors(user_id, query):
    embedding = model.encode(query).tolist()  # Convert the query embedding to a list
    return pc.query_data(user_id, embedding)

def ask_llm(question, response, rubric): # tell llm we are going to give u the question number
    prompt = PromptTemplate( # edit prompt to pass boolean for awarding partial credit and negative grading
        template="""You are an assistant for grading student responses to assignment questions.
        Use the following information from the rubric to help you grade the student response. Tell
        me how many points the student should receive. Follow this rubric exactly, do not deviate from it. 
        Base your decision off of the rubric only. If you truly do not know, say you do not know. 
        Use three sentences maximum and keep your answer concise. 
        Here is the question, the student's response, and the rubric:
        Do award partial credit. Adhere to this.
        Question: {question}
        Student's Response: {response}
        Rubric Information: {rubric}""",
        input_variables=[question, response, rubric]
    )
    rag_chain = prompt | llm | StrOutputParser()
    answer = rag_chain.invoke({"question": question, "response": response, "rubric": rubric})
    return answer