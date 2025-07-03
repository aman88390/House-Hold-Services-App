<template>
    <div>
      <h1>All Service Requests</h1>
      <table class="service-requests-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Service Name</th>
            <th>Professional Name</th>
            <th>Customer Name</th>
            <th>Date of Request</th>
            <th>Service Status</th>
            <th>Date of Completion</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in serviceRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.service_name }}</td>
            <td>{{ request.professional_name }}</td>
            <td>{{ request.customer_name }}</td>
            <td>{{ formatDate(request.date_of_request) }}</td>
            <td>{{ request.service_status }}</td>
            <td>{{ formatDate(request.date_of_completion) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        serviceRequests: [],  
      };
    },
    mounted() {
      this.fetchServiceRequests();  
    },
    methods: {
      async fetchServiceRequests() {
        try {
          const response = await axios.get(
            "http://127.0.0.1:5000/admin_all_services_requests",
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("authToken")}`,  
              },
            }
          );
          this.serviceRequests = response.data;  
        } catch (error) {
          console.error("Error fetching service requests:", error);
          alert("An error occurred while fetching service requests.");
        }
      },
      formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString("en-US"); 
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add basic table styling */
  table.service-requests-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    padding: 20%;
  }
  
  table.service-requests-table th,
  table.service-requests-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  table.service-requests-table th {
    background-color: #f4f4f4;
  }
  </style>
  