<template>
  <div>
    <!-- Navigation Bar -->
    <nav>
      <div class="logo">
        <span>ProDashboard</span>
      </div>
      <div class="links">
        <router-link to="" class="nav-link">Dashboard</router-link>
        <router-link to="" class="nav-link">Profile</router-link>
        <router-link to="/closed_services" class="nav-link">Closed Services</router-link>
        <button class="nav-link" @click="logout">Logout</button>
      </div>
    </nav>

    <!-- Dashboard Content -->
    <div class="dashboard">
      <h1>{{ message }}</h1>
    </div>

    <!-- Service Requests Section -->
    <div class="service-requests">
      <h2>Service Requests</h2>
      <div class="table-container">
        <table class="service-requests-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Service Name</th>
              <th>Customer Name</th>
              <th>Contact</th>
              <th>Address</th>
              <th>Pin Code</th>
              <th>Date of Request</th>
              <th>Date of Completion</th>
              <th>Status</th>
              <th>Rating</th>
              <th>Review</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in serviceRequests" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.service_name }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.customer_contact_number }}</td>
              <td>{{ request.customer_address }}</td>
              <td>{{ request.customer_pin_code }}</td>
              <td>{{ request.date_of_request }}</td>
              <td>{{ request.date_of_completion || 'N/A' }}</td>
              <td>
                <span :class="`status-badge ${request.service_status}`">
                  {{ request.service_status }}
                </span>
              </td>
              <td>{{ request.rating || 'No rating' }}</td>
              <td>{{ request.review }}</td>
              <td>
                <div v-if="request.service_status === 'requested'">
                  <button
                    @click="updateServiceRequestStatus(request.id, 'assigned')"
                  >
                    Assign
                  </button>
                  <button
                    @click="updateServiceRequestStatus(request.id, 'rejected')"
                  >
                    Reject
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";

export default {
  data() {
    return {
      message: "",
      serviceRequests: [],
    };
  },
  created() {
    this.fetchDashboardData();
    this.fetchServiceRequests();
  },
  methods: {
    async fetchDashboardData() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/professional/dashboard",
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("authToken")}`,
            },
          }
        );
        this.message = response.data.message || "Dashboard data not available";
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
        this.message = "Error fetching data from the server.";
      }
    },

    async fetchServiceRequests() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/service_requests_for_professionals",
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("authToken")}`,
            },
          }
        );
        this.serviceRequests = response.data;
      } catch (error) {
        console.error("Error fetching service requests:", error);
        this.serviceRequests = [];
      }
    },

    async updateServiceRequestStatus(serviceId, newStatus) {
      try {
        const response = await axios.put(
          `http://127.0.0.1:5000/professional/service_requests/${serviceId}`,
          { service_status: newStatus },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("authToken")}`,
            },
          }
        );

        if (response.status === 200) {
          alert(
            `Service request ${serviceId} updated successfully to ${newStatus}.`
          );
          this.fetchServiceRequests();
        }
      } catch (error) {
        console.error(`Error updating service request ${serviceId}:`, error);
        if (error.response && error.response.data.message) {
          alert(`Error: ${error.response.data.message}`);
        } else {
          alert("Failed to update service request. Please try again later.");
        }
      }
    },
    logout() {
  
  fetch("http://127.0.0.1:5000/logout", {
    method: "GET", 
    credentials: "include", 
  })
    .then(response => {
      if (response.ok) {
        localStorage.removeItem("authToken");
        this.$router.push("/");
      } else {
        alert(`Logout failed: ${response.status} ${response.statusText}`);
      }
    })
    .catch(error => {
      alert(`Error during logout: ${error.message}`);
    });
}
  },
};
</script>
<style scoped>
/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Arial", sans-serif;
}

/* Navigation Bar */
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #3b5998, #8b9dc3);
  padding: 20px;
  color: white;
  position: sticky;
  top: 0;
  z-index: 10;
}

nav .logo {
  font-size: 1.5em;
  font-weight: bold;
  color: white;
}

nav .links {
  display: flex;
}

nav .nav-link {
  margin-left: 20px;
  text-decoration: none;
  color: white;
  font-weight: bold;
  transition: color 0.3s ease;
}

nav .nav-link:hover {
  color: #f1c40f;
}

/* Dashboard */
.dashboard {
  padding: 40px;
  text-align: center;
  background: #f4f7f6;
  border-bottom: 2px solid #ddd;
}

.dashboard h1 {
  color: #2c3e50;
  font-size: 2em;
  margin-bottom: 20px;
}

/* Service Requests */
.service-requests {
  padding: 40px;
  background: #e6f7ff;
  border-radius: 10px;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
}

.service-requests h2 {
  font-size: 1.8em;
  color: #00796b;
  margin-bottom: 20px;
  text-align: center;
}

/* Table */
.table-container {
  overflow-x: auto;
}

.service-requests-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.service-requests-table th,
.service-requests-table td {
  text-align: left;
  padding: 12px 15px;
  border: 1px solid #ddd;
}

.service-requests-table th {
  background-color: #00796b;
  color: white;
}

.service-requests-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.service-requests-table tr:hover {
  background-color: #f1f1f1;
}

/* Status Badge */
.status-badge {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 8px;
  font-size: 0.9em;
  color: white;
}

.status-badge.requested {
  background-color: #ffa726;
}

.status-badge.assigned {
  background-color: #29b6f6;
}

.status-badge.closed {
  background-color: #66bb6a;
}

.status-badge.rejected {
  background-color: #ef5350;
}

/* Buttons */
button {
  background-color: #0288d1;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.3s ease;
  margin: 2px;
}

button:hover {
  background-color: #0277bd;
}

button:last-child {
  background-color: #d32f2f;
}

button:last-child:hover {
  background-color: #c62828;
}
</style>
