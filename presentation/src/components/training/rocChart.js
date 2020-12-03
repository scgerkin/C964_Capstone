import * as d3 from "d3"
import { round, toPascal } from "../../utils/utils"

const MARGIN = { TOP: 80, BOTTOM: 60, LEFT: 90, RIGHT: 70 }
const WIDTH = 900 - MARGIN.LEFT - MARGIN.RIGHT
const HEIGHT = 900 - MARGIN.TOP - MARGIN.BOTTOM
const TRANSITION_DURATION = 0 // ms

class RocChart {
  constructor(element, data) {
    this.initSVG(element)
    this.initXYLabels()
    this.initAxesGroup()
    this.update(data)
  }

  initSVG(element) {
    this.svg = d3.select(element)
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

  update(data) {
    this.setData(data)
    this.setXY()
    this.setAxes()
    this.drawGraph()
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
    const line = d3.line()
                   .x(d => this.x(d.fpr))
                   .y(d => this.y(d.tpr))

    Object.keys(this.data)
          .forEach((label, i) => {
            this.svg.append("path")
                .datum(this.data[label].points)
                .attr("fill", "none")
                .attr("stroke", colors[i])
                .attr("stroke-width", 2)
                .attr("d", line)
                .append("text")
                .attr("x", 200)
                .attr("y", 100 * i)
                .text(label)
                .attr("fill-opacity", 1)

            const legendXPos = WIDTH * 0.75
            const legendYPos = HEIGHT * 0.6 + (i * 20)

            this.svg.append("circle")
                .attr("cx", legendXPos)
                .attr("cy", legendYPos)
                .attr("r", 7)
                .style("fill", colors[i])
                .attr("stroke", "black")

            const auc = round(this.data[label].auc)
            const dispLabel = toPascal(label, "_")

            this.svg.append("text")
                .attr("x", legendXPos + 10)
                .attr("y", legendYPos + 5)
                .text(`${dispLabel}: ${auc}`)
          })
  }
}

const colors = [
  "#e6194B",
  "#3cb44b",
  "#ffe119",
  "#4363d8",
  "#f58231",
  "#911eb4",
  "#42d4f4",
  "#f032e6",
  "#bfef45",
  "#000075",
  "#808000",
  "#dcbeff",
  "#469990",
  "#9A6324",
  "#fabed4",
]

export default RocChart
