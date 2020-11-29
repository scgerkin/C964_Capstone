import * as d3 from "d3"
import { decimalToPercent, toPascal } from "../../utils/utils"

const MARGIN = { TOP: 80, BOTTOM: 10, LEFT: 100, RIGHT: 50 }
const WIDTH = 500 - MARGIN.LEFT - MARGIN.RIGHT
const HEIGHT = 500 - MARGIN.TOP - MARGIN.BOTTOM
const TRANSITION_DURATION = 1000 // ms

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
    // .attr("transform", `translate(0, ${HEIGHT})`)

    this.yAxisGroup = this.svg.append("g")
  }

  update(data) {
    this.cleanAndSetData(data)
    this.setXY()
    this.setAxes()
    this.joinData()
    this.removeStaleRects()
    this.addNewRects()
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

  joinData() {
    this.rects = this.svg.selectAll("rect")
                     .data(this.data)
  }

  removeStaleRects() {
    this.rects.exit()
        .transition()
        .duration(TRANSITION_DURATION)
        .attr("height", 0)
        .attr("y", HEIGHT)
        .remove()
  }

  addNewRects() {
    this.rects.enter()
        .append("rect")
        .attr("x", this.x(0))
        .attr("y", d => this.y(d.label))
        .attr("fill", fillColor)
        .attr("height", this.y.bandwidth())
        .transition()
        .duration(TRANSITION_DURATION)
        .attr("width", d => this.x(d.probability))

    this.rects.enter()
        .append("text")
        .attr("x", d => this.x(d.probability))
        .attr("y", d => this.y(d.label))
        .attr("transform", "translate(0, 20)")
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
