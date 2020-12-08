---
title: C964 Paper
author: Stephen Gerkin
date: December 7, 2020
output:
  word_document:
    path: parsed-document.docx
    highlight: tango
references:
  - id: nihDataset
    title: NIH Chest X-rays
    author:
      - family: Wang
        given: Xiaosong
      - family: Peng
        given: Yifan
      - family: Lu
        given: Zhiyong
      - family: Bagheri
        given: Mohammadhadi
      - family: Summers
        given: Ronald
    container-title: Kaggle.com
    URL: https://www.kaggle.com/nih-chest-xrays/data
    publisher: National Institutes of Health
    issued:
      year: 2018
  - id: nihPaper
    title: "ChestX-ray8: Hospital-scale Chest X-ray Database and Benchmarks on Weakly-Supervised Classification and Localization of Common Thorax Diseases"
    author:
      - family: Wang
        given: Xiaosong
      - family: Peng
        given: Yifan
      - family: Lu
        given: Zhiyong
      - family: Bagheri
        given: Mohammadhadi
      - family: Summers
        given: Ronald
    container-title: Computer Vision Foundation
    URL: https://openaccess.thecvf.com/content_cvpr_2017/papers/Wang_ChestX-ray8_Hospital-Scale_Chest_CVPR_2017_paper.pdf
    publisher: National Institutes of Health
    issued:
      year: 2017
  - id: oakdenRayner
    title: "Exploring the ChestXray14 dataset: problems"
    author:
      - family: Oakden-Rayner
        given: Luke
    container-title: Luke Oakden-Rayner
    URL: https://lukeoakdenrayner.wordpress.com/2017/12/18/the-chestxray14-dataset-problems/
    issued:
      year: 2017
      month: 12
      day: 18
---

# Section A - Project Proposal/Recommendation

## Problem Summary
`COMPANY_NAME`is a medical imaging company that provides on-going or on-call as needed radiologic image readings for physicians and clinicians in various settings ranging from urgent care facilities to general practitioners and family medicine. Clinicians rely on fast and accurate diagnostic readings of a wide range of imaging techniques but chief among these are chest X-ray images. Chest X-ray imaging is inexpensive, fast, and has a low radiologic risk to patients and as such is often the first-line diagnostic tool for disease diagnosis and patient treatment planning.

As `COMPANY_NAME` expands, more and more facilities and practitioners are contracting the expertise of `COMPANY_NAME`'s expertise in providing results in a timely fashion. This influx of clientele has stretched the existing resources beyond their current capabilities. As such, `COMPANY_NAME` has expressed a desire to create a pilot program for automating the diagnostic process with chest X-ray imaging with machine learning models to assist the existing radiologist staff with improving the turn-around time for diagnostic results in this high volume service.

## Application Benefits
The proposed solution is to create a predictive model that can receive a chest X-ray image and determine the probabilities of specific diagnostic labels being applied to the image. With a sufficiently accurate model, an automated system can be created to provide immediate results rather than necessitating manual review that can take several minutes or hours. These results can then be forwarded to radiologists for confirmation of the findings and aid them in looking for specific diagnostic markers that indicate the specified findings. Additionally, this service can be provided to existing clients of `COMPANY_NAME` to provide immediate results in urgent care situations.

## Application Description
The application will be segmented into four distinct parts:

- A data pipeline that can receive new image batches and information to continually improve the existing model.
- A REST[^REST] API[^API] endpoint for submitting images for classification and returning classification probabilities.
- A frontend dashboard for exploring the training data and results of training sessions.
- A web-based interface for interacting with the aforementioned API in a rate-limited fashion allowing prospective end-users to demo the prediction model.

