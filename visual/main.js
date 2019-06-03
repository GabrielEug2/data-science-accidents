const url = "https://servicodados.ibge.gov.br/api/v2/malhas/?resolucao=2&formato=application/vnd.geo+json";

let accidents;

d3.csv("latlon.csv").then(function(data) {
    accidents = data;
});

const width = 800;
const height = 800;

const svg = d3.select("div.container")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

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
    // svg
    // .selectAll("circle")
    // .data(accidents)
    // .enter()
    // .append("circle")
    // .attr("class", function(d) {return d.mortos === 1 ? "fatal" : "not"})
    // .attr("cx", function(d) {return projection([d.longitude, d.latitude])[0];})
    // .attr("cy", function(d) {return projection([d.longitude, d.latitude])[1];})
    // .attr("r", "1px");

    const days = Array.from(new Set(accidents.map(a => a.data_inversa)));

    for (let day of days) {
        svg
        .append("g")
        .selectAll("circle")
        .data(accidents.filter(e => e.data_inversa === day))
        .enter()
        .append("circle")
        .attr("class", function(d) {return d.mortos === 1 ? "fatal" : "not"})
        .attr("cx", function(d) {return projection([d.longitude, d.latitude])[0];})
        .attr("cy", function(d) {return projection([d.longitude, d.latitude])[1];})
        .attr("r", "1px");

        svg.select("text").remove();
        svg.append("text").attr("x",50).attr("y",700).text(day).attr("fill","white");

        await sleep(10);
    }
}
