<template>
  <div class="admin-dashboard">
    <!-- Admin Navigation Bar -->
    <nav class="admin-navbar">
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/admin_chart">Summary</router-link></li>
        <li><router-link to="/admin/manage_services1">Manage Services</router-link></li>
        <li><router-link to="/view_all_requests">Requested Services</router-link></li>
        <li><router-link to="/admin/manage_users">Manage Users</router-link></li>
        <li>
            <button @click="create_csv"> Export CSV </button>
        </li>
        <li><button @click="logout">Logout</button></li>
      </ul>
    </nav>

    <!-- Dashboard Content -->
    <section class="dashboard-content">
      <h2>Welcome, Admin!</h2>
      <p>This is your dashboard where you can manage the application.</p>

      <!-- Sections for Managing Services and Users -->
      <div class="dashboard-sections">
        <div class="section">
          <h3>Manage Services</h3>
          <p>View and update available services.</p>
          <router-link to="/admin/manage_services1">
            <button>Go to Manage Services</button>
          </router-link>
        </div>
        <div class="section">
          <h3>Manage Users</h3>
          <p>View and manage registered users.</p>
          <router-link to="/admin/manage_users">
            <button>Go to Manage Users</button>
          </router-link>
        </div>
      </div>

      <!-- Button to Fetch Unverified Professionals -->
      <div class="unverified-section">
        <h3>Professional Verification</h3>
        <p>View unverified professionals and verify them as needed.</p>
        <button @click="toggleUnverifiedProfessionals" class="fetch-button">
          {{ showUnverified ? "Hide" : "Show" }} Unverified Professionals
        </button>

        <!-- Display list of unverified professionals in a table -->
        <table v-if="showUnverified && unverifiedProfessionals.length > 0" class="unverified-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Experience</th>
              <th>Skills</th>
              <th>Service</th>
              <th>Phone</th>
              <th>Address</th>
              <th>Pin Code</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="professional in unverifiedProfessionals" :key="professional.id">
              <td>{{ professional.name }}</td>
              <td>{{ professional.experience }} years</td>
              <td>{{ professional.skills }}</td>
              <td>{{ professional.service }}</td>
              <td>{{ professional.phone }}</td>
              <td>{{ professional.address }}</td>
              <td>{{ professional.pin_code }}</td>
              <td>
                <button @click="verifyProfessional(professional.id)">Verify</button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Message if no unverified professionals are found -->
        <div v-else-if="unverifiedLoaded && showUnverified && unverifiedProfessionals.length === 0">
          <p>No unverified professionals at the moment.</p>
        </div>

        <!-- Error message if fetching data fails -->
        <div v-if="fetchError" class="error-message">
          <p>Error fetching data: {{ fetchError }}</p>
        </div>
      </div>

      <!-- Verified Professionals Section -->
      <div class="verified-section">
        <h3>Verified Professionals</h3>
        <p>View verified professionals and unverify them as needed.</p>
        <button @click="toggleVerifiedProfessionals" class="fetch-button">
          {{ showVerified ? "Hide" : "Show" }} Verified Professionals
        </button>

        <!-- Display list of verified professionals in a table -->
        <table v-if="showVerified && verifiedProfessionals.length > 0" class="verified-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Experience</th>
              <th>Skills</th>
              <th>Service</th>
              <th>Phone</th>
              <th>Address</th>
              <th>Pin Code</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="professional in verifiedProfessionals" :key="professional.id">
              <td>{{ professional.name }}</td>
              <td>{{ professional.experience }} years</td>
              <td>{{ professional.skills }}</td>
              <td>{{ professional.service }}</td>
              <td>{{ professional.phone }}</td>
              <td>{{ professional.address }}</td>
              <td>{{ professional.pin_code }}</td>
              <td>
                <button @click="unverifyProfessional(professional.id)">Unverify</button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Message if no verified professionals are found -->
        <div v-else-if="verifiedLoaded && showVerified && verifiedProfessionals.length === 0">
          <p>No verified professionals at the moment.</p>
        </div>

        <!-- Error message if fetching data fails -->
        <div v-if="fetchError" class="error-message">
          <p>Error fetching data: {{ fetchError }}</p>
        </div>
      </div>

    </section>
  </div>
</template>