[^REST]: [Representational State Transfer](https://en.wikipedia.org/wiki/Representational_state_transfer)
[^API]: [Application Programming Interface](https://en.wikipedia.org/wiki/API)

## Data Description
The data [^nihDatasetCite] to be used for training and creating a model to assist radiologists and physicians in the diagnostic process has been collected by the National Institutes of Health data made public for data exploration and machine learning modeling. The data includes over 100,000 chest X-ray images collected from a little more than 30,000 unique individuals. Additionally, a comma-separated value file accompanies the data listing the diagnostic labels applied to each image as well as patient age and sex, view position, and image dimensions.

[^nihDatasetCite]: @nihDataset

The finding labels consist of 15 different potential labels, 14 of which indicate a cause for follow-up and 1 label indicating none of the 14 labels could be applied to the individual image. Each X-ray can be assigned any combination of these labels (excluding "No Finding" which is always a unique label for an image). The diagnostic labels include:

- Atelectasis
- Cardiomegaly
- Consolidation
- Edema
- Effusion
- Emphysema
- Fibrosis
- Hernia
- Infiltration
- Mass
- Nodule
- Pleural Thickening
- Pneumonia
- Pneumothorax

Further discussion regarding these data can be found in the [Data Analysis](#data-analysis) section.

## Objectives
Three broad objectives have been identified to designate this project as a success. The objectives are the following:

1. Create a predictive model with a minimum 90% accuracy rate on label classification for new chest X-ray images.
2. Deploy this model as a web application that can be utilized by `COMPANY_NAME` and contracted clients.
3. Provide prospective `COMPANY_NAME` clients with an informative dashboard that can discuss the model, model accuracy, and training process as promotional material for drawing in additional business.

## Hypothesis
Through the use of a KMeans Clustering model, Convolutional Neural Network, or a combination of both, a predictive model can be trained and generalized to provide an accurate diagnostic classification system per the objective listed above. This model will be able to be deployed as a standalone web service and receive new imaging data and return the predicted label classifications.

## Methodology
With the initial prototype development consisting of a single developer, the Sashimi Waterfall methodology will be used for the development process. Additionally, the requirements are well understood for this project making this development lifecycle a prime candidate for use during development. The overall development will be broken down into the following phases and executed in order, with feedback and fine-tuning of each stage as necessary:

1. __Requirements gathering and analysis.__ The requirements have been well defined throughout this document and are unlikely to change during development.
2. __Data collection.__ As discussed previously, data for training the application prediction model has been gathered and will be further analyzed during the lifecycle of the project.
3. __Data analysis.__ The data will be analyzed for outliers, suitability for training, trimmed down to manageable batches, and explored for best results. This analysis is discussed further in the [Data Analysis section](#data-analysis) section below.
4. __Model creation, training, and evaluation.__ A predictive machine learning model will be created, trained, and evaluated on a variety of metrics to determine suitability for deployment and use for generalizing to new data. This is an iterative process and will persist until either a suitable model is created or it is determined that a model cannot be created with the given data or constraints.
5. __Deployment.__ The model will be deployed to a cloud service provider as a web service API for use in predicting and generalizing to testing data not presented during the training phase.
6. __Web Application Development.__ The data collected during data analysis and model training will be collated and made presentable as a web application. This application will then be wired to the deployed predictive model for demonstration purposes.
7. __Maintenance.__ At this time, the application will enter the maintenance phase of development. The predictive model will be fully modular and can be replaced by a new model that has been trained on new data points. Different versions of the model will be maintained and version-controlled to allow for gradual roll-outs to improvements to the overall system. At this time, the project will be handed over to the client.

## Funding Requirements
Total funding for project development and implementation is estimated at \$9,920 with an ongoing, yearly maintenance cost of approximately \$4,800 to \$5,100 for maintaining the cloud server environment on which the component services will live. A full cost breakdown of these costs is provided in the [Resources and Costs](#resources-and-costs) section.

## Stakeholders Impact
The stakeholders for this project include `COMPANY_NAME` and their clients. The predictive model created will enable `COMPANY_NAME` to provide greater efficiency in evaluating chest X-ray images for diagnostic classification and can potentially be offered as an additional service to its clients that require immediate diagnostic classification of chest X-rays but do not require the full usage of services from `COMPANY_NAME` radiology specialists.

## Data Precautions
The data used to train the prediction model complies with all HIPAA regulations and contains no protected health information (PHI) or personally identifiable information (PII). The data has been issued a CC0 1.0 Universal License[^CC0] and dedicated to the public domain. Furthermore, any new data that is to be gathered and consumed by the resultant web service will consist only of chest X-ray images with no identification information and no images will be retained by the web service. Finally, TLS/SSL encryption protocols will be enacted to only allow communication with the web service via HTTPS protocols.

[^CC0]: See [CC0 1.0 Universal https://creativecommons.org/publicdomain/zero/1.0/legalcode](https://creativecommons.org/publicdomain/zero/1.0/legalcode) for the full information regarding this license.

## Developer Expertise
The developer has 8 years of experience in software engineering, specializing in web applications and web service deployments. Additionally, the developer has 3 years of experience in architecting artificial intelligence systems and machine learning models for predictive analysis. Consultation with regards to radiologic expertise will be made available by `COMPANY_NAME` as needed for understanding the data during development.

# Section B - Business Requirements and Technical Summary

## Problem Statement
//TODO problem statement

## Customer Summary
//TODO customer summary

## System Analysis
This project is considered a pilot program for `COMPANY_NAME` and currently no infrastructure exists to support the development or deployment of the predictive model as a web service. Fortunately, the systems requirements for deployment are uncomplicated and can be easily provisioned in the cloud. Amazon Web Services has been selected as the cloud provider for this project as they provide the greatest number of resources for future scaling of the business needs for `COMPANY_NAME`.

The deployed web service will exist as two applications on a single server: a REST endpoint for receiving images and converting them to data that can be used by the prediction model and the prediction model itself. The forward endpoint will be served as a Flask[^Flask] RESTful service contained in a Docker image. This application will then communicate directly with the REST endpoint created by TensorFlow Serving[^TFServing] Docker container, receive the results, and then return them to the originating end-user. Both containers will be run in tandem using Docker Compose[^DockerCompose] on a single server.

![Prediction Server Diagram](./assets/prediction-server.png)

The servers will be deployed in an auto-scaling group to maintain high availability of the application, with a network load balancer to direct traffic between the servers. Two instances will be online at all times with each living in a separate availability zone. During peak traffic, additional servers will be provisioned automatically to adjust for this increase in traffic. When traffic begins to taper out, these servers will be automatically terminated to save on costs.

![Systems Architecture Diagram](./assets/systems-arch01.png)

[^Flask]: [https://flask.palletsprojects.com/en/1.1.x/](https://flask.palletsprojects.com/en/1.1.x/)
[^TFServing]: [https://www.tensorflow.org/tfx/serving/docker](https://www.tensorflow.org/tfx/serving/docker)
[^DockerCompose]: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)

## Data Analysis
The data used for training the predictive model has been published for use on Kaggle.com and can be located at https://www.kaggle.com/nih-chest-xrays/data. It consists of 112,120 distinct chest X-ray images taken both posterior-to-anterior (PA) and anterior-to-posterior (AP). Accompanying the images are comma-separated value files containing image metadata, patient diagnostic findings, follow-up information, and non-identifying patient ID numbers.

This data will be analyzed for outliers, incomplete data, and otherwise unusable data. Any data that is determined to be unusable will be excluded from the overall process. Metadata will be reformatted and/or reshaped to provide ease of usability. Lastly, training a model on image data will require that images are converted to raw number values that can be fed into the model for training.

## Project Methodology
This project will use the Sashimi Waterfall methodology for project development. Requirements are well understood and discussed throughout this document in detail. These factors make this project a prime candidate for the Waterfall methodology of project development. However, as development progresses and constraints are identified, feedback may require revisiting previous stages of development. The adoption of the Sashimi variation of Waterfall is therefore prudent during the development of this project. Further discussion regarding the individual stages of development follow.

### Requirements Analysis
The full requirements of this document will be analyzed for accuracy and understanding prior to any development of the project. This document will be modified or appended as necessary during this stage of development.

### Systems Design
The full system will undergo a complete design of broad functionality and individual parts and their interactions will be identified. Some basic systems design has been undertaken to better understand the requirements and is illustrated in the [Systems Analysis](#systems-analysis) portion of this document. This model will undergo refinement during the following phase as necessary.

### Coding and Implementation
This phase of development will be broken down into three distinct pieces, each contingent on the previous. During this phase, each individual piece will be evaluated and tested independent of the full project. Unit testing will be conducted at a granular level of each component.

#### Data Analysis
A complete understanding of the given data will be performed. During this time, any augmentation, additional collection, trimming of outliers, and collating into manageable chunks will result in visualizations for use describing the data. This is key to creating the predictive model.

#### Predictive Modeling
The keystone of the overall application, the predictive model, will be created, tested, and evaluated. As this is the most important part of the project, the majority of time spent will be during this development phase.

#### API Development
The completed (or prototypical) predictive model will be containerized. Following this, the middleware server API will be created to allow interaction with the predictive model.

#### Front-end Application Development
A front-end, single-page web application will be created, built, and deployed to cloud storage for demonstrating the predictive model to prospective clients and further evaluation.

### Systems Testing
Upon completion of each individual item above, the full environment will be evaluated for accuracy and integration.

### Deployment to Cloud Environment
Upon successful integration testing of the environment, the full project will be deployed to a prototyping cloud environment that will mirror the final specifications of the overall environment. During this time, further integration testing and acceptance testing will be undertaken. Should acceptance testing result in a successful outcome, the environment will be moved to a full production environment and transitioned to maintenance.

### Maintenance
The full project will undergo routine health checks, monitored via log output to AWS CloudWatch[^cloudWatchCite]. These logs will monitor individual server health metrics and activity. A full maintenance pipeline will be created to allow retraining and deployment of the predictive model to the production environment.

[^cloudWatchCite]: [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/)

## Project Deliverables
Project success is dependent on the following deliverables:
- Python script for instantiating, training, and saving a predictive model.
- Dockerfile for building a trained and saved model within a Docker container.
- Python Flask middleware server script for converting image data and interacting with the aforementioned container.
- Dockerfile for building the middleware server within a Docker container.
- Docker Compose file for initiating and linking these containers.
- Source code for the front-end, single-page web application build with the React[^reactCite] and Gatsby[^gatsbyCite] Javascript framework libraries.
- A complete analysis of the data used for training, as well as the results of the trained model.
- A zip file containing the subset of images used for training, validation, and testing.

[^reactCite]: [https://reactjs.org/](https://reactjs.org/)
[^gatsbyCite]: [https://www.gatsbyjs.com/](https://www.gatsbyjs.com/)

In addition to the above, the project will undergo full version-controlling using Git during development. This repository will be made available at [https://github.com/scgerkin/C964_Capstone](https://github.com/scgerkin/C964_Capstone).

## Implementation Plan
//TODO impl plan

## Evaluation Plan
//TODO eval plan

## Resources and Costs

### Programming Environment
The following environments are to be used for development and deployment of the final project. This is not meant to be a complete list and a full environment list will be available in the final source code. All tools listed below are open-source software. Licensing fees may apply, but are the responsibility of `COMPANY_NAME`.
- Python 3.7.9
- Anaconda 4.9.1
- Docker 19.03.13
- Node.js 12.16.3

### Environment Costs
Each instance of the full server application will reside on an AWS EC2 a1.xlarge instance. On-demand pricing in the US-EAST1 region is \$0.102 per hour. 2 servers are to be online at all times to maintain availability, costing a total of \$1787.04 per year. This can be discounted by 60% by purchasing reserved instances for these servers, bringing the yearly cost for both servers down to \$714.82. Additional costs will be incurred for additional on-demand servers during peak traffic hours. This is expected to be an average of 30 hours per week, adding an additional \$160 to \$480 year.

This makes the combined environment cost for maintenance approximately \$2,000 to $2,300 per year.

### Human Resource Requirements
Total upfront development for the project is estimated at 4 weeks at 40 hours per week. The contracted cost of the project developer is \$62/hr. This comes to a total of \$9,920 total cost for development.

Ongoing maintenance of the project is expected to take an average of 1 hour per week, assuming no additional development is required. This cost is prorated to \$55/hr, totalling \$2,860/yr.

## Timeline and Milestones
//TODO timeline

# Section C - Application Design and Development

## Data Methodologies

### Descriptive
//TODO descriptive discussion

### Prescriptive (NN)
//TODO prescriptive discussion

## Datasets Discussion
As noted in the paper[^nihPaperCitation] about the data, provided by the NIH, the diagnostic findings for each image are gathered by an NLP program, parsing from the original radiology reports. Unfortunately, these reports are not available, and there are some noted errors found in some of the diagnostic labels, as referenced in the provided table from the paper. A selection of these scans has been reviewed for accuracy by a third party radiologist[^Oakden-RaynerCite] and his findings indicate the labels may have significant accuracies, although he notes that the original diagnostic labels by the originating radiologists most likely had additional clinical information to assist them in determining a diagnosis.

[^nihPaperCitation]: @nihPaper
[^Oakden-RayerCite]: @oakdenRayner

Unfortunately, without a complete review of each scan by a trained radiologist, it is not possible to limit the data used for training the predictive model to only use particularly indicative images. This may lead to difficulty in creating a sufficiently accurate predictive model and, even if one should be created, it is unlikely that the resultant model is likely to generalize well to new information. However, at this time no additional data has been provided by `COMPANY_NAME` for the purposes of creating a predictive model, and as such, best efforts will be made given these constraints with the ability to retrain the model on new or improved data when it is available.

Lastly, the metadata about each image possibly contains several errors in reporting. For instance, the "age" column for images range from 1 to 414 with no associated units. As such, it is impossible to use this information for any significant information when analyzing or using for predictive modeling. The assumption has been made that this column is meant to indicate years. As such, any image with an age of greater than or equal to 100 has been trimmed from the prospective data.

## Analytics and Decision Making
The application has the ability to assist clinicians in the diagnosis of patients via chest X-ray. As a demonstration of the ability, the web application can be used to interact with the prediction API with a few simple clicks. The results of the analysis give probabilistic classification labels and are displayed to the end-user. A demonstration of this in action can be viewed in the [Real-Time Query](#real-time-query) section below.

## Data Cleaning
As discussed previously regarding the age column of the data, results with an age greater than or equal to 100 have been removed. The methodology behind this and the results is demonstrated with the following code snippets, using the Pandas[^pandasCite] data analysis tool for Python:

[^pandasCite]: [https://pandas.pydata.org/](https://pandas.pydata.org/)

```python
import pandas as pd
df = pandas.read_csv("..")
df["Patient Age"].describe()
```
```
count    112120.000000
mean         46.901463
std          16.839923
min           1.000000
25%          35.000000
50%          49.000000
75%          59.000000
max         414.000000
```
```python
df["Patient Age"][df["Patient Age"] < 100].describe()
```
```
count    112104.000000
mean         46.872574
std          16.598152
min           1.000000
25%          35.000000
50%          49.000000
75%          59.000000
max          95.000000
```

Additional modifications to the image metadata file have been made to allow for easier use with analysis and modeling. This includes normalizing the column names to remove spaces, splitting the diagnostic findings by label and creating a one-hot encoded array for each image, and removing additionally identified unusable images (either from poor image quality, sizing constraints, or others) in the `cxr14_bad_labels.csv` file.

The following code snippet illustrates a broad overview of how data cleaning was accomplished[^cleanDataFileLoc]. After cleaning, the resultant DataFrame was saved to a new CSV for future usage.
```python
img_metadata = pd.read_csv(img_metadata_loc)
img_metadata.rename(columns={
    "Image Index"   : "img_filename",
    "Patient ID"    : "pt_id",
    "Patient Age"   : "pt_age",
    "Patient Gender": "pt_sex",
    "View Position" : "view_position",
    "Image Width"   : "img_width",
    "Image Height"  : "img_height",
    "Spacing X"     : "x_spacing",
    "Spacing Y"     : "y_spacing"}, inplace=True)
unusable_imgs = pd.read_csv(unusable_img_loc)
finding_labels = get_finding_labels(img_metadata)
save_labels_to_csv(finding_labels)
img_metadata = remap_labels(img_metadata, finding_labels)
img_metadata = drop_known_unusable(img_metadata, unusable_imgs)
save_usable_to_csv(img_metadata)
```

[^cleanDataFileLoc]: The full code for this cleaning can be found in `clean-data.py`.

## Data Visualization
//TODO davaviz

## Real-Time Query
The front-end application allows a user to upload a chest X-ray image directly to the prediction model through their browser with a simple form element:
![Upload Image Button](./assets/analyze-xray/0.png)

Clicking on this form element will bring up a File Selector:
![File Selection](./assets/analyze-xray/1.png)

During analysis, the original image will be displayed on screen. Once analysis is complete, a graph will display the indicated classification probabilities:
![Diagnostic Classification Results](./assets/analyze-xray/5.png)

This portion of the web application functionality can be accessed at `//TODO: X-RAY_ANALYSIS_URL`.

## Adaptive Element
//TODO adaptive element? what is this

## Outcome Accuracy
//TODO outcome accuracy discussionn

## Security Measures
//TODO security measures

## Product Health Monitoring
//TODO product health monitoring

## Dashboard
//TODO dashboard

# Section D - Implementation Review Analysis

## Project Purpose
//TODO project purpose? what is this

## Datasets
//TODO datasets discussion?

## Data Product Code
//TODO data product code discussion

## Hypothesis Verification
//TODO hypothesis verification

## Visualizations and Reporting
//TODO visualisations and reporting

## Accuracy Analysis
//TODO accuracy analysis

## Application Testing
//TODO application testing???

## Application Files
//TODO list files

## User's Guide
//TODO installation guide?

## Summation of Learning Experience
//TODO summation of learning

# References
