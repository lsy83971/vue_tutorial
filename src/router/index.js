import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import JsmView from '../views/JsmView.vue'
import JsmViewTest from '../views/JsmViewTest.vue'
import JsmViewTest1 from '../views/JsmViewTest1.vue'
import JsmViewTest2 from '../views/JsmViewTest2.vue'

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
      path: '/jsmtest',
      name: 'jsm',
      component: JsmView
  },
  {
      path: '/jsm',
      name: 'jsmtest',
      component: JsmViewTest
  },
  {
      path: '/jsmtest1',
      name: 'jsmtest1',
      component: JsmViewTest1
  },
  {
      path: '/jsmtest2',
      name: 'jsmtest2',
      component: JsmViewTest2
  }
    
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