<script>
export default {
  name: "AdminDashboard",
  data() {
    return {
      unverifiedProfessionals: [],
      verifiedProfessionals: [],
      unverifiedLoaded: false,
      verifiedLoaded: false,
      fetchError: null,
      showUnverified: false,
      showVerified: false,
    };
  },
  methods: {
    async create_csv(){
            const res = await fetch( 'http://127.0.0.1:5000/export_csv', {
              headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
            'Content-Type': 'application/json',
          }
            })
            const task_id = (await res.json()).task_id

            const interval = setInterval(async() => {
                // const res = await fetch(`http://127.0.0.1:5000/get_export_csv/${task_id}` )
                if (res.ok){
                    console.log('data is ready')
                    window.open(`http://127.0.0.1:5000/get_export_csv/${task_id}`)
                    clearInterval(interval)
                }

            }, 100)
            
        },
    
    async fetchProfessionals() {
      this.fetchError = null; 
      try {
        const token = localStorage.getItem("authToken"); 
        console.log("Token from localStorage:", token);  

      if (!token) {
        console.error("No token found in localStorage");
        return;
      } 
        const headers = {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        };

        const responseUnverified = await fetch('http://127.0.0.1:5000/admin/unverified-professionals', { headers });
        const responseVerified = await fetch('http://127.0.0.1:5000/admin/verified-professionals', { headers });

        if (responseUnverified.ok && responseVerified.ok) {
          this.unverifiedProfessionals = await responseUnverified.json();
          this.verifiedProfessionals = await responseVerified.json();
          this.unverifiedLoaded = true;
          this.verifiedLoaded = true;
        } else {
          this.fetchError = `Failed to fetch: ${responseUnverified.status} ${responseUnverified.statusText}`;
        }
      } catch (error) {
        this.fetchError = `Error fetching professionals: ${error.message}`;
      }
    },

    toggleUnverifiedProfessionals() {
      if (this.showUnverified) {
        this.showUnverified = false;
        this.unverifiedProfessionals = [];
        this.unverifiedLoaded = false;
      } else {
        this.showUnverified = true;
        this.fetchProfessionals();
      }
    },

    toggleVerifiedProfessionals() {
      if (this.showVerified) {
        this.showVerified = false;
        this.verifiedProfessionals = [];
        this.verifiedLoaded = false;
      } else {
        this.showVerified = true;
        this.fetchProfessionals();
      }
    },

    async verifyProfessional(professionalId) {
      try {
        const token = localStorage.getItem("authToken");  
        const response = await fetch(`http://127.0.0.1:5000/admin/verify-professional/${professionalId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          this.unverifiedProfessionals = this.unverifiedProfessionals.filter(p => p.id !== professionalId);
          this.verifiedProfessionals.push(
            this.unverifiedProfessionals.find(p => p.id === professionalId)
          );
        } else {
          alert(`Failed to verify professional: ${response.status} ${response.statusText}`);
        }
      } catch (error) {
        alert(`Error verifying professional: ${error.message}`);
      }
    },

    async unverifyProfessional(professionalId) {
      try {
        const token = localStorage.getItem("authToken");
        const response = await fetch(`http://127.0.0.1:5000/admin/unverify-professional/${professionalId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          this.verifiedProfessionals = this.verifiedProfessionals.filter(p => p.id !== professionalId);
          this.unverifiedProfessionals.push(
            this.verifiedProfessionals.find(p => p.id === professionalId)
          );
        } else {
          alert(`Failed to unverify professional: ${response.status} ${response.statusText}`);
        }
      } catch (error) {
        alert(`Error unverify professional: ${error.message}`);
      }
    },

  logout() {
  
  fetch("http://127.0.0.1:5000/logout", {
    method: "GET", 
    credentials: "include", 
  })
    .then(response => {
      if (response.ok) {
        localStorage.removeItem("authToken");
        this.$router.push("/");
      } else {
        alert(`Logout failed: ${response.status} ${response.statusText}`);
      }
    })
    .catch(error => {
      alert(`Error during logout: ${error.message}`);
    });
}

  },
  created() {
    this.fetchProfessionals();
  }
};
</script>

<style scoped>

body {
  font-family: 'Poppins', sans-serif;
  background-color: #f7f8fc;
  margin: 0;
  padding: 0;
}

/* Admin Navbar */
.admin-navbar {
  background: linear-gradient(135deg, #4a90e2, #34495e);
  padding: 10px 20px;
  display: flex;
  justify-content: space-around;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.admin-navbar ul {
  list-style: none;
  display: flex;
  margin: 0;
  padding: 0;
}

.admin-navbar li {
  margin: 0 15px;
}

.admin-navbar a {
  text-decoration: none;
  color: white;
  font-weight: bold;
  transition: color 0.3s ease;
}

.admin-navbar a:hover {
  color: #ffce44;
}

/* Dashboard Content */
.dashboard-content {
  max-width: 1200px;
  margin: 20px auto;
  background: #ffffff;
  border-radius: 10px;
  padding: 20px 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.dashboard-content h2 {
  font-size: 24px;
  color: #34495e;
}

.dashboard-sections {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.section {
  width: 48%;
  padding: 15px;
  background: #f7f8fc;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section h3 {
  font-size: 18px;
  color: #4a90e2;
}

.section p {
  color: #7f8c8d;
  font-size: 14px;
}

button {
  background: linear-gradient(135deg, #4a90e2, #34495e);
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  transform: translateY(-2px);
  background: linear-gradient(135deg, #5cacee, #2c3e50);
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

thead {
  background-color: #4a90e2;
  color: white;
}

thead th {
  padding: 12px 15px;
  text-align: left;
}

tbody td {
  padding: 10px 15px;
  border-bottom: 1px solid #e0e0e0;
}

tbody tr:hover {
  background: #f0f0f0;
}

.toggle-button {
  margin-top: 10px;
  background: #ffce44;
  color: #34495e;
}
</style>