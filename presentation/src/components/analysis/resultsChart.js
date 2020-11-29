import * as d3 from "d3"

const MARGIN = { TOP: 80, BOTTOM: 10, LEFT: 120, RIGHT: 10 }
const WIDTH = 560 - MARGIN.LEFT - MARGIN.RIGHT
const HEIGHT = 500 - MARGIN.TOP - MARGIN.BOTTOM
const TRANSITION_DURATION = 1000 // ms

class ResultsChart {
  constructor(element, data) {
    this.initSVG(element)
    this.initXYLabels()
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

  initXYLabels() {
    this.xLabel = this.svg.append("text")
                      .attr("x", WIDTH / 2)
                      .attr("y", -30)
                      .attr("text-anchor", "middle")
                      .text("Probability %")
    this.yLabel = this.svg.append("text")
                      .attr("x", HEIGHT / -2)
                      .attr("y", -100)
                      .attr("text-anchor", "middle")
                      .text("Finding")
                      .attr("transform", "rotate(-90)")
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
        label: pascalCaseLabel(d.label),
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
        .attr("fill", d => d.probability > 50 ? "red" : "grey")
        .attr("height", this.y.bandwidth())
        .transition()
        .duration(TRANSITION_DURATION)
        .attr("width", d => this.x(d.probability))
  }
}

function pascalCaseLabel(label) {
  return label.split("_")
              .map(word => word.charAt(0)
                               .toUpperCase() + word.slice(1))
              .join(" ")
}

function decimalToPercent(value) {
  const precision = Math.pow(10, 2)
  return Math.ceil(parseFloat(value) * 100 * precision) / precision
}

export default ResultsChart
