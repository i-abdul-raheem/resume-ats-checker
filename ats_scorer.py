import re
import nltk
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ATSScorer:
    def __init__(self):
        """Initialize the ATS Scorer with necessary models and data."""
        try:
            # Load BERT model for semantic similarity
            self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Loaded semantic model successfully")
            
            # Load spaCy model for NLP tasks
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded spaCy model successfully")
            
            # Initialize NLTK components
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
            
            # Common technical skills and keywords
            self.technical_skills = {
                'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'go', 'rust', 'swift', 'kotlin'],
                'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sql server'],
                'frameworks': ['django', 'flask', 'react', 'angular', 'vue', 'spring', 'express', 'fastapi'],
                'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
                'ml_ai': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'nlp', 'computer vision'],
                'tools': ['git', 'jira', 'confluence', 'slack', 'postman', 'figma', 'tableau', 'power bi']
            }
            
            # Education levels mapping
            self.education_levels = {
                'high school': 1,
                'associate': 2,
                'bachelor': 3,
                'master': 4,
                'phd': 5,
                'doctorate': 5
            }
            
            # Experience level keywords
            self.experience_keywords = {
                'entry': ['entry level', 'junior', '0-2 years', '1-2 years'],
                'mid': ['mid level', 'intermediate', '3-5 years', '4-6 years'],
                'senior': ['senior', 'lead', '5+ years', '6+ years', '7+ years'],
                'expert': ['expert', 'principal', 'architect', '10+ years']
            }
            
        except Exception as e:
            logger.error(f"Error initializing ATS Scorer: {e}")
            raise
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis."""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\-\.]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # Tokenize
        tokens = word_tokenize(processed_text)
        
        # Remove stopwords and lemmatize
        keywords = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                lemmatized = self.lemmatizer.lemmatize(token)
                keywords.append(lemmatized)
        
        return keywords
    
    def calculate_semantic_similarity(self, resume_text: str, job_description: str) -> float:
        """Calculate semantic similarity between resume and job description using BERT."""
        try:
            # Encode texts
            resume_embedding = self.semantic_model.encode([resume_text])
            job_embedding = self.semantic_model.encode([job_description])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
            
            # Convert to percentage
            return float(similarity * 100)
            
        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {e}")
            return 0.0
    
    def calculate_keyword_match(self, resume_text: str, job_description: str) -> Tuple[float, List[str], List[str]]:
        """Calculate keyword matching score between resume and job description."""
        try:
            # Extract keywords
            resume_keywords = set(self.extract_keywords(resume_text))
            job_keywords = set(self.extract_keywords(job_description))
            
            # Find matched and missing keywords
            matched_keywords = list(resume_keywords.intersection(job_keywords))
            missing_keywords = list(job_keywords - resume_keywords)
            
            # Calculate score
            if len(job_keywords) == 0:
                return 0.0, matched_keywords, missing_keywords
            
            match_score = (len(matched_keywords) / len(job_keywords)) * 100
            
            return float(match_score), matched_keywords, missing_keywords
            
        except Exception as e:
            logger.error(f"Error calculating keyword match: {e}")
            return 0.0, [], []
    
    def extract_education_level(self, text: str) -> int:
        """Extract education level from text."""
        text_lower = text.lower()
        
        for level, score in self.education_levels.items():
            if level in text_lower:
                return score
        
        return 0
    
    def calculate_education_match(self, resume_text: str, job_description: str) -> float:
        """Calculate education level matching score."""
        try:
            resume_education = self.extract_education_level(resume_text)
            job_education = self.extract_education_level(job_description)
            
            if job_education == 0:
                return 100.0  # No education requirement specified
            
            if resume_education >= job_education:
                return 100.0
            else:
                # Penalize for lower education level
                penalty = (job_education - resume_education) * 20
                return max(0.0, 100.0 - penalty)
                
        except Exception as e:
            logger.error(f"Error calculating education match: {e}")
            return 0.0
    
    def extract_experience_level(self, text: str) -> str:
        """Extract experience level from text."""
        text_lower = text.lower()
        
        for level, keywords in self.experience_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return level
        
        return "unknown"
    
    def calculate_experience_alignment(self, resume_text: str, job_description: str) -> float:
        """Calculate experience level alignment score."""
        try:
            resume_exp = self.extract_experience_level(resume_text)
            job_exp = self.extract_experience_level(job_description)
            
            if job_exp == "unknown":
                return 100.0  # No experience requirement specified
            
            # Experience level scoring
            exp_scores = {"entry": 1, "mid": 2, "senior": 3, "expert": 4}
            
            resume_score = exp_scores.get(resume_exp, 0)
            job_score = exp_scores.get(job_exp, 0)
            
            if resume_score >= job_score:
                return 100.0
            else:
                # Penalize for lower experience level
                penalty = (job_score - resume_score) * 25
                return max(0.0, 100.0 - penalty)
                
        except Exception as e:
            logger.error(f"Error calculating experience alignment: {e}")
            return 0.0
    
    def generate_recommendations(self, missing_keywords: List[str], scores: Dict[str, float]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Keyword-based recommendations
        if missing_keywords:
            top_missing = missing_keywords[:5]  # Top 5 missing keywords
            recommendations.append(f"Add keywords: {', '.join(top_missing)}")
        
        # Score-based recommendations
        if scores.get('semantic_similarity', 0) < 70:
            recommendations.append("Improve resume content to better match job requirements")
        
        if scores.get('experience_alignment', 0) < 80:
            recommendations.append("Highlight relevant experience that matches the job level")
        
        if scores.get('education_match', 0) < 80:
            recommendations.append("Consider additional education or certifications")
        
        if not recommendations:
            recommendations.append("Resume looks well-aligned with the job description")
        
        return recommendations
    
    def calculate_ats_score(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Calculate comprehensive ATS score for resume against job description."""
        try:
            logger.info("Starting ATS score calculation")
            
            # Calculate individual scores
            semantic_score = self.calculate_semantic_similarity(resume_text, job_description)
            keyword_score, matched_keywords, missing_keywords = self.calculate_keyword_match(resume_text, job_description)
            education_score = self.calculate_education_match(resume_text, job_description)
            experience_score = self.calculate_experience_alignment(resume_text, job_description)
            
            # Weighted overall score
            weights = {
                'semantic_similarity': 0.3,
                'keyword_match': 0.4,
                'experience_alignment': 0.2,
                'education_match': 0.1
            }
            
            overall_score = (
                semantic_score * weights['semantic_similarity'] +
                keyword_score * weights['keyword_match'] +
                experience_score * weights['experience_alignment'] +
                education_score * weights['education_match']
            )
            
            # Generate recommendations
            scores = {
                'semantic_similarity': semantic_score,
                'keyword_match': keyword_score,
                'experience_alignment': experience_score,
                'education_match': education_score
            }
            
            recommendations = self.generate_recommendations(missing_keywords, scores)
            
            result = {
                'overall_score': round(overall_score, 1),
                'scores': {k: round(v, 1) for k, v in scores.items()},
                'analysis': {
                    'matched_keywords': matched_keywords[:10],  # Top 10 matches
                    'missing_keywords': missing_keywords[:10],  # Top 10 missing
                    'recommendations': recommendations
                }
            }
            
            logger.info(f"ATS score calculation completed. Overall score: {overall_score}")
            return result
            
        except Exception as e:
            logger.error(f"Error in ATS score calculation: {e}")
            return {
                'overall_score': 0.0,
                'scores': {
                    'semantic_similarity': 0.0,
                    'keyword_match': 0.0,
                    'experience_alignment': 0.0,
                    'education_match': 0.0
                },
                'analysis': {
                    'matched_keywords': [],
                    'missing_keywords': [],
                    'recommendations': ['Error occurred during analysis']
                }
            } 