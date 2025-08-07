#!/usr/bin/env python3
"""
Client example for ATS Score Calculator API
This script demonstrates how to use the API endpoints.
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False

def calculate_ats_score(resume_text, job_description):
    """Calculate ATS score using the API."""
    try:
        payload = {
            "resume_text": resume_text,
            "job_description": job_description
        }
        
        response = requests.post(f"{BASE_URL}/calculate-ats-score", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        return None

def analyze_resume(resume_text, job_description):
    """Get detailed resume analysis using the API."""
    try:
        payload = {
            "resume_text": resume_text,
            "job_description": job_description
        }
        
        response = requests.post(f"{BASE_URL}/analyze-resume", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        return None

def main():
    """Main function to demonstrate API usage."""
    # Test health check
    if not test_health_check():
        return
    
    # Sample data
    sample_resume = """
    JOHN DOE
    Software Engineer
    john.doe@email.com | (555) 123-4567
    
    SUMMARY
    Experienced software engineer with 5+ years developing scalable web applications using Python, JavaScript, and cloud technologies. Passionate about machine learning and data-driven solutions.
    
    EXPERIENCE
    Senior Software Engineer | TechCorp Inc. | 2020 - Present
    - Developed and maintained RESTful APIs using Python Flask and FastAPI
    - Implemented machine learning models for data analysis using scikit-learn and TensorFlow
    - Led a team of 3 developers in building a microservices architecture
    - Deployed applications using Docker and AWS services
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology | 2014 - 2018
    
    SKILLS
    Programming: Python, JavaScript, Java, SQL
    Frameworks: Flask, FastAPI, React, Node.js
    Cloud & DevOps: AWS, Docker, Kubernetes
    Machine Learning: TensorFlow, scikit-learn, pandas
    """
    
    sample_job_description = """
    Senior Software Engineer - Machine Learning Focus
    
    Requirements:
    - 5+ years of experience in software development
    - Strong proficiency in Python programming
    - Experience with machine learning frameworks (TensorFlow, PyTorch, scikit-learn)
    - Knowledge of cloud platforms (AWS, Azure, or GCP)
    - Experience with Docker and containerization
    - Bachelor's degree in Computer Science or related field
    
    Responsibilities:
    - Develop and maintain machine learning models and pipelines
    - Build scalable backend services using Python
    - Deploy and monitor applications in cloud environments
    """
    
    # Calculate ATS score
    result = calculate_ats_score(sample_resume, sample_job_description)
    
    if result:
        print(f"\nOverall ATS Score: {result['overall_score']}/100")
        
        print("\nIndividual Component Scores:")
        for component, score in result['scores'].items():
            print(f"  {component.replace('_', ' ').title()}: {score}/100")
        
        print("\nMatched Keywords:")
        if result['analysis']['matched_keywords']:
            print(f"  {', '.join(result['analysis']['matched_keywords'])}")
        
        print("\nMissing Keywords:")
        if result['analysis']['missing_keywords']:
            print(f"  {', '.join(result['analysis']['missing_keywords'])}")
        
        print("\nRecommendations:")
        for rec in result['analysis']['recommendations']:
            print(f"  • {rec}")
    
    # Get detailed analysis
    detailed_result = analyze_resume(sample_resume, sample_job_description)
    
    if detailed_result:
        print("\nDetailed Analysis Results:")
        print(json.dumps(detailed_result, indent=2))
        
        # Save results to file
        with open('api_test_results.json', 'w') as f:
            json.dump(detailed_result, f, indent=2)
        print("\nResults saved to 'api_test_results.json'")

if __name__ == "__main__":
    main() 