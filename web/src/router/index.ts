import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RightSidebar from '../components/PRightSidebar.vue'
import NotFound from '../views/NotFound.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      components: {
        default: HomeView,
        RightSidebar: RightSidebar
      },
    },
    {
      path: '/:shortcode',
      name: 'view',
      components: {
        default: HomeView,
        RightSidebar: RightSidebar
      },
    },
    {
      path: '/:pathMatch(.*)*',
      components:{
        default: NotFound,
        RightSidebar: RightSidebar
      }
    }
  ],
})

export default router
