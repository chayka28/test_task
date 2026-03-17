import { createRouter, createWebHistory } from "vue-router";

import FeedPage from "../pages/FeedPage.vue";
import MobilePage from "../pages/MobilePage.vue";

const routes = [
  {
    path: "/",
    name: "feed",
    component: FeedPage,
    props: { viewMode: "feed" },
  },
  {
    path: "/favorites",
    name: "favorites",
    component: FeedPage,
    props: { viewMode: "favorites" },
  },
  {
    path: "/mobile-preview",
    name: "mobile-preview",
    component: MobilePage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
