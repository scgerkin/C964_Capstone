import React from "react"
import ImgUpload from "../components/imgUpload"
import Layout from "../components/layout/layout"

export default function predict() {
  return (
    <Layout>
      <h1>Analyze an X-ray</h1>
      <ImgUpload/>
    </Layout>
  )
}
