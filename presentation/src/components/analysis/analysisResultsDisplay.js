import React from "react"

function AnalysisResultsDisplay(props) {
  const { predictions } = props
  return (
    <div>
      <h2>Finding: {predictions.finding ? "True" : "False"}</h2>
      <h3>Label probabilities</h3>
      <ul>
        {Object.keys(predictions.labels).map(label =>
          <li key={label}>
            {label + ": " + predictions.labels[label]}
          </li>)}
      </ul>
    </div>
  )
}

export default AnalysisResultsDisplay
