import React, { useState } from 'react';
import axios from 'axios';
import './FileUploader.css';

/**
 * FileUploader Component - Handles file uploads and API calls
 * @param {Object} props - Component props
 * @param {Function} props.onAnalysisStart - Called when analysis starts
 * @param {Function} props.onAnalysisResult - Called with analysis results
 * @param {Function} props.onError - Called with error message if API call fails
 */
function FileUploader({ onAnalysisStart, onAnalysisResult, onError }) {
  const [selectedFile, setSelectedFile] = useState(null);
  
  /**
   * Handle file selection
   * @param {Event} event - File input change event
   */
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const fileExtension = file.name.split('.').pop().toLowerCase();
      if (['js', 'jsx', 'py'].includes(fileExtension)) {
        setSelectedFile(file);
      } else {
        onError('Invalid file type. Please select a .js, .jsx, or .py file.');
        event.target.value = null;
      }
    }
  };
  
  /**
   * Handle file upload and analysis
   * @param {Event} event - Form submit event
   */
  const handleUpload = async (event) => {
    event.preventDefault();
    
    if (!selectedFile) {
      onError('Please select a file to analyze.');
      return;
    }
    
    // Create form data for file upload
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
      onAnalysisStart();
      
      // Send file to API for analysis
      const response = await axios.post('/analyze-code', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });
      
      // Call analysis result handler with API response
      onAnalysisResult(response.data);
    } catch (error) {
      // Handle API errors
      console.error('Error analyzing code:', error);
      
      let errorMessage = 'An error occurred while analyzing the code.';
      
      // Get detailed error message from API if available
      if (error.response && error.response.data && error.response.data.detail) {
        errorMessage = error.response.data.detail;
      }
      
      onError(errorMessage);
    }
  };
  
  return (
    <div className="file-uploader">
      <form onSubmit={handleUpload}>
        <div className="file-input-container">
          <label htmlFor="file-upload" className="file-input-label">
            Choose a file
            <input
              id="file-upload"
              type="file"
              accept=".js,.jsx,.py"
              onChange={handleFileChange}
              className="file-input"
            />
          </label>
          <span className="file-name">
            {selectedFile ? selectedFile.name : 'No file selected'}
          </span>
        </div>
        
        <button 
          type="submit" 
          className="analyze-button" 
          disabled={!selectedFile}
        >
          Analyze Code
        </button>
      </form>
    </div>
  );
}

export default FileUploader; 