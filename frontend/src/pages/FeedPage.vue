<template>
  <main class="feed-page">
    <div class="feed-shell">
      <FeedSidebar
        :collapsed="isSidebarCollapsed"
        :creative-expanded="isCreativeExpanded"
        :is-authenticated="isAuthenticated"
        :radar-count="radarCount"
        :token-used="tokenUsed"
        :token-total="tokenTotal"
        :profile-name="profileName"
        :profile-phone="profilePhone"
        @toggle-sidebar="isSidebarCollapsed = !isSidebarCollapsed"
        @toggle-creative="isCreativeExpanded = !isCreativeExpanded"
        @open-auth="openAuthModal"
        @logout="handleLogout"
      />

      <section class="content-area">
        <section class="post-grid">
          <FeedPostCard
            v-for="post in posts"
            :key="post.id"
            :post="post"
            :liked="isPostLiked(post.id)"
            @open="openPost"
            @toggle-like="toggleLike"
          />
        </section>

        <div class="state-line">
          <LoadingIndicator v-if="isInitialLoading" label="Загрузка публикаций..." />
          <LoadingIndicator v-else-if="isLoadingMore" label="Подгружаем ещё..." />
          <p v-else-if="errorText" class="error-state">{{ errorText }}</p>
          <p v-else-if="!posts.length" class="empty-state">Публикации не найдены</p>
          <p v-else-if="!hasMore" class="empty-state">Больше публикаций нет</p>
        </div>

        <div class="floating-actions">
          <button type="button" class="more-btn" :disabled="isGeneratingBatch" @click="handleFindMoreClick">
            <img src="/assets/icons/Vector-5.png" alt="" />
            <span>{{ isGeneratingBatch ? "Подбираем..." : "Найти еще ролики" }}</span>
          </button>
          <div class="counter-pill">
            <img src="/assets/icons/Vector-12.png" alt="" />
            <span>Видео: {{ posts.length }} из {{ estimatedTotal }}</span>
          </div>
        </div>
      </section>
    </div>

    <Transition name="modal-fade">
      <PostDetailsModal v-if="selectedPost" :post="selectedPost" @close="selectedPost = null" />
    </Transition>

    <Transition name="auth-fade">
      <AuthModal
        v-if="isAuthModalOpen"
        :is-loading="isRegistering"
        :error-text="authErrorText"
        @submit="handleRegister"
        @close="isAuthModalOpen = false"
      />
    </Transition>
  </main>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

import AuthModal from "../components/AuthModal.vue";
import FeedPostCard from "../components/FeedPostCard.vue";
import FeedSidebar from "../components/FeedSidebar.vue";
import LoadingIndicator from "../components/LoadingIndicator.vue";
import PostDetailsModal from "../components/PostDetailsModal.vue";
import { fetchDemoUser, fetchPostsByUser, registerUser, seedDemoPosts } from "../services/postsApi";
import { clearSession, loadLikedPostIds, loadSession, saveLikedPostIds, saveSession } from "../services/localState";

const pageSize = 12;

const posts = ref([]);
const selectedPost = ref(null);
const viewerUserId = ref(null);
const demoUser = ref(null);
const session = ref(loadSession());
const likedPostIds = ref(loadLikedPostIds());

const isInitialLoading = ref(false);
const isLoadingMore = ref(false);
const isGeneratingBatch = ref(false);
const isRegistering = ref(false);
const hasMore = ref(true);
const errorText = ref("");
const authErrorText = ref("");
const offset = ref(0);

const isSidebarCollapsed = ref(false);
const isCreativeExpanded = ref(false);
const isAuthModalOpen = ref(false);

const isAuthenticated = computed(() => Boolean(session.value?.accessToken));
const activeViewer = computed(() => session.value?.user || demoUser.value || null);

const profileName = computed(() => activeViewer.value?.name || "Гостевой режим");
const profilePhone = computed(() => {
  if (isAuthenticated.value && activeViewer.value?.id) {
    return `+7 (9${(activeViewer.value.id % 9) + 10}) 99${activeViewer.value.id % 10}-99-99`;
  }
  return "Создайте аккаунт, чтобы сохранить свою ленту";
});

const radarCount = computed(() => Math.min(999, 120 + posts.value.length * 7));
const tokenTotal = computed(() => 4200 + (activeViewer.value?.id || 1) * 37);
const tokenUsed = computed(() => Math.min(tokenTotal.value, 680 + posts.value.length * 19));
const estimatedTotal = computed(() => (hasMore.value ? Math.max(3000, posts.value.length * 120) : posts.value.length));

async function loadNextBatch() {
  if (!viewerUserId.value || !hasMore.value || isInitialLoading.value || isLoadingMore.value) return;

  if (offset.value === 0) {
    isInitialLoading.value = true;
  } else {
    isLoadingMore.value = true;
  }
  errorText.value = "";

  try {
    const nextPosts = await fetchPostsByUser({
      userId: viewerUserId.value,
      limit: pageSize,
      offset: offset.value,
    });

    posts.value = offset.value === 0 ? nextPosts : [...posts.value, ...nextPosts];
    offset.value += nextPosts.length;
    if (nextPosts.length < pageSize) hasMore.value = false;
  } catch (error) {
    errorText.value = error.message;
  } finally {
    isInitialLoading.value = false;
    isLoadingMore.value = false;
    requestAnimationFrame(onScroll);
  }
}

