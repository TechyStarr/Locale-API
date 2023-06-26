import axios from 'axios';

export default {
  data() {
    return {
      apiKey: null,
    };
  },
  mounted() {
    this.getApiKey();
  },
  methods: {
    getApiKey() {
      axios.get('your-backend-url/api-key-endpoint')
        .then(response => {
          this.apiKey = response.data.apiKey;
        })
        .catch(error => {
          console.error('Error retrieving API key:', error);
        });
    },
  },
};
