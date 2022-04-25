<template>
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

    <div v-if="worldData != null && exportData != null">
    <svg :width="width" :height="height">
        <path
            v-for="feature in worldData.features"
            :key="feature.properties.ADM0_A3"
            :d="getPathForFeature(feature)"
            :fill="fillColor(feature.properties.ISO_A3)"
            >
        </path>

    </svg>
    </div>
</template>

<script>
import { json, csv, geoMercator, geoPath, interpolateRgb } from "d3"

export default {
    data: () => ({
        worldData: null,
        exportData: null,
        importData: null,
        dataType: 'import',
        year: 2020,
        width: 1000,
        height: 800
    }),
    mounted() {
        json("./data/world.geojson").then(data => {
            this.worldData = data
            console.log(this.worldData)
        })
        csv("./data/exports.csv").then(data => {
            this.exportData = data
        })
        csv("./data/imports.csv").then(data => {
            this.importData = data
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
                value = this.filterData(country, 'ISO3', this.importData)
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
        }
    }
}
</script>

<style>

</style>