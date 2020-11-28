import React, { Component } from "react"
import { analyzeXray } from "../../api/api"
import AnalysisResultsDisplay from "./analysisResultsDisplay"
import XrayPreview from "./xrayPreview"

const NO_FILE_SELECTION = "NO_FILE_SELECTION"
const ANALYZING_XRAY = "ANALYZING_XRAY"
const DISPLAYING_RESULTS = "DISPLAYING_RESULTS"

const DEFAULT_SELECTION_TEXT = "Select an X-ray to analyze."
const PERFORMING_ANALYSIS = "Performing analysis..."

class XrayAnalysis extends Component {
  state = {
    image: undefined,
    preview: undefined,
    status: NO_FILE_SELECTION,
    fileSelectionWindowText: DEFAULT_SELECTION_TEXT,
    predictions: undefined,
  }

  onSelectFile = (event) => {
    if (event.target.files.length < 1) {
      this.setState({
        image: undefined,
        preview: undefined,
        status: NO_FILE_SELECTION,
        fileSelectionWindowText: DEFAULT_SELECTION_TEXT,
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
        fileSelectionWindowText: image.name,
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
    const { predictions, preview, status } = this.state
    return (
      <div>
        <input type="file"
               multiple={false}
               accept=".png,.jpg,.jpeg"
               onChange={this.onSelectFile}
        />

        {!!preview
          ? (<XrayPreview preview={preview}/>)
          : (<p>{DEFAULT_SELECTION_TEXT}</p>)
        }

        {/*TODO: replace "analyzing" text with loading spinner or something similar*/}
        {status === ANALYZING_XRAY ? <p>{PERFORMING_ANALYSIS}</p> : null}

        {!!predictions && <AnalysisResultsDisplay predictions={predictions}/>}
      </div>
    )
  }
}

export default XrayAnalysis
