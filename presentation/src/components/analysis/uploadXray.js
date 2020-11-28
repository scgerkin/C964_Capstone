import React from "react"

export default function uploadXray(props) {
  const { onSelectFile } = props
  return (
    <div>
      <input type="file"
             multiple={false}
             accept=".png,.jpg,.jpeg"
             onChange={onSelectFile}
      />
    </div>
  )
}
