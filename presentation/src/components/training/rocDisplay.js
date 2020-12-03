import React, { useEffect, useRef, useState } from "react"
import RocChart from "./rocChart"

const RocDisplay = ({data, selections}) => {
  const chartArea = useRef(null)
  const [chart, setChart] = useState(null)


  useEffect(() => {
    if (!chart) {
      setChart(new RocChart(chartArea.current, data, selections))
    } else{
      chart.update(data, selections)
    }
  }, [chart, data, selections])

  return (
    <>
      <div className="chart-area" ref={chartArea}/>
    </>
  )
}

export default RocDisplay
