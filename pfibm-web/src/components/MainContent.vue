<template>
  <div>
      <h1>{{title}}</h1>
    <hr>

    <table>
      <tr v-for="field in fields">
        <td>{{field.name}}:</td>
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
  methods: {
    handleChange(e){
      this.changed = true
    },
  },

}
</script>

<style scoped>

</style>