import React, { Component } from "react"
import Layout from "../components/layout/layout"
import { analyzeXray } from "../api/api"
import ResultsDisplay from "../components/analysis/resultsDisplay"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import Form from "react-bootstrap/Form"
import Container from "react-bootstrap/Container"
import Image from "react-bootstrap/cjs/Image"

const NO_FILE_SELECTION = "NO_FILE_SELECTION"
export const ANALYZING_XRAY = "ANALYZING_XRAY"
const DISPLAYING_RESULTS = "DISPLAYING_RESULTS"

const defaultFileWindowPrompt = "No file selected"

const allowedExtensions = ["png", "jpg", "jpeg"]

const invalidFileFeedback = `Please select a file with one of the
 following extensions: '${allowedExtensions.join("', '")}'`

class Analyze extends Component {
  state = {
    image: undefined,
    preview: undefined,
    predictions: undefined,
    status: NO_FILE_SELECTION,
    touched: false,
    fileWindowText: defaultFileWindowPrompt,
  }

  setNoFileSelectedState() {
    this.setState({
      image: undefined,
      preview: this.state.preview,
      status: NO_FILE_SELECTION,
      predictions: this.state.predictions,
      touched: true,
      fileWindowText: defaultFileWindowPrompt,
    })
  }

  onSelectFile = (event) => {

    if (event.target.files.length < 1) {
      this.setNoFileSelectedState()
      return
    }

    const image = event.target.files[0]

    const filename = image.name
    if (!validExtension(filename)) {
      this.setNoFileSelectedState()
      return
    }

    if (!!image) {
      this.setState({
        status: ANALYZING_XRAY,
        image: image,
        preview: URL.createObjectURL(image),
        predictions: undefined,
        fileWindowText: filename,
      })
      analyzeXray(image)
        .then(r => {
          this.setPrediction(r.data)
        })
        .catch(e => console.log(e.response))
    }

  }

  setPrediction(predictions) {
    this.setState({
      predictions: predictions,
      status: DISPLAYING_RESULTS,
    })
  }

  render() {
    const { preview, predictions, status, touched } = this.state
    return (
      <Layout>
        <h1>Analyze an X-ray</h1>

        <Container>
          <Row>
            <Col>
              <Row>
                {!!preview && (
                  <Image className={"m-3"} alt={this.state.fileWindowText}
                         src={preview}
                         width={450} height={450}/>)}
              </Row>

              <Form onChange={this.onSelectFile} as={"div"} className={"mb-3"}>
                <Form.File id={"xray-image-selector"}
                           accept={".png,.jpg,.jpeg"}
                           custom
                >
                  <Form.File.Input
                    isInvalid={status === NO_FILE_SELECTION && touched}
                  />
                  <Form.File.Label data-browse={"Select X-Ray Image"}>
                    {this.state.fileWindowText}
                  </Form.File.Label>
                  <Form.Control.Feedback type={"invalid"}>
                    {invalidFileFeedback}
                  </Form.Control.Feedback>
                </Form.File>
              </Form>
            </Col>
            <Col>
              {status === ANALYZING_XRAY ? <p>Performing analysis...</p> : null}
              {!!predictions && (<ResultsDisplay predictions={predictions}/>)}
            </Col>
          </Row>
        </Container>
      </Layout>
    )
  }
}

function validExtension(filename) {
  const parts = filename.split(".")
  const pattern = `^(${allowedExtensions.join("|")})$`
  const regex = new RegExp(pattern)
  return regex.test(parts[parts.length - 1])
}

export default Analyze
