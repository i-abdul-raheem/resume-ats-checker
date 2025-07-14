# ATS Score Calculator - Project Overview

## 🎯 Project Description

The ATS Score Calculator is a comprehensive API that analyzes resumes against job descriptions to calculate Applicant Tracking System (ATS) compatibility scores. It uses advanced NLP techniques including BERT-based semantic similarity, keyword matching, and multi-factor analysis to provide detailed insights and recommendations.

## 🏗️ Architecture

### Core Components

1. **ATS Scorer Engine** (`ats_scorer.py`)
   - Semantic similarity using BERT embeddings
   - Keyword extraction and matching
   - Experience level analysis
   - Education requirement matching
   - Multi-factor weighted scoring

2. **FastAPI Web Server** (`main.py`)
   - RESTful API endpoints
   - Web interface serving
   - Health checks and monitoring
   - Input validation and error handling

3. **Web Interface** (`templates/index.html`)
   - User-friendly web form
   - Real-time score calculation
   - Visual results display
   - Responsive design

### Technology Stack

- **Backend**: Python 3.9+, FastAPI
- **NLP Models**: Sentence Transformers (BERT), spaCy, NLTK
- **ML Libraries**: scikit-learn, NumPy, Pandas
- **Deployment**: Docker, Docker Compose
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## 🔧 Key Features

### 1. Semantic Similarity Analysis
- Uses BERT-based embeddings to understand context and meaning
- Calculates cosine similarity between resume and job description
- Accounts for semantic relationships beyond exact keyword matches

### 2. Keyword Matching
- Extracts important keywords from both texts
- Identifies matched and missing keywords
- Provides actionable insights for resume improvement

### 3. Experience Level Alignment
- Detects experience requirements in job descriptions
- Analyzes resume for experience indicators
- Scores alignment between candidate and job requirements

### 4. Education Matching
- Identifies education requirements
- Compares candidate education levels
- Provides scoring based on educational fit

### 5. Comprehensive Scoring
- Weighted combination of multiple factors
- Overall ATS score (0-100)
- Individual component scores for detailed analysis

### 6. Actionable Recommendations
- Specific keyword suggestions
- Resume improvement tips
- Experience and education guidance

## 📊 Scoring Algorithm

The ATS score is calculated using a weighted combination of four components:

1. **Semantic Similarity (30%)**: BERT-based contextual understanding
2. **Keyword Match (40%)**: Direct keyword overlap analysis
3. **Experience Alignment (20%)**: Experience level compatibility
4. **Education Match (10%)**: Educational requirement fit

## 🚀 API Endpoints

### Core Endpoints

- `GET /` - Web interface
- `GET /api` - API information
- `GET /health` - Health check
- `POST /calculate-ats-score` - Calculate ATS score
- `POST /analyze-resume` - Detailed resume analysis
- `GET /docs` - Interactive API documentation

### Request/Response Format

**Request:**
```json
{
  "resume_text": "Resume content...",
  "job_description": "Job description content..."
}
```

**Response:**
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
    "matched_keywords": ["python", "machine learning"],
    "missing_keywords": ["docker", "kubernetes"],
    "recommendations": ["Add cloud computing experience"]
  }
}
```

## 🛠️ Installation & Setup

### Quick Start

1. **Clone and Setup:**
   ```bash
   git clone <repository>
   cd twitter-sentiment
   python setup.py
   ```

2. **Start the Server:**
   ```bash
   python main.py
   # or
   uvicorn main:app --reload
   ```

3. **Access the Application:**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t ats-scorer .
docker run -p 8000:8000 ats-scorer
```

## 🧪 Testing

### Test Scripts

- `test_ats.py` - Direct testing of the ATS scorer
- `client_example.py` - API client testing
- `setup.py` - Automated setup and dependency installation

### Sample Data

The project includes sample resume and job description data for testing the functionality.

## 📈 Performance Considerations

### Model Loading
- BERT model is loaded once at startup
- spaCy model is cached for efficiency
- NLTK data is downloaded during setup

### Response Times
- Typical response time: 2-5 seconds
- Depends on text length and complexity
- Semantic similarity calculation is the most time-intensive operation

### Scalability
- Stateless API design
- Can be horizontally scaled
- Docker containerization for easy deployment

## 🔒 Security & Privacy

- No external API calls (all processing is local)
- No data persistence (stateless processing)
- Input validation and sanitization
- Error handling without exposing sensitive information

## 🎨 User Interface

### Web Interface Features
- Clean, modern design
- Responsive layout
- Real-time score calculation
- Visual score indicators (color-coded)
- Detailed analysis display
- Keyword highlighting

### API Documentation
- Interactive Swagger UI
- Request/response examples
- Schema validation
- Try-it-out functionality

## 🔮 Future Enhancements

### Potential Improvements
1. **File Upload Support**: PDF, DOCX resume parsing
2. **Industry-Specific Scoring**: Tailored algorithms for different sectors
3. **Resume Optimization Suggestions**: AI-powered improvement recommendations
4. **Batch Processing**: Multiple resume analysis
5. **Custom Scoring Weights**: User-configurable scoring parameters
6. **Integration APIs**: Connect with job boards and ATS systems

### Technical Enhancements
1. **Model Optimization**: Faster inference with quantized models
2. **Caching**: Redis-based response caching
3. **Monitoring**: Prometheus metrics and Grafana dashboards
4. **Load Balancing**: Multiple instance deployment
5. **Database Integration**: Store analysis history and user preferences

## 📝 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the documentation at `/docs`
- Review the test examples
- Open an issue on the repository

---

**Built with ❤️ using FastAPI, BERT, and modern NLP techniques** 