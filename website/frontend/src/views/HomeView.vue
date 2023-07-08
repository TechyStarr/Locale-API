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
      <div v-if="searchResults !== ''">
        <div v-if="searchResults !== Null">
          <p v-if="searchResults.length === 0" class="error">No results found.</p>
          <p v-else-if="searchResults === 'error'">An error occurred during the search. Please try again later.</p>
          <div v-else>
            <div class="search-result" v-for="result in searchResults" :key="result.id">
              <p>You searched for {{ result.name }}</p>
              <div class="search-item">
                <p>State</p>
                <p>{{ result.name }} </p>
              </div>
              <hr>
              <div class="search-item">
                <p>Region</p>
                <p> {{ result.region }} </p>
              </div>
              <hr>
              <div class="search-item">
                <p>Capital</p>
                <p> {{ result.capital }} </p>
              </div>
              <hr>
              <div class="search-item">
                <p>Number of LGA</p>
                <p> {{ result.lgas }} </p>
              </div>
              <hr>
              <div class="search-item">
                <p>Slogan</p>
                <p> {{ result.slogan }} </p>
              </div>
              <hr>
              <div class="search-item">
                <p>Population</p>
                <p> {{ result.population }} </p>
              </div>

            </div>
          </div>
      </div>
    </div>
      <!-- Add schools -->
      <!-- food marts, restaurants -->
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
      <!-- <ul>
        <li v-for="location in filteredLocations" :key="location.id">
          {{ location.name }}
        </li>
      </ul> -->
    </div>
    <places-of-interest></places-of-interest>
    <log-out></log-out>
  </div>
</template>

<script>
import LogOut from '@/components/LogOut.vue'
import axios from 'axios'
import PlacesOfInterest from '@/components/PlacesOfInterest.vue'
// import SearchComponent from '@/components/SearchComponent.vue'
// import RegisterView from './RegisterView.vue'

export default {
  name: 'HomeView',
  components: {
    LogOut,
    PlacesOfInterest
    // SearchComponent
    // RegisterView
  },
  data () {
    return {
      searchQuery: '', // searchQuery is the variable that holds the search query from the user
      searchResults: [],
      region: '',
      state: '',
      lga: '',
      filteredLocations: []
      // imageURL: 'https://images.unsplash.com/photo-1560792523-9b3e98060a4d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHw1fHx8ZW58MHx8fHx8&auto=format&fit=crop&w=800&q=60'
    }
  },
  methods: {
    handleAutoComplete () {
      if (this.searchQuery.length > 2) {
        axios.get('http://127.0.0.1:5000/query/autocomplete', {
          params: {
            query: this.searchQuery
          }
        })
      }
    },
    search () {
      axios.get('http://127.0.0.1:5000/query?keyword=' + this.searchQuery)
        .then(response => {
          if (Array.isArray(response.data) && response.data.length > 0) {
            // Search results found
            this.searchResults = response.data
            // No search results found
            this.searchResults = 'error'
          }
          this.searchResults = response.data
          console.log(this.searchResults)
        })
        .catch(error => {
          console.log(error)
        })
      console.log(typeof this.searchResults)
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
  font-size: 1.6rem;
  font-weight: 300;
  margin-top: 12rem;
}

h1 {
  font-size: 3rem;
  overflow: hidden;
}

.get-started-btn {
  padding: 16px 20px;
  background-color: #f44336;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 4rem;
}

.get-started-btn:hover {
  background-color: #1e1e1e;
}

.search-input {
  padding: 15px 72px;
  border: 1px solid #ccc;
  border-radius: 4px 0 0 4px;
}

.search-input::placeholder {
  float: left;
}

.search-button {
  padding: 16px 24px;
  background-color: #f44336;
  color: #fff;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
}

.search-result {
  display: block;
  justify-content: flex-start;
  align-items: center;
  margin: 350px;
  margin-top: 32px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-item {
  margin-top: 32px;
  font-size: 18px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-result p,
.search-result li {
  flex: 24%;
  color: #1e1e1e;
  font-size: 18px;
  list-style: none;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 24px;
  margin-bottom: 8px;
  margin-left: 400px;
  margin-right: 400px;
  background-color: rgb(255, 228, 228);
  padding: 15px 72px;
  /* border: 1px solid red; */
  border-radius: 4px 0 0 4px;
}

hr {
  border-color: #e2e2e2;
  border-width: 1px;
  border-style: solid;
  width: 100%;
}

@media (max-width: 768px) {
  .header-text {
    font-size: 1.2rem;
    margin-top: 6rem;
  }

  h1 {
    font-size: 1.8rem;
  }

  .get-started-btn {
    padding: 12px 16px;
    margin-bottom: 2rem;
  }

  .search-input {
    padding: 10px 48px;
  }

  .search-button {
    padding: 12px 18px;
  }

  .search-result {
    margin: 150px;
    margin-top: 32px;
  }

  .search-item {
    font-size: 14px;
  }

  .search-result p,
  .search-result li {
    font-size: 14px;
  }
}

</style>
