from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re
import os
import tempfile
from typing import List, Dict, Any
import io

app = FastAPI(title="Code Quality Analyzer")

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Code Quality Analyzer API is running"}

@app.post("/analyze-code")
async def analyze_code(file: UploadFile = File(...)):
    """
    Analyze a code file and return quality metrics.
    
    Accepts .js, .jsx, or .py files and returns:
    - overall score out of 100
    - breakdown of scores by category
    - recommendations for improvement
    """
    # Check file extension
    filename = file.filename
    if not filename or not (filename.endswith(".py") or filename.endswith(".js") or filename.endswith(".jsx")):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only .py, .js, and .jsx files are supported."
        )
        
    content = await file.read()
    file_extension = os.path.splitext(filename)[1]
    
    if file_extension == ".py":
        return analyze_python_code(content.decode())
    else:
        return analyze_js_code(content.decode())

def analyze_python_code(content: str) -> Dict[str, Any]:
    """Analyze Python code for quality metrics."""
    
    lines = content.split('\n')
    
    # Initialize scores
    naming_score = 10
    modularity_score = 20
    comments_score = 20
    formatting_score = 15
    reusability_score = 15
    best_practices_score = 20
    
    recommendations = []
    
    # Analyze naming conventions
    naming_issues = analyze_python_naming(content)
    if naming_issues:
        naming_score -= min(len(naming_issues) * 2, 10)
        recommendations.extend(naming_issues[:2])  # Add up to 2 naming recommendations
        
    # Analyze function length and modularity
    modularity_issues = analyze_function_modularity(content, is_python=True)
    if modularity_issues:
        modularity_score -= min(len(modularity_issues) * 5, 20)
        recommendations.extend(modularity_issues[:1])  # Add up to 1 modularity recommendation
        
    # Analyze comments and documentation
    comments_issues = analyze_python_comments(content)
    if comments_issues:
        comments_score -= min(len(comments_issues) * 5, 20)
        recommendations.extend(comments_issues[:1])  # Add up to 1 comment recommendation
        
    # Analyze formatting
    formatting_issues = analyze_python_formatting(content)
    if formatting_issues:
        formatting_score -= min(len(formatting_issues) * 3, 15)
        recommendations.extend(formatting_issues[:1])  # Add up to 1 formatting recommendation
        
    # Analyze reusability and DRY principles
    reusability_issues = analyze_reusability(content, is_python=True)
    if reusability_issues:
        reusability_score -= min(len(reusability_issues) * 5, 15)
        recommendations.extend(reusability_issues[:1])  # Add up to 1 reusability recommendation
        
    # Analyze best practices
    best_practices_issues = analyze_python_best_practices(content)
    if best_practices_issues:
        best_practices_score -= min(len(best_practices_issues) * 5, 20)
        recommendations.extend(best_practices_issues[:1])  # Add up to 1 best practice recommendation
    
    # Calculate overall score
    overall_score = naming_score + modularity_score + comments_score + formatting_score + reusability_score + best_practices_score
    
    return {
        "overall_score": overall_score,
        "breakdown": {
            "naming": naming_score,
            "modularity": modularity_score,
            "comments": comments_score,
            "formatting": formatting_score,
            "reusability": reusability_score,
            "best_practices": best_practices_score
        },
        "recommendations": recommendations[:5]  # Limit to 5 recommendations
    }

