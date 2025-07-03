<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Admin Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            v-model="username"
            id="username"
            type="text"
            placeholder="Enter your username"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            v-model="password"
            id="password"
            type="password"
            placeholder="Enter your password"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/admin/login', {
          username: this.username,
          password: this.password,
        });

        const token = response.data.authToken;
        if (token) {
          localStorage.setItem('authToken', token);
          this.$router.push('/admin/dashboard');
        } else {
          this.errorMessage = 'Token not received from server.';
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.message || 'Login failed';
      }
    },
  },
};
</script>


<style scoped>
/* General Styling */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(to right, #5f0259, #6ea8fe); 
  font-family: "Roboto", sans-serif;
}

/* Login Card */
.login-card {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
  text-align: center;
}

.login-card h2 {
  margin-bottom: 20px;
  color: #333; 
  font-size: 1.8rem;
}

/* Form Styling */
.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555; 
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus {
  border-color: #0056b3; 
  outline: none;
  box-shadow: 0 0 4px rgba(0, 86, 179, 0.3);
}

/* Button Styling */
.btn {
  display: inline-block;
  padding: 10px 20px;
  font-size: 1rem;
  color: white;
  background-color: #0056b3; 
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #004494; 
}

/* Error Message */
.error {
  margin-top: 15px;
  color: #d9534f; 
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 500px) {
  .login-card {
    padding: 20px;
  }

  .login-card h2 {
    font-size: 1.5rem;
  }

  .form-group input {
    font-size: 0.9rem;
  }
}
</style>
