<template>
  
</template>

<script>
import { csv } from "d3"
export default {
    data: () => ({
        pieData: null,
    }),
    mounted() {
        json("./data/pieData.csv").then(data => {
            this.pieData = data
            console.log(this.pieData)
        })
    },
}
</script>

<style>

</style>