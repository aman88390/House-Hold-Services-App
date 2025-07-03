<template>
    <div>
      <h3>Service Types</h3>
  
      <!-- List Existing Service Types -->
      <ul>
        <li v-for="type in serviceTypes" :key="type.id">
          {{ type.name }} - {{ type.description }}
          <button @click="editServiceType(type)">Edit</button>
          <button @click="deleteServiceType(type.id)">Delete</button>
        </li>
      </ul>
  
      <!-- Create Service Type -->
      <form @submit.prevent="createServiceType">
        <input v-model="newType.name" placeholder="Service Type Name" required />
        <input v-model="newType.description" placeholder="Description" required />
        <button type="submit">Create</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        serviceTypes: [],
        newType: { name: "", description: "" },
      };
    },
    methods: {
      fetchServiceTypes() {
        axios.get("/ http://127.0.0.1:5000/get_existing_service_types").then((response) => {
          this.serviceTypes = response.data;
        });
      },
      createServiceType() {
        axios.post(" http://127.0.0.1:5000/create_new_service_type", this.newType).then(() => {
          this.fetchServiceTypes();
          this.newType = { name: "", description: "" };
        });
      },
      editServiceType(type) {
        // Code to handle editing
      },
      deleteServiceType(id) {
        axios.delete(`/ http://127.0.0.1:5000/delete_service_type/${id}`).then(() => {
          this.fetchServiceTypes();
        });
      },
    },
    mounted() {
      this.fetchServiceTypes();
    },
  };
  </script>
  