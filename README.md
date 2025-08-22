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
├── src/
│   ├── qa_generation/
│   │   ├── __init__.py
│   │   └── pipeline.py          # Main pipeline implementation
│   └── models/
│       └── pipeline_models.py   # Pydantic validation models
├── test_pipeline.py             # Testing script
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
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

### Python API

```python
from src.qa_generation.pipeline import QAGenerationPipeline

# Initialize pipeline
pipeline = QAGenerationPipeline(
    model_name="openai/gpt-4o-mini",
    api_base="https://your-api-endpoint.com/v1",
    api_key="your-api-key"
)

# Read PDF file
with open("document.pdf", "rb") as f:
    pdf_content = f.read()

# Extract text
text = pipeline.extract_pdf_text(pdf_content)

# Create chunks
chunks = pipeline.chunk_text(text, chunk_size=2048, overlap=200)

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

Test the pipeline directly:

```bash
cd src
python qa_generation/pipeline.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0**: Initial release with PDF processing and QA generation
- Modular architecture with Pydantic validation
- Configurable generation parameters including max_generation_tokens