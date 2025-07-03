<template>
  <div class="app-container">
    <h2 class="app-title">Service Types & Service Management</h2>
    <div v-if="showSuccessMessage" class="message_success">
  {{ showSuccessMessage }}
</div>
<div v-if="showErrorMessage" class="message_error">
  {{ showErrorMessage }}
</div>
    <div class="card" v-if="serviceTypes.length > 0">
      <h3 class="card-title">Existing Service Types</h3>
      <ul class="list">
        <li v-for="serviceType in serviceTypes" :key="serviceType.id" class="list-item">
          <div class="details">
            <h4>{{ serviceType.name }}</h4>
            <p>{{ serviceType.description }}</p>
          </div>
          <div class="actions">
            <button class="btn edit" @click="editServiceType(serviceType)">Edit</button>
            <button class="btn delete" @click="confirmDeleteServiceType(serviceType.id)">Delete</button>
          </div>
        </li>
      </ul>
    </div>
    <div class="card">
      <h3 class="card-title">Create New Service Type</h3>
      <form class="form" @submit.prevent="createServiceType">
        <input class="input" v-model="newServiceTypeName" placeholder="Service Type Name" required />
        <input class="input" v-model="newServiceTypeDescription" placeholder="Service Type Description" required />
        <button class="btn create" type="submit">Create Service Type</button>
      </form>
    </div>
    <div class="card" v-if="services.length > 0">
      <h3 class="card-title">Existing Services</h3>
      <ul class="list">
        <li v-for="service in services" :key="service.id" class="list-item">
          <div class="details">
            <h4>{{ service.service_name }}</h4>
            <p>{{ service.service_description }}</p>
            <p class="price">Rs.{{ service.price }}</p>
            <p> {{ service.service_type_id }}- {{ service.service_type }} </p>
          </div>
          <div class="actions">
            <button class="btn edit" @click="editService(service)">Edit</button>
            <button class="btn delete" @click="confirmDeleteService(service.id)">Delete</button>
          </div>
        </li>
      </ul>
    </div>

    <div class="card">
      <h3 class="card-title">Create New Service</h3>
      <form class="form" @submit.prevent="createService">
        <input class="input" v-model="newServiceName" placeholder="Service Name" required />
        <input class="input" v-model="newServiceDescription" placeholder="Service Description" required />
        <input 
            class="input" 
             v-model="newServicePrice" 
             placeholder="Price" 
             type="number" 
              required 
              min="0.01" 
              step="0.01" 
              />

        <select class="input" v-model="service_type_id" placeholder="Select Service Type"  required>
          <option v-for="serviceType in serviceTypes" :value="serviceType.id" :key="serviceType.id">
            {{ serviceType.name }}
          </option>
        </select>
        <button class="btn create" type="submit" >Create Service</button>

      </form>
    </div>
    <div v-if="editModalVisible" class="modal">
  <div class="modal-content">
    <h4>Edit Service</h4>
    <input class="input" v-model="editServiceData.service_name" placeholder="Service Name" />
    <input class="input" v-model="editServiceData.service_description" placeholder="Service Description" />
    <input 
  class="input" 
  v-model="editServiceData.price" 
  placeholder="Price" 
  type="number" 
  required 
  min="0.01" 
  step="0.01" 
/>

  
    <select class="input" v-model="editServiceData.service_type_id" placeholder="Select Service Type">
      <option v-for="serviceType in serviceTypes" :value="serviceType.id" :key="serviceType.id">
        {{ serviceType.name }}
      </option>
    </select>
    
    <div class="modal-actions">
      <button class="btn save" @click="updateService">Save Changes</button>
      <button class="btn cancel" @click="closeEditModal">Cancel</button>
    </div>
  </div>
