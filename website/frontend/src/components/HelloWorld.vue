<template>
  <div>
    <button @click="getData">Get Data</button>
    <div v-if="parsedData">
      <ul>
        <li v-for="item in parsedData" :key="item.id" class="item">
          <p :style="{ fontWeight: item.highlighted ? 'bold' : 'normal' }">{{ item.name }}</p>
          <p>{{ item.region }}</p>
          <p>{{ item.description }}</p>
          <p>{{ item.capital }}</p>
          <p>{{ item.population }}</p>
          <p>{{ item.area }}</p>
          <p>{{ item.lga }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      responseData: null,
      parsedData: null,
      searchQuery: '',
      searchResults: null
    }
  },
  // Call the getData method on creation to get the data from the API server and store it in the responseData variable
  methods: {
    getData () {
      axios
        .get('http://127.0.0.1:5000/query/?keyword=umuahia')
        .then(response => {
          // this.responseData = response.data
          this.parsedData = response.data
        })
        .catch(error => {
          // Handle the error here
          console.log('Error: ', error)
        })
    }
    // search () {
    //   axios.get('http://')
    //     .then(response => {
    //       this.searchResults = response.data
    //     })
    //     .catch(error => {
    //       console.log('Error: ', error)
    //     })
    // },
    // // Use a computed property to parse the data and store it in the parsedData variable
    // computed: {
    //   parsedData () {
    //     if (this.responseData) {
    //       return JSON.parse(this.responseData)
    //     }
    //   }
    // }
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
