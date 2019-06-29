// Salvo no arquivo geo.json
// const brazil_geojson_url = "https://servicodados.ibge.gov.br/api/v2/malhas/?resolucao=2&formato=application/vnd.geo+json";

let accidents;
let validBrs;
let validWeathers;

d3.csv("../data/only_brs_with_most_accidents.csv").then(function(data) {
    accidents = data;

    validBrs = d3.map(accidents, function(d) { return d.br; }).keys();

    let brSelect = document.getElementById("br_select");
    for (let br of validBrs) {
        let option = document.createElement("option");
        option.text = br;
        option.value = br;
        brSelect.add(option);
    }

    validWeathers = d3.map(accidents, function(d) { return d.condicao_metereologica; }).keys();

    let weatherSelect = document.getElementById("weather_select");
    for (let weather of validWeathers) {
        let option = document.createElement("option");
        option.text = weather;
        option.value = weather;
        weatherSelect.add(option);
    }
});

const width = 800;
const height = 800;

const svg = d3.select("div.map")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

const projection = d3.geoMercator()
    .center([-52.887284, -11.880655]) // mais ou menos o centro do Brasil
    .translate([width/2, height/2])
    .scale(1000);
    
const path = d3.geoPath().projection(projection);

let mapGeojson;
d3.json("geo.json").then(function(data) {
    mapGeojson = data;
    svg.selectAll("path")
        .data(data.features)
        .enter()
        .append("path")
        .attr("class", "state")
        .attr("d", path);
});

function updateMap() {
    let selectedBr = null;
    let brSelect = document.getElementById("br_select");
    if (brSelect.selectedIndex > 0) {
        selectedBr = brSelect.options[brSelect.selectedIndex].value;
    }

    let selectedWeather = null;
    let weatherSelect = document.getElementById("weather_select");
    if (weatherSelect.selectedIndex > 0) {
        selectedWeather = weatherSelect.options[weatherSelect.selectedIndex].value;
    }
    
    if (selectedBr) {
        // Da um zoom nessa área do mapa
        let coordinatesOnSelectedBr = accidents
            .filter(function(d) { return d.br === selectedBr; })
            .map(function(d) {
                return {
                    lat: parseFloat(d.latitude),
                    lng: parseFloat(d.longitude)
                };
            });
        let pointsGeojson = GeoJSON.parse(coordinatesOnSelectedBr, {Point: ['lat', 'lng']});

        projection.fitSize([width, height], pointsGeojson);
        svg.selectAll("path").attr("d", path);
    }

    // Plota só os acidentes na BR e no clima selecionados
    // (se não estiver selecionado, considera todos)
    let accidentsToPlot = accidents;
    if (selectedBr) {
        accidentsToPlot = accidentsToPlot.filter(function(d) { return d.br === selectedBr; });
    }
    if (selectedWeather) {
        accidentsToPlot = accidentsToPlot.filter(function(d) {
            return d.condicao_metereologica === selectedWeather;
        });
    }

    svg.selectAll("circle").remove();
    svg.append("g")
        .selectAll("circle")
        .data(accidentsToPlot)
        .enter()
        .append("circle")
        .attr("class", function(d) {return d.mortos === "1" ? "fatal" : "not-fatal"})
        .attr("cx", function(d) {return projection([d.longitude, d.latitude])[0];})
        .attr("cy", function(d) {return projection([d.longitude, d.latitude])[1];})
        .attr("r", "2px");
}