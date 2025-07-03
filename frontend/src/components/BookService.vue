<template>
  <div class="container">
    <h1>Available Professionals</h1>
    <div v-if="professionals.length" class="professionals-grid">
      <div
        v-for="professional in professionals"
        :key="professional.id"
        class="professional-card"
      >
        <h3>{{ professional.name }}</h3>
        <p><strong>Experience:</strong> {{ professional.experience }} years</p>
        <p><strong>Average Rating:</strong> {{ professional.average_rating }}</p>
        <label class="appointment-label">
          Date of Appointment:
          <input
            type="date"
            v-model="professional.dateOfRequest"
            class="date-picker"
            :min="todayDate"
          />
        </label>
        <button class="book-button" @click="bookService(professional.id)">
          Book This Professional
        </button>
      </div>
    </div>
    <div v-else class="no-professionals">
      <p>No professionals available for this service.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: ["serviceId"],
  data() {
    return {
      professionals: [], 
      todayDate: this.getTodayDate(), 
    };
  },
  methods: {
    async fetchProfessionals() {
      try {
        const token = this.getAuthToken();
        const response = await axios.get(
          `http://127.0.0.1:5000/service/${this.serviceId}/professionals`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        this.professionals = response.data.map((professional) => ({
          ...professional,
          dateOfRequest: null, 
        }));
      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    },

    getAuthToken() {
      return localStorage.getItem("authToken"); 
    },

    getTodayDate() {
      const today = new Date();
      const dd = String(today.getDate()).padStart(2, "0");
      const mm = String(today.getMonth() + 1).padStart(2, "0"); 
      const yyyy = today.getFullYear();
      return `${yyyy}-${mm}-${dd}`;
    },

    async bookService(professionalId) {
      try {
        const token = this.getAuthToken();
        const professional = this.professionals.find(
          (p) => p.id === professionalId
        );

        if (!professional || !professional.dateOfRequest) {
          alert("Please select a date before booking.");
          return;
        }

        const response = await axios.post(
          "http://127.0.0.1:5000/service_request",
          {
            service_id: this.serviceId,
            professional_id: professionalId,
            date_of_request: professional.dateOfRequest, 
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.status === 201) {
          alert(response.data.message || "Service booked successfully!");
        } else {
          alert(response.data.message || "Unexpected response from the server.");
        }
      } catch (error) {
        if (error.response && error.response.data) {
          alert(error.response.data.message || "Failed to book the service.");
        } else {
          alert("An error occurred while booking the service.");
        }
        console.error("Error booking service:", error);
      }
    },
  },
  mounted() {
    this.fetchProfessionals(); 
  },
};
</script>

<style scoped>
.container {
  font-family: "Arial", sans-serif;
  background-color: #f9fafc;
  color: #333;
  padding: 20px;
  margin: 0 auto;
  max-width: 900px;
}

h1 {
  text-align: center;
  font-size: 28px;
  color: #004aad;
  margin-bottom: 20px;
}

.professionals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.professional-card {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.professional-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.professional-card h3 {
  font-size: 20px;
  color: #004aad;
  margin-bottom: 10px;
}

.professional-card p {
  font-size: 16px;
  color: #555;
  margin: 5px 0;
}

.appointment-label {
  display: block;
  font-weight: bold;
  margin-top: 15px;
  color: #333;
}

.date-picker {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.book-button {
  margin-top: 15px;
  background-color: #2a9d8f;
  color: #ffffff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.book-button:hover {
  background-color: #21867a;
}

.no-professionals {
  text-align: center;
  color: #ff4d4d;
  font-size: 18px;
}
</style>
