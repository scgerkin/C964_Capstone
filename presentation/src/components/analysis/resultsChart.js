import * as d3 from "d3"

const MARGIN = { TOP: 10, BOTTOM: 50, LEFT: 70, RIGHT: 10 }
const WIDTH = 800 - MARGIN.LEFT - MARGIN.RIGHT
const HEIGHT = 500 - MARGIN.TOP - MARGIN.BOTTOM
const TRANSITION_DURATION = 500 // ms

class ResultsChart {
  constructor(element, data) {
    const vis = this

    vis.svg = d3.select(element)
                .append("svg")
                .attr("width", WIDTH + MARGIN.LEFT + MARGIN.RIGHT)
                .attr("height", HEIGHT + MARGIN.TOP + MARGIN.BOTTOM)
                .append("g")
                .attr("transform", `translate(${MARGIN.LEFT}, ${MARGIN.TOP})`)

    vis.xLabel = vis.svg.append("text")
                    .attr("x", WIDTH / 2)
                    .attr("y", HEIGHT + 50)
                    .attr("text-anchor", "middle")
                    .text("Diagnostic Labels")

    vis.yLabel = vis.svg.append("text")
                    .attr("x", HEIGHT / -2)
                    .attr("y", -50)
                    .attr("text-anchor", "middle")
                    .text("Probability %")
                    .attr("transform", "rotate(-90)")

    vis.xAxisGroup = vis.svg.append("g")
                        .attr("transform", `translate(0, ${HEIGHT})`)

    vis.yAxisGroup = vis.svg.append("g")

    this.update(data)
  }

  update(data) {
    const vis = this

    vis.data = data
    console.log(data)

    const y = d3.scaleLinear()
                .domain([0, 1])
                .range([HEIGHT, 0])

    const x = d3.scaleBand()
                .domain(vis.data.labels.map(i => i.label))
                .range([0, WIDTH])
                .padding(0.4)

    const xAxisCall = d3.axisBottom(x)
    vis.xAxisGroup.transition()
       .duration(TRANSITION_DURATION)
       .call(xAxisCall)

    const yAxisCall = d3.axisLeft(y)
    vis.yAxisGroup.transition()
       .duration(TRANSITION_DURATION)
       .call(yAxisCall)

    // JOIN
    const rects = vis.svg.selectAll("rect")
                     .data(vis.data.labels)

    // EXIT
    rects.exit()
         .transition()
         .duration(TRANSITION_DURATION)
         .attr("height", 0)
         .attr("y", HEIGHT)
         .remove()

    // UPDATE
    rects.transition()
         .duration(TRANSITION_DURATION)
         .attr("x", d => x(d.label))
         .attr("y", d => y(d.probability))
         .attr("width", x.bandwidth)
         .attr("height", d => HEIGHT - y(d.height))

    // ENTER
    rects.enter()
         .append("rect")
         .attr("x", d => x(d.label))
         .attr("width", x.bandwidth())
         .attr("fill", d => {
           if (d.probability > 0.5) {
             return "red"
           }
           return "grey"
         })
         .attr("y", HEIGHT)
         .transition()
         .duration(TRANSITION_DURATION)
         .attr("height", d => HEIGHT - y(d.probability))
         .attr("y", d => y(d.probability))
  }
}

export default ResultsChart
