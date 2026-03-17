<template>
  <main class="mobile-page">
    <MobilePreviewCard :post="previewPost" />
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue";

import MobilePreviewCard from "../components/MobilePreviewCard.vue";
import { fetchDemoUser, fetchPostsByUser } from "../services/postsApi";

const previewPost = ref(null);

onMounted(async () => {
  try {
    const viewer = await fetchDemoUser();
    const posts = await fetchPostsByUser({ userId: viewer.id, limit: 1, offset: 0 });
    previewPost.value = posts?.[0] || null;
  } catch {
    previewPost.value = null;
  }
});
</script>

<style scoped>
.mobile-page {
  min-height: 100vh;
  background: #ffffff;
  display: grid;
  place-items: center;
  padding: 12px;
}
</style>
