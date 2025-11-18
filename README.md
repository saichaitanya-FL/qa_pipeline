# QA Generation Pipeline

A robust Question-Answer generation pipeline built with synthetic-data-kit that extracts text from PDF documents and generates high-quality QA pairs using Large Language Models.

## 🚀 Features

- **PDF Text Extraction**: Extract text from PDF documents with automatic preprocessing
- **Intelligent Chunking**: Split documents into optimal chunks with configurable overlap
- **QA Generation**: Generate contextual question-answer pairs using LLMs
- **Pydantic Validation**: Input validation with comprehensive error handling
- **Easy Integration**: Simple API for integration into existing workflows
- **Modular Architecture**: Clean, maintainable code structure

## 📁 Project Structure

```
qa-pipeline/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration
│   │   └── pipeline.py         # QA generation pipeline
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models
│   ├── __init__.py
│   └── main.py                 # FastAPI application
├── tests/
│   └── test_api.py             # API tests
├── .env                        # Environment variables
├── .env.example                # Example environment file
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
└── requirements.txt            # Dependencies
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd qa-pipeline
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Configuration

The pipeline requires:
- **API Base URL**: Your LLM service endpoint
- **API Key**: Authentication key for the LLM service
- **Model Name**: The specific model to use (e.g., "openai/gpt-4o-mini")

## 🚀 Usage

### FastAPI Endpoint

1. **Create .env file**
   ```bash
   MODEL_NAME=openai/gpt-4o-mini
   API_BASE=https://dev-gateway.flotorch.cloud/api/openai/v1
   API_KEY=your-api-key
   ```

2. **Start the server**
   ```bash
   python run.py
   ```
   
   Or:
   ```bash
   python -m app.main
   ```

3. **Generate QA pairs from PDF**
   ```bash
   curl -X POST "http://localhost:8000/generate-qa" \
     -F "file=@document.pdf" \
     -F "num_pairs=5" \
     -F "chunk_size=2048" \
     -F "overlap=200" \
     -F "max_tokens=512" \
     -F "max_chunks=10"
   ```

### Python API

```python
from app.core.pipeline import QAGenerationPipeline
from app.core.config import MODEL_NAME, API_BASE, API_KEY

# Initialize pipeline
pipeline = QAGenerationPipeline(
    model_name=MODEL_NAME,
    api_base=API_BASE,
    api_key=API_KEY
)

# Read PDF file
with open("document.pdf", "rb") as f:
    pdf_content = f.read()

# Extract text
text = pipeline.extract_pdf_text(pdf_content)

# Create chunks
chunks = pipeline.chunk_text(text, max_sequence_lenght=2048, overlap=200)

# Generate QA pairs
qa_pairs = pipeline.generate_qa_pairs_from_text(
    chunks=chunks, 
    num_pairs=5, 
    max_generation_tokens=512
)

# Display results
for i, qa in enumerate(qa_pairs, 1):
    print(f"Q{i}: {qa['question']}")
    print(f"A{i}: {qa['answer']}")
    print("-" * 50)
```

## 📋 API Reference

### FastAPI Endpoints

#### POST /generate-qa

Generate QA pairs from uploaded PDF file.

**Parameters:**
- `file` (required): PDF file upload
- `num_pairs` (optional, default=5): Number of QA pairs per chunk
- `chunk_size` (optional, default=2048): Size of text chunks
- `overlap` (optional, default=200): Overlap between chunks
- `max_tokens` (optional, default=512): Maximum tokens for generation
- `max_chunks` (optional, default=10): Maximum chunks to process

**Response:**
```json
{
  "filename": "document.pdf",
  "text_length": 47338,
  "num_chunks": 10,
  "qa_pairs": [
    {
      "question": "What is AI?",
      "answer": "Artificial Intelligence..."
    }
  ],
  "total_pairs": 20
}
```

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "pipeline_initialized": true
}
```

### QAGenerationPipeline

Main pipeline class for QA generation.

#### Methods

- **`__init__(model_name, api_base, api_key)`**
  - Initialize the pipeline with LLM configuration
  - Validates input parameters using Pydantic models

- **`extract_pdf_text(pdf_content: bytes) -> str`**
  - Extract text from PDF file content
  - Handles temporary file creation and cleanup
  - Returns extracted text as string

- **`chunk_text(text: str, chunk_size: int = 2048, overlap: int = 200) -> List[str]`**
  - Split text into manageable chunks
  - Configurable chunk size and overlap
  - Returns list of text chunks

- **`generate_qa_pairs_from_text(chunks: List[str], num_pairs: int = 5, max_generation_tokens: int = 512) -> List[dict]`**
  - Generate QA pairs from text chunks
  - Creates summary for each chunk
  - Returns list of QA dictionaries
  - Controls response length with max_generation_tokens parameter

### Validation Models

Located in `src/models/pipeline_models.py`:

- **PipelineConfig**: Validates pipeline initialization parameters
- **ChunkConfig**: Validates text chunking parameters
- **QAGenerationConfig**: Validates QA generation parameters

## 🔍 Parameters

### Chunking Parameters
- **chunk_size**: Size of each text chunk 
- **overlap**: Overlap between chunks 

### QA Generation Parameters
- **num_pairs**: Number of QA pairs per chunk (default: 5)
- **chunks**: List of text chunks to process
- **max_generation_tokens**: Maximum tokens for generated responses (default: 512)

## 🧪 Testing

Test the API:

```bash
# Start the server first
python -m app.main

# In another terminal, run tests
python tests/test_api.py
```
