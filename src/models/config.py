"""
Pydantic models for Q&A pipeline configuration and validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from pathlib import Path


class PipelineConfig(BaseModel):
    """Configuration model for Q&A generation pipeline"""
    
    pdf_file: str = Field(..., description="Path to PDF file")
    base_url: str = Field(..., description="API base URL")
    api_key: str = Field(..., description="API key for authentication")
    max_sequence_length: int = Field(default=2048, ge=100, le=8192, description="Maximum sequence length for chunks")
    chunk_overlap: int = Field(default=200, ge=0, description="Overlap between chunks")
    num_pairs_per_chunk: int = Field(default=5, ge=1, le=20, description="Number of Q&A pairs per chunk")
    
    @validator('pdf_file')
    def validate_pdf_file(cls, v):
        if not Path(v).exists():
            raise ValueError(f'PDF file not found: {v}')
        if not v.lower().endswith('.pdf'):
            raise ValueError('File must be a PDF')
        return v
    
    @validator('chunk_overlap')
    def validate_chunk_overlap(cls, v, values):
        if 'max_sequence_length' in values and v >= values['max_sequence_length']:
            raise ValueError('chunk_overlap must be less than max_sequence_length')
        return v


class QAPair(BaseModel):
    """Model for Q&A pair"""
    
    question: str
    answer: str
    source_chunk: Optional[str] = None