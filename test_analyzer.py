"""
Test script for the code quality analyzer.
"""
import json
import sys
from backend.main import analyze_python_code, analyze_js_code

def test_python_sample():
    """Test the Python analyzer with the sample file."""
    with open('backend/sample_files/bad_python_sample.py', 'r') as f:
        content = f.read()
    
    result = analyze_python_code(content)
    print("\n=== Python Sample Analysis ===")
    print(json.dumps(result, indent=2))
    return result

def test_js_sample():
    """Test the JavaScript analyzer with the sample file."""
    with open('backend/sample_files/bad_js_sample.jsx', 'r') as f:
        content = f.read()
    
    result = analyze_js_code(content)
    print("\n=== JavaScript Sample Analysis ===")
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    test_python_sample()
    test_js_sample() 