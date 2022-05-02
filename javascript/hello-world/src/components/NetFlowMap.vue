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
        <template v-if="hover != null && imexFlowsData[hover] != null && imexFlowsData[hover][year] != null">
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
        min: -20909069.0,
        max: 13559228.0,
        yearList: [1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017],
        yearIndex: 0,
        minmax: {'1997': {'min': -20909069.0, 'max': 13559228.0}, '1998': {'min': -20302486.0, 'max': 8625975.0}, '1999': {'min': -21203185.0, 'max': 12146493.0}, '2000': {'min': -23041308.0, 'max': 11446802.0}, '2001': {'min': -20026711.0, 'max': 11656353.0}, '2002': {'min': -17868912.0, 'max': 10130077.0}, '2003': {'min': -19642671.0, 'max': 11127461.0}, '2004': {'min': -24363558.0, 'max': 13738748.0}, '2005': {'min': -23375013.0, 'max': 15815402.0}, '2006': {'min': -22131319.0, 'max': 13294242.0}, '2007': {'min': -18414021.0, 'max': 10099149.0}, '2008': {'min': -20038725.0, 'max': 14141927.0}, '2009': {'min': -11911060.0, 'max': 11521904.0}, '2010': {'min': -15670242.0, 'max': 17579193.0}, '2011': {'min': -17105081.0, 'max': 21589225.0}, '2012': {'min': -16978933.0, 'max': 20833455.0}, '2013': {'min': -18486239.0, 'max': 24327738.0}, '2014': {'min': -18564801.0, 'max': 23898061.0}, '2015': {'min': -17270627.0, 'max': 20577430.0}, '2016': {'min': -16821975.0, 'max': 21022238.0}, '2017': {'min': -18323166.0, 'max': 29274030.0}},
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
            console.log(this.imexFlowsData[this.hover])
            if (this.yearIndex == (this.yearList.length - 1)) {
                this.yearIndex = 0
                this.year = 2017
            } else {
                this.year = this.yearList[this.yearIndex]
                this.yearIndex++;
            }
            this.min = this.minmax[this.year]['min']
            this.max = this.minmax[this.year]['max']
        },
        generateLink(feature) {
            var d = this.getPathForFeature(
                {
                    type: "LineString",
                    coordinates: [
                        [this.imexFlowsData['AFG']['lat'], this.imexFlowsData['AFG']['lon']],
                        [feature.lat, feature.lon]
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