<template>
  <div class="home">

    <h3>locale</h3>
    <HelloWorld msg="Welcome to Your Vue.js App"/>

    <div>
    <h1>Welcome to Locale</h1>
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
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>
