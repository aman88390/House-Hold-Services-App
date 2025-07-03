<template>
  <div class="register">
    <h1>Register</h1>
    <form @submit.prevent="registerUser">
      <label for="username">Username:</label>
      <input type="text" v-model="form.username" required />
      <label for="name">Name:</label>
      <input type="text" v-model="form.name" required />

      <label for="email">Email:</label>
      <input type="email" v-model="form.email" required />

      <label for="password">Password:</label>
      <input type="password" v-model="form.password" required />

      <label for="role">Role:</label>
      <select v-model="form.role" required>
        <option value="customer">Customer</option>
        <option value="professional">Professional</option>
      </select>

      <div v-if="form.role === 'professional'">
        <label for="service_id">Select Service:</label>
        <select v-model="form.service_id" required>
          <option v-for="service in services" :key="service.id" :value="service.id">
            {{ service.name }}
          </option>
        </select>
        
        <label for="experience">Experience:</label>
        <input type="number" v-model="form.experience" required />
      </div>

      <label for="phone">Phone:</label>
      <input type="text" v-model="form.phone"  />

      <label for="address">Address:</label>
      <input type="text" v-model="form.address"  />

      <label for="pin_code">Pin Code:</label>
      <input type="text" v-model="form.pin_code"  />

      <button type="submit">Register</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Register",
  data() {
    return {
      form: {
        username: "",
        name:"",
        email: "",
        password: "",
        role: "customer",
        service_id: null,
        experience: "",
        phone: "",
        address: "",
        pin_code: "",
      },
      services: [],
      message: "",
    };
  },
  methods: {
    async experience_cannot_be_negative() {
      if (this.form.role === "professional" && this.form.experience < 0) {
        this.message = "Experience cannot be negative.";
        return;
      }

    },
    async fetchServices() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/get_services");
        this.services = response.data;
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    async registerUser() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/register", this.form);
        this.message = response.data.message;
      } catch (error) {
        this.message = error.response.data.message || "Registration failed.";
      }
    },
  },
  watch: {
    "form.experience"(value) {
      if (value < 0) {
        this.form.experience = "";
        this.message = "Experience cannot be negative.";
      }
    },
  },
  mounted() {
    this.fetchServices();
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
}
.template {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #ba2793;
}

.register {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px
}
.form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column; 
}
label {
  margin-bottom: 5px;
  font-weight: bold;
}
input, select, button {
  padding: 8px;
  font-size: 14px;
  width: 100%;
  box-sizing: border-box;
}
button {
  background-color: #007bff;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 10px;
}

button:hover {
  background-color: #0056b3;
}

</style>
