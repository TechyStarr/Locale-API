<template>
  <div class="home">
    <div>
      <h1>Locale, your best bet to knowing Nigeria well</h1>
      <input type="text" v-model="searchQuery" placeholder="Search..." class="search-input">
      <button class="search-btn" @click="search">Search</button>
      <div v-if="searchResults">
        <ul>
          <li v-for="result in searchResults" :key="result.id">
            {{ result.name }}
          </li>
        </ul>
      </div>
    </div>
    <log-out></log-out> <!-- Use the LogOut component -->
  </div>
</template>

<script>
import LogOut from '@/components/LogOut.vue'

export default {
  name: 'HomeView',
  components: {
    LogOut
  }
}
</script>

<style>
.search-input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-btn {
  padding: 10px 20px;
  background-color: #f44336;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
