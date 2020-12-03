import * as d3 from "d3"
import { round, toPascal } from "../../utils/utils"

const MARGIN = { TOP: 10, BOTTOM: 60, LEFT: 70, RIGHT: 10 }
const WIDTH = 900 - MARGIN.LEFT - MARGIN.RIGHT
const HEIGHT = 900 - MARGIN.TOP - MARGIN.BOTTOM
const TRANSITION_DURATION = 0 // ms

class RocChart {
  constructor(element, data, selections) {
    this.element = element
    this.selections = selections
    this.update(data, selections)
  }

  initSVG() {
    d3.select(this.element)
      .selectAll("*")
      .remove()
    this.svg = d3.select(this.element)
                 .append("svg")
                 .attr("width", WIDTH + MARGIN.LEFT + MARGIN.RIGHT)
                 .attr("height", HEIGHT + MARGIN.TOP + MARGIN.BOTTOM)
                 .append("g")
                 .attr("transform", `translate(${MARGIN.LEFT}, ${MARGIN.TOP})`)
  }

  initXYLabels() {
    this.xLabel = this.svg.append("text")
                      .attr("x", WIDTH / 2)
                      .attr("y", HEIGHT + 50)
                      .attr("text-anchor", "middle")
                      .text("False Positive Rate")
    this.yLabel = this.svg.append("text")
                      .attr("x", HEIGHT / -2)
                      .attr("y", -50)
                      .attr("text-anchor", "middle")
                      .text("True Positive Rate")
                      .attr("transform", "rotate(-90)")
  }

  initAxesGroup() {
    this.xAxisGroup = this.svg.append("g")
                          .attr("transform", `translate(0, ${HEIGHT})`)
    this.yAxisGroup = this.svg.append("g")
  }

  update(data, selections) {
    this.selections = selections
    this.initSVG()
    this.initXYLabels()
    this.initAxesGroup()
    this.setData(data)
    this.setXY()
    this.setAxes()
    this.drawGraph(selections)
  }

  setData(data) {
    this.data = data
  }

  setXY() {
    this.x = d3.scaleLinear()
               .domain([0, 1])
               .range([0, WIDTH])
    this.y = d3.scaleLinear()
               .domain([0, 1])
               .range([HEIGHT, 0])
  }

  setAxes() {
    const xAxisCall = d3.axisBottom(this.x)
    this.xAxisGroup.transition()
        .duration(TRANSITION_DURATION)
        .call(xAxisCall)

    const yAxisCall = d3.axisLeft(this.y)
    this.yAxisGroup.transition()
        .duration(TRANSITION_DURATION)
        .call(yAxisCall)
  }

  drawGraph() {
    this.selections
        .forEach((selection, i) => {

          const lineData = (item) =>
            d3.line()
              .x(d => this.x(d.fpr))
              .y(d => this.y(d.tpr))(item[selection.label].points)

          this.svg.append("path")
              .datum(this.data)
              .attr("fill", "none")
              .attr("stroke", selection.color)
              .attr("stroke-width", 2)
              .attr("d", lineData)
              .append("text")
              .attr("x", 200)
              .attr("y", 100 * i)
              .text(selection)
              .attr("fill-opacity", 1)

          const legendXPos = WIDTH * 0.75
          const legendYPos = HEIGHT * 0.6 + (i * 20)

          this.svg.append("circle")
              .attr("cx", legendXPos)
              .attr("cy", legendYPos)
              .attr("r", 7)
              .style("fill", selection.color)
              .attr("stroke", "black")

          const auc = round(this.data[selection.label].auc)
          const dispLabel = toPascal(selection.label, "_")

          this.svg.append("text")
              .attr("x", legendXPos + 10)
              .attr("y", legendYPos + 5)
              .text(`${dispLabel}: ${auc}`)
        })
  }
}

export default RocChart
