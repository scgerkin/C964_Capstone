import React, { Component } from "react"
import Layout from "../components/layout/layout"
import RocDisplay from "../components/analysis/rocDisplay"
import { rocCurve } from "../api/api"

class TrainingAnalysis extends Component {
  state = { data: undefined}

  componentDidMount() {
    rocCurve(null).then(data => this.setState({data}))
  }

  render() {
    const {data} = this.state
    return <Layout>
      <h1>Training Analysis</h1>
      {!!data && (<RocDisplay data={data}/>)}
    </Layout>
  }
}

export default TrainingAnalysis
