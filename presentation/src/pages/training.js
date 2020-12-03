import React, { Component } from "react"
import Layout from "../components/layout/layout"
import RocDisplay from "../components/training/rocDisplay"
import { rocCurve } from "../api/api"
import Container from "react-bootstrap/Container"
import DataSelect from "../components/training/dataSelect"

class Training extends Component {
  state = { data: undefined, dataTypes: undefined, labels: undefined }

  componentDidMount() {
    rocCurve(null)
      .then(data => {
        const dataTypes = Object.keys(data)
                                .map((label, i) => {
                                  return { label: label, selected: i === 0 }
                                })

        const labels = Object.keys(data[Object.keys(data)[0]])
                             .map(label => {
                               return { label: label, selected: true }
                             })

        this.setState({ data: data, dataTypes: dataTypes, labels: labels })
      })
  }

  onDataTypeSelect = (dataType) => {
    const updated = this.state.dataTypes.map(item => {
      return { label: item.label, selected: item.label === dataType }
    })
    this.setState({ dataTypes: updated })
  }

  onLabelSelect = (label) => {
    const updated = this.state.labels.map(item => {
      if (item.label === label) {
        return { label: label, selected: !item.selected }
      } else {
        return item
      }
    })
    this.setState({ labels: updated })
  }

  render() {
    const { data, dataTypes, labels } = this.state
    if (!!data) {
      return <Layout>
        <Container>
          {!!data && (<RocDisplay data={data[Object.keys(data)[0]]}/>)}
          <DataSelect dataSelections={dataTypes}
                      labelSelections={labels}
                      onDataTypeSelect={this.onDataTypeSelect}
                      onLabelSelect={this.onLabelSelect}/>
        </Container>
      </Layout>
    }
    return <Layout/>
  }
}

export default Training
