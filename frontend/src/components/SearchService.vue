<template>
  <div class="search-services">
    <h1>Search Services</h1>

    <!-- Search Form -->
    <form @submit.prevent="searchServices">
      <div>
        <label for="keyword">Keyword:</label>
        <input
          v-model="keyword"
          type="text"
          id="keyword"
          placeholder="Enter keyword (e.g., service name, address, pin code)"
        />
      </div>
      <button type="submit">Search</button>
    </form>

    <!-- Results Section -->
    <div v-if="services.length" class="results">
      <h2>Results:</h2>
      <div v-for="service in services" :key="service.id" class="service">
        <h3>{{ service.name }}</h3>
        <p>{{ service.description }}</p>
        <p><strong>Base Price:</strong> ₹{{ service.base_price }}</p>

        <div v-if="service.professional">
          <h4>Professional:</h4>
          <p><strong>Name:</strong> {{ service.professional.name }}</p>
          <p><strong>Address:</strong> {{ service.professional.address }}</p>
          <p><strong>Pin Code:</strong> {{ service.professional.pin_code }}</p>
          <p><strong>Experience:</strong> {{ service.professional.experience }} years</p>
        </div>
        <div v-else>
          <p>No professional available for this service.</p>
        </div>

        <!-- Book Now Button -->
        <button @click="openBookingModal(service)">Book Now</button>
      </div>
    </div>

    <div v-else-if="searchPerformed">
      <p>No services found matching your keyword.</p>
    </div>

    <!-- Booking Modal -->
    <div v-if="showBookingModal" class="modal">
      <div class="modal-content">
        <h3>Book Appointment</h3>
        <p><strong>Service:</strong> {{ selectedService.name }}</p>
        <p><strong>Professional:</strong> {{ selectedService.professional?.name || "N/A" }}</p>

        <div>
          <label for="appointment-date">Appointment Date:</label>
          <input
            type="date"
            id="appointment-date"
            v-model="appointmentDate"
            :min="todayDate"
          />
        </div>

        <div class="modal-actions">
          <button @click="bookAppointment">Book</button>
          <button @click="closeBookingModal">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SearchServices",
  data() {
    return {
      keyword: "",
      services: [],
      searchPerformed: false,
      showBookingModal: false,
      selectedService: "",
      appointmentDate: "",
      todayDate: this.getTodayDate(),
    };
  },
  methods: {
    getAuthToken() {
      return localStorage.getItem('authToken'); 
    },

  
    getTodayDate() {
      const today = new Date();
      const dd = String(today.getDate()).padStart(2, '0');
      const mm = String(today.getMonth() + 1).padStart(2, '0'); 
      const yyyy = today.getFullYear();
      return `${yyyy}-${mm}-${dd}`;
    },
    async searchServices() {
      this.searchPerformed = false;

      try {
        const response = await axios.get("http://127.0.0.1:5000/search-services", {
          params: { keyword: this.keyword },
          headers: {
            'Authorization': `Bearer ${this.getAuthToken()}`, 
          },
        });

        this.services = response.data.services;
        this.searchPerformed = true;
      } catch (error) {
        console.error("Error fetching services:", error);
        alert("An error occurred while searching for services. Please try again later.");
      }
    },

    // Open booking modal
    openBookingModal(service) {
      this.selectedService = service;
      this.showBookingModal = true;
    },

    // Close booking modal
    closeBookingModal() {
      this.showBookingModal = false;
      this.selectedService = "";
      this.appointmentDate = "";
    },

    // Book the appointment
    async bookAppointment() {
      if (!this.appointmentDate) {
        alert("Please select an appointment date.");
        return;
      }

      try {
        const response = await axios.post("http://127.0.0.1:5000/service_request", {
          professional_id: this.selectedService.professional?.id || null,
          service_id: this.selectedService.id,
          date_of_request: this.appointmentDate,
        }, {
          headers: {
            'Authorization': `Bearer ${this.getAuthToken()}`, // Include token in header
          },
        });

        alert(response.data.message || "Appointment booked successfully!");
        this.closeBookingModal();
      } catch (error) {
        console.error("Error booking appointment:", error);
        alert("An error occurred while booking the appointment. Please try again later.");
      }
    },
  },
};
</script>

<style>
.search-services {
  max-width: 600px;
  margin: auto;
}

form {
  margin-bottom: 20px;
}

form div {
  margin-bottom: 10px;
}

button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.results {
  margin-top: 20px;
}

.service {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 300px;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}
</style>
