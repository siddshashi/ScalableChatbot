import axios from 'axios';

// Create an instance of axios with the base URL
const api = axios.create({
    baseURL: "http://34.59.183.102"
});

// Export the Axios instance
export default api;