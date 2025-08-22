"""Q&A Generation Pipeline using synthetic-data-kit"""
import warnings
import tempfile
import os
from typing import List

from synthetic_data_kit.models.llm_client import LLMClient
from synthetic_data_kit.generators.qa_generator import QAGenerator
from synthetic_data_kit.utils.text import split_into_chunks
from synthetic_data_kit.parsers.pdf_parser import PDFParser

from models.pipeline_models import PipelineConfig, ChunkConfig, QAGenerationConfig


class QAGenerationPipeline:
    def __init__(self, model_name: str, api_base: str, api_key: str):
        config = PipelineConfig(
            model_name=model_name,
            api_base=api_base,
            api_key=api_key
        )
        self.client = LLMClient(
            api_base=config.api_base,
            model_name=config.model_name,
            api_key=config.api_key
        )
        self.generator = QAGenerator(client=self.client)
    
    def extract_pdf_text(self, pdf_content: bytes) -> str:
        """Extract text from PDF file content"""
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            # Create temporary file from bytes
            temp_dir = tempfile.mkdtemp()
            temp_file_path = os.path.join(temp_dir, "temp.pdf")
            
            try:
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(pdf_content)
                
                parser = PDFParser()
                text = parser.parse(temp_file_path)
                
                # Cleanup
                os.remove(temp_file_path)
                os.rmdir(temp_dir)
                
                return text
            except Exception as e:
                # Cleanup on error
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                if os.path.exists(temp_dir):
                    os.rmdir(temp_dir)
                raise e
    
    def chunk_text(self, text: str, max_sequence_lenght: int = 2048, overlap: int = 200) -> List[str]:
        """Split text into chunks"""
        config = ChunkConfig(
            text=text,
            max_sequence_lenght=max_sequence_lenght,
            overlap=overlap
        )
        return split_into_chunks(
            config.text, 
            chunk_size=config.max_sequence_lenght, 
            overlap=config.overlap
        )
    
    def generate_qa_pairs_from_text(self, chunks: List[str], num_pairs: int = 5, max_generation_tokens: int = 512) -> List[dict]:
        """Generate QA pairs from text chunks using LLM"""
        config = QAGenerationConfig(
            chunks=chunks,
            num_pairs=num_pairs,
            max_generation_tokens=max_generation_tokens
        )

        if hasattr(self.client, "config"):
            self.client.config.setdefault("generation", {})
            self.client.config["generation"]["max_tokens"] = config.max_generation_tokens
        
        all_qa_pairs = []
        for chunk in config.chunks:
            try:
                summary = self.generator.generate_summary(document_text=chunk)
                qa_pairs = self.generator.generate_qa_pairs(
                    num_pairs=config.num_pairs,
                    document_text=chunk,
                    summary=summary
                )
                all_qa_pairs.extend(qa_pairs)
            except Exception as e:
                print(f"Error processing chunk: {str(e)}")
                continue
        return all_qa_pairs


