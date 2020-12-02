import * as d3 from "d3"

const MARGIN = { TOP: 80, BOTTOM: 60, LEFT: 90, RIGHT: 70 }
const WIDTH = 500 - MARGIN.LEFT - MARGIN.RIGHT
const HEIGHT = 500 - MARGIN.TOP - MARGIN.BOTTOM
const TRANSITION_DURATION = 2000 // ms

class RocChart {
  constructor(element, data) {
    this.initSVG(element)
    this.initXYLabels()
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
                      .text("True False Rate")
    this.yLabel = this.svg.append("text")
                      .attr("x", HEIGHT / -2)
                      .attr("y", -50)
                      .attr("text-anchor", "middle")
                      .text("True Positive Rate")
                      .attr("transform", "rotate(-90)")
  }

  initAxesGroup() {
    this.xAxisGroup = this.svg.append("g")
    this.yAxisGroup = this.svg.append("g")
  }
}

export default RocChart
