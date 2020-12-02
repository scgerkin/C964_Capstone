import * as d3 from "d3"

const MARGIN = { TOP: 80, BOTTOM: 60, LEFT: 90, RIGHT: 70 }
const WIDTH = 500 - MARGIN.LEFT - MARGIN.RIGHT
const HEIGHT = 500 - MARGIN.TOP - MARGIN.BOTTOM
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
                          .attr("transform", `translate(0, ${HEIGHT})`)
    this.yAxisGroup = this.svg.append("g")
  }

  update(data) {
    this.setData(data)
    this.setXY()
    this.setAxes()
    this.drawData()
  }

  setData(data) {
    console.log(Object.keys(data))
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

  drawData() {



    Object.keys(this.data)
          .forEach(label => {
            const line = d3.line()
                           .x(d => this.x(d.fpr))
                           .y(d => this.y(d.tpr))


            this.svg.append("path")
                .datum(this.data[label].points)
                .attr("fill", "none")
                .attr("stroke", "red")
                .attr("stroke-width", 2)
                .attr("d", line)


          })

  }
}

export default RocChart
