<template>
  <div id="app">
    <PdfCheck msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
import PdfCheck from "@/components/PdfCheck";

export default {
  name: 'App',
  components: {
    PdfCheck
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
