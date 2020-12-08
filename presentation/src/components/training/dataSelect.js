import React from "react"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import Dropdown from "react-bootstrap/Dropdown"
import { toPascal } from "../../utils/utils"
import Container from "react-bootstrap/Container"

const DataSelect = ({
                      dataSelections,
                      labelSelections,
                      onDataTypeSelect,
                      onLabelSelect,
                    }) => {
  if (!dataSelections || !labelSelections) {
    return <></>
  }
  const activeCount = labelSelections.filter(item => item.selected).length
  const dataTypeDisplay = toPascal(dataSelections.filter(item => item.selected)[0].label) + " data"
  return (
    <Container>
      <Row>
        <Col>
          <Dropdown>
            <Dropdown.Toggle variant={"outline-dark"} id={"data-type"}>
              {dataTypeDisplay}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {dataSelections.map(item =>
                <Dropdown.Item key={item.label}
                               onClick={() => onDataTypeSelect(item.label)}
                               active={item.selected}>{toPascal(
                  item.label) + " data"}</Dropdown.Item>)}
            </Dropdown.Menu>
          </Dropdown>
        </Col>
        <Col>
          <Dropdown>
            <Dropdown.Toggle variant={"outline-dark"} id={"labels"}>
              Select Diagnostic Labels
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {labelSelections.map(item =>
                <Dropdown.Item key={item.label} active={item.selected}
                               onClick={() => onLabelSelect(item.label)}>
                  {toPascal(item.label, "_")}
                </Dropdown.Item>)}
              <Dropdown.Item key={"select-none"} active={activeCount === 0}
                             onClick={() => onLabelSelect("select-none")}>Select
                None</Dropdown.Item>
              <Dropdown.Item key={"select-all"}
                             active={activeCount === labelSelections.length}
                             onClick={() => onLabelSelect("select-all")}>Select
                All</Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </Col>
      </Row>
    </Container>
  )
}

export default DataSelect
