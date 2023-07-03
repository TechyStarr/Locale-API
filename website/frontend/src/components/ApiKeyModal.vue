<template>
  <b-modal id="apiKeyModal" title="Generated API Key">
    <p>{{ apiKey }}</p>
  </b-modal>
</template>

<script>
export default {
  props: ['apiKey']
}
</script>

<style>

#apiKeyModal {
  font-size: 1.6rem;
  font-weight: 300;
}

</style>
