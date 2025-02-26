from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

class NoteRequest(BaseModel):
    raw_text: str
    detail_level: int

async def query_llm(prompt: str):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:11434/generate", json={"prompt": prompt})
        response.raise_for_status()
        return response.json()

@app.post("/process")
async def process_notes(note: NoteRequest):
    try:
        prompt = f"Process the following note with detail level {note.detail_level}: {note.raw_text}"
        llm_response = await query_llm(prompt)
        return {
            "title": "Processed Note",
            "content": llm_response.get("content", "No content returned"),
            "detail_level": note.detail_level
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))