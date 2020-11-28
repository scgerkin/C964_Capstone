import React from "react"
import { ANALYZING_XRAY } from "../../pages/analyze"

const PERFORMING_ANALYSIS = "Performing analysis..."

/*TODO: replace "analyzing" text with loading spinner or something*/
export default function statusDisplay(props) {
  const { status } = props
  return (
    <>
      {status === ANALYZING_XRAY ? <p>{PERFORMING_ANALYSIS}</p> : null}
    </>
  )
}
