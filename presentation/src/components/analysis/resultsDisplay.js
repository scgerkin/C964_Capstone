import React from "react"

export default function resultsDisplay(props) {
  const { predictions } = props

  if (!predictions) return null

  return (
    <>
      <h2>Finding: {predictions.finding ? "True" : "False"}</h2>
      <h3>Label probabilities</h3>
      <ul>
        {Object.keys(predictions.labels).map(label =>
          <li key={label}>
            {label + ": " + predictions.labels[label]}
          </li>)}
      </ul>
    </>
  )
}
