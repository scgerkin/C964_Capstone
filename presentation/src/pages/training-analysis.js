import React, { Component } from "react"
import Layout from "../components/layout/layout"
import RocDisplay from "../components/analysis/rocDisplay"
import { rocCurve } from "../api/api"
import Container from "react-bootstrap/Container"

class TrainingAnalysis extends Component {
  state = { data: undefined }

  componentDidMount() {
    rocCurve(null)
      .then(data => this.setState({ data }))
  }

  render() {
    const { data } = this.state
    return <Layout>
      <Container>
        {!!data && (<RocDisplay data={data}/>)}
      </Container>
    </Layout>
  }
}

export default TrainingAnalysis
