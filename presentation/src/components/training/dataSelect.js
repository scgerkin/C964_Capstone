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

  return (
    <Container>
      <Row>
        <Col>
          <Dropdown>
            <Dropdown.Toggle variant={"outline-primary"} id={"data-type"}>
              Select Data Type
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {dataSelections.map(item =>
                <Dropdown.Item key={item.label}
                               onClick={() => onDataTypeSelect(item.label)}
                               active={item.selected}>{toPascal(
                  item.label)}</Dropdown.Item>)}
            </Dropdown.Menu>
          </Dropdown>
        </Col>
        <Col>
          <Dropdown>
            <Dropdown.Toggle variant={"outline-primary"} id={"labels"}>
              Select Diagnostic Labels
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {labelSelections.map(item =>
                <Dropdown.Item key={item.label} active={item.selected}
                               onClick={() => onLabelSelect(item.label)}>
                  {toPascal(item.label, "_")}
                </Dropdown.Item>)}
            </Dropdown.Menu>
          </Dropdown>
        </Col>
      </Row>
    </Container>
  )
}

export default DataSelect
