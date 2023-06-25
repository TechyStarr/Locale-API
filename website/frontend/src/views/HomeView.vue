<template>
  <div class="home">
    <div>
    <h1>Locale, your best bet to knowing Nigeria well</h1>
    <input type="text" v-model="searchQuery" placeholder="Search...">
    <button @click="search">Search</button>
    <div v-if="searchResults">
      <ul>
        <li v-for="result in searchResults" :key="result.id">
          {{ result.name }}
        </li>
      </ul>
    </div>
  </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import searchQuery from '@/components/SearchQuery.vue'

export default {
  name: 'HomeView',
  components: {
    // searchQuery
  }
}
</script>
