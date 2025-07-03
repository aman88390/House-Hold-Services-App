<template>
  <div>
    <h1>My Service Requests</h1>

    <!-- Message Display -->
    <div v-if="message" class="message" :class="{'success': isSuccess, 'error': !isSuccess}">
      {{ message }}
    </div>

    <div v-if="serviceRequests.length">
      <table class="service-requests-table">
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Service Name</th>
            <th>Professional</th>
            <th>Date of Appointment</th>
            <th>Date of request</th>
            <th>Status</th>
            <th>Date of Completion</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in serviceRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.service_name }}</td>
            <td>{{ request.professional_name }}</td>
            <td>{{ request.date_of_appointment }}</td>
            <td>{{ request.date_of_request }}</td>
            <td>{{ request.service_status }}</td>
            <td>{{ request.date_of_completion || "Not completed yet" }}</td>
            <td>
              <!-- Edit Button -->
              <button
                v-if="request.service_status === 'requested'"
                @click="showEditForm(request)"
              >
                Edit
              </button>

              <!-- Delete Button -->
              <button
                v-if="['requested', 'rejected'].includes(request.service_status)"
                @click="deleteServiceRequest(request)"
              >
                Delete
              </button>

              <!-- Close Button -->
              <button
                v-if="request.service_status === 'assigned'"
                @click="showClosePopup(request)"
              >
                Close
              </button>

              <!-- Edit Form -->
              <div v-if="request.showEditForm">
                <label>
                  New Appointement Date:
                  <input type="date" v-model="request.editDate" :min="today" />
                </label>
                <label>
                  New Professional:
                  <select v-model="request.newProfessionalId">
                    <option v-for="professional in professionals" :key="professional.id" :value="professional.id">
                      {{ professional.name }}
                    </option>
                  </select>
                </label>
                <button @click="updateServiceRequest(request)">Save Changes</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>No service requests found.</p>
    </div>

    <!-- Close Service Popup -->
    <div v-if="showPopup" class="popup-overlay">
      <div class="popup-content">
        <h2>Close Service Request</h2>
        <p>Please provide a review and rating before closing this request.</p>
        <label>
          Review:
          <textarea v-model="review" rows="3"></textarea>
        </label>
        <label>
          Rating:
          <select v-model="rating">
            <option value="" disabled>Select rating</option>
            <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
          </select>
        </label>
        <div class="popup-buttons">
          <button @click="submitCloseRequest">Submit</button>
          <button @click="closePopup">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      serviceRequests: [],
      professionals: [],
      message: "",
      isSuccess: true,
      showPopup: false,
      selectedRequest: null,
      review: "",
      rating: "",
    };
  },
  computed: {
    today() {
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, "0");
      const day = String(today.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    },
  },
  methods: {
    setMessage(message, isSuccess = true) {
      this.message = message;
      this.isSuccess = isSuccess;
      setTimeout(() => {
        this.message = "";
      }, 5000);
    },
    getAuthToken() {
      return localStorage.getItem("authToken");
    },
    async fetchServiceRequests() {
      try {
        const token = this.getAuthToken();
        const response = await axios.get("http://127.0.0.1:5000/customer/service_requests", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.serviceRequests = response.data;
      } catch (error) {
        console.error("Error fetching service requests:", error);
        this.setMessage("Failed to load service requests.", false);
      }
    },
    async fetchProfessionals(serviceId) {
      try {
        const token = this.getAuthToken();
        const response = await axios.get(`http://127.0.0.1:5000/service/${serviceId}/professionals`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.professionals = response.data;
      } catch (error) {
        console.error("Error fetching professionals:", error);
        this.professionals = [];
      }
    },
    showEditForm(request) {
      request.showEditForm = true;
      request.editDate = request.date_of_request;
      request.newProfessionalId = request.professional_id;
      this.fetchProfessionals(request.service_id);
    },
    async updateServiceRequest(request) {
      try {
        const token = this.getAuthToken();
        await axios.put(
          `http://127.0.0.1:5000/customer/edit_service_requests/${request.id}`,
          {
            // date_of_request: request.editDate,
            date_of_request: request.editDate,
            professional_id: request.newProfessionalId,
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        request.date_of_request = request.editDate;
        request.professional_id = request.newProfessionalId;
        request.showEditForm = false;
        this.setMessage("Service request updated successfully.", true);
      } catch (error) {
        console.error("Error updating service request:", error);
        this.setMessage("Failed to update service request.", false);
      }
    },
    async deleteServiceRequest(request) {
      const token = this.getAuthToken();
      if (confirm("Are you sure you want to delete this service request?")) {
        try {
          await axios.delete(`http://127.0.0.1:5000/customer/delete_service_requests/${request.id}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          this.serviceRequests = this.serviceRequests.filter((r) => r.id !== request.id);
          this.setMessage("Service request deleted successfully.", true);
        } catch (error) {
          console.error("Error deleting service request:", error);
          this.setMessage("Failed to delete service request.", false);
        }
      }
    },
    showClosePopup(request) {
      this.showPopup = true;
      this.selectedRequest = request;
      this.review = "";
      this.rating = "";
    },
    closePopup() {
      this.showPopup = false;
      this.selectedRequest = null;
    },
    async submitCloseRequest() {
      if (!this.rating || !this.review) {
        alert("Please provide both a review and a rating.");
        return;
      }
      const token = this.getAuthToken();
      try {
        await axios.put(
          `http://127.0.0.1:5000/customer/service_requests/${this.selectedRequest.id}`,
          {
            status: "closed",
            review: this.review,
            rating: this.rating,
            date_of_completion: new Date().toISOString().slice(0, 10),
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.selectedRequest.service_status = "closed";
        this.selectedRequest.date_of_completion = new Date().toISOString().slice(0, 10);
        this.showPopup = false;
        this.setMessage("Service request closed successfully.", true);
      } catch (error) {
        console.error("Error closing service request:", error);
        this.setMessage("Failed to close service request.", false);
      }
    },
    formatDate(dateString) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
  },
  mounted() {
    this.fetchServiceRequests();
  },
};
</script>
<style>
/* General Table Styles */
.service-requests-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.service-requests-table th,
.service-requests-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

.service-requests-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

/* Message Styles */
.message {
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 4px;
  text-align: center;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

/* Button Styles */
button {
  padding: 8px 12px;
  font-size: 14px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:first-child {
  margin-right: 5px;
}

button:last-child {
  margin-left: 5px;
}

button.delete {
  background-color: #dc3545;
}

button.delete:hover {
  background-color: #a71d2a;
}

button.edit {
  background-color: #ffc107;
  color: #000;
}

button.edit:hover {
  background-color: #e0a800;
}

/* Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  z-index: 1100;
}

.popup-content h2 {
  font-size: 18px;
  margin-bottom: 15px;
}

.popup-content p {
  font-size: 14px;
  margin-bottom: 20px;
}

.popup-content label {
  display: block;
  font-size: 14px;
  margin-bottom: 10px;
}

.popup-content textarea,
.popup-content select {
  width: calc(100% - 20px);
  padding: 10px;
  margin: 10px auto;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.popup-buttons {
  display: flex;
  justify-content: space-around;
}

.popup-buttons button {
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 4px;
}

.popup-buttons button:first-child {
  background-color: #28a745;
}

.popup-buttons button:first-child:hover {
  background-color: #218838;
}

.popup-buttons button:last-child {
  background-color: #dc3545;
}

.popup-buttons button:last-child:hover {
  background-color: #c82333;
}

/* Responsive Design */
@media screen and (max-width: 768px) {
  .service-requests-table,
  .popup-content {
    font-size: 12px;
  }

  .popup-content {
    width: 90%;
    padding: 15px;
  }

  button {
    font-size: 12px;
    padding: 6px 10px;
  }
}

</style>