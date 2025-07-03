<template>
    <!-- Navbar -->
    <nav class="navbar">
      <div class="navbar-brand">
        <span class="logo"></span> Household Services
      </div>
      <ul class="navbar-links">
        <li><a href="#dashboard">Dashboard</a></li>
        <li><a href="#users">Users</a></li>
        <li><a href="#settings">Settings</a></li>
        <li><a href="#help">Help</a></li>
      </ul>
    </nav>
    <div class="search-container">
    <form class="navbar-search" @submit.prevent="searchProfessionals">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search professionals..."
      />
      <button type="submit">Search</button>
    </form>
    <div v-if="searchResults.length === 0 && searchQuery" class="no-results">
      <p>No professionals found for your search. Try refining your query.</p>
    </div>
    <div v-else-if="searchResults.length > 0" class="search-results">
      <h3>Search Results</h3>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Username</th>
            <th>Email</th>
            <th>Service</th>
            <th>Rating</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in searchResults" :key="result.id">
            <td>{{ result.name }}</td>
            <td>{{ result.username }}</td>
            <td>{{ result.email }}</td>
            <td>{{ result.service_name }}</td>
            <td>{{ result.rating || "No Ratings" }}</td>
            <td>
              <button @click="toggleBlock(result)">
                {{ result.block ? "Unblock" : "Block" }}
              </button>
              <button @click="viewDetails(result)">See More</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="admin-user-list">
    <!-- Professional Users -->
    <h1>Professionals</h1>
    <table v-if="filteredProfessionals.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Name</th>
          <th>Email</th>
          <th>Role</th>
          <th>Average Rating</th>
          <th>Account Status</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in filteredProfessionals" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>{{ user.average_rating }}</td>
          <td>{{ user.block ? 'Blocked' : 'Active' }}</td>
          <td>{{ new Date(user.created_at).toLocaleString() }}</td>
          <td>
            <button
              @click="toggleBlock(user)"
              :class="{ blocked: user.block }"
              :disabled="user.loading"
            >
              {{ user.block ? 'Unblock' : 'Block' }}
            </button>
            <button @click="viewDetails(user)">See More</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>No professionals found.</p>

    <!-- Customer Users -->
    <h1>Customers</h1>
    <table v-if="filteredCustomers.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Name</th>
          <th>Email</th>
          <th>Role</th>
          <th>Account Status</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in filteredCustomers" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>{{ user.block ? 'Blocked' : 'Active' }}</td>
          <td>{{ new Date(user.created_at).toLocaleString() }}</td>
          <td>
            <button
              @click="toggleBlock(user)"
              :class="{ blocked: user.block }"
              :disabled="user.loading"
            >
              {{ user.block ? 'Unblock' : 'Block' }}
            </button>
            <button @click="viewDetails(user)">See More</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>No customers found.</p>

    <!-- Combined Modal -->
    <div v-if="selectedUser" class="details">
      <div class="content">
        <span class="close" @click="selectedUser = null">&times;</span>
        <h2 v-if="selectedUser.role === 'professional'">Professional Details</h2>
        <h2 v-else>Customer Details</h2>
        <p v-if="selectedUser.name!='N/A'"><strong>Name:</strong> {{ selectedUser.name }}</p>
        <p v-if="selectedUser.username!='N/A'"><strong>Username:</strong> {{ selectedUser.username }}</p>
        <p v-if="selectedUser.email!='N/A'"><strong>Email:</strong> {{ selectedUser.email }}</p>
        <p v-if="selectedUser.phone!=''"><strong>Phone:</strong> {{ selectedUser.phone }}</p>
        <p v-if="selectedUser.address!=''"><strong>Address:</strong> {{ selectedUser.address }}</p>
        <p v-if="selectedUser.pin_code!=''"><strong>Pin Code:</strong> {{ selectedUser.pin_code }}</p>
        <p v-if="selectedUser.role === 'professional' && selectedUser.average_rating!= null "><strong>Average Rating:</strong> {{ selectedUser.average_rating }}</p>
        <ul>
          <li v-for="review in selectedUser.reviews" :key="review.review">
            <strong v-if="selectedUser.rating!='N/A' && selectedUser.review!='N/A' ">Rating:</strong> {{ review.rating }} | <strong>Review:</strong> {{ review.review }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      users: [],
      selectedUser: null,
      searchQuery: '',
      searchResults: [],
    };
  },
  computed: {
    filteredProfessionals() {
      return this.users.filter((user) => user.role === "professional");
    },
    filteredCustomers() {
      return this.users.filter((user) => user.role === "customer");
    },
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem("authToken");
        const response = await axios.get("http://127.0.0.1:5000/admin/manageusers", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.users = response.data.map((user) => ({
          ...user,
          loading: false,
        }));
      } catch (error) {
        console.error("Failed to fetch users:", error);
      }
    },
    async viewDetails(user) {
      try {
        const token = localStorage.getItem("authToken");
        const response = await axios.get(`http://127.0.0.1:5000/admin/user_details/${user.id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.selectedUser = response.data;
      } catch (error) {
        console.error("Failed to fetch user details:", error);
      }
    },
    async toggleBlock(user) {
      const newBlockStatus = !user.block;
      user.loading = true;

      try {
        const token = localStorage.getItem("authToken");
        await axios.post(
          `http://127.0.0.1:5000/admin/block_user/${user.id}`,
          { block: newBlockStatus },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        user.block = newBlockStatus;
      } catch (error) {
        console.error("Failed to toggle block status:", error);
      } finally {
        user.loading = false;
      }
    },
    async searchProfessionals() {
      if (!this.searchQuery) {
        this.searchResults = [];
        return;
      }

      try {
        const token = localStorage.getItem("authToken");
        const response = await axios.get(
          `http://127.0.0.1:5000/admin/search_professionals?query=${this.searchQuery}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.searchResults = response.data;
      } catch (error) {
        console.error("Failed to search professionals:", error);
      }
    
  },
    
  },
  created() {
    this.fetchUsers();
  },
};
</script>
<style scoped>
/* General Body Styles */
body {
  margin: 0;
  font-family: 'Poppins', sans-serif;
  background-color: #f9f9f9;
  color: #333;
}

/* Navbar Styles */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background: linear-gradient(90deg, #4c13dc, #684fe5);
  color: white;
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-size: 24px;
  font-weight: bold;
  color: #ffffff;
}

.navbar-links {
  list-style: none;
  display: flex;
  gap: 20px;
  margin: 0;
}

.navbar-links a {
  text-decoration: none;
  color: #ffffff;
  font-weight: 500;
  font-size: 14px;
  transition: color 0.3s ease;
}

.navbar-links a:hover {
  color: #ffdf5d;
}

/* Search Container */
.search-container {
  margin-top: 80px;
  padding: 20px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.navbar-search {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.navbar-search input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 300px;
  font-size: 14px;
}

.navbar-search button {
  padding: 10px 16px;
  background-color: #4c13dc;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.navbar-search button:hover {
  background-color: #684fe5;
}

/* Table Styles */
table {
  width: 100%;
  margin: 20px 0;
  border-collapse: collapse;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

thead {
  background-color: #4c13dc;
  color: #ffffff;
}

thead th {
  padding: 12px;
  font-weight: bold;
  text-transform: uppercase;
}

tbody tr {
  border-bottom: 1px solid #dddddd;
  transition: background-color 0.3s ease;
}

tbody tr:nth-child(even) {
  background-color: #f4f4f4;
}

tbody tr:hover {
  background-color: #f0f0f0;
}

td {
  padding: 10px;
  color: #333;
  text-align: left;
}

button {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

/* Block Button */
button.blocked {
  background-color: #e55a4f;
  color: white;
  margin-right: 8px; 
}

button.blocked:hover {
  background-color: #d14842;
}

/* Active Button */
button:not(.blocked) {
  background-color: #179f4b;
  color: white;
  margin-right:8px; 
}

button:not(.blocked):hover {
  background-color: #137f3d;
}

/* See More Button */
button + button {
  background-color: #007bff;
  color: white;
}

button + button:hover {
  background-color: #0056b3;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* Modal Styles */
.details {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  background: #ffffff;
  border-radius: 8px;
  width: 50%;
  padding: 20px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
}

.details .content {
  position: relative;
}

.details .close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 16px;
  font-weight: bold;
  background: #e55a4f;
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  text-align: center;
  cursor: pointer;
}

.details .close:hover {
  background-color: #c94b40;
}

.details h2 {
  color: #4c13dc;
  margin-bottom: 10px;
  text-align: center;
}

.details p {
  margin: 8px 0;
  line-height: 1.5;
  color: #555;
}

.details ul {
  list-style: none;
  padding: 0;
}

.details ul li {
  margin-bottom: 10px;
  padding: 8px;
  background: #f4f4f4;
  border-radius: 4px;
}


</style>