import React from "react"
import XrayAnalysis from "../components/analysis/xrayAnalysis"
import Layout from "../components/layout/layout"

export default function analyze() {
  return (
    <Layout>
      <h1>Analyze an X-ray</h1>
      <XrayAnalysis/>
    </Layout>
  )
}
