// Salvo no arquivo geo.json
// const brazil_geojson_url = "https://servicodados.ibge.gov.br/api/v2/malhas/?resolucao=2&formato=application/vnd.geo+json";

let accidents;
let days;

d3.csv("../data/visualizations_data.csv").then(function(data) {
    accidents = data;
    days = Array.from(new Set(accidents.map(a => a.data_inversa)));
});

const width = 800;
const height = 800;
let running = 0;

const svg = d3.select("div.map")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

const canvasLayer = d3.select("div.map")
    .append('canvas')
    .attr('id', 'heatmap')
    .attr('width', width)
    .attr('height', height);

const projection = d3.geoMercator().scale(1000).translate([1000, 100]).center([-20, 2]);
const path = d3.geoPath().projection(projection);

const json = d3.json("geo.json").then(function (data) {
    svg.selectAll("path")
        .data(data.features)
        .enter()
        .append("path")
        .attr("class", "state")
        .attr("d", path);
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
    running = true

    for (let day of days) {
        if (!running) {
            return;
        }

        svg.append("g")
            .selectAll("circle")
            .data(accidents.filter(e => e.data_inversa === day))
            .enter()
            .append("circle")
            .attr("class", function(d) {return d.mortos === "1" ? "fatal" : "not-fatal"})
            .attr("cx", function(d) {return projection([d.longitude, d.latitude])[0];})
            .attr("cy", function(d) {return projection([d.longitude, d.latitude])[1];})
            .attr("r", "1px");

        svg.select("text").remove();
        svg.append("text")
            .attr("x",50)
            .attr("y",700)
            .text(day)
            .attr("fill","white");

        await sleep(10);
    }
}

function heat() {
  // Prepare a color palette
  var color = d3.scaleLinear()
      .domain([0, 1]) // Points per square pixel.
      .range(["lime", "orange", "red"])

  // compute the density data
  var densityData = d3.contourDensity()
    .x(function(d) {return Math.round(projection([d.longitude, d.latitude])[0]);})
    .y(function(d) {return Math.round(projection([d.longitude, d.latitude])[1]);})
    .size([width, height])
    .bandwidth(20)
    (accidents)

  // show the shape!
  svg.insert("g", "g")
    .selectAll("path")
    .data(densityData)
    .enter()
    .append("path")
    .style("opacity", 0.2)
    .attr("d", d3.geoPath())
    .attr("fill", function(d) { return color(d.value); })
}

function reset() {
    running = false;
    svg.selectAll("circle,text").remove();
}

function pause() {
    running = false;
}
