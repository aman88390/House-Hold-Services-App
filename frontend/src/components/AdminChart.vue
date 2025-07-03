<template>
  <div>
    <h1>Admin Dashboard</h1>
  
    <div>
      <h2>Service Requests by Type</h2>
      <canvas id="serviceTypeChart"></canvas>
    </div>

    <div>
      <h2>Service Requests by Status</h2>
      <canvas id="serviceStatusChart"></canvas>
    </div>
  </div>
</template>

<script>
import { Chart } from 'chart.js/auto';
import axios from 'axios';

export default {
  name: 'AdminChart',
  data() {
    return {
      serviceTypeChart: null,
      serviceStatusChart: null,
    };
  },
  methods: {
    getAuthToken() {
      const token = localStorage.getItem('authToken'); 
      if (!token) {
        console.error('No authToken found in localStorage');
      }
      return token;
    },
    async fetchServiceTypeData() {
      const authToken = this.getAuthToken();
      if (!authToken) return;

      try {
        const response = await axios.get('http://127.0.0.1:5000/admin_chart', {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });
        const { labels, data } = response.data;
        this.createChart('serviceTypeChart', labels, data, 'Service Requests');
      } catch (error) {
        console.error('Error fetching service type data:', error);
      }
    },
    async fetchServiceStatusData() {
      const authToken = this.getAuthToken();
      if (!authToken) return;

      try {
        const response = await axios.get('http://127.0.0.1:5000/admin_service_req', {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });
        const { labels, counts } = response.data;
        this.createChart('serviceStatusChart', labels, counts, 'Service Status');
      } catch (error) {
        console.error('Error fetching service status data:', error);
      }
    },
    createChart(canvasId, labels, data, chartLabel) {
      const ctx = document.getElementById(canvasId).getContext('2d');
      
      if (this[canvasId]) {
        this[canvasId].destroy();
      }

      this[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: chartLabel,
            data,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    },
  },
  mounted() {
    this.fetchServiceTypeData();
    this.fetchServiceStatusData();
  },
};
</script>

<style scoped>
 h1 {
  text-align: center;
}
h2 {
  text-align: center;
}
h3 {
  text-align: center;
}
canvas {
  height: 500px;
  width: 400px;
  margin: 20px auto;
  display: block;
}
</style>
