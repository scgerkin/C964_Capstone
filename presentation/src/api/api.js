import FormData from "form-data"
import Axios from "axios"

export async function analyzeXray(image) {
  return analyzeActual(image)
}

export async function rocCurve(setType) {
  return new Promise((res, rej) => {
    setTimeout(() => {
      const data = require("../../static/combined.json")
      res(data)
    }, 0)
  })
}

async function analyzeRandom(image) {
  return new Promise((res, rej) => {
    setTimeout(() => {
      const response = {
        "labels": [
          { label: "atelectasis", probability: Math.random() },
          { label: "cardiomegaly", probability: Math.random() },
          { label: "consolidation", probability: Math.random() },
          { label: "edema", probability: Math.random() },
          { label: "effusion", probability: Math.random() },
          { label: "emphysema", probability: Math.random() },
          { label: "fibrosis", probability: Math.random() },
          { label: "infiltration", probability: Math.random() },
          { label: "mass", probability: Math.random() },
          { label: "no_finding", probability: Math.random() },
          { label: "nodule", probability: Math.random() },
          { label: "pleural_thickening", probability: Math.random() },
          { label: "pneumothorax", probability: Math.random() },
        ],
      }
      const data = { "data": response }
      res(data)
    }, 500)
  })
}

async function analyzeActual(image) {
  const request = new FormData()
  request.append("image", image, image.fileName)
  return await Axios.post("http://ec2-3-93-24-102.compute-1.amazonaws.com", request)
}
