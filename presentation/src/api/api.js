import FormData from "form-data"
import Axios from "axios"

export async function analyzeXray(image) {
  return await analyzeStub(null);
}

async function analyzeStub(image) {
  return new Promise((res, rej) => {
    setTimeout(() => {
      const response = {
        "finding": Math.random() >= 0.5,
        "labels": {
          "atelectasis": Math.random(),
          "cardiomegaly": Math.random(),
          "consolidation": Math.random(),
          "edema": Math.random(),
          "effusion": Math.random(),
          "emphysema": Math.random(),
          "fibrosis": Math.random(),
          "hernia": Math.random(),
          "infiltration": Math.random(),
          "mass": Math.random(),
          "nodule": Math.random(),
          "pleural_thickening": Math.random(),
          "pneumonia": Math.random(),
          "pneumothorax": Math.random(),
        },
      }
      const data = {"data": response}
      res(data)
    }, 2500)
  })
}

async function analyzeActual(image) {
  const request = new FormData()
  request.append("image", image, image.fileName)
  return await Axios.post("http://localhost:5000", request)
}
