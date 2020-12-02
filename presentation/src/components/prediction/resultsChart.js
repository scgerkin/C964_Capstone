import * as d3 from "d3"
import { decimalToPercent, toPascal } from "../../utils/utils"

const MARGIN = { TOP: 80, BOTTOM: 10, LEFT: 90, RIGHT: 70 }
const WIDTH = 500 - MARGIN.LEFT - MARGIN.RIGHT
const HEIGHT = 500 - MARGIN.TOP - MARGIN.BOTTOM
const TRANSITION_DURATION = 2000 // ms

class ResultsChart {
  constructor(element, data) {
    this.initSVG(element)
    this.initXLabel()
    this.initAxesGroups()
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

  initXLabel() {
    this.xLabel = this.svg.append("text")
                      .attr("x", WIDTH / 2)
                      .attr("y", -30)
                      .attr("text-anchor", "middle")
                      .text("Probability %")
  }

  initAxesGroups() {
    this.xAxisGroup = this.svg.append("g")
    this.yAxisGroup = this.svg.append("g")
  }

  update(data) {
    this.cleanAndSetData(data)
    this.setXY()
    this.setAxes()
    this.drawData()
  }

  cleanAndSetData(data) {
    // sort descending
    data = data.sort(
      (a, b) => parseFloat(b.probability) - parseFloat(a.probability))
    // clean labels
    data = data.map(d => {
      return {
        label: toPascal(d.label, "_"),
        probability: decimalToPercent(d.probability),
      }
    })

    this.data = data
  }

  setXY() {
    this.x = d3.scaleLinear()
               .domain([0, 100])
               .range([0, WIDTH])

    this.y = d3.scaleBand()
               .domain(this.data.map(d => d.label))
               .range([0, HEIGHT])
               .padding(0.1)

  }

  setAxes() {
    const xAxisCall = d3.axisTop(this.x)
    this.xAxisGroup.transition()
        .duration(TRANSITION_DURATION)
        .call(xAxisCall)
        .selectAll("text")
        .attr("transform", `translate(15,-10)rotate(-45)`)
        .style("text-anchor", "end")

    const yAxisCall = d3.axisLeft(this.y)
    this.yAxisGroup.transition()
        .duration(TRANSITION_DURATION)
        .call(yAxisCall)
  }

  drawData() {
    const lines = this.svg.selectAll("data-line")
                      .data(this.data)

    lines.enter()
         .append("line")
         .attr("x2", this.x(0))
         .attr("y1", d => this.y(d.label))
         .attr("y2", d => this.y(d.label))
         .attr("transform", "translate(0,13)")
         .attr("stroke", "grey")
         .transition()
         .duration(TRANSITION_DURATION)
         .attr("x1", d => this.x(d.probability))

    this.svg.selectAll("data-point")
        .data(this.data)
        .enter()
        .append("circle")
        .attr("cx", this.x(0))
        .attr("cy", d => this.y(d.label))
        .attr("r", "6")
        .style("fill", fillColor)
        .attr("stroke", "black")
        .attr("transform", "translate(0,13)")
        .transition()
        .duration(TRANSITION_DURATION)
        .attr("cx", d => this.x(d.probability))
        .attr("cy", d => this.y(d.label))



    lines.enter()
         .append("text")
         .attr("x", d => this.x(d.probability))
         .attr("y", d => this.y(d.label))
         .attr("transform", "translate(10, 20)")
         .text(d => `${d.probability}%`)
         .attr("fill-opacity", 0)
         .transition()
         .delay(TRANSITION_DURATION)
         .duration(TRANSITION_DURATION)
         .attr("fill-opacity", 1)

  }
}

function fillColor(data) {
  const p = data.probability
  const red = 255 * (p / 100)
  const green = 255 - red
  const blue = 255 / 10

  return `rgb(${red}, ${green}, ${blue})`
}

export default ResultsChart
