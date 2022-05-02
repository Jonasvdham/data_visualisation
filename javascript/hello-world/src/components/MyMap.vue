<template>
    <center>
    <div class="p-5 text-center bg-light">
        <h1 class="mb-3">Trade flows in and out of Afghanistan</h1>
    </div>
    </center>
    <select v-model='year'>
        <option value=2020>2020</option>
        <option value=2010>2010</option>
        <option value=2000>2000</option>
        <option value=1990>1990</option>
        <option value=1980>1980</option>
    </select>
    <select v-model='dataType'>
        <option value='import'>import</option>
        <option value='export'>export</option>
    </select>
    <center>
    <div v-if="worldData != null && exportData != null && importData != null && tradeFlowsForestProd != null">
    <svg :width="width" :height="height">
        <path
            v-for="feature in worldData.features"
            :key="feature.properties.ADM0_A3"
            :d="getPathForFeature(feature)"
            :fill="fillColor(feature.properties.ISO_A3)"
            @mouseover="hover = feature.properties.ADM0_A3"
            @mouseleave="hover = null"
            >
        </path>
        <path
            v-for="feature in tradeFlowsForestProd"
            :key="feature.partnerISO3"
            :d="generateLink(feature)"
            :fill="'none'"
            :stroke="linkStyle.stroke"
            :strokeWidth="linkStyle.strokeWidth"
        >
        </path>
    </svg>
    </div>
    </center>
</template>

<script>
import { json, csv, geoMercator, geoPath, interpolateRgb } from "d3"

export default {
    data: () => ({
        worldData: null,
        exportData: null,
        importData: null,
        tradeFlows: null,
        tradeFlowsForestProd: null,
        hover: null,
        dataType: 'import',
        year: 2020,
        width: 1000,
        height: 800,
        link: {type: "LineString", coordinates: [[100, 60], [-60, -30]]},
        linkStyle: {fill: "grey", stroke: "orange", strokeWidth: "100"},
    }),
    mounted() {
        json("./data/world.geojson").then(data => {
            this.worldData = data
        })
        csv("./data/exports.csv").then(data => {
            this.exportData = data
        })
        csv("./data/imports.csv").then(data => {
            this.importData = data
        })
        // csv("./data/forestry_tradeflows_full.csv").then(data => {
        //     this.tradeFlows = data.slice(0,10)
        // })
        csv("./data/forestry_tradeflows_forestproducts.csv").then(data => {
            this.tradeFlowsForestProd = data.slice(0,10)
        })
    },
    computed: {
        projection() {
            return geoMercator()
                .translate([this.width/2, this.height/2])
        },
    },
    methods: {
        getPathForFeature(feature) {
            return geoPath()
                .projection(this.projection)(feature)
        },
        fillColor(country) {
            var value;
            if (this.dataType == 'import') {
                value = this.filterData(country, 'ISO3', this.importData)
                return interpolateRgb("black", "red")(value/4532171)
            }
            else {
                value = this.filterData(country, 'ISO3', this.exportData)
                return interpolateRgb("black", "blue")(value/4532171)
            }
            
        },
        filterData(name, col, data) {
            for (let i = 0; i < data.length; i++) {
                if (data[i][col] == name){
                    return data[i][this.year];
                }
            }
            return 0;
        },
        generateLink(feature) {
            var d = this.getPathForFeature(
                {
                    type: "LineString",
                    coordinates: [
                        [feature.reporter_lon, feature.reporter_lat],
                        [feature.partner_lon, feature.partner_lat]
                        ]
                }
            )
            return d
        }
    }
}
</script>

<style>

</style>