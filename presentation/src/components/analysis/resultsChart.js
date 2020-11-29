import * as d3 from "d3"

const MARGIN = { TOP: 10, BOTTOM: 50, LEFT: 70, RIGHT: 10 }
const WIDTH = 800 - MARGIN.LEFT - MARGIN.RIGHT
const HEIGHT = 500 - MARGIN.TOP - MARGIN.BOTTOM
const TRANSITION_DURATION = 500 // ms

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
                      .attr("y", HEIGHT + 50)
                      .attr("text-anchor", "middle")
                      .text("Diagnostic Labels")

    this.yLabel = this.svg.append("text")
                      .attr("x", HEIGHT / -2)
                      .attr("y", -50)
                      .attr("text-anchor", "middle")
                      .text("Probability %")
                      .attr("transform", "rotate(-90)")

  }

  initAxesGroups() {
    this.xAxisGroup = this.svg.append("g")
                          .attr("transform", `translate(0, ${HEIGHT})`)

    this.yAxisGroup = this.svg.append("g")
  }

  update(data) {
    this.data = data
    this.setXY()
    this.setAxes()
    this.joinData()
    this.removeStaleRects()
    this.updateExistingRects()
    this.addNewRects()
  }

  setXY() {
    this.y = d3.scaleLinear()
               .domain([0, 1])
               .range([HEIGHT, 0])

    this.x = d3.scaleBand()
               .domain(this.data.labels.map(i => i.label))
               .range([0, WIDTH])
               .padding(0.4)

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

  joinData() {
    this.rects = this.svg.selectAll("rect")
                     .data(this.data.labels)
  }

  removeStaleRects() {
    this.rects.exit()
        .transition()
        .duration(TRANSITION_DURATION)
        .attr("height", 0)
        .attr("y", HEIGHT)
        .remove()
  }

  updateExistingRects() {
    this.rects.transition()
        .duration(TRANSITION_DURATION)
        .attr("x", d => this.x(d.label))
        .attr("y", d => this.y(d.probability))
        .attr("width", this.x.bandwidth)
        .attr("height", d => HEIGHT - this.y(d.height))
  }

  addNewRects() {
    this.rects.enter()
        .append("rect")
        .attr("x", d => this.x(d.label))
        .attr("width", this.x.bandwidth())
        .attr("fill", d => {
          if (d.probability > 0.5) {
            return "red"
          }
          return "grey"
        })
        .attr("y", HEIGHT)
        .transition()
        .duration(TRANSITION_DURATION)
        .attr("height", d => HEIGHT - this.y(d.probability))
        .attr("y", d => this.y(d.probability))
  }
}

export default ResultsChart
