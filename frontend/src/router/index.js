import { createRouter, createWebHistory } from "vue-router";

import FeedPage from "../pages/FeedPage.vue";
import MobilePage from "../pages/MobilePage.vue";

const routes = [
  {
    path: "/",
    name: "feed",
    component: FeedPage,
    props: { viewMode: "feed", routeUserId: null },
  },
  {
    path: "/favorites",
    name: "favorites",
    component: FeedPage,
    props: { viewMode: "favorites", routeUserId: null },
  },
  {
    path: "/my-posts",
    name: "my-posts",
    component: FeedPage,
    props: { viewMode: "my-posts", routeUserId: null },
  },
  {
    path: "/users/:userId/posts",
    name: "user-posts",
    component: FeedPage,
    props: (route) => ({
      viewMode: "user",
      routeUserId: Number(route.params.userId),
    }),
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
