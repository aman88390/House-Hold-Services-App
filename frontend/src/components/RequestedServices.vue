<template>
    <div>
      <h2>Service Requests</h2>
  
      <!-- Filters for service requests (optional) -->
      <div>
        <label for="status">Status:</label>
        <select v-model="statusFilter">
          <option value="">All</option>
          <option value="requested">Requested</option>
          <option value="assigned">Assigned</option>
          <option value="closed">Closed</option>
        </select>
  
        <label for="service_id">Service:</label>
        <input type="number" v-model="serviceIdFilter" placeholder="Service ID" />
  
        <label for="customer_id">Customer:</label>
        <input type="number" v-model="customerIdFilter" placeholder="Customer ID" />
  
        <button @click="fetchServiceRequests">Fetch Service Requests</button>
      </div>
  
      <!-- Display the list of service requests in a table -->
      <div v-if="serviceRequests.length > 0">
        <h3>Service Requests</h3>
        <table>
          <thead>
            <tr>
              <th>Service Name</th>
              <th>Customer Name</th>
              <th>Professional</th>
              <th>Status</th>
              <th>Requested On</th>
              <th>Remarks</th>
              <th>Completed On</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in serviceRequests" :key="request.id">
              <td>{{ request.service_name }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.professional_name }} </td>
              <td>{{ request.service_status }}</td>
              <td>{{ request.date_of_request }}</td>
              <td>{{ request.remarks || 'No remarks' }}</td>
              <td>{{ request.date_of_completion || 'Not completed yet' }}</td>
              <td>
                <button @click="editServiceRequest(request)">Edit</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>No service requests found.</p>
      </div>
  
      <!-- Edit Service Request Modal -->
      <div v-if="showEditModal" class="modal">
        <div class="modal-content">
          <h3>Edit Service Request</h3>
          <form @submit.prevent="updateServiceRequest">
            <div>
              <label for="professional_id">Select Professional:</label>
              <select v-model="updatedRequest.professional_id" id="professional_id" required>
                <option v-for="professional in professionals" :key="professional.id" :value="professional.id">
                  {{ professional.name }}- {{ professional.service }}

                </option>
              </select>
            </div>
  
            <div>
              <label for="service_status">Service Status:</label>
              <select v-model="updatedRequest.service_status" id="service_status" required>
                <option value="assigned">Assigned</option>
                <option value="closed">Closed</option>
              </select>
            </div>
            <
  
            <div v-if="updatedRequest.service_status === 'closed'">
              <label for="date_of_completion">Date of Completion:</label>
              <input type="datetime-local" v-model="updatedRequest.date_of_completion" id="date_of_completion" required />
            </div>
  
            <button type="submit">Update Service Request</button>
            <button @click="closeModal">Cancel</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        serviceRequests: [],
        statusFilter: '', 
        serviceIdFilter: '', 
        customerIdFilter: '', 
        showEditModal: false, 
        updatedRequest: {}, 
        professionals: [], 
        authToken: localStorage.getItem('authToken') || '', 
      };
    },
    methods: {
      async fetchServiceRequests() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/api/service_requests', {
            params: {
              status: this.statusFilter,
              service_id: this.serviceIdFilter,
              customer_id: this.customerIdFilter,
            },
            headers: {
              Authorization: `Bearer ${this.authToken}`,
            },
          });
          this.serviceRequests = response.data;
        } catch (error) {
          console.error('Error fetching service requests:', error);
        }
      },
  
      // Fetch professionals list for the modal dropdown
      async fetchProfessionals() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/admin/verified-professionals', {
            headers: {
              Authorization: `Bearer ${this.authToken}`,
            },
          });
          this.professionals = response.data;
        } catch (error) {
          console.error('Error fetching professionals:', error);
        }
      },
  
      editServiceRequest(request) {
        this.updatedRequest = { ...request };
        this.showEditModal = true; 
        this.fetchProfessionals(); 
      },
      async updateServiceRequest() {
        try {
          const payload = {
            professional_id: this.updatedRequest.professional_id,
            service_status: this.updatedRequest.service_status,
            date_of_completion: this.updatedRequest.date_of_completion || null,
          };
  
          await axios.put(
            `http://127.0.0.1:5000/api/service_requests/${this.updatedRequest.id}/assign`,
            payload,
            {
              headers: {
                Authorization: `Bearer ${this.authToken}`,
              },
            }
          );
  
          this.showEditModal = false; 
          this.fetchServiceRequests(); 
        } catch (error) {
          console.error('Error updating service request:', error);
        }
      },
  
      closeModal() {
        this.showEditModal = false;
      },
    },
    mounted() {
      this.fetchServiceRequests();
    },
  };
  </script>
  
  <style scoped>

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  th, td {
    padding: 10px;
    text-align: left;
    border: 1px solid #ddd;
  }
  
  th {
    background-color: #f4f4f4;
  }
  
  tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  
  tr:hover {
    background-color: #f1f1f1;
  }
  
  button {
    padding: 6px 12px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  /* Modal styling */
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 4px;
    width: 400px;
  }
  
  .modal-content input,
  .modal-content select {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
  }
  
  .modal-content button {
    width: 48%;
    margin-right: 4%;
  }
  
  .modal-content button:last-child {
    margin-right: 0;
  }
  </style>
  