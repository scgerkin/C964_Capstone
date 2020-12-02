import React from "react"
import Layout from "../components/layout/layout"
import RocDisplay from "../components/analysis/rocDisplay"

export default function Home() {
  return <Layout>
    <h1>Training Analysis</h1>
    <RocDisplay/>
  </Layout>
}
