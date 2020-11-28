import React from "react"

const DEFAULT_SELECTION_TEXT = "Select an X-ray to analyze."

export default function xrayPreview(props) {
  const { preview } = props
  return (
    <>
      {!!preview
        ? <img alt={"xray"} src={preview} width={"100"} height={"100"}/>
        : <p>{DEFAULT_SELECTION_TEXT}</p>
      }
    </>
  )
}
