<template>
  <div id="home">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="navbar-brand">Household Services</div>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/services">Services</router-link></li>
        <li><router-link to="/contact">Contact Us</router-link></li>
        <!-- <li><router-link to="/about">About</router-link></li> -->
        <li><router-link to="/login">Login</router-link></li>
        <li><a @click="navigateTo('AdminLogin')" class="hidden-link">Admin Login</a></li>
      </ul>
    </nav>

    <!-- Hero Section -->
    <header class="hero-section">
      <div class="hero-content">
        <h1>Welcome to Household Services</h1>
        <p>We make your household chores easier, faster, and stress-free.</p>
        <div class="cta-buttons">
          <router-link to="/services" class="btn btn-primary">Explore Services</router-link>
          <router-link to="/contact" class="btn btn-secondary">Get in Touch</router-link>
        </div>
      </div>
    </header>

    <!-- Quotes Section -->
    <section class="quotes-section">
      <div class="quote">
        <blockquote>
          "A well-maintained home is the foundation of a happy life."
        </blockquote>
        <p>- Anonymous</p>
      </div>
      <div class="quote">
        <blockquote>
          "Quality is never an accident; it is always the result of intelligent effort."
        </blockquote>
        <p>- John Ruskin</p>
      </div>
    </section>
  </div>
</template>


<script>
export default {
  name: "Home",
  methods: {
    navigateTo(routeName) {
      this.$router.push({ name: routeName });
    }
  }
};
</script>

<style scoped>
/* General Styling */
#home {
  font-family: "Roboto", sans-serif;
  color: #333;
  line-height: 1.6;
}

/* Navigation Bar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1e00b3;
  padding: 15px 20px;
  color: white;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.navbar ul {
  list-style: none;
  display: flex;
  gap: 20px;
  margin: 0;
  padding: 0;
}

.navbar li a {
  color: rgb(255, 255, 255);
  text-decoration: none;
  font-size: 1rem;
  padding: 10px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.navbar li a:hover {
  background-color: #004494;
}

.hidden-link {
  cursor: pointer;

}

/* Hero Section */
.hero-section {
  background: linear-gradient(to bottom, #333436, #45474b);
  color: white;
  padding: 50px 20px;
  text-align: center;
  animation: fadeIn 1s ease-in-out;
}

.hero-content {
  max-width: 600px;
  margin: 0 auto;
}

.hero-content h1 {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 25px;
}

.cta-buttons .btn {
  margin: 5px;
}

/* Quotes Section */
.quotes-section {
  padding: 40px 20px;
  background-color: #48bada;
  text-align: center;
}

.quotes-section .quote {
  margin-bottom: 20px;
}

.quotes-section blockquote {
  font-size: 1.5rem;
  font-style: italic;
  margin: 0 auto 10px;
  color: #258766;
  max-width: 600px;
}

.quotes-section p {
  font-size: 1rem;
  color: #777;
}

/* Buttons */
.btn {
  display: inline-block;
  font-size: 1rem;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background-color: #0056b3;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #004494;
}

.btn-secondary {
  background-color: #6ea8fe;
  color: white;
  border: none;
}

.btn-secondary:hover {
  background-color: #0056b3;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
