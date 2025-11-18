"""Pydantic models for validation"""
from typing import List
from pydantic import BaseModel, Field, validator


class PipelineConfig(BaseModel):
    model_name: str = Field(..., min_length=1, description="Model name")
    api_base: str = Field(..., min_length=1, description="API base URL")
    api_key: str = Field(..., min_length=1, description="API key")


class ChunkConfig(BaseModel):
    text: str = Field(..., min_length=1, description="Text to chunk")
    max_sequence_lenght: int = Field(2048, gt=0, le=8192, description="Chunk size")
    overlap: int = Field(200, ge=0, description="Overlap size")
    
    @validator('overlap')
    def validate_overlap(cls, v, values):
        if 'max_sequence_lenght' in values and v >= values['max_sequence_lenght']:
            raise ValueError('Overlap must be less than max_sequence_lenght')
        return v


class QAGenerationConfig(BaseModel):
    chunks: List[str] = Field(..., min_items=1, description="Text chunks")
    num_pairs: int = Field(5, description="Number of QA pairs per chunk")
    max_generation_tokens: int = Field(512, description="Maximum tokens for generated responses")
