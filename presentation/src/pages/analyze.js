import React, { Component } from "react"
import UploadXray from "../components/analysis/uploadXray"
import Layout from "../components/layout/layout"
import { analyzeXray } from "../api/api"
import XrayPreview from "../components/analysis/xrayPreview"
import ResultsDisplay from "../components/analysis/resultsDisplay"
import StatusDisplay from "../components/analysis/statusDisplay"

const NO_FILE_SELECTION = "NO_FILE_SELECTION"
export const ANALYZING_XRAY = "ANALYZING_XRAY"
const DISPLAYING_RESULTS = "DISPLAYING_RESULTS"


class Analyze extends Component {
  state = {
    image: undefined,
    preview: undefined,
    status: NO_FILE_SELECTION,
    predictions: undefined,
  }

  onSelectFile = (event) => {
    if (event.target.files.length < 1) {
      this.setState({
        image: undefined,
        preview: undefined,
        status: NO_FILE_SELECTION,
        predictions: undefined,
      })
      return
    }

    const image = event.target.files[0]

    if (!!image) {
      this.setState({
        status: ANALYZING_XRAY,
        image: image,
        preview: URL.createObjectURL(image),
        predictions: undefined,
      })
      analyzeXray(image).then(r => {
        this.setPrediction(r.data)
      }).catch(e => console.log(e.response))
    }

  }

  setPrediction(predictions) {
    this.setState({
      predictions: predictions,
      status: DISPLAYING_RESULTS,
    })
  }

  render() {
    const { preview, predictions, status } = this.state
    return (
      <Layout>
        <h1>Analyze an X-ray</h1>

        <UploadXray onSelectFile={this.onSelectFile}/>

        <XrayPreview preview={preview}/>

        <StatusDisplay status={status}/>

        {!!predictions && (<ResultsDisplay predictions={predictions}/>)}
      </Layout>
    )
  }
}

export default Analyze
