import React, { useEffect, useRef, useState } from "react"
import D3Chart from "./D3Chart"

const ChartWrapper = ({gender}) => {
  const chartArea = useRef(null)
  const [chart, setChart] = useState(null)

  useEffect(() => {
    if (!chart) {
      setChart(new D3Chart(chartArea.current))
    } else if (chart.menData) {
      chart.update(gender)
    }
  }, [chart, gender])

  return (
    <div className="chart-area" ref={chartArea}/>
  )
}

export default ChartWrapper
