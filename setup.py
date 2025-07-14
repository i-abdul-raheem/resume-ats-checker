#!/usr/bin/env python3
"""
Setup script for ATS Score Calculator
This script helps install dependencies and set up the environment.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("ATS Score Calculator - Setup Script")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install pip dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("Failed to install dependencies. Please check your internet connection and try again.")
        sys.exit(1)
    
    # Download NLTK data
    nltk_commands = [
        "python -c \"import nltk; nltk.download('punkt')\"",
        "python -c \"import nltk; nltk.download('stopwords')\"",
        "python -c \"import nltk; nltk.download('wordnet')\""
    ]
    
    for cmd in nltk_commands:
        if not run_command(cmd, "Downloading NLTK data"):
            print("Warning: Failed to download some NLTK data. The application may still work.")
    
    # Download spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy model"):
        print("Warning: Failed to download spaCy model. The application may still work.")
    
    print("\n" + "=" * 60)
    print("Setup completed!")
    print("=" * 60)
    
    print("\nTo start the API server:")
    print("  python main.py")
    print("  or")
    print("  uvicorn main:app --reload")
    
    print("\nTo test the functionality:")
    print("  python test_ats.py")
    
    print("\nAPI will be available at:")
    print("  http://localhost:8000")
    print("  http://localhost:8000/docs (API documentation)")

if __name__ == "__main__":
    main() 