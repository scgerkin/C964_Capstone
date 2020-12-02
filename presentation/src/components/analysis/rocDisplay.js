import React, { useEffect, useRef, useState } from "react"
import RocChart from "./rocChart"

const RocDisplay = ({data}) => {
  const chartArea = useRef(null)
  const [chart, setChart] = useState(null)

  useEffect(() => {
    if (!chart) {
      setChart(new RocChart(chartArea.current, data))
    } else{
      // chart.update(data)
    }
  }, [chart, data])

  return (
    <>
      <div className="chart-area" ref={chartArea}/>
    </>
  )
}

export default RocDisplay
