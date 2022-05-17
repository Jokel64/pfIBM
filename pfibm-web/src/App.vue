<template>
  <div id="app">
    <VueSidebarMenuAkahon menu-title="pfIBM" profileImg="" profileName="ToDo: Username"
                          profileRole="" :menu-items="getMenuItems()" :is-search="searchEnabled"/>
    <MainContent :title="title" :fields="current_fields"></MainContent>
  </div>
</template>

<script>
import VueSidebarMenuAkahon from "vue-sidebar-menu-akahon"
import MainContent from "./components/MainContent";
import axios from "axios"

export default {
  name: 'App',
  components: {
    MainContent,
    VueSidebarMenuAkahon
  },
  data(){
    return {
      menu_items: null,
      title: "Loading...",
      current_fields:[]
    }
  },
  computed:{
    searchEnabled(){
      return false;
    }
  },
  watch:{
    $route (to, from){
      let new_path = to.hash.substring(2, to.hash.length)
      this.routeUpdate(new_path)
    }
  },
  methods:{
    routeUpdate(new_path){
      this.title = new_path
      axios.get(`http://localhost:5000/${new_path}`).then(result =>{
        this.current_fields = result.data
      }).catch(err =>{
        console.log(err)
      })
    },
    getMenuItems(){
      if(this.menu_items == null){
        return [{link: '#',name: 'Loading Items', tooltip: '', icon: 'loading' }]
      }
      else{
        var items = []
        for(let i = 0; i < this.menu_items.length; i++){
          let item = this.menu_items[i]
          items.push({link: `#/${item.name}`, name: item.name, tooltip: item.tooltip, icon: item.icon})
        }
        return items
      }
    }
  },
  created() {
    let that = this
    axios.get("http://localhost:5000/").then(result =>{
      this.menu_items = result.data
    }).catch(err =>{
      console.log(err)
    }).finally(()=>{
      if(history.pushState) {
        history.pushState(null, null, '#/Dashboard');
      }
      else {
        location.hash = '#/Dashboard';
      }
      this.routeUpdate("Dashboard")
    })
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
table {
  width:100%;
}
</style>
