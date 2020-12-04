import React, { Component } from "react"
import Layout from "../components/layout/layout"
import RocDisplay from "../components/training/rocDisplay"
import { rocCurve } from "../api/api"
import Container from "react-bootstrap/Container"
import DataSelect from "../components/training/dataSelect"

class Training extends Component {
  state = { data: undefined, dataTypes: undefined, labels: undefined }

  componentDidMount() {
    //todo loading spinner
    rocCurve(null)
      .then(data => {
        const dataTypes = Object.keys(data)
                                .map((label, i) => {
                                  return { label: label, selected: i === 2 }
                                })

        const labels = Object.keys(data[Object.keys(data)[0]])
                             .map((label, i) => {
                               return {
                                 label: label,
                                 selected: true,
                                 color: colors[i],
                               }
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
      return {
        ...item,
        selected: this.determineSelection(label, item.label, item.selected),
      }
    })
    this.setState({ labels: updated })
  }

  determineSelection = (newLabel, oldLabel, oldSelected) => {
    switch (newLabel) {
      case "select-all":  // fallthrough
      case "select-none":
        return newLabel === "select-all"
      case oldLabel:
        return !oldSelected
      default:
        return oldSelected
    }
  }

  render() {
    const { data, dataTypes, labels } = this.state
    if (!!data) {
      const selection = dataTypes.find(item => item.selected)

      return <Layout>
        <Container>
          <h1>ROC Curves</h1>

          {!!data && (
            <RocDisplay data={data[selection.label]}
                        selections={labels.filter(label => label.selected)}
            />)}
          <DataSelect dataSelections={dataTypes}
                      labelSelections={labels}
                      onDataTypeSelect={this.onDataTypeSelect}
                      onLabelSelect={this.onLabelSelect}
          />
        </Container>
      </Layout>
    }
    return <Layout/>
  }
}

const colors = [
  "#e6194B",
  "#3cb44b",
  "#ffe119",
  "#4363d8",
  "#f58231",
  "#911eb4",
  "#42d4f4",
  "#f032e6",
  "#bfef45",
  "#000075",
  "#808000",
  "#dcbeff",
  "#469990",
  "#9A6324",
  "#fabed4",
]

export default Training
