<template>
    <!-- <select v-model='dataType'>
        <option value='import'>import</option>
        <option value='export'>export</option>
    </select> -->
    <div class="p-5 text-center bg-light">
        <center>
        <h1 class="mb-3">Net import/export per country</h1>
        <h4 class="mb-3">{{year}}</h4>
        </center>
    </div>
    <center>
    <transition name="fadeColor">
        <div v-if="worldData != null && netFlowsData != null">
        <svg :width="width" :height="height">
            <path
                v-for="feature in worldData.features"
                :key="feature.properties.ADM0_A3"
                :d="getPathForFeature(feature)"
                :fill="fillColor(feature.properties.ISO_A3, year)"
                >
            </path>
        </svg>
        </div>
    </transition>
    </center>
</template>

<script>
import { json, csv, geoMercator, geoPath } from "d3"
import { interpolateBrBG } from "d3-scale-chromatic"

export default {
    data: () => ({
        worldData: null,
        netFlowsData: null,
        dataType: 'import',
        year: 2017,
        width: 1000,
        height: 800,
        min: 0,
        max: 0,
        yearList: [1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017],
        yearIndex: 0
    }),
    
    mounted() {
        json("./data/world.geojson").then(data => {
            this.worldData = data
            console.log(this.worldData)
        })
        csv("./data/netflows.csv").then(data => {
            this.netFlowsData = data
        })
        setInterval(() => this.updateYear(), 1500)
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
        fillColor(country, year) {
            var value = this.filterData(country, this.netFlowsData, year)
            return interpolateBrBG(value/4532171)
        },
        filterData(name, data, year) {
            for (let i = 0; i < data.length; i++) {
                if (data[i]['ISO3'] == name){
                    return data[i][year];
                }
            }
            return 0;
        },
        updateYear() {
            if (this.yearIndex == (this.yearList.length - 1)) {
                this.yearIndex = 0
                this.year = 2017
            } else {
                this.year = this.yearList[this.yearIndex]
                this.yearIndex++;
            }
        }
    }
}
</script>

<style>
    h1, h2 {
        font-family: 'Trebuchet MS', sans-serif;
    }
</style>