def analyze_js_code(content: str) -> Dict[str, Any]:
    """Analyze JavaScript/JSX code for quality metrics."""
    
    lines = content.split('\n')
    
    # Initialize scores
    naming_score = 10
    modularity_score = 20
    comments_score = 20
    formatting_score = 15
    reusability_score = 15
    best_practices_score = 20
    
    recommendations = []
    
    # Analyze naming conventions
    naming_issues = analyze_js_naming(content)
    if naming_issues:
        naming_score -= min(len(naming_issues) * 2, 10)
        recommendations.extend(naming_issues[:2])  # Add up to 2 naming recommendations
        
    # Analyze function length and modularity
    modularity_issues = analyze_function_modularity(content, is_python=False)
    if modularity_issues:
        modularity_score -= min(len(modularity_issues) * 5, 20)
        recommendations.extend(modularity_issues[:1])  # Add up to 1 modularity recommendation
        
    # Analyze comments and documentation
    comments_issues = analyze_js_comments(content)
    if comments_issues:
        comments_score -= min(len(comments_issues) * 5, 20)
        recommendations.extend(comments_issues[:1])  # Add up to 1 comment recommendation
        
    # Analyze formatting
    formatting_issues = analyze_js_formatting(content)
    if formatting_issues:
        formatting_score -= min(len(formatting_issues) * 3, 15)
        recommendations.extend(formatting_issues[:1])  # Add up to 1 formatting recommendation
        
    # Analyze reusability and DRY principles
    reusability_issues = analyze_reusability(content, is_python=False)
    if reusability_issues:
        reusability_score -= min(len(reusability_issues) * 5, 15)
        recommendations.extend(reusability_issues[:1])  # Add up to 1 reusability recommendation
        
    # Analyze best practices
    best_practices_issues = analyze_js_best_practices(content)
    if best_practices_issues:
        best_practices_score -= min(len(best_practices_issues) * 5, 20)
        recommendations.extend(best_practices_issues[:1])  # Add up to 1 best practice recommendation
    
    # Calculate overall score
    overall_score = naming_score + modularity_score + comments_score + formatting_score + reusability_score + best_practices_score
    
    return {
        "overall_score": overall_score,
        "breakdown": {
            "naming": naming_score,
            "modularity": modularity_score,
            "comments": comments_score,
            "formatting": formatting_score,
            "reusability": reusability_score,
            "best_practices": best_practices_score
        },
        "recommendations": recommendations[:5]  # Limit to 5 recommendations
    }

# Analysis helper functions
def analyze_python_naming(content: str) -> List[str]:
    """Analyze Python naming conventions."""
    issues = []
    
    # Check for camelCase in functions (should be snake_case)
    func_pattern = re.compile(r'def\s+([A-Za-z0-9_]+)\s*\(')
    functions = func_pattern.findall(content)
    
    for func_name in functions:
        if any(c.isupper() for c in func_name):
            issues.append(f"Use snake_case for function names in Python (found '{func_name}').")
            
    # Check for non-snake_case variables
    var_pattern = re.compile(r'([A-Za-z][A-Za-z0-9_]*)\s*=\s*')
    variables = var_pattern.findall(content)
    
    for var_name in variables:
        if var_name in ["sum", "list", "dict", "set", "int", "str", "float", "bool", "type", "object"]:
            issues.append(f"Avoid using '{var_name}' as a variable name—it's a built-in Python name.")
        if any(c.isupper() for c in var_name) and not var_name.isupper():
            if not func_pattern.search(f"def {var_name}"):  # Make sure it's not already caught as a function
                issues.append(f"Use snake_case for variable names in Python (found '{var_name}').")
    
    return issues

def analyze_js_naming(content: str) -> List[str]:
    """Analyze JavaScript naming conventions."""
    issues = []
    
    # Check for snake_case in functions (should be camelCase)
    func_pattern = re.compile(r'(function|const|let|var)\s+([a-zA-Z0-9_$]+)\s*=?\s*(\(|\s*=>)')
    functions = func_pattern.findall(content)
    
    for func_type, func_name, _ in functions:
        if '_' in func_name and not func_name.startswith('_'):
            issues.append(f"Use camelCase for function/variable names in JavaScript (found '{func_name}').")
    
    # Check for React component naming (should be PascalCase)
    component_pattern = re.compile(r'(function|const|class)\s+([a-zA-Z0-9_$]+)\s*(?:extends React\.Component|\(props\)|\(\)\s*{)')
    components = component_pattern.findall(content)
    
    for _, comp_name in components:
        if comp_name[0].islower():
            issues.append(f"Use PascalCase for React component names (found '{comp_name}').")
    
    return issues

