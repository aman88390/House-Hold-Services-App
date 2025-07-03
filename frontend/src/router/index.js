import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/components/Home.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/components/LoginPage.vue')
    },
    {
      path: '/admin/login',
      name: 'AdminLogin',
      component: () => import('@/components/AdminLogin.vue')
    },
    {
      path: '/admin/dashboard',
      name: 'AdminDashboard',
      component: () => import('@/components/AdminDashboard.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/components/Register.vue')
    },
    {
      path: '/customer/dashboard',
      name: 'CustomerDashboard',
      component: () => import('@/components/CustomerDashboard.vue')
    },
    {
      path:'/admin/manage_services',
      name:'manageServices',
      component: () => import('@/components/ManageServices.vue')
    },
    {
      path: '/professional/dashboard',
      name: 'ProfessionalDashboard',
      component: () => import('@/components/ProfessionalDashboard.vue')

    },
    {
      path: '/admin/requested_services',
      name: 'RequestedServices',
      component: () => import('@/components/RequestedServices.vue')
    },
    {
      path:'/service/:serviceId/professionals',
      name :'BookService',
      component: () => import('@/components/BookService.vue'),
      props: true
    },
    {
      path:'/customer/requested_services',
      name :'CustomerRequestedServices',
      component: () => import('@/components/CustomerRequestedServices.vue'),
    },
    {
      path:'/admin/manage_services1',
      name:'manageServices1',
      component: () => import('@/components/ManageServices1.vue')
    },
    {
      path:'/admin/manage_users',
      name:'manageusers',
      component: () => import('@/components/ManageUsers.vue')
    },

    {
      path:'/search_services',
      name:'SearchServices',
      component: () => import('@/components/SearchService.vue')
    },
    {
      path:'/customer_summary',
      name:'CustomerSummary',
      component: () => import('@/components/CustomerSummary.vue')
    },
    {
      path:'/view_all_requests',
      name:'ViewAllRequests',
      component: () => import('@/components/ViewAllRequests.vue')
    },
    {
      path:'/admin_chart',
      name:'AdminChart',
      component: () => import('@/components/AdminChart.vue')
    },
    {
      path:'/closed_services',
      name:'ClosedServices',
      component: () => import('@/components/ClosedServices.vue')
    }
   
  ]
})

export default router
