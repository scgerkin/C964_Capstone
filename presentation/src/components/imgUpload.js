import React, { Component } from "react"
import Axios from "axios"
import FormData from "form-data"

const NO_FILE_SELECTION = "NO_FILE_SELECTION"
const ANALYZING_XRAY = "ANALYZING_XRAY"

const DEFAULT_SELECTION_TEXT = "Select an X-ray to analyze."

class ImgUpload extends Component {
  state = {
    image: undefined,
    uploadState: NO_FILE_SELECTION,
    fileSelectionWindowText: DEFAULT_SELECTION_TEXT,
    predictions: undefined,
  }

  setDefaultState() {
    this.setState({
      image: undefined,
      uploadState: NO_FILE_SELECTION,
      fileSelectionWindowText: DEFAULT_SELECTION_TEXT,
      predictions: undefined,
    })
  }

  setPrediction(prediction) {
    this.setDefaultState()
    this.setState({
      ...this.state,
      prediction: prediction,
    })
  }

  onSelectFile = (event) => {
    if (!event.target.files) {
      this.setDefaultState()
      return
    }

    const image = event.target.files[0]

    if (!!image) {
      this.setState({
        image: image,
        fileSelectionWindowText: image.name,
        uploadState: undefined,
      })
    }

  }

  onSubmit = () => {
    const { image } = this.state

    if (!!image) {
      this.setState({
        uploadState: ANALYZING_XRAY,
      })
      analyzeXray(image).then(r => {
        console.log(r.data)
        this.setPrediction(r.data)
      }).catch(e => console.log(e.response))
    } else {
      alert("No file selected.")
    }

    this.setDefaultState()
  }

  render() {
    return (
      <div>
        <input type="file"
               multiple={false}
               accept=".png,.jpg,.jpeg"
               onChange={this.onSelectFile}
        />
        <button type="submit" onClick={this.onSubmit}>Submit</button>
      </div>
    )
  }
}

async function analyzeXray(image) {
  const request = new FormData()
  request.append("image", image, image.fileName)
  return await Axios.post("http://localhost:5000", request)
}

export default ImgUpload
