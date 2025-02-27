from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import fitz  # PyMuPDF
from openai import OpenAI
import os
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()
client = OpenAI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers, including file uploads
)


class TextInput(BaseModel):
    text: str
    length: str  # short, medium, long

def summarize_text(text: str, length: str):
    """Calls OpenAI API to generate a summary and key points."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant that summarizes text."},
            {"role": "user", "content": f"Summarize this text in a {length} format and extract key points: {text}"}
        ]
    )
    summary = response.choices[0].message.content
    return summary


def extract_text_from_pdf(pdf_file: UploadFile):
    """Extracts text from a PDF file."""
    pdf_reader = fitz.open(stream=pdf_file.file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in pdf_reader])
    return text


@app.post("/summarize")
def summarize(input: TextInput):
    """API endpoint to summarize text."""
    if not input.text.strip():
        return {"error": "Text cannot be empty."}
    summary = summarize_text(input.text, input.length)
    return {"summary": summary, "key_points": summary.split("\n")}  # Splitting summary into key points


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """API endpoint to handle file uploads and extract text."""
    if file.content_type == "application/pdf":
        text = extract_text_from_pdf(file)
    elif file.content_type.startswith("text/"):
        text = file.file.read().decode("utf-8")
    else:
        return {"error": "Unsupported file format."}

    return {"text": text}
