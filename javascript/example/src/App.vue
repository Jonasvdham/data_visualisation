<template>
  <div id="app">
    <select v-model="selection">
      <option value="NL">The Netherlands</option>
      <option value="IT">Italy</option>
    </select>
    <div class="chart-container">
      <BarChart :chartData="barChartData"/>
    </div>
    <div class="chart-container">
      <LineChart :chartData="lineChartData" />
    </div>
  </div>
</template>

<script>
import BarChart from './components/BarChart.vue'
import LineChart from './components/LineChart.vue'
import { csv } from 'd3-fetch'

export default {
  data: () => ({
    selection: "NL",
    rawData: []
  }),
  
  components: {
    BarChart,
    LineChart
  },
  
  mounted() {
    csv("data/nl_it.csv").then(data => {
      this.rawData = data
    })
  },
  
  computed: {
    barChartData() {
      if (!this.rawData.length) {
        return null;
      }
      else if (this.selection == "NL") {
        let plotData = []
        plotData = this.filterData(this.rawData, "Netherlands")
        return {
          labels: plotData[0],
          datasets: [
            {
              label: 'Cases in the Netherlands',
              backgroundColor: '#1E4785',
              data: plotData[1]
            }
          ]
        };
      } else {
        let plotData = []
        plotData = this.filterData(this.rawData, "Italy")
        return {
          labels: plotData[0],
          datasets: [
            {
              label: 'Cases in Italy',
              backgroundColor: '#008c45',
              data: plotData[1]
            }
          ]
        }
      }
    },
    lineChartData() {
      let nl = []
      nl = this.filterData(this.rawData, "Netherlands")[1]
      let it = []
      it = this.filterData(this.rawData, "Italy")[1]
      nl = Array.from(nl, item => item || 0).slice(100,150);
      it = Array.from(it, item => item || 0).slice(100,150);
      console.log(nl);
      return {
        datasets: [
          {
            label: 'The Netherlands',
            backgroundColor: '#1E4785',
            data: nl
          }, {
            label: 'Italy',
            backgroundColor: '#008c45',
            data: it
          }
        ]
      }
    }
  },
  methods: {
    filterData(data, country) {
      let xData = []
      let yData = [] 
      let i = 0
      let len = data.length

      while ((country != data[i].location) && (i < len)) {
        i++;
      }

      for ( ; i < len; i++) {
        if (country == data[i].location) {
          let date = data[i].date;
          let cases = parseInt(data[i].new_cases_smoothed_per_million);
          
          xData.push(date);
          yData.push(cases);
        }
      }
      console.log(xData);
      console.log(yData);
      return [xData, yData];
    }
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 10px;
}
.chart-container {
  width: 400px;
  height: 400px;
  margin: 20px;
}
</style>