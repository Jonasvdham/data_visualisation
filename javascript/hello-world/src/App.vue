<template>
  <NetFlowMap></NetFlowMap>
  <MyMap></MyMap>
</template>

<script>
import MyMap from './components/MyMap.vue'
import NetFlowMap from './components/NetFlowMap.vue'

export default {
  name: 'App',
  components: {
    MyMap,
    NetFlowMap
  }
}
</script>

<style>

</style>
