<script>
  import { Line } from 'vue-chartjs'

  export default {
    extends: Line,
    data: () => ({
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes:[{
            ticks: {
              beginAtZero: true
            }
          }],
        },
      }
    }),
    props: {
      chartData: Object
    },

    mounted () {
      console.log(this.chartData)
      this.renderChart(this.chartData, this.options)
      this.$watch(
        'chartData', () => {
          this.renderChart(this.chartData, this.options)
        }
      )
    }
  }
</script>