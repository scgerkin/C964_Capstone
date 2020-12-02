import React, { useEffect, useRef, useState } from "react"
import ResultsChart from "./resultsChart"

const ResultsDisplay = ({ predictions }) => {
  const chartArea = useRef(null)
  const [chart, setChart] = useState(null)

  useEffect(() => {
    if (!chart) {
      setChart(new ResultsChart(chartArea.current, predictions.labels))
    }
  }, [chart, predictions])

  return (
    <>
      {!!predictions}
      <h2>Finding: {predictions.finding ? "True" : "False"}</h2>
      <div className="chart-area" ref={chartArea}/>
    </>
  )
}

export default ResultsDisplay
