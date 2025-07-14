# ATS Score Calculator

A comprehensive API that calculates ATS (Applicant Tracking System) scores by comparing resumes with job descriptions using advanced NLP techniques.

## Features

- **Semantic Similarity**: Uses BERT-based models to understand context and meaning
- **Keyword Matching**: Identifies and scores relevant keywords and skills
- **Experience Alignment**: Matches experience levels and requirements
- **Education Matching**: Compares educational requirements
- **Overall ATS Score**: Combines multiple factors for a comprehensive score

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download required NLTK data:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

4. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

### Start the API Server
```bash
uvicorn main:app --reload
```

### API Endpoints

#### POST /calculate-ats-score
Calculate ATS score for a resume against a job description using text input.

**Request Body:**
```json
{
  "resume_text": "Your resume content here...",
  "job_description": "Job description content here..."
}
```

#### POST /calculate-ats-score-file
Calculate ATS score using uploaded resume file (PDF, DOCX, TXT) and job description text.

**Request:** Multipart form data
- `resume_file`: Resume file (PDF, DOCX, or TXT)
- `job_description`: Job description text

#### POST /analyze-resume-file
Detailed resume analysis using uploaded file with comprehensive insights.

**Request:** Multipart form data
- `resume_file`: Resume file (PDF, DOCX, or TXT)
- `job_description`: Job description text

#### GET /supported-formats
Get list of supported file formats for resume upload.

**Response:**
```json
{
  "supported_formats": [".pdf", ".docx", ".txt"],
  "description": "Supported file formats for resume upload"
}
```

**Response (for all scoring endpoints):**
```json
{
  "overall_score": 85.5,
  "scores": {
    "semantic_similarity": 78.2,
    "keyword_match": 92.1,
    "experience_alignment": 88.7,
    "education_match": 82.3
  },
  "analysis": {
    "matched_keywords": ["python", "machine learning", "data analysis"],
    "missing_keywords": ["docker", "kubernetes"],
    "recommendations": ["Add more cloud computing experience", "Include specific project metrics"]
  },
  "file_info": {
    "filename": "resume.pdf",
    "file_size": 245760,
    "extracted_text_length": 1250
  }
}
```

## How It Works

1. **Text Preprocessing**: Cleans and normalizes both resume and job description text
2. **Semantic Analysis**: Uses BERT embeddings to understand semantic similarity
3. **Keyword Extraction**: Identifies important skills and requirements
4. **Multi-factor Scoring**: Combines various metrics for comprehensive evaluation
5. **Detailed Analysis**: Provides actionable feedback and recommendations

## Technical Details

- **Framework**: FastAPI for high-performance API
- **NLP Models**: Sentence Transformers (BERT-based) for semantic understanding
- **Text Processing**: spaCy and NLTK for advanced text analysis
- **Scoring Algorithm**: Custom weighted scoring system

## License

MIT License 