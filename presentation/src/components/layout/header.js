import React from "react"
import Navbar from "react-bootstrap/Navbar"
import Nav from "react-bootstrap/Nav"
import {navigate} from "gatsby"

const Header = () => {

  const onNavSelect = (key) => {
    console.log(key)
    navigate(key)
  }

  return (
    <Navbar bg={"light"} expand={"lg"}>
      <Navbar.Brand>Chest X-Ray Classification</Navbar.Brand>
      <Nav className={"mr-auto"} onSelect={onNavSelect}>
        <Nav.Link eventKey={"/"}>Home</Nav.Link>
        <Nav.Link eventKey={"/data/"}>Data Analysis</Nav.Link>
        <Nav.Link eventKey={"/training/"}>Training Analysis</Nav.Link>
        <Nav.Link eventKey={"/analyze"}>Analyze X-ray</Nav.Link>
      </Nav>
    </Navbar>
  )
}


export default Header
