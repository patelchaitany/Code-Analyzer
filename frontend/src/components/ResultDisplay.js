import React from 'react';
import './ResultDisplay.css';

/**
 * ResultDisplay Component - Displays code analysis results
 * @param {Object} props - Component props
 * @param {Object} props.result - Analysis result from API
 */
function ResultDisplay({ result }) {
  if (!result) return null;
  
  const { overall_score, breakdown, recommendations } = result;
  
  /**
   * Get color based on score value
   * @param {number} score - Score value
   * @param {number} maxScore - Maximum possible score
   * @returns {string} CSS color value
   */
  const getScoreColor = (score, maxScore) => {
    const percentage = (score / maxScore) * 100;
    
    if (percentage >= 80) return '#4caf50'; // Green
    if (percentage >= 60) return '#ff9800'; // Orange
    return '#f44336'; // Red
  };
  
  /**
   * Render the score gauge based on score value
   * @param {string} label - Category label
   * @param {number} score - Score value
   * @param {number} maxScore - Maximum possible score
   * @returns {JSX.Element} Gauge component
   */
  const renderScoreGauge = (label, score, maxScore) => {
    const percentage = (score / maxScore) * 100;
    const color = getScoreColor(score, maxScore);
    
    return (
      <div className="score-gauge">
        <div className="score-label">{label}</div>
        <div className="gauge-container">
          <div 
            className="gauge-fill"
            style={{ 
              width: `${percentage}%`,
              backgroundColor: color
            }}
          />
        </div>
        <div className="score-value">{score}/{maxScore}</div>
      </div>
    );
  };
  
  return (
    <div className="result-display card">
      <h2>Analysis Results</h2>
      
      <div className="overall-score">
        <div 
          className="score-circle"
          style={{ borderColor: getScoreColor(overall_score, 100) }}
        >
          <span className="score-number">{overall_score}</span>
          <span className="score-label">out of 100</span>
        </div>
      </div>
      
      <div className="score-breakdown">
        <h3>Score Breakdown</h3>
        
        <div className="scores-grid">
          {renderScoreGauge('Naming', breakdown.naming, 10)}
          {renderScoreGauge('Modularity', breakdown.modularity, 20)}
          {renderScoreGauge('Comments', breakdown.comments, 20)}
          {renderScoreGauge('Formatting', breakdown.formatting, 15)}
          {renderScoreGauge('Reusability', breakdown.reusability, 15)}
          {renderScoreGauge('Best Practices', breakdown.best_practices, 20)}
        </div>
      </div>
      
      <div className="recommendations">
        <h3>Recommendations</h3>
        
        {recommendations.length > 0 ? (
          <ul className="recommendations-list">
            {recommendations.map((recommendation, index) => (
              <li key={index} className="recommendation-item">
                {recommendation}
              </li>
            ))}
          </ul>
        ) : (
          <p>No recommendations - Great job!</p>
        )}
      </div>
    </div>
  );
}

export default ResultDisplay; 