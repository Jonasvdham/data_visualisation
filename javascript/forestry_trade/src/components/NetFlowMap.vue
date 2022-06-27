<template>
    <div>
        <div class="p-5 text-center bg-light">
            <center>
            <h1 class="mb-3">Net wood import/export per country (x1000$)</h1>
            </center>
        </div>
        <div id='grad'>
            <div style="float: left; width: 15%; height: auto; line-height: 30px; vertical-align: middle; font-family: Verdana; font-size: 10px; overflow: hidden; text-align: center; color: white;">
                <b><span>{{min}}</span></b>
            </div>
            <div style="float: right; width: 15%; height: auto; line-height: 30px; vertical-align: middle; font-family: Verdana; font-size: 10px; overflow: hidden; text-align: center; color: white;">
                <b><span>{{max}}</span></b>
            </div>
        </div>
        <center>
            <div v-if="worldData != null && netFlowsData != null && imexFlowsData != null">
                <svg class='map' :width="width" :height="height">
                    <text class="year" x="180" y="80" font-family="Verdana (sans-serif)" font-weight="bold" font-size="20pt" dy="0.35em">{{year}}</text>
                    <template v-if="hover != null && imexFlowsData[hover] != null">
                        <text class="year" x="180" y="120" font-family="Verdana (sans-serif)" font-weight="bold" font-size="14pt" dy="0.35em">{{hover}}</text>
                        <text class="year" x="180" y="120" font-family="Verdana (sans-serif)" font-weight="bold" font-size="14pt" dy="0.35em">{{imexFlowsData[hover]['country']}}</text>
                    </template>
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
                        <template v-if="imexFlowsData[hover][year]">
                            <path
                            class='lines'
                            v-for="(feature, index) in imexFlowsData[hover][year]"
                            :key="`${feature.ISO3}${index}`"
                            :d="generateLink(feature)"
                            :fill="'none'"
                            :stroke="linkStyle.stroke"
                            :stroke-width="generateWidth(feature)"
                            >
                            </path>
                        </template>
                    </template>
                </svg>
            </div>
        </center>
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
        width: 1400,
        height: 960,
        min: -18278800.0,
        max: 18278800.0,
        yearList: [1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017],
        yearIndex: 0,
        link: {type: "LineString", coordinates: [[100, 60], [-60, -30]]},
        linkStyle: {fill: "grey", stroke: "orange", strokeWidth: 7}
    }),
    
    mounted() {
        json("./data/world.geojson").then(data => {
            this.worldData = data
        })
        json("./data/netflows.json").then(data => {
            this.netFlowsData = data
        })
        json("./data/imexflows_top10.json").then(data => {
            console.log(data)
            this.imexFlowsData = data
        })
        setInterval(() => this.updateYear(), 2000)
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
                if (country == this.hover) {
                    return 'black'
                } else if (!this.imexFlowsData[this.hover]) {
                    return '#999999'
                } else if (!(this.year in this.imexFlowsData[this.hover])){
                    return '#999999'
                }
                else {
                    return country in this.imexFlowsData[this.hover][this.year] ? this.generateColor(this.netFlowsData[country][this.year])
                    : '#999999'
                }
            } else {
                return (
                    country in this.netFlowsData ? this.generateColor(this.netFlowsData[country][this.year])
                    : '#999999'
                )
            }
        },
        generateColor(value) {
            // - t / (this.minmax[this.year]['max'] - this.minmax[this.year]['min']
            // console.log(Math.log(value-this.min)+1)
            //console.log(interpolateBrBG(0), interpolateBrBG(0.5), interpolateBrBG(1))
            return interpolateBrBG(1-(value-this.min)/(this.max-this.min))
        },
        updateYear() {
            if (this.yearIndex == (this.yearList.length - 1)) {
                this.yearIndex = 0
                this.year = 2017
            } else {
                this.year = this.yearList[this.yearIndex]
                this.yearIndex++;
            }
        },
        generateLink(feature) {
            //if (this.imexFlowsData[this.hover]['imex'] > 0):
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
        },
        generateWidth(feature) {
            var val = 100*feature.imex / this.max
            if (val < 1) {
                return 1
            } else if (val > 10) {
                return 10
            } else {
                return val
            }
        }
    }
}
</script>

<style>
    h1, h2 {
        font-family: 'Trebuchet MS', sans-serif;
        color: white;
    }
    .country {
        transition: 1s fill ease;
    }
    .year {
        fill: white;
    }
    .lines {
        pointer-events: none;
    }
    #grad {
        height: 30px;
        width: 800px;
        background-color: red; /* For browsers that do not support gradients */
        background-image: linear-gradient(to right, rgb(84, 48, 5), rgb(238, 241, 234), rgb(0, 60, 48));
        /* background-image: linear-gradient(to right, rgb(84, 48, 5) rgb(238, 241, 234) rgb(0, 60, 48)); */
        /*linear-gradient(to right, var(--min_color), var(--max_color));*/
        padding: 0;
        margin: auto;
        border-top-left-radius: 20px;
        border-bottom-left-radius: 20px;
        border-top-right-radius: 20px;
        border-bottom-right-radius: 20px; 
    }
</style>