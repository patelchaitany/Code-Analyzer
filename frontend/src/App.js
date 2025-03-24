import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import ResultDisplay from './components/ResultDisplay';
import './App.css';

/**
 * Main App component for the Code Quality Analyzer
 */
function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  /**
   * Handle file analysis results
   * @param {Object} data - Analysis results from the API
   */
  const handleAnalysisResult = (data) => {
    setResult(data);
    setLoading(false);
  };

  /**
   * Handle API errors
   * @param {string} errorMessage - Error message
   */
  const handleError = (errorMessage) => {
    setError(errorMessage);
    setLoading(false);
  };

  /**
   * Set loading state when analysis starts
   */
  const handleAnalysisStart = () => {
    setLoading(true);
    setError('');
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Code Quality Analyzer</h1>
        <p>Upload a .js, .jsx, or .py file to analyze its code quality</p>
      </header>
      
      <main className="container">
        <div className="card">
          <FileUploader 
            onAnalysisStart={handleAnalysisStart}
            onAnalysisResult={handleAnalysisResult}
            onError={handleError}
          />

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          {loading && (
            <div className="loading-message">
              Analyzing code... Please wait.
            </div>
          )}
        </div>
        
        {result && (
          <ResultDisplay result={result} />
        )}
      </main>
      
      <footer className="app-footer">
        <p>Code Quality Analyzer &copy; 2023</p>
      </footer>
    </div>
  );
}

export default App; 