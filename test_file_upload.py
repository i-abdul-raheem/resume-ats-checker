#!/usr/bin/env python3
"""
Test script for ATS Score Calculator with file upload functionality
This script demonstrates how to use the file upload endpoints.
"""

import requests
import json
import os

# API base URL
BASE_URL = "http://localhost:8000"

def test_supported_formats():
    """Test the supported formats endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/supported-formats")
        if response.status_code == 200:
            data = response.json()
            print("✓ Supported formats endpoint working")
            print(f"  Supported formats: {', '.join(data['supported_formats'])}")
        else:
            print("✗ Supported formats endpoint failed")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API server. Make sure the server is running.")
        return False
    return True

def test_file_upload_with_text_file():
    """Test file upload with a text file."""
    try:
        # Create a sample text file
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
        
        # Write to temporary file
        with open('sample_resume.txt', 'w') as f:
            f.write(sample_resume)
        
        # Sample job description
        job_description = """
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
        
        # Prepare file upload
        with open('sample_resume.txt', 'rb') as f:
            files = {'resume_file': ('sample_resume.txt', f, 'text/plain')}
            data = {'job_description': job_description}
            
            response = requests.post(f"{BASE_URL}/calculate-ats-score-file", files=files, data=data)
        
        # Clean up temporary file
        os.remove('sample_resume.txt')
        
        if response.status_code == 200:
            result = response.json()
            print("✓ File upload test successful")
            print(f"  Overall Score: {result['overall_score']}/100")
            print(f"  File Info: {result['file_info']['filename']} ({result['file_info']['file_size']} bytes)")
            return result
        else:
            print(f"✗ File upload test failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ Error in file upload test: {e}")
        return None

def test_file_upload_analysis():
    """Test the detailed file analysis endpoint."""
    try:
        # Create a sample text file
        sample_resume = """
        JANE SMITH
        Data Scientist
        jane.smith@email.com | (555) 987-6543
        
        SUMMARY
        Data scientist with 3+ years experience in machine learning, statistical analysis, and data visualization. Expertise in Python, R, and SQL for data manipulation and modeling.
        
        EXPERIENCE
        Data Scientist | DataCorp | 2021 - Present
        - Built predictive models using scikit-learn and TensorFlow
        - Performed statistical analysis and A/B testing
        - Created data visualizations using matplotlib and seaborn
        - Collaborated with engineering teams to deploy ML models
        
        EDUCATION
        Master of Science in Data Science
        University of Analytics | 2019 - 2021
        
        SKILLS
        Programming: Python, R, SQL
        ML/AI: scikit-learn, TensorFlow, PyTorch
        Data Visualization: matplotlib, seaborn, Tableau
        Statistics: hypothesis testing, regression analysis
        """
        
        # Write to temporary file
        with open('sample_resume_analysis.txt', 'w') as f:
            f.write(sample_resume)
        
        # Sample job description
        job_description = """
        Senior Data Scientist
        
        Requirements:
        - 3+ years of experience in data science or machine learning
        - Strong programming skills in Python and SQL
        - Experience with machine learning frameworks (scikit-learn, TensorFlow)
        - Knowledge of statistical analysis and hypothesis testing
        - Master's degree in Data Science, Statistics, or related field
        
        Responsibilities:
        - Develop and deploy machine learning models
        - Perform statistical analysis and data visualization
        - Collaborate with cross-functional teams
        - Present findings to stakeholders
        """
        
        # Prepare file upload
        with open('sample_resume_analysis.txt', 'rb') as f:
            files = {'resume_file': ('sample_resume_analysis.txt', f, 'text/plain')}
            data = {'job_description': job_description}
            
            response = requests.post(f"{BASE_URL}/analyze-resume-file", files=files, data=data)
        
        # Clean up temporary file
        os.remove('sample_resume_analysis.txt')
        
        if response.status_code == 200:
            result = response.json()
            print("✓ File analysis test successful")
            print(f"  Overall Score: {result['ats_score']['overall_score']}/100")
            print(f"  File Info: {result['file_info']['filename']}")
            print(f"  Extracted Text Preview: {result['file_info']['extracted_text_preview'][:100]}...")
            return result
        else:
            print(f"✗ File analysis test failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ Error in file analysis test: {e}")
        return None

def main():
    """Main function to test file upload functionality."""
    print("=" * 60)
    print("ATS Score Calculator - File Upload Test")
    print("=" * 60)
    
    # Test supported formats
    if not test_supported_formats():
        return
    
    print("\n" + "=" * 60)
    print("TESTING FILE UPLOAD FUNCTIONALITY")
    print("=" * 60)
    
    # Test basic file upload
    result1 = test_file_upload_with_text_file()
    
    print("\n" + "=" * 60)
    print("TESTING DETAILED FILE ANALYSIS")
    print("=" * 60)
    
    # Test detailed file analysis
    result2 = test_file_upload_analysis()
    
    # Save results to file
    if result1 or result2:
        with open('file_upload_test_results.json', 'w') as f:
            json.dump({
                'basic_upload_test': result1,
                'detailed_analysis_test': result2
            }, f, indent=2)
        print("\nResults saved to 'file_upload_test_results.json'")
    
    print("\n" + "=" * 60)
    print("File upload testing completed!")
    print("=" * 60)

if __name__ == "__main__":
    main() 