<script>
  import { Bar } from 'vue-chartjs'

  export default {
    extends: Bar,
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
          console.log(this.chartData)
          this.renderChart(this.chartData, this.options)
        }
      )
    }
  }
</script>