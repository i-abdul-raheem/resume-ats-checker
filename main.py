from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
from ats_scorer import ATSScorer
from file_processor import FileProcessor
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ATS Score Calculator API",
    description="Calculate ATS scores by comparing resumes with job descriptions using advanced NLP",
    version="1.0.0"
)

# Initialize ATS Scorer and File Processor (will be loaded when first request comes)
ats_scorer = None
file_processor = None

class ATSRequest(BaseModel):
    resume_text: str = Field(..., description="The resume text content", min_length=10)
    job_description: str = Field(..., description="The job description text content", min_length=10)

class ATSResponse(BaseModel):
    overall_score: float = Field(..., description="Overall ATS score (0-100)")
    scores: Dict[str, float] = Field(..., description="Individual component scores")
    analysis: Dict[str, Any] = Field(..., description="Detailed analysis and recommendations")

@app.on_event("startup")
async def startup_event():
    """Initialize the ATS scorer and file processor on startup."""
    global ats_scorer, file_processor
    try:
        logger.info("Initializing ATS Scorer...")
        ats_scorer = ATSScorer()
        logger.info("ATS Scorer initialized successfully")
        
        logger.info("Initializing File Processor...")
        file_processor = FileProcessor()
        logger.info(f"File Processor initialized successfully. Supported formats: {file_processor.get_supported_formats()}")
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface."""
    try:
        with open("templates/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
        <body>
            <h1>ATS Score Calculator API</h1>
            <p>Web interface not found. Use the API endpoints directly:</p>
            <ul>
                <li>POST /calculate-ats-score - Calculate ATS score</li>
                <li>GET /health - Health check</li>
                <li>GET /docs - API documentation</li>
            </ul>
        </body>
        </html>
        """)

