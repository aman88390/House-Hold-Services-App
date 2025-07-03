<template>
    <div>
      <header class="header">
        <h1>Closed Service Requests</h1>
      </header>
      <div class="service-requests">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Service Name</th>
              <th>Customer Name</th>
              <th>Contact</th>
              <th>Address</th>
              <th>Pin Code</th>
              <th>Date of Appointement</th>
              <th>Completion Date</th>
              <th>Rating</th>
              <th>Review</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in closedServiceRequests" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.service_name }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.customer_contact_number }}</td>
              <td>{{ request.customer_address }}</td>
              <td>{{ request.customer_pin_code }}</td>
              <td>{{ request.date_of_request }}</td>
              <td>{{ request.date_of_completion || 'N/A' }}</td>
              <td>{{ request.rating || 'No rating' }}</td>
              <td>{{ request.review || 'No review' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "ClosedServiceRequests",
    data() {
      return {
        closedServiceRequests: [], 
      };
    },
    created() {
      this.fetchClosedServiceRequests(); 
    },
    methods: {
      async fetchClosedServiceRequests() {
        try {
          const response = await axios.get("http://127.0.0.1:5000/closed_service", {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("authToken")}`,
            },
          });
          this.closedServiceRequests = response.data || [];
        } catch (error) {
          console.error("Error fetching closed service requests:", error);
          this.closedServiceRequests = [];
        }
      },
    },
  };
  </script>

<style scoped>
/* Global Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Roboto", sans-serif;
}

/* Page Header */
.header {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #4a90e2, #50c9c3);
  color: white;
  border-radius: 8px;
  margin-bottom: 20px;
}

.header h1 {
  font-size: 2em;
  font-weight: bold;
}

/* Table Container */
.table-container {
  padding: 20px;
  background: #f4f6f8;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 90%;
  margin: 0 auto;
  overflow-x: auto;
}

/* Table Styles */
table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
}

thead {
  background: purple;
  color: white;
}

th,
td {
  text-align: left;
  padding: 12px 15px;
}

th {
  font-size: 0.9em;
  font-weight: bold;
  text-transform: uppercase;
}

td {
  color: #333;
  font-size: 0.95em;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1faff;
}

td:first-child,
th:first-child {
  border-radius: 8px 0 0 8px;
}

td:last-child,
th:last-child {
  border-radius: 0 8px 8px 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  th,
  td {
    font-size: 0.85em;
  }

  .header h1 {
    font-size: 1.5em;
  }
}

/* Additional Styling */
.table-container {
  animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
