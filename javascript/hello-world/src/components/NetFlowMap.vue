<template>
    <!-- <select v-model='dataType'>
        <option value='import'>import</option>
        <option value='export'>export</option>
    </select> -->
    <div class="p-5 text-center bg-light">
        <h1 class="mb-3">Net import/export per country</h1>
    </div>
    <div v-if="worldData != null && netFlowsData != null && imexFlowsData != null">
    <svg class='map' :width="width" :height="height">
        <text x="0" y="50" font-family="Verdana (sans-serif)" font-weight="bold" font-size="20pt" dy="0.35em">{{year}}</text>
        <path
            @mouseover="hover = feature.properties.ISO_A3"
            @mouseleave="hover = null"
            class='country'
            v-for="feature in worldData.features"
            :key="feature.properties.ADM0_A3"
            :d="getPathForFeature(feature)"
            :fill="fillColor(feature.properties.ISO_A3)"
            >
        </path>
        <template v-if="hover != null && imexFlowsData[hover] != null">
            <template v-if="imexFlowsData[hover][year] != null">
                <path
                v-for="feature in imexFlowsData[hover][year]"
                :key="feature.ISO3"
                :d="generateLink(feature)"
                :fill="'none'"
                :stroke="linkStyle.stroke"
                :strokeWidth="linkStyle.strokeWidth"
                >
                </path>
            </template>
        </template>
    </svg>
    </div>
</template>

<script>
import { json, geoMercator, geoPath } from "d3"
import { interpolateBrBG } from "d3-scale-chromatic"

export default {
    data: () => ({
        worldData: null,
        netFlowsData: null,
        imexFlowsData: null,
        hover: null,
        dataType: 'import',
        year: 2017,
        width: 1000,
        height: 800,
        min: -18278800.0,
        max: 18278800.0,
        yearList: [1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017],
        yearIndex: 0,
        link: {type: "LineString", coordinates: [[100, 60], [-60, -30]]},
        linkStyle: {fill: "grey", stroke: "orange", strokeWidth: "100"}
    }),
    
    mounted() {
        json("./data/world.geojson").then(data => {
            this.worldData = data
        })
        json("./data/netflows.json").then(data => {
            this.netFlowsData = data
        })
        json("./data/imexflows.json").then(data => {
            console.log(data)
            this.imexFlowsData = data
        })
        setInterval(() => this.updateYear(), 3000)
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
            if (this.hover != null) {
                return '#999999'
            } else {
                return (
                    country in this.netFlowsData ? this.generateColor(this.netFlowsData[country][String(this.year)])
                    : '#999999'
                )
            }
        },
        generateColor(value) {
            // - t / (this.minmax[this.year]['max'] - this.minmax[this.year]['min']
            // console.log(Math.log(value-this.min)+1)
            return interpolateBrBG((value-this.min)/(this.max-this.min))
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
            console.log(this.hover)
            console.log(this.imexFlowsData[String(this.hover)])
            console.log(Object.keys(this.imexFlowsData))
            if (this.yearIndex == (this.yearList.length - 1)) {
                this.yearIndex = 0
                this.year = 2017
            } else {
                this.year = this.yearList[this.yearIndex]
                this.yearIndex++;
            }
        },
        generateLink(feature) {
            var d = this.getPathForFeature(
                {
                    type: "LineString",
                    coordinates: [
                        [this.imexFlowsData[this.hover]['lon'], this.imexFlowsData[this.hover]['lat']],
                        [feature.lon, feature.lat]
                        ]
                }
            )
            return d
        }
    }
}
</script>

<style>
    h1, h2 {
        font-family: 'Trebuchet MS', sans-serif;
    }
    .country {
        transition: 1s fill ease;
    }
</style>