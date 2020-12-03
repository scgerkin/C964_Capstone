import React, { Component } from "react"
import Layout from "../components/layout/layout"
import ChartWrapper from "../components/data/chartWrapper"
import Container from "react-bootstrap/Container"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import Dropdown from "react-bootstrap/Dropdown"

class Data extends Component {
  state = { gender: "men" }

  genderSelected = (gender) => this.setState({ gender })

  render() {
    return <Layout>
      <h1>Data Analysis</h1>
      <Container>
        <Row>
          <Col xs={12}>
            {genderDropdown(this.genderSelected)}
          </Col>
        </Row>
        <Row>
          <Col xs={12}><ChartWrapper gender={this.state.gender}/></Col>
        </Row>
      </Container>
    </Layout>
  }
}

function genderDropdown(genderSelected) {
  return (
    <Dropdown>
      <Dropdown.Toggle variant={"primary"} id={"dropdown-basics"}>
        Select Gender
      </Dropdown.Toggle>

      <Dropdown.Menu>
        <Dropdown.Item onSelect={() => genderSelected("men")} >Men</Dropdown.Item>
        <Dropdown.Item onSelect={() => genderSelected("women")}>Women</Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
  )
}

export default Data
