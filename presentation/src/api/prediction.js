import FormData from "form-data"
import Axios from "axios"

export async function analyzeXray(image) {
  return await analyzeStub(null);
}

async function analyzeStub(image) {
  const response = {
    "Finding": false,
    "Label": {
      "atelectasis": 0.3454742751235631,
      "cardiomegaly": 0.9014383347671051,
      "consolidation": 0.592618961353012,
      "edema": 0.11987655598440261,
      "effusion": 0.9094852664595179,
      "emphysema": 0.1601115309628558,
      "fibrosis": 0.3456766122675696,
      "hernia": 0.08024542221684827,
      "infiltration": 0.21905928332278823,
      "mass": 0.9880370872294559,
      "nodule": 0.573179761995914,
      "pleural_thickening": 0.5546641217849224,
      "pneumonia": 0.41838854009633053,
      "pneumothorax": 0.9593831391532914,
    },
  }
  const data = {"data": response}
  return Promise.resolve(null).then(() => data)
}

async function analyzeActual(image) {
  const request = new FormData()
  request.append("image", image, image.fileName)
  return await Axios.post("http://localhost:5000", request)
}