def analyze_function_modularity(content: str, is_python: bool) -> List[str]:
    """Analyze function length and modularity."""
    issues = []
    
    if is_python:
        # Find functions in Python code
        func_pattern = re.compile(r'def\s+([A-Za-z0-9_]+)\s*\(.*?\):(.*?)(?=(?:^def|\Z))', re.DOTALL | re.MULTILINE)
        functions = func_pattern.findall(content)
        
        for func_name, func_body in functions:
            lines = func_body.count('\n')
            if lines > 20:
                issues.append(f"Function '{func_name}' is too long ({lines} lines)—consider refactoring.")
            
            # Check indentation levels (nested blocks)
            max_indent = 0
            current_indent = 0
            for line in func_body.split('\n'):
                if line.strip() and line.startswith(' ' * 4):
                    indent_level = (len(line) - len(line.lstrip())) // 4
                    current_indent = indent_level
                    max_indent = max(max_indent, current_indent)
            
            if max_indent > 3:
                issues.append(f"Function '{func_name}' has deep nesting (level {max_indent})—simplify logic.")
    else:
        # Find functions in JS code
        func_pattern = re.compile(r'(?:function|const|let|var)\s+([A-Za-z0-9_$]+)\s*(?:=\s*(?:\(\)|\([^)]*\))\s*=>|[=\(][^{]*)\s*{(.*?)}(?=(?:function|\Z))', re.DOTALL)
        functions = func_pattern.findall(content)
        
        for func_name, func_body in functions:
            lines = func_body.count('\n')
            if lines > 20:
                issues.append(f"Function '{func_name}' is too long ({lines} lines)—consider refactoring.")
            
            # Check for deep nesting
            brackets_count = 0
            max_brackets = 0
            for char in func_body:
                if char == '{':
                    brackets_count += 1
                    max_brackets = max(max_brackets, brackets_count)
                elif char == '}':
                    brackets_count -= 1
            
            if max_brackets > 3:
                issues.append(f"Function '{func_name}' has deep nesting—simplify logic.")
    
    return issues

def analyze_python_comments(content: str) -> List[str]:
    """Analyze Python comments and documentation."""
    issues = []
    
    # Check for docstrings in functions
    func_pattern = re.compile(r'def\s+([A-Za-z0-9_]+)\s*\(.*?\):(.*?)(?=(?:^def|\Z))', re.DOTALL | re.MULTILINE)
    functions = func_pattern.findall(content)
    
    for func_name, func_body in functions:
        if not re.search(r'""".*?"""', func_body, re.DOTALL) and not re.search(r"'''.*?'''", func_body, re.DOTALL):
            issues.append(f"Add a docstring to explain the purpose of function '{func_name}'.")
    
    # Check for overall module docstring
    if not re.match(r'(?:""".*?"""|\'\'\'.*?\'\'\')', content.strip(), re.DOTALL):
        issues.append("Add a module-level docstring at the top of the file.")
    
    # Calculate comment ratio
    code_lines = [line for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
    comment_lines = [line for line in content.split('\n') if line.strip() and line.strip().startswith('#')]
    
    if len(code_lines) > 10 and len(comment_lines) / len(code_lines) < 0.1:
        issues.append("Add more comments to explain complex logic (less than 10% comment ratio).")
    
    return issues

def analyze_js_comments(content: str) -> List[str]:
    """Analyze JavaScript comments and documentation."""
    issues = []
    
    # Check for JSDoc comments in functions
    func_pattern = re.compile(r'(?:function|const|let|var)\s+([A-Za-z0-9_$]+)\s*(?:=\s*(?:\(\)|\([^)]*\))\s*=>|[=\(][^{]*)\s*{', re.DOTALL)
    functions = func_pattern.findall(content)
    
    for func_name in functions:
        jsdoc_pattern = re.compile(r'/\*\*[\s\S]*?\*/\s*(?:function|const|let|var)\s+' + re.escape(func_name))
        if not jsdoc_pattern.search(content):
            issues.append(f"Add JSDoc comments to document function '{func_name}'.")
    
    # Check for comments in React components
    component_pattern = re.compile(r'(function|const|class)\s+([a-zA-Z0-9_$]+)(?:\s+extends\s+React\.Component|\s*=\s*\((?:props|{[^}]*})\)\s*=>)', re.DOTALL)
    components = component_pattern.findall(content)
    
    for _, comp_name in components:
        if not re.search(r'/\*\*[\s\S]*?\*/\s*(?:function|const|class)\s+' + re.escape(comp_name), content):
            issues.append(f"Add JSDoc comments to document React component '{comp_name}'.")
    
    # Calculate comment ratio
    code_lines = [line for line in content.split('\n') if line.strip() and not line.strip().startswith('//') and not line.strip().startswith('/*')]
    comment_lines = [line for line in content.split('\n') if line.strip() and (line.strip().startswith('//') or line.strip().startswith('/*') or line.strip().startswith('*'))]
    
    if len(code_lines) > 10 and len(comment_lines) / len(code_lines) < 0.1:
        issues.append("Add more comments to explain complex logic (less than 10% comment ratio).")
    
    return issues

def analyze_python_formatting(content: str) -> List[str]:
    """Analyze Python formatting and indentation."""
    issues = []
    
    lines = content.split('\n')
    
    # Check line length
    long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 79]
    if long_lines:
        issues.append(f"Lines {', '.join(map(str, long_lines[:3]))} exceed the recommended limit of 79 characters.")
    
    # Check consistent indentation
    indent_sizes = set()
    for line in lines:
        leading_spaces = len(line) - len(line.lstrip(' '))
        if leading_spaces > 0 and leading_spaces % 2 == 0:
            indent_sizes.add(leading_spaces)
    
    if len(indent_sizes) > 1 and any(size % 4 != 0 for size in indent_sizes):
        issues.append("Use consistent indentation (PEP 8 recommends 4 spaces).")
    
    # Check for blank lines between functions
    func_lines = [i for i, line in enumerate(lines) if line.strip().startswith('def ')]
    for i in range(len(func_lines) - 1):
        if func_lines[i+1] - func_lines[i] < 3:  # Less than 2 blank lines between functions
            issues.append("Add two blank lines between function definitions (PEP 8).")
            break
    
    return issues

