import React from "react"
import { Link } from "gatsby"

const Navbar = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to={"/"}>Home</Link>
        </li>
        <li>
          <Link to={"/about/"}>About</Link>
        </li>
        <li>
          <Link to={"/data-prediction/"}>Data Analysis</Link>
        </li>
        <li><
          Link to={"/training-prediction/"}>Training Analysis</Link>
        </li>
        <li>
          <Link to={"/analyze/"}>Analyze X-ray</Link>
        </li>
      </ul>
    </nav>
  )
}

export default Navbar