@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "message": "ATS Score Calculator API",
        "version": "1.0.0",
        "endpoints": {
            "POST /calculate-ats-score": "Calculate ATS score for resume vs job description",
            "GET /health": "Health check endpoint",
            "GET /docs": "Interactive API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    global ats_scorer
    if ats_scorer is None:
        raise HTTPException(status_code=503, detail="ATS Scorer not initialized")
    
    return {
        "status": "healthy",
        "ats_scorer_ready": ats_scorer is not None
    }

@app.post("/calculate-ats-score", response_model=ATSResponse)
async def calculate_ats_score(request: ATSRequest):
    """
    Calculate ATS score for a resume against a job description.
    
    This endpoint analyzes the semantic similarity, keyword matching,
    experience alignment, and education matching between the resume
    and job description to provide a comprehensive ATS score.
    """
    global ats_scorer
    
    if ats_scorer is None:
        raise HTTPException(status_code=503, detail="ATS Scorer not initialized")
    
    try:
        logger.info("Received ATS score calculation request")
        
        # Validate input
        if not request.resume_text.strip() or not request.job_description.strip():
            raise HTTPException(status_code=400, detail="Resume text and job description cannot be empty")
        
        # Calculate ATS score
        result = ats_scorer.calculate_ats_score(request.resume_text, request.job_description)
        
        logger.info(f"ATS score calculation completed: {result['overall_score']}")
        
        return ATSResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in ATS score calculation: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/analyze-resume")
async def analyze_resume(request: ATSRequest):
    """
    Detailed resume analysis endpoint.
    
    Provides more detailed analysis including:
    - Keyword extraction
    - Skills identification
    - Experience level detection
    - Education level detection
    """
    global ats_scorer
    
    if ats_scorer is None:
        raise HTTPException(status_code=503, detail="ATS Scorer not initialized")
    
    try:
        logger.info("Received resume analysis request")
        
        # Extract keywords
        resume_keywords = ats_scorer.extract_keywords(request.resume_text)
        job_keywords = ats_scorer.extract_keywords(request.job_description)
        
        # Extract experience and education levels
        resume_exp = ats_scorer.extract_experience_level(request.resume_text)
        job_exp = ats_scorer.extract_experience_level(request.job_description)
        resume_edu = ats_scorer.extract_education_level(request.resume_text)
        job_edu = ats_scorer.extract_education_level(request.job_description)
        
        # Calculate ATS score
        ats_result = ats_scorer.calculate_ats_score(request.resume_text, request.job_description)
        
        analysis_result = {
            "ats_score": ats_result,
            "detailed_analysis": {
                "resume_keywords": resume_keywords[:20],  # Top 20 keywords
                "job_keywords": job_keywords[:20],
                "experience_levels": {
                    "resume": resume_exp,
                    "job_requirement": job_exp
                },
                "education_levels": {
                    "resume": resume_edu,
                    "job_requirement": job_edu
                }
            }
        }
        
        return analysis_result
        
    except Exception as e:
        logger.error(f"Error in resume analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/calculate-ats-score-file")
async def calculate_ats_score_file(
    resume_file: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Calculate ATS score using uploaded resume file and job description text.
    
    Supports PDF, DOCX, and TXT file formats for resume upload.
    """
    global ats_scorer, file_processor
    
    if ats_scorer is None or file_processor is None:
        raise HTTPException(status_code=503, detail="Components not initialized")
    
    try:
        logger.info(f"Received file upload request: {resume_file.filename}")
        
        # Validate file format
        if not file_processor.is_supported_format(resume_file.filename):
            supported_formats = file_processor.get_supported_formats() + ['.txt']
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format. Supported formats: {', '.join(supported_formats)}"
            )
        
        # Read file content
        file_content = await resume_file.read()
        
        # Extract text from file
        resume_text = file_processor.extract_text_from_upload(file_content, resume_file.filename)
        
        if not resume_text:
            raise HTTPException(
                status_code=400, 
                detail="Failed to extract text from the uploaded file. Please check if the file is valid."
            )
        
        # Calculate ATS score
        result = ats_scorer.calculate_ats_score(resume_text, job_description)
        
        # Add file information to response
        result["file_info"] = {
            "filename": resume_file.filename,
            "file_size": len(file_content),
            "extracted_text_length": len(resume_text)
        }
        
        logger.info(f"ATS score calculation completed for {resume_file.filename}: {result['overall_score']}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in file-based ATS score calculation: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/analyze-resume-file")
async def analyze_resume_file(
    resume_file: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Detailed resume analysis using uploaded file.
    
    Provides comprehensive analysis including:
    - File text extraction
    - Keyword extraction
    - Skills identification
    - Experience level detection
    - Education level detection
    """
    global ats_scorer, file_processor
    
    if ats_scorer is None or file_processor is None:
        raise HTTPException(status_code=503, detail="Components not initialized")
    
    try:
        logger.info(f"Received file analysis request: {resume_file.filename}")
        
        # Validate file format
        if not file_processor.is_supported_format(resume_file.filename):
            supported_formats = file_processor.get_supported_formats() + ['.txt']
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format. Supported formats: {', '.join(supported_formats)}"
            )
        
        # Read file content
        file_content = await resume_file.read()
        
        # Extract text from file
        resume_text = file_processor.extract_text_from_upload(file_content, resume_file.filename)
        
        if not resume_text:
            raise HTTPException(
                status_code=400, 
                detail="Failed to extract text from the uploaded file. Please check if the file is valid."
            )
        
        # Extract keywords
        resume_keywords = ats_scorer.extract_keywords(resume_text)
        job_keywords = ats_scorer.extract_keywords(job_description)
        
        # Extract experience and education levels
        resume_exp = ats_scorer.extract_experience_level(resume_text)
        job_exp = ats_scorer.extract_experience_level(job_description)
        resume_edu = ats_scorer.extract_education_level(resume_text)
        job_edu = ats_scorer.extract_education_level(job_description)
        
        # Calculate ATS score
        ats_result = ats_scorer.calculate_ats_score(resume_text, job_description)
        
        analysis_result = {
            "ats_score": ats_result,
            "file_info": {
                "filename": resume_file.filename,
                "file_size": len(file_content),
                "extracted_text_length": len(resume_text),
                "extracted_text_preview": resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
            },
            "detailed_analysis": {
                "resume_keywords": resume_keywords[:20],  # Top 20 keywords
                "job_keywords": job_keywords[:20],
                "experience_levels": {
                    "resume": resume_exp,
                    "job_requirement": job_exp
                },
                "education_levels": {
                    "resume": resume_edu,
                    "job_requirement": job_edu
                }
            }
        }
        
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in file-based resume analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/supported-formats")
async def get_supported_formats():
    """Get list of supported file formats for resume upload."""
    global file_processor
    
    if file_processor is None:
        raise HTTPException(status_code=503, detail="File processor not initialized")
    
    return {
        "supported_formats": file_processor.get_supported_formats() + ['.txt'],
        "description": "Supported file formats for resume upload"
    }

if __name__ == "__main__":
    import sys
    port = 8002
    if len(sys.argv) > 1 and sys.argv[1] == "--port":
        port = int(sys.argv[2])
    uvicorn.run(app, host="0.0.0.0", port=port) 