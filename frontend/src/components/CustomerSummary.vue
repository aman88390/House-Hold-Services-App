<template>
  <div>
    <h1>Service Status Summary</h1>
    <canvas id="serviceStatusChart" width="1200" height="600"></canvas>
  </div>
</template>

<script>
import { defineComponent, onMounted } from "vue";
import { Chart } from "chart.js/auto";
import axios from "axios";

export default defineComponent({
  name: "CustomerSummary",
  setup() {
    const fetchServiceStatusData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/customer_summary", {
          headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
        });

        const { labels, counts } = response.data;

        renderBarChart(labels, counts);
      } catch (error) {
        console.error("Error fetching service status data:", error);
      }
    };

    const renderBarChart = (labels, counts) => {
      const canvas = document.getElementById("serviceStatusChart");
      if (!canvas) {
        console.error("Canvas element not found");
        return;
      }

      const ctx = canvas.getContext("2d");

      new Chart(ctx, {
        type: "bar", 
        data: {
          labels: labels, 
          datasets: [
            {
              label: "Service Requests",
              data: counts, 
              backgroundColor: [
                "rgba(75, 192, 192, 0.6)", 
                "rgba(255, 99, 132, 0.6)",
                "rgba(255, 206, 86, 0.6)",
                "rgba(54, 162, 235, 0.6)",
              ],
              borderColor: [
                "rgba(75, 192, 192, 1)",
                "rgba(255, 99, 132, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(54, 162, 235, 1)",
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: true,
              position: "top",
            },
            title: {
              display: true,
              text: "Service Status Overview",
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Status", 
              },
            },
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Count", 
              },
            },
          },
        },
      });
    };

    onMounted(() => {
      fetchServiceStatusData();
    });
  },
});
</script>

<style>
canvas {
  width: 500px !important; 
  height: 500px !important; 
  max-width: none; 
  margin: 0 auto;
  display: block;
}
</style>
