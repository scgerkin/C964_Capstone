import React, { Component } from "react"
import Layout from "../components/layout/layout"
import Container from "react-bootstrap/Container"
import Image from "react-bootstrap/Image"

const BASE_PATH = "https://scgrk.com/c964"

class Data extends Component {
  render() {
    return <Layout>
      <h1>Data Analysis</h1>
      <Container>
        <p>Data exploration is accomplished by visualizing the diagnostic labels
          associated with each image. This information helped to understand the
          given dataset and determine the course for standardizing the eventual
          training data to be fed to the model.
        </p>
        <p>
          In the following graph, we can visualize the number of diagnostic
          labels per image, separated by patient sex to understand the potential
          bias of the data sampling, in order to better understand the weights
          of each image sample. Images with "No Finding" are separated as this
          accounts for nearly half of the data and does not give a complete
          picture of the label classifications.
        </p>
        <Image src={BASE_PATH + "/assets/data/classification-by-sex.png"}
               fluid/>
        <p>The numbers above show an imbalance of the data, favoring
          infiltration and effusion above other diagnostic markers.
          Additionally, there are fewer samples for hernia and pneumonia
          diagnosis, indicating that there may not be enough samples of this
          data for training and it should be trimmed from the dataset before
          training. Patient sex also indicates a higher number of scans for men;
          however, without further information about these findings and their
          respective prevalence among the population, it is difficult to
          determine if this will introduce a significant bias in our model.
          Theoretically, the images themselves should not affect the model
          training, but this does not account for the potential physiological
          differences between men and women vis a vis breast tissue.
        </p>
        <p>
          Next, the label frequency is plotted against the age of each patient.
          The combined scatter plot below paints a similar picture to the
          markers above, showing a higher number of scans for infiltration.
        </p>
        <Image src={BASE_PATH + "/assets/data/dx-freq-by-age.png"} fluid/>
        <p>
          With 14 potential labels, the image above is a bit cluttered and it is
          hard to make any determinations from this alone. Therefore, each
          individual diagnostic label is plotted below to show the frequencies
          by age for each.
        </p>
        <Image src={BASE_PATH + "/assets/data/indiv-dx-by-age.png"} fluid/>
        <p>
          These individual plots show an overall normal distribution for the
          data, with the median value for most around the same area (between
          50-60 years old). However, hernia again stands as an outlier, showing
          an unusual distribution that does not fit into a typical bell-curve.
          This also indicates that it is likely this should be trimmed from the
          data before training.
        </p>
        <p>
          Lastly, the correlation of diagnoses shows the potential comorbidities
          for each label with the following correlation matrix:
        </p>
        <Image src={BASE_PATH + "/assets/data/dx-corr-matrix.png"} fluid/>
        <p>
          With this matrix, we can see that there is a correlation for
          atelectasis and effusion, as well as edema and pneumonia. These
          correlations are worth noting for training the model, as it is
          possible that this may confuse the model during training and lead to
          a
          lower degree of accuracy with differentiating between these labels.
        </p>
      </Container>
    </Layout>
  }
}

export default Data
