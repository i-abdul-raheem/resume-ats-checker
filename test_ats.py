#!/usr/bin/env python3
"""
Test script for ATS Score Calculator
This script demonstrates the functionality with sample resume and job description data.
"""

import json
from ats_scorer import ATSScorer

def test_ats_scoring():
    """Test the ATS scoring functionality with sample data."""
    
    # Sample resume text
    sample_resume = """
    JOHN DOE
    Software Engineer
    john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe
    
    SUMMARY
    Experienced software engineer with 5+ years developing scalable web applications using Python, JavaScript, and cloud technologies. Passionate about machine learning and data-driven solutions.
    
    EXPERIENCE
    Senior Software Engineer | TechCorp Inc. | 2020 - Present
    - Developed and maintained RESTful APIs using Python Flask and FastAPI
    - Implemented machine learning models for data analysis using scikit-learn and TensorFlow
    - Led a team of 3 developers in building a microservices architecture
    - Deployed applications using Docker and AWS services
    - Improved system performance by 40% through optimization and caching strategies
    
    Software Engineer | StartupXYZ | 2018 - 2020
    - Built full-stack web applications using React.js and Node.js
    - Integrated third-party APIs and payment systems
    - Collaborated with cross-functional teams using Agile methodologies
    - Used Git for version control and JIRA for project management
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology | 2014 - 2018
    
    SKILLS
    Programming: Python, JavaScript, Java, SQL
    Frameworks: Flask, FastAPI, React, Node.js, Django
    Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins
    Machine Learning: TensorFlow, scikit-learn, pandas, numpy
    Tools: Git, JIRA, Postman, VS Code
    """
    
    # Sample job description
    sample_job_description = """
    Senior Software Engineer - Machine Learning Focus
    
    We are looking for a Senior Software Engineer with expertise in machine learning and Python development to join our growing team.
    
    Requirements:
    - 5+ years of experience in software development
    - Strong proficiency in Python programming
    - Experience with machine learning frameworks (TensorFlow, PyTorch, scikit-learn)
    - Knowledge of cloud platforms (AWS, Azure, or GCP)
    - Experience with Docker and containerization
    - Familiarity with RESTful APIs and microservices architecture
    - Bachelor's degree in Computer Science or related field
    - Experience with Git version control and Agile methodologies
    
    Preferred Skills:
    - Experience with big data technologies (Spark, Hadoop)
    - Knowledge of Kubernetes and orchestration tools
    - Experience with CI/CD pipelines
    - Understanding of data engineering concepts
    - Experience with monitoring and logging tools
    
    Responsibilities:
    - Develop and maintain machine learning models and pipelines
    - Build scalable backend services using Python
    - Collaborate with data scientists and engineers
    - Deploy and monitor applications in cloud environments
    - Participate in code reviews and technical discussions
    """
    
    try:
        print("Initializing ATS Scorer...")
        scorer = ATSScorer()
        print("ATS Scorer initialized successfully!\n")
        
        print("Calculating ATS Score...")
        result = scorer.calculate_ats_score(sample_resume, sample_job_description)
        
        print("=" * 60)
        print("ATS SCORE ANALYSIS RESULTS")
        print("=" * 60)
        
        print(f"\nOverall ATS Score: {result['overall_score']}/100")
        
        print("\nIndividual Component Scores:")
        for component, score in result['scores'].items():
            print(f"  {component.replace('_', ' ').title()}: {score}/100")
        
        print("\nMatched Keywords:")
        if result['analysis']['matched_keywords']:
            print(f"  {', '.join(result['analysis']['matched_keywords'])}")
        else:
            print("  None found")
        
        print("\nMissing Keywords:")
        if result['analysis']['missing_keywords']:
            print(f"  {', '.join(result['analysis']['missing_keywords'])}")
        else:
            print("  None found")
        
        print("\nRecommendations:")
        for rec in result['analysis']['recommendations']:
            print(f"  • {rec}")
        
        print("\n" + "=" * 60)
        
        # Save results to JSON file
        with open('ats_test_results.json', 'w') as f:
            json.dump(result, f, indent=2)
        print("Results saved to 'ats_test_results.json'")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ats_scoring() 