function onScroll() {
  if (!viewerUserId.value) return;
  const viewportBottom = window.scrollY + window.innerHeight;
  const threshold = document.documentElement.scrollHeight - 500;
  if (viewportBottom >= threshold) loadNextBatch();
}

async function reloadFeed() {
  if (!viewerUserId.value) return;
  posts.value = [];
  selectedPost.value = null;
  offset.value = 0;
  hasMore.value = true;
  await loadNextBatch();
}

async function loadDemoViewer() {
  demoUser.value = await fetchDemoUser();
  viewerUserId.value = demoUser.value.id;
}

function openPost(post) {
  selectedPost.value = post;
}

function openAuthModal() {
  authErrorText.value = "";
  isAuthModalOpen.value = true;
}

function isPostLiked(postId) {
  return likedPostIds.value.has(postId);
}

function toggleLike(postId) {
  const nextLikedPostIds = new Set(likedPostIds.value);

  if (nextLikedPostIds.has(postId)) {
    nextLikedPostIds.delete(postId);
  } else {
    nextLikedPostIds.add(postId);
  }

  likedPostIds.value = nextLikedPostIds;
  saveLikedPostIds(nextLikedPostIds);
}

async function handleRegister(name) {
  isRegistering.value = true;
  authErrorText.value = "";

  try {
    const response = await registerUser({ name });
    const nextSession = {
      accessToken: response.access_token,
      tokenType: response.token_type,
      user: response.user,
    };

    saveSession(nextSession);
    session.value = nextSession;
    demoUser.value = null;
    viewerUserId.value = response.user.id;

    await seedDemoPosts({
      token: nextSession.accessToken,
      count: 18,
      append: false,
    });

    isAuthModalOpen.value = false;
    await reloadFeed();
  } catch (error) {
    authErrorText.value = error.message;
  } finally {
    isRegistering.value = false;
  }
}

async function handleFindMoreClick() {
  if (!isAuthenticated.value || !session.value?.accessToken) {
    openAuthModal();
    return;
  }

  isGeneratingBatch.value = true;

  try {
    await seedDemoPosts({
      token: session.value.accessToken,
      count: 8,
      append: true,
    });
    await reloadFeed();
  } catch (error) {
    errorText.value = error.message;
  } finally {
    isGeneratingBatch.value = false;
  }
}

async function handleLogout() {
  clearSession();
  session.value = null;
  isCreativeExpanded.value = false;
  openAuthModal();

  try {
    await loadDemoViewer();
    await reloadFeed();
  } catch (error) {
    errorText.value = error.message;
  }
}

async function bootstrap() {
  try {
    if (isAuthenticated.value && session.value?.user?.id) {
      viewerUserId.value = session.value.user.id;
    } else {
      await loadDemoViewer();
      isAuthModalOpen.value = true;
    }

    await reloadFeed();
  } catch (error) {
    errorText.value = error.message;
  }
}

onMounted(async () => {
  await bootstrap();
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", onScroll);
});
</script>

<style scoped>
.feed-page {
  min-height: 100vh;
  width: 100%;
  background: #f4f5f6;
  padding: 0;
}

.feed-shell {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: stretch;
  background: #ffffff;
}

.content-area {
  flex: 1;
  background: #ffffff;
  padding: 8px 16px 96px;
  position: relative;
}

.post-grid {
  margin-top: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, 220px);
  gap: 16px;
  justify-content: flex-start;
  align-content: start;
  width: 100%;
}

.state-line {
  margin-top: 8px;
  min-height: 30px;
}

.empty-state,
.error-state {
  margin: 0;
  font-size: 13px;
}

.empty-state {
  color: #667390;
}

.error-state {
  color: #cb4051;
}

.floating-actions {
  position: fixed;
  right: 20px;
  bottom: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 10;
}

.more-btn {
  height: 52px;
  border: 0;
  border-radius: 18px;
  background: #2b31b3;
  color: #ffffff;
  padding: 0 24px;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 700;
  line-height: 1;
  cursor: pointer;
  letter-spacing: 0.2px;
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}

.more-btn:disabled {
  opacity: 0.7;
  cursor: default;
}

.more-btn:not(:disabled):hover {
  transform: translateY(-1px);
}

.more-btn img {
  width: 19px;
  height: 18px;
}

.counter-pill {
  height: 52px;
  border-radius: 26px;
  background: rgba(32, 32, 32, 0.78);
  color: #ffffff;
  padding: 0 20px;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  line-height: 1;
}

.counter-pill img {
  width: 20px;
  height: 20px;
}

.modal-fade-enter-active,
.modal-fade-leave-active,
.auth-fade-enter-active,
.auth-fade-leave-active {
  transition:
    opacity 0.22s ease,
    transform 0.22s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to,
.auth-fade-enter-from,
.auth-fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (max-width: 1280px) {
  .content-area {
    padding: 8px 10px 92px;
  }

  .post-grid {
    grid-template-columns: repeat(auto-fill, 220px);
    gap: 12px;
  }
}

@media (max-width: 980px) {
  .feed-shell {
    flex-direction: column;
  }

  .content-area {
    width: 100%;
  }

  .post-grid {
    justify-items: center;
    grid-template-columns: 1fr;
  }

  .floating-actions {
    right: 10px;
    left: 10px;
    bottom: 10px;
    justify-content: space-between;
  }

  .counter-pill {
    font-size: 14px;
  }
}
</style>
