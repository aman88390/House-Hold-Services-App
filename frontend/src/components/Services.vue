<template>
    <div>
      <h3>Services</h3>
  
      <!-- List Existing Services -->
      <ul>
        <li v-for="service in services" :key="service.id">
          {{ service.name }} - {{ service.description }} - {{ service.price }}
          <button @click="editService(service)">Edit</button>
          <button @click="deleteService(service.id)">Delete</button>
        </li>
      </ul>
  
      <!-- Create Service -->
      <form @submit.prevent="createService">
        <input v-model="newService.name" placeholder="Service Name" required />
        <input v-model="newService.description" placeholder="Description" required />
        <input v-model="newService.price" placeholder="Price" type="number" required />
        <button type="submit">Create</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        services: [],
        newService: { name: "", description: "", price: "" },
      };
    },
    methods: {
      fetchServices() {
        axios.get(" http://127.0.0.1:5000/get_existing_services").then((response) => {
          this.services = response.data;
        });
      },
      createService() {
        axios.post(" http://127.0.0.1:5000/create_new_service", this.newService).then(() => {
          this.fetchServices();
          this.newService = { name: "", description: "", price: "" };
        });
      },
      editService(service) {
        // Code to handle editing
      },
      deleteService(id) {
        axios.delete(`http://127.0.0.1:5000/edit_service/${id}`).then(() => {
          this.fetchServices();
        });
      },
    },
    mounted() {
      this.fetchServices();
    },
  };
  </script>
  