<template>
    <div class="home">
        <developer-component></developer-component>
        <api-key-modal :api-key="generatedApiKey" v-if="generatedApiKey" />
    </div>
  </template>

<script>
import DeveloperComponent from '@/components/DeveloperComponent.vue'
// import ApiKeyModal from '@/components/ApiKeyModal.vue'

export default {
  name: 'DeveloperView',
  components: {
    DeveloperComponent
    // ApiKeyModal
  },
  data () {
    return {
      apiKey: ''
      // generatedApiKey: null
    }
  }
}
</script>

<style>
.header-text {
  font-size: 1.6rem;
  font-weight: 300;
  margin-top: 12rem;
  /* display: flex;
  justify-content: center;
  align-items: center; */
  /* white-space: ; */
  /* padding-bottom: 2rem; */
}

h1 {
  font-size: x; /* Adjust the font size to your desired value */
  overflow: hidden; /* Hide any overflowing text */
}
</style>
