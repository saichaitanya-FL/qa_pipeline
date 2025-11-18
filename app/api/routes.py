"""API routes"""
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.core.config import MODEL_NAME, API_BASE, API_KEY
from app.core.pipeline import QAGenerationPipeline

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=1)


def process_pdf_sync(pdf_content, chunk_size, overlap, num_pairs, max_tokens, max_chunks):
    """Synchronous function to process PDF and generate QA pairs"""
    pipeline = QAGenerationPipeline(
        model_name=MODEL_NAME,
        api_base=API_BASE,
        api_key=API_KEY
    )
    
    text = pipeline.extract_pdf_text(pdf_content)
    print(f"Extracted text length: {len(text)} characters")
    
    chunks = pipeline.chunk_text(text, max_sequence_lenght=chunk_size, overlap=overlap)
    print(f"Created {len(chunks)} chunks")
    
    if len(chunks) > max_chunks:
        print(f"Limiting to first {max_chunks} chunks (out of {len(chunks)})")
        chunks = chunks[:max_chunks]
    
    print(f"Processing {len(chunks)} chunks with num_pairs={num_pairs}, max_tokens={max_tokens}")
    qa_pairs = pipeline.generate_qa_pairs_from_text(
        chunks=chunks,
        num_pairs=num_pairs,
        max_generation_tokens=max_tokens
    )
    print(f"Generated {len(qa_pairs)} QA pairs")
    
    return {
        "text_length": len(text),
        "num_chunks": len(chunks),
        "qa_pairs": qa_pairs,
        "total_pairs": len(qa_pairs)
    }


@router.post("/generate-qa")
async def generate_qa_from_pdf(
    file: UploadFile = File(...),
    num_pairs: Optional[int] = Form(5),
    chunk_size: Optional[int] = Form(2048),
    overlap: Optional[int] = Form(200),
    max_tokens: Optional[int] = Form(512),
    max_chunks: Optional[int] = Form(10)
):
    """Generate QA pairs from uploaded PDF"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        print(f"\n{'='*60}")
        print(f"Processing file: {file.filename}")
        pdf_content = await file.read()
        print(f"PDF content size: {len(pdf_content)} bytes")
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            process_pdf_sync,
            pdf_content, chunk_size, overlap, num_pairs, max_tokens, max_chunks
        )
        
        result["filename"] = file.filename
        print(f"{'='*60}\n")
        return result
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "pipeline_initialized": True}
