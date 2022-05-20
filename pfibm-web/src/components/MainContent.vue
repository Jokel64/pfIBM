<template>
  <div>
      <h1>{{title}}</h1>
    <hr>

    <table>
      <tr v-for="field in fields" :class="getDisplaySeparatorClass(field)">
        <td :style="getPaddingForTD(field)">{{field.name}}<span v-if="field.value !== ''">:</span></td>

        <td v-if="field.type == null">{{field.value}}</td>
        <td v-else><input :type="field.type" :value="field.value" :key="field.name" @change="handleChange"></td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  props:{
    title: String,
    fields: Array
  },
  data(){
    return {
      changed: false,
    }
  },
  name: "MainContent",
  computed:{
  },
  methods: {
    handleChange(e){
      this.changed = true
    },
    getDisplaySeparatorClass(field){
      if(field.value === ""){
        return "tr-separator"
      }
      return ""
    },
    getPaddingForTD(field){
      if(field.value === ""){
        return "padding-top: 10px"
      }
      return ""
    }
  },

}
</script>

<style scoped>
table {
  border-collapse: collapse;
}

.tr-separator{
  border-bottom: solid 1px #2c3e50;
  font-weight: bold;
}
</style>