</div>

    <div v-if="editServiceTypeModalVisible" class="modal">
      <div class="modal-content">
        <h4>Edit Service Type</h4>
        <input class="input" v-model="editServiceTypeData.name" placeholder="Service Type Name" />
        <input class="input" v-model="editServiceTypeData.description" placeholder="Service Type Description" />
        <div class="modal-actions">
          <button class="btn save" @click="updateServiceType">Save Changes</button>
          <button class="btn cancel" @click="closeEditServiceTypeModal">Cancel</button>
        </div>
      </div>
    </div>

    <div v-if="confirmDeleteVisible" class="modal">
      <div class="modal-content">
        <h4>Are you sure you want to delete this item?</h4>
        <div class="modal-actions">
          <button class="btn delete" @click="deleteServiceTypeOrService">Yes, Delete</button>
          <button class="btn cancel" @click="cancelDelete">Cancel</button>
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
      serviceTypes: [],
      services: [],
      newServiceTypeName: "",
      newServiceTypeDescription: "",
      newServiceName: "",
      newServiceDescription: "",
      showSuccessMessage: "",
      showErrorMessage: "",
      service_type_id: null,
      newServicePrice: "",
      newServiceTypeId: "",
      editModalVisible: false,
      editServiceData: {
        service_name: "",
        service_description: "",
        price: 0,
        service_type_id: null,
      },
      editServiceTypeModalVisible: false,
      editServiceTypeData: {
        name: "",
        description: "",
      },
      confirmDeleteVisible: false,
      itemToDelete: null,
      isServiceType: false,
    };
  },
  methods: {
    clearMessages() {
      this.showSuccessMessage = "";
      this.showErrorMessage = "";
    },
    async fetchServiceTypes() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/get_existing_service_types", {
          headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
        });
        this.serviceTypes = response.data;
      } catch (error) {
        console.error("Error fetching service types:", error);
      }
    },
    async fetchServices() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/get_existing_services", {
          headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
        });
        this.services = response.data;
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    editService(service) {
      this.editServiceData = { ...service };
      this.editModalVisible = true;
    },
    editServiceType(serviceType) {
      this.editServiceTypeData = { ...serviceType };
      this.editServiceTypeModalVisible = true;
    },
    async createServiceType() {
      try {
        const response =await axios.post(
          "http://127.0.0.1:5000/create_new_service_type",
          { name: this.newServiceTypeName, description: this.newServiceTypeDescription },
          { headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` } }
        );
        // this.showSuccessMessage = response.data.message;
        this.newServiceTypeName = "";
        this.newServiceTypeDescription = "";
        this.fetchServiceTypes();
        if (response.status === 201) {
        alert(response.data.message );
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      // Handle errors
      if (error.response && error.response.data) {
        alert(error.response.data.message );
      } else {
        alert('An error occurred while creating the service type .');
      }
      console.error('Error:', error);}
        
      //   setTimeout(this.clearMessages, 3000);// 
      // } catch (error) {
      //   console.error("Error creating service type:", error);
      // }
    },
    async createService() {
      try {
        const response =
        await axios.post(
          "http://127.0.0.1:5000/admin/create_new_service",
          {
            service_name: this.newServiceName,
            service_description: this.newServiceDescription,
            price: this.newServicePrice,
            service_type_id: this.service_type_id,
          },
          { headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` } }
        );
        this.newServiceName = "";
        this.newServiceDescription = "";
        this.newServicePrice = "";
        this.service_type_id = null;
        this.fetchServices(); 

        if (response.status === 200) {
        alert(response.data.message || 'Service created successfully!');
      } else {
        alert(response.data.message || 'Unexpected response from the server.');
      }
    } catch (error) {
      // Handle errors
      if (error.response && error.response.data) {
        alert(error.response.data.message || 'Failed to create the service.');
      } else {
        alert('An error occurred while creating the service.');
      }
      console.error('Error creating service:', error);
      }
    },
    async updateService() {

      try { if (this.editServiceData.price <= 0) {
    alert('Price must be grater than 0.');
    return;
  }
        const response =
        await axios.put(
          `http://127.0.0.1:5000/edit_service/${this.editServiceData.id}`,
          this.editServiceData,
          { headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` } }
        );
        this.editModalVisible = false;
        this.fetchServices(); // Added: Refresh services
        if (response.status === 201) {
        alert(response.data.message );
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      // Handle errors
      if (error.response && error.response.data) {
        alert(error.response.data.message );
      } else {
        alert('An error occurred while editing the service.');
      }
      console.error('Error :', error);}
      // } catch (error) {
      //   console.error("Error updating service:", error);
      // }
    },
    async updateServiceType() {
      try {
        const response =
        await axios.put(
          `http://127.0.0.1:5000/edit_service_type/${this.editServiceTypeData.id}`,
          this.editServiceTypeData,
          { headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` } }
        );
        this.editServiceTypeModalVisible = false;
        this.fetchServiceTypes(); // Added: Refresh service types
        if (response.status === 201) {
        alert(response.data.message );
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      // Handle errors
      if (error.response && error.response.data) {
        alert(error.response.data.message );
      } else {
        alert('An error occurred while editing the service type.');
      }
      console.error('Error:', error);}
      // } catch (error) {
      //   console.error("Error updating service type:", error);
      // }
    },
    closeEditModal() {
      this.editModalVisible = false;
      this.editServiceData = {};
    },
    closeEditServiceTypeModal() {
      this.editServiceTypeModalVisible = false;
      this.editServiceTypeData = {};
    },
    confirmDeleteService(serviceId) {
      this.itemToDelete = serviceId;
      this.isServiceType = false;
      this.confirmDeleteVisible = true;
    },
    confirmDeleteServiceType(serviceTypeId) {
      this.itemToDelete = serviceTypeId;
      this.isServiceType = true;
      this.confirmDeleteVisible = true;
    },
    async deleteServiceTypeOrService() {
  try {
    if (this.isServiceType) {
    const response = 
      await axios.delete(`http://127.0.0.1:5000/delete_service_type/${this.itemToDelete}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
      });
      // this.showSuccessMessage = response.data.message;
      this.fetchServiceTypes(); // Refresh service types
      // setTimeout(this.clearMessages, 6000);
      if (response.status === 200) {
        alert(response.data.message );
      } else {
        alert(response.data.message);
      }
      
    } else {
      const response =
      await axios.delete(`http://127.0.0.1:5000/delete_service/${this.itemToDelete}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
      });
      this.showSuccessMessage = "Service deleted successfully!";
      this.fetchServices(); 
      setTimeout(this.clearMessages, 6000);
      alert(response.data.message )
    }
    this.confirmDeleteVisible = false;
    this.itemToDelete = null;
    
    if (response.status === 200) {
        alert(response.data.message || "delete successfully" );
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      // Handle errors
      if (error.response && error.response.data) {
        alert(error.response.data.error );
      }

  // } catch (error) {
  //   console.error("Error deleting item:", error);
    // this.showErrorMessage = error.response?.data?.error || "Failed to delete item.";
    // this.confirmDeleteVisible = false;
    // setTimeout(this.clearMessages, 6000);
  }
},

    cancelDelete() {
      this.confirmDeleteVisible = false;
      this.itemToDelete = null;
    },
  },
  mounted() {
    this.fetchServiceTypes();
    this.fetchServices();
  },
};
</script>


<style scoped>
.app-container {
  font-family: Arial, sans-serif;
  padding: 10px;
  max-width: 800px;
  margin: 0 auto;
}

.app-title {
  text-align: center;
  color: #3f35c7;
  margin-bottom: 20px;
}

.card {
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 10px;
  margin-bottom: 10px;
}

.card-title {
  color: #333;
  margin-bottom: 1px;
}

.list {
  list-style: none;
  padding: 0;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding: 10px 0;
}

.details h4 {
  margin: 0;
  font-size: 16px;
}

.details p {
  margin: 5px 0;
  color: #666;
}

.price {
  color: #4CAF50;
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 10px;
}

.btn {
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  color: white;
}

.btn.create {
  background-color: #4c65af;
}

.btn.edit {
  background-color: #0707ff;
}

.btn.delete {
  background-color: #F44336;
}

.btn.cancel {
  background-color: #9E9E9E;
}

.btn.save {
  background-color: #2196F3;
}

.btn:hover {
  opacity: 0.9;
}

.input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal {
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

.modal-content {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
.message_success{
  background-color: #117e0f;
  color: white;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
}
.message_error{
  background-color: #F44336;
  color: white;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
}
</style>
