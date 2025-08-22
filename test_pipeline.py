"""Test script for QA Generation Pipeline"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from qa_generation.pipeline import QAGenerationPipeline

def test_pipeline():
    """Test the QA generation pipeline with sample text"""
    
    # Configuration
    api_base = "https://dev-gateway.flotorch.cloud/api/openai/v1"
    model_name = "openai/gpt-4o-mini"
    api_key = input("Enter your API key: ")
    
    if not api_key:
        print("API key is required")
        return
    
    try:
        # Initialize pipeline
        print("Initializing pipeline...")
        pipeline = QAGenerationPipeline(
            model_name=model_name,
            api_base=api_base,
            api_key=api_key
        )
        print("✓ Pipeline initialized successfully")
        
        # Sample text
        sample_text = """
        Artificial Intelligence (AI) is a branch of computer science that aims to create 
        intelligent machines that work and react like humans. Some of the activities 
        computers with artificial intelligence are designed for include speech recognition, 
        learning, planning, and problem solving. AI research has been highly successful 
        in developing effective techniques for solving a wide range of problems, from 
        game playing to medical diagnosis. Machine learning is a subset of AI that 
        focuses on the development of algorithms that can learn and make decisions 
        from data without being explicitly programmed.
        """
        
        # Chunk text
        print("Chunking text...")
        chunks = pipeline.chunk_text(sample_text, max_sequence_lenght=1024, overlap=100)
        print(f"✓ Created {len(chunks)} chunks")
        
        # Generate QA pairs
        print("Generating QA pairs...")
        qa_pairs = pipeline.generate_qa_pairs_from_text(
            chunks=chunks,
            num_pairs=3,
            max_generation_tokens=256
        )
        print(f"✓ Generated {len(qa_pairs)} QA pairs")
        
        # Display results
        print("\n" + "="*50)
        print("GENERATED QA PAIRS")
        print("="*50)
        
        for i, qa in enumerate(qa_pairs, 1):
            print(f"\nQA Pair {i}:")
            print(f"Q: {qa.get('question', 'N/A')}")
            print(f"A: {qa.get('answer', 'N/A')}")
            print("-" * 30)
        
        print(f"\n✓ Test completed successfully!")
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")

if __name__ == "__main__":
    test_pipeline()