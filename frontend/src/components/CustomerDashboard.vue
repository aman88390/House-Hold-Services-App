<template>
  <div>
    <nav class="navbar">
      <ul class="nav-links">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/customer/requested_services">Services</router-link></li>
        <li><router-link to="/search_services">Search Services</router-link></li>
        <li><router-link to="/customer_summary">Summary</router-link></li>
        <li>
          <button class="logout-btn" @click="logout">Logout</button>
        </li>
      </ul>
    </nav>

    <div class="main-content">
      <h1 class="heading">Available Services</h1>
      <div class="filter-section">
        <label for="serviceType" class="filter-label">Filter by Service Type:</label>
        <select v-model="selectedServiceType" @change="fetchServices" class="filter-select">
          <option value="">All</option>
          <option v-for="type in serviceTypes" :key="type.id" :value="type.id">
            {{ type.name }}
          </option>
        </select>
      </div>

      <div class="services-section" v-if="services.length">
        <div v-for="service in services" :key="service.id" class="service-card">
          <h3 class="service-title">{{ service.name }}</h3>
          <p class="service-description">{{ service.description }}</p>
          <p class="service-price">Base Price: ${{ service.base_price }}</p>
          <button class="book-btn" @click="goToBooking(service.id)">Book Now</button>
        </div>
      </div>
      <div v-else class="no-services">
        <p>No services available.</p>
      </div>
    </div>
  </div>
</template>

  <script>
  import axios from 'axios';
  import BookService from './BookService.vue'
  import CustomerRequestedServices from './CustomerRequestedServices.vue';
  
  export default {
    data() {
      return {
        serviceTypes: [],
        services: [],
        selectedServiceType: '',
      };
    },
    methods: {
      getAuthToken() {
        return localStorage.getItem('authToken'); 
      },
  
      async fetchServiceTypes() {
        try {
          const token = this.getAuthToken();
          const response = await axios.get('http://127.0.0.1:5000/service_types_', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.serviceTypes = response.data;
        } catch (error) {
          console.error("Error fetching service types:", error);
        }
      },
  
      async fetchServices() {
        const params = {};
        if (this.selectedServiceType) params.service_type_id = this.selectedServiceType;
  
        try {
          const token = this.getAuthToken();
          const response = await axios.get('http://127.0.0.1:5000/services_', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
            params,
          });
          this.services = response.data;
        } catch (error) {
          console.error("Error fetching services:", error);
        }
      },
  
      goToBooking(serviceId) {
        this.$router.push({ name: 'BookService', params: { serviceId } });
      },
      logout() {
    fetch("http://127.0.0.1:5000/logout", {
      method: "GET",
      credentials: "include",
    })
      .then((response) => {
        if (response.ok) {
          localStorage.removeItem("authToken");
          this.$router.push("/");
        } else {
          alert(`Logout failed: ${response.status} ${response.statusText}`);
        }
      })
      .catch((error) => {
        alert(`Error during logout: ${error.message}`);
      });
  },
    },

    mounted() {
      this.fetchServiceTypes();
      this.fetchServices();
    },
  };
  </script>
  
  <style scoped>
/* General styles */
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Navbar styles */
.navbar {
  background-color: #1a202c;
  color: white;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  list-style-type: none;
  display: flex;
  gap: 15px;
  margin: 0;
  padding: 0;
}

.nav-links li {
  display: inline-block;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #63b3ed;
}

.logout-btn {
  background-color: #e53e3e;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #c53030;
}

/* Main content styles */
.main-content {
  padding: 20px;
}

.heading {
  color: #2d3748;
  text-align: center;
  margin-bottom: 20px;
}

.filter-section {
  margin-bottom: 20px;
  text-align: center;
}

.filter-label {
  font-weight: bold;
  margin-right: 10px;
}

.filter-select {
  padding: 5px;
  border: 1px solid #cbd5e0;
  border-radius: 5px;
}

/* Service card styles */
.services-section {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.service-card {
  background-color: #f7fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 15px;
  width: 300px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.service-title {
  color: #2c5282;
  font-size: 1.25em;
  margin-bottom: 10px;
}

.service-description {
  color: #4a5568;
  margin-bottom: 15px;
}

.service-price {
  font-weight: bold;
  color: #2f855a;
  margin-bottom: 20px;
}

.book-btn {
  background-color: #48bb78;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.book-btn:hover {
  background-color: #38a169;
}

/* No services available styles */
.no-services {
  text-align: center;
  color: #718096;
}
</style>
