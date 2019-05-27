const url = "https://servicodados.ibge.gov.br/api/v2/malhas/?resolucao=2&formato=application/vnd.geo+json";

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

function test() {
    const accidents = d3.csv("latlon.csv").then(function(data) {
        svg.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr("class", "accident")
            .attr("cx", function(d) {return projection([d.longitude, d.latitude])[0];})
            .attr("cy", function(d) {return projection([d.longitude, d.latitude])[1];})
            .attr("r", "1px");
    });
}