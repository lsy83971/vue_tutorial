import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import mindcode from '../views/MindCode.vue'
import modelview from '../views/ModelView.vue'
import mindtext from '../views/MindText.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
      path: '/mindcode',
      name: 'mindcode',
      component: mindcode
  },
  {
      path: '/mp',
      name: 'mp',
      component: modelview
  },
  {
      path: '/mindtext',
      name: 'mindtext',
      component: mindtext,
  }    
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


export default router
