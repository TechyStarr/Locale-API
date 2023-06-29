<template>
  <div>
    <h2>Places of Interest</h2>
      <div v-for="place in places" :key="place.id">
      <h3>{{ place.name }}</h3>
      <p>{{ place.location }}</p>
      <img :src="place.image" alt="Place of Interest" />
      <p>{{ place.description }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      places: []
    }
  },
  mounted () {
    // Make API call to retrieve places of interest
    // Replace 'apiEndpoint' with the actual endpoint URL
    axios.get('http://127.0.0.1:5000/query/places?keyword=' + this.searchQuery)
      .then(response => {
        this.places = response.data
      })
      .catch(error => {
        console.error('Error retrieving places of interest:', error)
      })
  }

}
</script>
