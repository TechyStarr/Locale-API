<template>
  <nav>
    <!-- <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
    <router-link to="/locale">Locale</router-link> -->
  </nav>
  <router-view/>
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
      parsedData: null
    }
  },
  // Call the getData method on creation to get the data from the API server and store it in the responseData variable
  methods: {
    getData () {
      axios
        .get('http://127.0.0.1:5000/view/states')
        .then(response => {
          // this.responseData = response.data
          this.parsedData = response.data
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
