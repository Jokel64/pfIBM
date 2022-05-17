<template>
  <div id="app">
    <VueSidebarMenuAkahon menu-title="pfIBM" profileImg="" profileName="ToDo: Username"
                          profileRole="" :menu-items="getMenuItems()"/>
    <MainContent title="Test"></MainContent>
  </div>
</template>

<script>
import VueSidebarMenuAkahon from "vue-sidebar-menu-akahon"
import MainContent from "./components/MainContent";

export default {
  name: 'App',
  components: {
    MainContent,
    VueSidebarMenuAkahon
  },
  methods:{
    getMenuItems(){
      return [{link: '/test',name: 'Dashboard', tooltip: 'Dashboard', icon: 'bx-grid-alt' }]
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 2em;
  color: #2c3e50;
}
</style>
