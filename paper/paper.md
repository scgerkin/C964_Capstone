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
The data [@nihDataset] to be used for training and creating a model to assist radiologists and physicians in the diagnostic process has been collected by the National Institutes of Health data made public for data exploration and machine learning modeling. The data includes over 100,000 chest X-ray images collected from a little more than 30,000 unique individuals. Additionally, a comma-separated value file accompanies the data listing the diagnostic labels applied to each image as well as patient age and sex, view position, and image dimensions.

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
With the initial prototype development consisting of a single developer, the waterfall methodology will be used for the development process. Additionally, the requirements are well understood for this project making this development lifecycle a prime candidate for use during development. The overall development will be broken down into the following phases and executed in order:

1. __Requirements gathering and analysis.__ The requirements have been well defined throughout this document and are unlikely to change during development.
2. __Data collection.__ As discussed previously, data for training the application prediction model has been gathered and will be further analyzed during the lifecycle of the project.
3. __Data analysis.__ The data will be analyzed for outliers, suitability for training, trimmed down to manageable batches, and explored for best results. This analysis is discussed further in the [Data Analysis section](#data-analysis) section below.
4. __Model creation, training, and evaluation.__ A predictive machine learning model will be created, trained, and evaluated on a variety of metrics to determine suitability for deployment and use for generalizing to new data. This is an iterative process and will persist until either a suitable model is created or it is determined that a model cannot be created with the given data or constraints.
5. __Deployment.__ The model will be deployed to a cloud service provider as a web service API for use in predicting and generalizing to testing data not presented during the training phase.
6. __Web Application Development.__ The data collected during data analysis and model training will be collated and made presentable as a web application. This application will then be wired to the deployed predictive model for demonstration purposes.
7. __Maintenance.__ At this time, the application will enter the maintenance phase of development. The predictive model will be fully modular and can be replaced by a new model that has been trained on new data points. Different versions of the model will be maintained and version-controlled to allow for gradual roll-outs to improvements to the overall system. At this time, the project will be handed over to the client.

## Funding Requirements
Total funding for project development and implementation is estimated at `DEVELOPMENT_FUNDING` with an ongoing maintenance cost of `MAINTENANCE_COST` for maintaining the cloud server environment on which the component services will live. A full cost breakdown of these costs is provided in the [Resources and Costs](#resources-and-costs) section.

## Stakeholders Impact
The stakeholders for this project include `COMPANY_NAME` and their clients. The predictive model created will enable `COMPANY_NAME` to provide greater efficiency in evaluating chest X-ray images for diagnostic classification and can potentially be offered as an additional service to its clients that require immediate diagnostic classification of chest X-rays but do not require the full usage of services from `COMPANY_NAME` radiology specialists.

## Data Precautions
The data used to train the prediction model complies with all HIPAA regulations and contains no protected health information (PHI) or personally identifiable information (PII). The data has been issued a CC0 1.0 Universal License[^CC0] and dedicated to the public domain. Furthermore, any new data that is to be gathered and consumed by the resultant web service will consist only of chest X-ray images with no identification information and no images will be retained by the web service. Finally, TLS/SSL encryption protocols will be enacted to only allow communication with the web service via HTTPS protocols.

[^CC0]: See [CC0 1.0 Universal https://creativecommons.org/publicdomain/zero/1.0/legalcode](https://creativecommons.org/publicdomain/zero/1.0/legalcode) for the full information regarding this license.

## Developer Expertise
The developer has 8 years of experience in software engineering, specializing in web applications and web service deployments. Additionally, the developer has 3 years of experience in architecting artificial intelligence systems and machine learning models for predictive analysis. Consultation with regards to radiologic expertise will be made available by `COMPANY_NAME` as needed for understanding the data during development.

# Section B - Business Requirements and Technical Summary

## Problem Statement

## Customer Summary

## Existing System Analysis

## Data Analysis

## Project Methodology

## Project Outcomes

## Implementation Plan

## Evaluation Plan

## Resources and Costs

### Programming Environment

### Environment Costs

### Human Resource Requirements

## Timeline and Milestones

# Section C - Application Design and Development

## Data Methodologies

### Descriptive

### Prescriptive (NN)

## Datasets Discussion

## Analytics and Decision Making

## Data Cleaning

## Data Visualization

## Real-Time Queries

## Adaptive Element

## Outcome Accuracy

## Security Measures

## Product Health Monitoring

## Dashboard

# Section D - Implementation Review Analysis

## Project Purpose

## Datasets

## Data Product Code

## Hypothesis Verification

## Visualizations and Reporting

## Accuracy Analysis

## Application Testing

## Application Files

## User's Guide

## Summation of Learning Experience

# References
