<template>
  <div>
    <h2>Service Types & Service Management</h2>
    <div v-if="serviceTypes.length > 0">
      <h3>Existing Service Types</h3>
      <ul>
        <li v-for="serviceType in serviceTypes" :key="serviceType.id">
          {{ serviceType.name }} - {{ serviceType.description }}
          <button @click="editServiceType(serviceType)">Edit</button>
          <button @click="confirmDeleteServiceType(serviceType.id)">Delete</button>
        </li>
      </ul>
    </div>
    <form @submit.prevent="createServiceType">
      <h4>Create New Service Type</h4>
      <input v-model="newServiceTypeName" placeholder="Service Type Name" required />
      <input v-model="newServiceTypeDescription" placeholder="Service Type Description" required />
      <button type="submit">Create Service Type</button>
    </form>
    <div v-if="services.length > 0">
      <h3>Existing Services</h3>
      <ul>
        <li v-for="service in services" :key="service.id">
          {{ service.service_name }} - {{ service.service_description }} - ${{ service.price }}
          <button @click="editService(service)">Edit</button>
          <button @click="confirmDeleteService(service.id)">Delete</button>
        </li>
      </ul>
    </div>
    <form @submit.prevent="createService">
      <h4>Create New Service</h4>
      <input v-model="newServiceName" placeholder="Service Name" required />
      <input v-model="newServiceDescription" placeholder="Service Description" required />
      <input v-model="newServicePrice" placeholder="Price" type="number" required />
      <select v-model="newServiceTypeId" required>
        <option v-for="serviceType in serviceTypes" :value="serviceType.id" :key="serviceType.id">
          {{ serviceType.name }}
        </option>
      </select>
      <button type="submit">Create Service</button>
    </form>

    <div v-if="editModalVisible" class="modal">
      <h4>Edit Service</h4>
      <input v-model="editServiceData.service_name" placeholder="Service Name" />
      <input v-model="editServiceData.service_description" placeholder="Service Description" />
      <input v-model="editServiceData.price" placeholder="Price" type="number" />
      <select v-model="editServiceData.service_type_id">
        <option v-for="serviceType in serviceTypes" :value="serviceType.id" :key="serviceType.id">
          {{ serviceType.name }}
        </option>
      </select>
      <button @click="updateService">Save Changes</button>
      <button @click="closeEditModal">Cancel</button>
    </div>

    <div v-if="editServiceTypeModalVisible" class="modal">
      <h4>Edit Service Type</h4>
      <input v-model="editServiceTypeData.name" placeholder="Service Type Name" />
      <input v-model="editServiceTypeData.description" placeholder="Service Type Description" />
      <button @click="updateServiceType">Save Changes</button>
      <button @click="closeEditServiceTypeModal">Cancel</button>
    </div>

    <div v-if="confirmDeleteVisible" class="confirm-delete-modal">
      <h4>Are you sure you want to delete this item?</h4>
      <button @click="deleteServiceTypeOrService">Yes, Delete</button>
      <button @click="cancelDelete">Cancel</button>
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
      console.log("Editing service:", service);
      this.editServiceData = { ...service };
      this.editModalVisible = true;
    },
    editServiceType(serviceType) {
      console.log("Editing service type:", serviceType);
      this.editServiceTypeData = { ...serviceType };
      this.editServiceTypeModalVisible = true;
    },
    async createServiceType() {
      try {
        await axios.post(
          "http://127.0.0.1:5000/create_new_service_type",
          { name: this.newServiceTypeName, description: this.newServiceTypeDescription },
          { headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` } }
        );
        this.newServiceTypeName = "";
        this.newServiceTypeDescription = "";
        this.fetchServiceTypes();
      } catch (error) {
        console.error("Error creating service type:", error);
      }
    },
    async createService() {
      try {
        await axios.post(
          "http://127.0.0.1:5000/create_new_service",
          {
            service_name: this.newServiceName,
            service_description: this.newServiceDescription,
            price: this.newServicePrice,
            service_type_id: this.newServiceTypeId,
          },
          { headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` } }
        );
        this.newServiceName = "";
        this.newServiceDescription = "";
        this.newServicePrice = "";
        this.newServiceTypeId = "";
        this.fetchServices();
      } catch (error) {
        console.error("Error creating service:", error);
      }
    },
    async updateService() {
      try {
        console.log("Updating service:", this.editServiceData);
        await axios.put(
          `http://127.0.0.1:5000/edit_service/${this.editServiceData.id}`,
          this.editServiceData,
          { headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` } }
        );
        this.editModalVisible = false;
        this.fetchServices();
      } catch (error) {
        console.error("Error updating service:", error);
      }
    },
    async updateServiceType() {
      try {
        console.log("Updating service type:", this.editServiceTypeData);
        await axios.put(
          `http://127.0.0.1:5000/edit_service_type/${this.editServiceTypeData.id}`,
          this.editServiceTypeData,
          { headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` } }
        );
        this.editServiceTypeModalVisible = false;
        this.fetchServiceTypes();
      } catch (error) {
        console.error("Error updating service type:", error);
      }
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
          await axios.delete(`http://127.0.0.1:5000/delete_service_type/${this.itemToDelete}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
          });
          this.fetchServiceTypes();
        } else {
          await axios.delete(`http://127.0.0.1:5000/delete_service/${this.itemToDelete}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
          });
          this.fetchServices();
        }
        this.confirmDeleteVisible = false;
        this.itemToDelete = null;
      } catch (error) {
        console.error("Error deleting item:", error);
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
/* General Layout */
.container {
  font-family: Arial, sans-serif;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  text-align: center;
  color: #4CAF50;
  margin-bottom: 20px;
}

/* Cards */
.card {
  margin-bottom: 30px;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  border-radius: 8px;
}

.card h3 {
  margin-bottom: 15px;
  color: #333;
}

.list {
  margin-bottom: 15px;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
}

.details h4 {
  margin: 0;
  font-size: 16px;
  color: #555;
}

.details p {
  margin: 4px 0;
  font-size: 14px;
  color: #777;
}

.price {
  color: #4CAF50;
  font-weight: bold;
}

/* Buttons */
.btn {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn.create {
  background-color: #4CAF50;
  color: white;
}

.btn.edit {
  background-color: #FFC107;
  color: white;
}

.btn.delete {
  background-color: #F44336;
  color: white;
}

.btn.cancel {
  background-color: #9E9E9E;
  color: white;
}

.btn.save {
  background-color: #2196F3;
  color: white;
}

.btn:hover {
  opacity: 0.9;
}

/* Form Inputs */
.input {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

/* Modal */
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
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 400px;
  text-align: center;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
</style>