def analyze_js_formatting(content: str) -> List[str]:
    """Analyze JavaScript formatting and indentation."""
    issues = []
    
    lines = content.split('\n')
    
    # Check line length
    long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 80]
    if long_lines:
        issues.append(f"Lines {', '.join(map(str, long_lines[:3]))} exceed the recommended limit of 80 characters.")
    
    # Check consistent indentation
    indent_sizes = set()
    for line in lines:
        leading_spaces = len(line) - len(line.lstrip(' '))
        if leading_spaces > 0:
            indent_sizes.add(leading_spaces)
    
    if len(indent_sizes) > 1 and any(size % 2 != 0 for size in indent_sizes):
        issues.append("Use consistent indentation (2 or 4 spaces recommended).")
    
    # Check for semicolon usage
    missing_semicolons = [i+1 for i, line in enumerate(lines) 
                       if line.strip() and not line.strip().startswith('//') 
                       and not line.strip().startswith('/*')
                       and not line.strip().endswith('{')
                       and not line.strip().endswith('}')
                       and not line.strip().endswith(';')]
    
    if missing_semicolons and len(missing_semicolons) > len(lines) * 0.2:
        issues.append("Use semicolons consistently at the end of statements.")
    
    return issues

def analyze_reusability(content: str, is_python: bool) -> List[str]:
    """Analyze code for reusability and DRY (Don't Repeat Yourself) principles."""
    issues = []
    
    lines = content.split('\n')
    clean_lines = [line.strip() for line in lines if line.strip() and not (line.strip().startswith('#') or line.strip().startswith('//') or line.strip().startswith('/*'))]
    
    # Simple duplicate code detection
    code_blocks = {}
    for i, line in enumerate(clean_lines):
        if len(line) > 20:  # Only check substantial lines
            if line in code_blocks:
                code_blocks[line].append(i)
            else:
                code_blocks[line] = [i]
    
    duplicates = {line: positions for line, positions in code_blocks.items() if len(positions) > 1}
    if duplicates:
        issues.append("Possible code duplication detected. Consider refactoring repeated logic into functions.")
    
    # Check for hard-coded values
    magic_number_pattern = re.compile(r'[^0-9a-zA-Z][0-9]{2,}[^0-9a-zA-Z]')
    magic_numbers = magic_number_pattern.findall(content)
    if len(magic_numbers) > 3:
        issues.append("Replace magic numbers with named constants for better maintainability.")
    
    if is_python:
        # Check for long list comprehensions
        list_comp_pattern = re.compile(r'\[.* for .* in .*\]')
        list_comps = list_comp_pattern.findall(content)
        for comp in list_comps:
            if len(comp) > 60:
                issues.append("Long list comprehensions are hard to read. Consider breaking down into multiple lines or using a for loop.")
                break
    else:
        # Check for lack of component props validation in React
        if "React" in content and "prop" in content.lower():
            if "PropTypes" not in content and "interface" not in content and "type Props" not in content:
                issues.append("Add prop validation using PropTypes or TypeScript interfaces for React components.")
    
    return issues

