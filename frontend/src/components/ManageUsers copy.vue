<template>
  <div class="admin-user-list">
    <h1>professional</h1>
    <table v-if="users.length">
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
        <tr v-for="user in users" :key="user.id">
          <div v-if="user.role=='professional'">
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
        </div>
        </tr>
      </tbody>
    </table>
    <p v-else>No Professional found.</p>

    <!-- Modal -->
    <div v-if="selectedUser" class="details">
      <div class="content" v-if="selectedUser.role == 'professional'">
        <span class="close" @click="selectedUser = null">&times;</span>
        <h2>Professional Details</h2>
        <p><strong>Name:</strong> {{ selectedUser.name }}</p>
        <p><strong>Username:</strong> {{ selectedUser.username }}</p>
        <p><strong>Email:</strong> {{ selectedUser.email }}</p>
        <p><strong>Phone:</strong> {{ selectedUser.phone }}</p>
        <p><strong>Address:</strong> {{ selectedUser.address }}</p>
        <p><strong>Pin Code:</strong> {{ selectedUser.pin_code }}</p>
        <p><strong>Average Rating:</strong> {{ selectedUser.average_rating || 'N/A' }}</p>
        <h3>Reviews:</h3>
        <ul>
          <li v-for="review in selectedUser.reviews" :key="review.review">
            <strong>Rating:</strong> {{ review.rating }} | <strong>Review:</strong> {{ review.review }}
          </li>
        </ul>
      </div>

    </div>
  </div>




  <div class="admin-user-list">
    <h1>Customers</h1>
    <table v-if="users.length">
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
        <tr v-for="user in users" :key="user.id">
          <div v-if="user.role=='customer'">
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
        </div>
        </tr>
      </tbody>
    </table>
    <p v-else>Customers not found.</p>

    <!-- Modal -->
    <div v-if="selectedUser" class="details">
      <!-- ============================= -->

      <div class="content" v-if="selectedUser.role == 'customer'">
        <span class="close" @click="selectedUser = null">&times;</span>
        <h2>User Details</h2>
        <p><strong>Name:</strong> {{ selectedUser.name }}</p>
        <p><strong>Username:</strong> {{ selectedUser.username }}</p>
        <p><strong>Email:</strong> {{ selectedUser.email }}</p>
        <p><strong>Phone:</strong> {{ selectedUser.phone }}</p>
        <p><strong>Address:</strong> {{ selectedUser.address }}</p>
        <p><strong>Pin Code:</strong> {{ selectedUser.pin_code }}</p>
        <!-- <p><strong>Average Rating:</strong> {{ selectedUser.average_rating || 'N/A' }}</p> -->
        <!-- <h3>Reviews:</h3> -->
        <ul>
          <li v-for="review in selectedUser.reviews" :key="review.review">
            <strong>Rating:</strong> {{ review.rating }} | <strong>Review:</strong> {{ review.review }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdminUserList",
  data() {
    return {
      users: [],
      selectedUser: null, 
    };
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem("authToken");
        const response = await axios.get("http://127.0.0.1:5000/admin/manageusers", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.users = response.data.map(user => ({
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
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log("User details response:", response.data);
    // alert(JSON.stringify(response.data));
    this.selectedUser = response.data;
  } catch (error) {
    console.error("Failed to fetch user details:", error);
  }
}


    ,
    async toggleBlock(user) {
      const newBlockStatus = !user.block;
      user.loading = true;

      try {
        const token = localStorage.getItem("authToken");
        const response = await axios.post(
          `http://127.0.0.1:5000/admin/block_user/${user.id}`,
          { block: newBlockStatus },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        user.block = response.data.block;
        this.fetchUsers();
      } catch (error) {
        console.error("Failed to toggle block status:", error);
        user.block = !newBlockStatus;
      } finally {
        user.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.details {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  background: linear-gradient(135deg, #f9f9f9, #ffffff);
  border-radius: 16px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
  width: 50%;
  max-width: 600px;
  padding: 30px;
  font-family: 'Poppins', sans-serif;
  color: #333;
  transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;
  opacity: 1;
}

.details:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0));
  border-radius: inherit;
  z-index: -1;
}

.content {
  position: relative;
  animation: slideIn 0.5s ease forwards;
}

.close {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  background: #f5f5f5;
  color: #ff6666;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.close:hover {
  background-color: #ff6666;
  color: white;
  transform: scale(1.1);
}

h2, h3 {
  color: #444;
  margin: 10px 0;
  font-weight: bold;
}

p {
  margin: 10px 0;
  line-height: 1.6;
  color: #555;
}

ul {
  list-style: none;
  padding: 0;
}

ul li {
  margin-bottom: 8px;
  padding: 10px;
  background: #f4f4f4;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 14px;
}

ul li strong {
  font-weight: bold;
  color: #333;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.details h2::after {
  content: '';
  display: block;
  width: 60px;
  height: 3px;
  margin-top: 5px;
  background: #ff6666;
  border-radius: 5px;
  margin-left: auto;
  margin-right: auto;
}
</style>
