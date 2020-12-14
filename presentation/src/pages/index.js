import React from "react"
import Layout from "../components/layout/layout"
import Container from "react-bootstrap/Container"
import Link from "gatsby-link"

export default function Home() {
  return <Layout>
    <Container>
      <h1>Chest X-Ray Classification and Analysis</h1>
      <p>
        This site is my capstone project for Western Governor's University
        Bachelor's of Computer Science C964 Capstone Project. It consists of a
        full
        machine learning prediction
        model for analyzing chest X-ray images to predict the diagnostic
        classifications for an image.
        Select from the navigation bar above to get more information about the
        model.</p>
      <h5>For the full information about this
        project, you can read the associated paper <Link
          to={"https://scgrk.com/c964/paper.pdf"}>here</Link>.
      </h5><h5>The rubric for this
      project can be found <Link
        to={"https://scgrk.com/c964/rubric.pd"}>here</Link>.</h5><h5>For my
      personal site, please visit <Link
        to={"https://scgrk.com"}>scgrk.com</Link></h5>


    </Container>

  </Layout>
}
