# Chest X-Ray Classification and Analysis
This site is my capstone project for Western Governor's University Bachelor's of Computer Science C964 Capstone Project. It consists of a full machine learning prediction model for analyzing chest X-ray images to predict the diagnostic classifications for an image.


For the full information about this project, you can read the associated paper [here](https://scgrk.com/c964/paper.pdf)


The full source code is available on [my GitHub](https://github.com/scgerkin/C964_Capstone)


The rubric for this project can be found [here](https://scgrk.com/c964/rubric.pdf)


For my personal site, please visit [scgrk.com](https://scgrk.com)


## Usage Instructions
This application is fully deployed at [http://cxr-dx.scgrk.com](http://cxr-dx.scgrk.com)

## Local Installation
The full application requires the use of [Docker](https://docker.com), [Docker Compose](https://docs.docker.com/compose/) and the [Gatsby.js](https://www.gatsbyjs.com/) CLI tool.

To run the application locally, the full source code can be downloaded from GitHub. Both Docker containers must be built and run with Docker Compose.

The following script contains the complete instructions to accomplish this:
```shell
git clone https://github.com/scgerkin/C964_Capstone.git

# Build the prediction model
cd C964_Capstone/api/tf
docker build -t c964/dx .

# Build the API to interact with the prediction model
cd ..
docker build -t c964/svr .
docker-compose up

# Launch Gatsby developer mode to interact with the frontend.
cd ../presentation
gatsby develop
```

The frontend application will then be available at `http://localhost:8000`. To interact with the locally deployed containers, the API communication must be modified to use the local host. This is located in `presentation/src/api/api.js`.

Modify the following function as indicated below:
```js
async function analyzeActual(image) {
  const request = new FormData()
  request.append("image", image, image.fileName)
  return await Axios.post("http://localhost:80", request) // Modify this line
}
```