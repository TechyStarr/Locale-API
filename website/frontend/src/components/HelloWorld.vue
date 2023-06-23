<template>
  <div>
    <button @click="getData">Get Data</button>
    <div v-if="responseData">
      <p>{{ responseData }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      responseData: null
    }
  },
  methods: {
    getData () {
      axios.get('http://127.0.0.1:5000/view/regions')
        .then(response => {
          this.responseData = response.data
        })
        .catch(error => {
          // Handle the error here
          console.log('Error: ', error)
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
