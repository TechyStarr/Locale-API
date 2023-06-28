<template>
  <div class="home">
    <div>
    <div class="header-text">
      <h1>Locale, your best bet to knowing Nigeria well</h1>
      <!-- <h2>Search for any location in Nigeria</h2> -->
    </div>
    <div>
      <router-link to="/register">
      <button class="get-started-btn">Sign Up to Get Started</button>
    </router-link>
    </div>

      <input type="text" v-model="searchQuery" placeholder="Search for locations in nigeria" class="search-input" @keyup.enter="search">
      <button @click="search" class="search-button">Search</button>
      <div v-if="searchResults">
        <ul>
          <li v-for="result in searchResults" :key="result.id">
            {{ result.name }}
            {{ result.description }}
            <!-- {{ result.lgas }} -->
          </li>
        </ul>
      </div>
      <!-- <search-component></search-component> -->
      <!-- <div> -->
        <!-- filter for regions, state and LGA -->
        <!-- <input v-model="region" placeholder="Region"> -->
        <!-- <input v-model="state" placeholder="State">
        <input v-model="lga" placeholder="LGA">
      </div> -->

      <!-- Button to trigger the filter request -->
      <!-- <button @click="filterLocations">Filter</button> -->

        <!-- Display the filtered locations -->
      <ul>
        <li v-for="location in filteredLocations" :key="location.id">
          {{ location.name }}
        </li>
      </ul>
    </div>
    <log-out></log-out>
  </div>
</template>

<script>
import LogOut from '@/components/LogOut.vue'
import axios from 'axios'
// import SearchComponent from '@/components/SearchComponent.vue'
// import RegisterView from './RegisterView.vue'

export default {
  name: 'HomeView',
  components: {
    LogOut
    // SearchComponent
    // RegisterView
  },
  data () {
    return {
      searchQuery: '',
      searchResults: [],
      region: '',
      state: '',
      lga: '',
      filteredLocations: []
    }
  },
  methods: {
    search () {
      axios.post('http://127.0.0.1:5000/query/?keyword=' + this.searchQuery)
        .then(response => {
          this.searchResults = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    filterLocations () {
      const url = 'http://127.0.0.1:5000/query/?keyword=' + this.searchQuery
      const params = {
        region: this.region,
        state: this.state,
        lga: this.lga
      }
      axios.get(url, { params })
        .then(response => {
          this.filteredLocations = response.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}

</script>

<style>
.header-text {
  font-size: 1.2rem;
  font-weight: 300;
  margin-top: 4rem;
  display: flex;
  justify-content: center;
  align-items: center;
  /* padding-bottom: 2rem; */
}

.get-started-btn {
  padding: 10px 20px;
  background-color: #f44336;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 4rem;
}

.search-input {
  padding: 10px 4rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-input::placeholder {
  float: left;
}

.search-button {
  padding: 10px 20px;
  background-color: #f44336;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
