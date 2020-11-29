import FormData from "form-data"
import Axios from "axios"

export async function analyzeXray(image) {
  return await analyzeGradient(null)
  // return await analyzeRandom(null)
  // return analyzeActual(image)
}

async function analyzeRandom(image) {
  return new Promise((res, rej) => {
    setTimeout(() => {
      const response = {
        "finding": Math.random() >= 0.5,
        "labels": [
          { label: "atelectasis", probability: Math.random() },
          { label: "cardiomegaly", probability: Math.random() },
          { label: "consolidation", probability: Math.random() },
          { label: "edema", probability: Math.random() },
          { label: "effusion", probability: Math.random() },
          { label: "emphysema", probability: Math.random() },
          { label: "fibrosis", probability: Math.random() },
          { label: "hernia", probability: Math.random() },
          { label: "infiltration", probability: Math.random() },
          { label: "mass", probability: Math.random() },
          { label: "nodule", probability: Math.random() },
          { label: "pleural_thickening", probability: Math.random() },
          { label: "pneumonia", probability: Math.random() },
          { label: "pneumothorax", probability: Math.random() },
        ],
      }
      const data = { "data": response }
      res(data)
    }, 500)
  })
}

async function analyzeGradient(image) {
  return new Promise((res, rej) => {
    setTimeout(() => {
      const response = {
        "finding": Math.random() >= 0.5,
        "labels": [
          { label: "atelectasis", probability: 1 },
          { label: "cardiomegaly", probability: 0.97 },
          { label: "consolidation", probability: 0.92 },
          { label: "edema", probability: 0.87 },
          { label: "effusion", probability: 0.82 },
          { label: "emphysema", probability: 0.77 },
          { label: "fibrosis", probability: 0.72 },
          { label: "hernia", probability: 0.67 },
          { label: "infiltration", probability: 0.62 },
          { label: "mass", probability: 0.57 },
          { label: "nodule", probability: 0.52 },
          { label: "pleural_thickening", probability: 0.47 },
          { label: "pneumonia", probability: 0.37 },
          { label: "pneumothorax", probability: 0.27 },
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
  return await Axios.post("http://localhost:5000", request)
}
