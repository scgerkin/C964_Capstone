import React, { Component } from "react"
import RocComponent from "../components/training/rocComponent"
import Layout from "../components/layout/layout"
import Container from "react-bootstrap/Container"
import Image from "react-bootstrap/Image"
import Link from "gatsby-link"

const BASE_PATH = "https://scgrk.com/c964"

class Training extends Component {
  render() {
    return <Layout>
      <Container>
        <h1>Training and Methodology Analysis</h1>
        <h2 id={"hypothesis-verification"}>Hypothesis Verification</h2>
        <p>
          The initial hypothesis, that a predictive model to classify chest
          X-ray images with diagnostic labels, could be created is tentatively
          accepted. Despite the fact that the created model was unable to reach
          an appropriate level of accuracy on validation and testing data, the
          model did show the ability to have a high degree of accuracy during
          training. This is indicative of data <i>overfitting</i>, or a
          propensity to
          accurately predict on the training data with failure to generalize to
          new, unknown data.
        </p>
        <p>
          The overfitting of the model is best demonstrated in the training
          accuracy per epoch in the following graph:
        </p>
        <Image src={BASE_PATH + "/assets/training-analysis/model-acc.png"} fluid
               alt={"Model Accuracy per Epoch"}/>
        <p>
          As the model received more and more training information, the overall
          accuracy adapted to the data; however, this was not present in the
          validation phase of training. When compared to the loss function of
          the model, this is again evident as the training loss decreases, while
          the validation loss increases, indicating poor generalization of the
          model:
        </p>
        <Image src={BASE_PATH + "/assets/training-analysis/model-loss.png"}
               fluid alt={"Model Loss per Epoch"}/>
        <p>
          Interestingly, the model did see a marked improvement in the mean
          absolute error over training periods:
        </p>
        <Image src={BASE_PATH + "/assets/training-analysis/model-mae.png"} fluid
               alt={"Model Mean Absolute Error per Epoch"}/>
        <p>
          These findings indicate that, while the model overall may not
          generalize to new data, the error rate of the model overall improves
          and can likely be used for classification in low-risk situations where
          precision is not a requirement.
        </p>
        <p>
          The failure to generalize can be mitigated in future iterations of the
          project with a variety of methods, such as longer training sessions or
          increasing the dataset, but were unable to be explored due to the time
          constraints of this project. However, it should be noted that, with
          the model successfully deployed within a simple Docker container,
          future iterations of training and prediction will be trivial to
          implement due to the modular design of the application overall.
        </p>
        <h2>Data Methodologies</h2>
        <h3>Descriptive (KMeans Clustering)</h3>
        <p>KMeans clustering was explored as a means of
          dimensionality reduction for the training data before processing by
          the neural net. Using the training data selected to be fed into the
          neural net, the appropriate number of clusters was assumed to be 13
          (the number of classification labels present on the trimmed data).
          However, this assumption was tested by testing a range of clusters
          from 2 to 100 and the respective inertias and silhouette scores for
          each model created for these clusters were analyzed.
        </p>
        <p>
          The results of this cluster determination were inconclusive, showing
          no particular number of clusters as an appropriate means of evaluating
          the data. The inertia of each model continued on a downward trend,
          save a few unusual findings in the 20-30 range, and again from 70-80.

        </p>
        <Image src={BASE_PATH + "/assets/training-analysis/KMeans-Inertia.png"}
               fluid alt={"KMeans Inertia Scores"}/>
        <p>
          The inertia of a model is also not as indicative of the appropriate
          cluster range as the silhouette score, or the number of samples
          appearing accurately within a cluster. These scores are plotted below:
        </p>
        <Image src={BASE_PATH +
        "/assets/training-analysis/KMeans-Silhouette-score.png"} fluid
               alt={"KMeans Silhouette Scores"}
        />
        <p>
          With the highest silhouette score at 2 clusters of 0.10, the
          indication is clear that no number of clusters accurately represents
          the data fed into the model. As such, and because the number of labels
          we wish to analyze is known, the number of clusters chosen for the
          model is 13. But, as discussed, it is not clear that this number of
          clusters is an appropriate value for the model. Below, the scores for
          each are shown more clearly on the graphs and annotated for clarity:
        </p>
        <Image src={BASE_PATH +
        "/assets/training-analysis/KMeans-Inertia-annotated.png"} fluid
               alt={"KMeans Inertia Scores with annotation"}
        />
        <Image src={BASE_PATH +
        "/assets/training-analysis/KMeans-Silhouette-score-annotated.png"}
               fluid
               alt={"KMeans Silhouette Scores with annotation"}
        />
        <h3>Predictive (Neural Net)</h3>
        <p>
          A convolutional neural net (CNN), more specifically
          InceptionV3, was used for image classification
          and prediction. Inception, sometimes referred to as
          GoogLeNet, is a CNN created by Google and trained on
          the ImageNet database. It shows a significant accuracy rate on this
          database and has been used in several computer vision problems since.
          As such, it was selected to provide the predictive model for this
          application. The model used for this application was given the
          pre-trained weights created with ImageNet to potentially show greater
          accuracy in the overall model and provide a reasonable training time.
        </p>
        <h2>Accuracy Analysis</h2>
        <p>
          The accuracy of the application overall is broken down between the
          descriptive analysis of the KMeans clustering for dimensionality
          reduction and the accuracy of the neural net for classification.
        </p>
        <h3>KMeans Clustering Accuracy Analysis</h3>
        <p>
          For analysis of the KMeans clustering, the model and predictions for
          testing data, along with the accuracy metrics. The results of the
          confusion matrix can be best viewed with the following graph:
        </p>
        <Image src={BASE_PATH +
        "/assets/training-analysis/kmeans-cf-matrix-diag.png"} fluid
               alt={"KMeans Confusion Matrix"}/>
        <p>
          As shown on these results, the precision, recall, and F1 scores are
          all 7.66%, indicating a significantly inaccurate result. The heat-map
          shows the true labels of an image on the y-axis, with the predicted
          label on the x-axis. The diagonal (highlighted with the green line)
          are frequencies of accurate predictions. As can be seen from the
          scores and this heat-map, the model is fully inadequate at providing a
          reasonable classification of the images via 13 clusters for KMeans. As
          a result, this method of dimensionality reduction was abandoned.
        </p>
        <h3>Neural Net Accuracy Analysis</h3>
        <p>
          The accuracy of the neural net was evaluated in a combination of
          methods. As previously discussed in the <Link
          to={"#hypothesis-verification"}>Hypothesis Verification</Link>
          section, the validation data used during training of the model
          indicated a poor adaption to the
          data, showing very poor scores for categorical cross-entropy as a loss
          function and accuracy overall. However, when plotting the
          true-positive rate and false-positive rate for the model to create the
          ROC curves, this paints a completely different picture.
        </p>
        <RocComponent/>
        <p>
          The area under the curve for each classification label shows a wide
          range of values, from 0.5405 for <b>Mass</b> vs. up to 0.8466 for
          <b>Consolidation</b>. A score of near 0.5 for this value indicates
          that the
          model was no better at determining a matching label than flipping a
          coin. For <b>Mass</b>, it is clear that the model was unable to match
          well
          to this diagnostic label. This may have skewed the overall combined
          accuracy of the model, as well as other low scoring classification
          labels. Additionally, as categorical cross-entropy is a measure of the
          overall probability matches, this may cloud the findings of individual
          diagnostic classifications. This indicates that the model may adapt
          well to some labels but not others. However, it should be noted that
          this is an unusual finding overall and may be due to an error in the
          overall evaluation process.
        </p>
        <h3>Accuracy Conclusion</h3>
        <p>
          Based on the results of the above evaluations and metrics and the
          unusual nature of the findings above, it is concluded that the model
          overall failed to meet the expectations of Arrow Medical Imaging for
          accuracy. However, individual diagnostic labels show some promise
          overall, indicating that the model may be adapted for binary
          classification of <b>Finding</b> vs. <b>No Finding</b> should the
          training data
          and model be modified to fit this classification model.
        </p>
        <p>
          Lastly, it is worth mentioning that increasing the size of the dataset
          and the training sessions may have produced a more favorable outcome.
          The training data may have also been improved by providing random
          transformations to individual images, such as rotations, inversions,
          shifting horizontally or vertically, or other such image
          transformations. However, due to the time constraints of this project,
          this could not be explored in more detail.
        </p>
      </Container>
    </Layout>
  }
}

export default Training
