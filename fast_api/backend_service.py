from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

app = FastAPI()

# Set your OpenAI API key
openai.api_key = ""  # Replace with your actual OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

class QueryRequest(BaseModel):
    query: str

@app.on_event("startup")
async def startup_event():
    global chat_engine
    try:
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        Settings.llm = OpenAI(
            model="gpt-4o",
            temperature=0.2,
            system_prompt="""You are an expert on 
            the <about your data> and your 
            job is to answer technical questions. 
            Assume that all questions are related 
            to the given data. Keep 
            your answers technical and based on 
            facts – do not hallucinate features.""",
        )
        index = VectorStoreIndex.from_documents(docs)
        chat_engine = index.as_chat_engine(
            chat_mode="condense_question", verbose=True, streaming=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during startup: {str(e)}")

@app.post("/query")
async def query_data(request: QueryRequest):
    try:
        if not chat_engine:
            raise HTTPException(status_code=500, detail="Chat engine not initialized")
        response_stream = chat_engine.stream_chat(request.query)
        response_text = "".join([chunk for chunk in response_stream.response_gen])
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
