<!-- SearchComponent.vue -->
<!-- <template>
  <div>
    <input type="text" v-model="searchQuery" placeholder="Search...">
    <button @click="search">Search</button>
  </div>
</template> -->

<script>
import axios from 'axios'

export default {
  data () {
    return {
      searchQuery: ''
    }
  },
  methods: {
    handleAutoComplete () {
      if (this.searchQuery.length > 2) {
        axios.get('http://127.0.0.1:5000/query/?keyword=awka', {
        params: {
          query: this.searchQuery
        }
      })
      }
    },
    // Perform the search request using the API service
    performSearch () {
      axios.get('http://127.0.0.1:5000/query/?keyword=' + this.searchQuery, {
        params: {
          query: this.searchQuery
        }
      })
        .then(response => {
          // Handle the response data
          const searchResults = response.data
          console.log(searchResults)
          // Do something with the search results
        })
        .catch(error => {
          // Handle any errors
          console.error(error)
        })
    }
  }
}
</script>
