import React, { useEffect, useRef, useState } from "react"
import RocChart from "./rocChart"

const RocDisplay = () => {
  const chartArea = useRef(null)
  const [chart, setChart] = useState(null)

  useEffect(() => {
    if (!chart) {
      setChart(new RocChart(chartArea.current, null))
    }
  }, [chart, null])

  return (
    <>
      <div className="chart-area" ref={chartArea}/>
    </>
  )
}

export default RocDisplay
