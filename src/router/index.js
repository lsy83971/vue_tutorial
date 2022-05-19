import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import JsmViewTest3 from '../views/JsmViewTest3.vue'
import ModelView from '../views/ModelView.vue'

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
      path: '/jsmtest3',
      name: 'jsmtest3',
      component: JsmViewTest3
  },
  {
      path: '/mp',
      name: 'models',
      component: ModelView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