def analyze_python_best_practices(content: str) -> List[str]:
    """Analyze Python code for best practices in web development."""
    issues = []
    
    # Check for exception handling
    try_blocks = len(re.findall(r'\btry\b', content))
    except_blocks = len(re.findall(r'\bexcept\b', content))
    
    if try_blocks > 0 and try_blocks == except_blocks and 'except:' in content:
        issues.append("Avoid bare 'except:' clauses. Catch specific exceptions instead.")
    
    # Check for proper imports
    if re.search(r'from\s+\S+\s+import\s+\*', content):
        issues.append("Avoid wildcard imports (from module import *). Be explicit about what you import.")
    
    # Check for context managers when handling files
    open_calls = re.findall(r'(\w+)\s*=\s*open\(', content)
    with_statements = len(re.findall(r'with\s+open\(', content))
    
    if open_calls and len(open_calls) > with_statements:
        issues.append("Use context managers ('with' statement) when working with files.")
    
    # Check for f-strings (modern Python)
    if re.search(r'\.format\(', content) and not re.search(r'f[\'"]', content):
        issues.append("Consider using f-strings for string formatting (Python 3.6+).")
    
    # Check for FastAPI best practices if applicable
    if "fastapi" in content.lower():
        if not re.search(r'from\s+pydantic\s+import', content) and "BaseModel" not in content:
            issues.append("Use Pydantic models for request/response validation in FastAPI.")
            
        if "async def" not in content and "app.add_middleware" in content:
            issues.append("Consider using async/await for API endpoints to improve concurrency.")
    
    return issues

def analyze_js_best_practices(content: str) -> List[str]:
    """Analyze JavaScript code for best practices in web development."""
    issues = []
    
    # Check for error handling
    try_blocks = len(re.findall(r'\btry\b', content))
    catch_blocks = len(re.findall(r'\bcatch\b', content))
    
    if try_blocks > 0 and try_blocks == catch_blocks and re.search(r'catch\s*\(\s*(?:error|err)?\s*\)', content):
        issues.append("Add error type checking in catch blocks instead of catching all errors.")
    
    # Check for modern JS syntax
    if "var " in content:
        issues.append("Use 'const' and 'let' instead of 'var' for variable declarations.")
    
    # Check for React hooks best practices
    if "useState" in content or "useEffect" in content:
        if "useEffect" in content and re.search(r'useEffect\(\s*\(\s*\)\s*=>\s*{[^}]*}\s*\)', content):
            issues.append("Add dependency array to useEffect hooks to prevent unnecessary renders.")
        
        if not re.search(r'use[A-Z]', content):
            issues.append("Extract complex logic into custom React hooks for better reusability.")
    
    # Check for async/await vs promises
    if ".then(" in content and "async" not in content:
        issues.append("Consider using async/await instead of promise chains for better readability.")
    
    # Check for proper event handling in React
    onclick_handlers = re.findall(r'onClick\s*=\s*{[^}]*}', content)
    if onclick_handlers and any("bind(this)" in handler for handler in onclick_handlers):
        issues.append("Use arrow functions or constructor binding for event handlers in React components.")
    
    # Check for inline styles
    if re.search(r'style\s*=\s*{\s*{', content):
        issues.append("Extract inline styles into CSS/SCSS files or styled-components for better maintainability.")
    
    return issues

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 