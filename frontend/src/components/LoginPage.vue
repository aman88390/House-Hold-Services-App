<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Welcome Back!</h2>
      <p class="login-subtitle">Log in to continue</p>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            placeholder="Enter your username"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            placeholder="Enter your password"
          />
        </div>
        
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
      
      <div class="register-redirect">
        <p>Don't have an account? <span @click="redirectToRegister" class="register-link">Register here</span></p>
      </div>
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
      errorMessage: ''
    };
  },
  methods: {
    async handleLogin() {
      this.errorMessage = ''; 

      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          username: this.username,
          password: this.password
        });

        if (response.data.authToken) {
          localStorage.setItem('authToken', response.data.authToken);
          this.$router.push(response.data.redirect || '/dashboard');
        } else {
          this.errorMessage = response.data.message || 'Login failed.';
        }
      } catch (error) {
        this.errorMessage = 'An error occurred. Please try again later.';
      }
    },
    redirectToRegister() {
      this.$router.push('/register');
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(to bottom right, #f8f9fa, #dee2e6); 
  font-family: 'Roboto', sans-serif;
}

/* Login Card */
.login-card {
  background-color: #ffffff; 
  padding: 40px 30px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-card h2 {
  color: #343a40;
  margin-bottom: 10px;
  font-size: 2rem;
}

.login-subtitle {
  color: #6c757d; 
  margin-bottom: 20px;
  font-size: 1rem;
}


.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #495057;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-group input:focus {
  border-color: #74c0fc; 
  box-shadow: 0 0 8px rgba(116, 192, 252, 0.5);
  outline: none;
}

.error-message {
  color: #e03131; /* Red */
  font-size: 0.9rem;
  margin-bottom: 10px;
}


.btn {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background-color: #339af0;
  color: white;
}

.btn-primary:hover {
  background-color: #1c7ed6; 
}

.btn-secondary {
  background-color: #adb5bd; 
  color: white;
  margin-top: 10px;
}

.btn-secondary:hover {
  background-color: #868e96;
}


.register-redirect {
  margin-top: 20px;
  font-size: 0.9rem;
  color: #6c757d; 
}

.register-link {
  color: #339af0;
  font-weight: bold;
  cursor: pointer;
}

.register-link:hover {
  text-decoration: underline;
}


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
