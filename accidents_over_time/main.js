// Salvo no arquivo geo.json
// const brazil_geojson_url = "https://servicodados.ibge.gov.br/api/v2/malhas/?resolucao=2&formato=application/vnd.geo+json";

let accidents;
let days;
let states;

d3.csv("../data/visualizations_data.csv").then(function (data) {
    accidents = data;
    days = Array.from(new Set(accidents.map(a => a.data_inversa)));
});

d3.json("../data/states.json").then(function (data) {
    states = data;
});

const width = 800;
const height = 800;
let running = false;

const svg = d3.select("div.map")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// const canvasLayer = d3.select("div.map")
//     .append('canvas')
//     .attr('id', 'heatmap')
//     .attr('width', width)
//     .attr('height', height);

const projection = d3.geoMercator().scale(1000).translate([1000, 100]).center([-20, 2]);
const path = d3.geoPath().projection(projection);

const json = d3.json("uf.json").then(function (data) {
    console.log(data)
    svg.selectAll("path")
        .data(topojson.feature(data, data.objects.uf).features)
        .enter()
        .append("path")
        .attr("class", "state")
        .attr("d", path)
        .on('mouseover', function (d, i) {
            const state = d.id;
            
            d3.select(this).style('fill-opacity', .5);
            d3.select("#state").text(state)
            d3.select("#total").text(states[state].total)
            d3.select("#ranking").text(states[state].rank)
            d3.select("#city").text(states[state].top_city)
            d3.select("#city-total").text(states[state].city_total)
            d3.select("#br").text(states[state].top_br)
            d3.select("#br-total").text(states[state].br_total)
            d3.select("#type").text(states[state].top_type)
            d3.select("#info").style('visibility', 'visible');
        })
        .on('mouseout', function (d, i) {
            d3.select(this).style('fill-opacity', 1);
            d3.select("#info").style('visibility', 'hidden');
        });
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
    running = true;

    for (let day of days) {
        if (!running) {
            return;
        }

        svg.append("g")
            .selectAll("circle")
            .data(accidents.filter(e => e.data_inversa === day))
            .enter()
            .append("circle")
            .attr("class", function (d) { return d.mortos === "1" ? "fatal" : "not-fatal" })
            .attr("cx", function (d) { return projection([d.longitude, d.latitude])[0]; })
            .attr("cy", function (d) { return projection([d.longitude, d.latitude])[1]; })
            .attr("r", "1px");

        svg.select("text").remove();
        svg.append("text")
            .attr("x", 50)
            .attr("y", 700)
            .text(day)
            .attr("fill", "white");

        await sleep(10);
    }
}

function heat() {
    d3.selectAll(".heatmap").remove();

    // Prepare a color palette
    var color = d3.scaleLinear()
        .domain([0, 1]) // Points per square pixel.
        .range(["lime", "orange", "red"])

    // compute the density data
    var densityData = d3.contourDensity()
        .x(function (d) { return Math.round(projection([d.longitude, d.latitude])[0]); })
        .y(function (d) { return Math.round(projection([d.longitude, d.latitude])[1]); })
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
        .attr("fill", function (d) { return color(d.value); })
        .attr("class", "heatmap")
}

function reset() {
    running = false;
    svg.selectAll("circle, text, .heatmap").remove();
}

function pause() {
    running = false;
}
