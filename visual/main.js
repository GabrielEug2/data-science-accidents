const url = "https://servicodados.ibge.gov.br/api/v2/malhas/?resolucao=2&formato=application/vnd.geo+json";

let accidents;
let days;

d3.csv("latlon.csv").then(function(data) {
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

const canvasLayer = d3.select("div.map").append('canvas').attr('id', 'heatmap').attr('width', width).attr('height', height);

const projection = d3.geoMercator().scale(1000).translate([1000, 100]).center([-20, 2]);
const path = d3.geoPath().projection(projection);

const json = d3.json("geo.json").then(
    function (data) {
        svg.selectAll("path")
            .data(data.features)
            .enter()
            .append("path")
            .attr("class", "state")
            .attr("d", path);
    }
);

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
    const current = running + 1;
    reset();

    for (let day of days) {
        svg
        .append("g")
        .selectAll("circle")
        .data(accidents.filter(e => e.data_inversa === day))
        .enter()
        .append("circle")
        .attr("class", function(d) {return d.mortos === "1" ? "fatal" : "not"})
        .attr("cx", function(d) {return projection([d.longitude, d.latitude])[0];})
        .attr("cy", function(d) {return projection([d.longitude, d.latitude])[1];})
        .attr("r", "1px");

        svg.select("text").remove();
        svg.append("text").attr("x",50).attr("y",700).text(day).attr("fill","white");

        if (current !== running) {
            return;
        }
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
    .enter().append("path")
    .style("opacity", 0.2)
    .attr("d", d3.geoPath())
    .attr("fill", function(d) { return color(d.value); })
}

function reset() {
    running += 1;
    svg.selectAll("circle,text").remove();
}

function pause() {
    running += 1;
}
