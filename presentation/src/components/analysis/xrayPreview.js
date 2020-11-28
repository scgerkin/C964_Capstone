import React from "react"

function XrayPreview(props) {
  const { preview } = props
  return (
    <div>
      <img alt={"xray"} src={preview} width={"100"} height={"100"}/>
    </div>
  )
}

export default XrayPreview
