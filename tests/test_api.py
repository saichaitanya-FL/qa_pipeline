"""Test script for API endpoints"""
import requests

API_URL = "http://localhost:8000"

def test_api():
    # Health check
    print("Testing health check...")
    response = requests.get(f"{API_URL}/health")
    print(f"Health: {response.json()}\n")
    
    # Generate QA pairs
    pdf_path = input("Enter PDF file path: ")
    print("Generating QA pairs...")
    
    with open(pdf_path, "rb") as f:
        files = {"file": f}
        data = {
            "num_pairs": 3,
            "chunk_size": 2048,
            "overlap": 200,
            "max_tokens": 256,
            "max_chunks": 5
        }
        response = requests.post(f"{API_URL}/generate-qa", files=files, data=data)
    
    result = response.json()
    print(f"\nFilename: {result['filename']}")
    print(f"Text length: {result['text_length']}")
    print(f"Chunks: {result['num_chunks']}")
    print(f"Total QA pairs: {result['total_pairs']}\n")
    
    print("="*50)
    print("GENERATED QA PAIRS")
    print("="*50)
    
    for i, qa in enumerate(result['qa_pairs'], 1):
        print(f"\nQA Pair {i}:")
        print(f"Q: {qa.get('question', 'N/A')}")
        print(f"A: {qa.get('answer', 'N/A')}")
        print("-" * 30)

if __name__ == "__main__":
    test_api()
