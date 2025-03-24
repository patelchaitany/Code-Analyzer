# Code Quality Analyzer

A lightweight tool that analyzes React (JavaScript) or FastAPI (Python) code files and scores them on clean code practices, while also offering recommendations for improvement.

## Features

- Accepts .js, .jsx, or .py files for analysis
- Provides an overall score out of 100
- Breaks down scores by categories:
  - Naming conventions (10)
  - Function length and modularity (20)
  - Comments and documentation (20)
  - Formatting/indentation (15)
  - Reusability and DRY (15)
  - Best practices in web dev (20)
- Offers 3-5 recommendations for improvement

## Project Structure

```
└── BRC/
    ├── backend/
    │   ├── main.py                  # FastAPI backend code
    │   └── sample_files/            # Sample code files for testing
    │       ├── bad_python_sample.py
    │       └── bad_js_sample.jsx
    ├── frontend/
    │   ├── public/                  # Static files
    │   └── src/                     # React source code
    │       ├── components/
    │       │   ├── FileUploader.js
    │       │   ├── FileUploader.css
    │       │   ├── ResultDisplay.js
    │       │   └── ResultDisplay.css
    │       ├── App.js
    │       ├── App.css
    │       ├── index.js
    │       └── index.css
    ├── .github/
    │   └── workflows/
    │       └── code-quality.yml     # GitHub Action for code quality checks
    ├── requirements.txt             # Python dependencies
    ├── run.py                       # Script to run the backend server
    └── README.md
```

## Setup and Installation

### Backend (FastAPI)

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the backend server:
   ```
   python run.py
   ```
   or directly with uvicorn:
   ```
   uvicorn backend.main:app --reload
   ```

### Frontend (React)

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```

## Usage

1. Open the web interface at http://localhost:3000
2. Upload a .js, .jsx, or .py file
3. Click "Analyze" to get results
4. Review the score, breakdown, and recommendations

## API Endpoints

- `GET /` - Health check endpoint
- `POST /analyze-code` - Accepts a file upload and returns the analysis result

## Sample Test Files

Sample test files are included in the `backend/sample_files` directory:

- `bad_python_sample.py` - Example Python file with code quality issues
- `bad_js_sample.jsx` - Example React component with code quality issues

## GitHub Action Integration

This project includes a GitHub Action workflow (`.github/workflows/code-quality.yml`) that:

1. Runs on every pull request and push to main/master branches
2. Analyzes all modified Python and JavaScript files
3. Outputs the results as a comment on pull requests
4. Logs the results in the GitHub Action output for pushes

## Code Analysis Logic

The analyzer evaluates code based on these criteria:

1. **Naming conventions (10 points)**
   - Python: snake_case for functions/variables
   - JavaScript: camelCase for functions/variables, PascalCase for components

2. **Function length and modularity (20 points)**
   - Long functions (>20 lines)
   - Deep nesting levels

3. **Comments and documentation (20 points)**
   - Docstrings/JSDoc presence
   - Comment-to-code ratio
   - Module-level documentation

4. **Formatting/indentation (15 points)**
   - Line length
   - Consistent indentation
   - Proper spacing

5. **Reusability and DRY (15 points)**
   - Code duplication
   - Magic numbers
   - Component props validation (React)

6. **Best practices in web dev (20 points)**
   - Proper error handling
   - Modern syntax usage
   - Framework-specific best practices

## Future Improvements

- Support for more file types (.ts, .tsx)
- More detailed analysis with AST parsing
- Code fixing suggestions
- Integration with more code quality tools (ESLint, Pylint)
- User accounts to track improvements over time 