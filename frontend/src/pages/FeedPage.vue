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
        :profile-avatar="profileAvatar"
        :avatar-seed="avatarSeed"
        @toggle-sidebar="isSidebarCollapsed = !isSidebarCollapsed"
        @toggle-creative="isCreativeExpanded = !isCreativeExpanded"
        @open-auth="openAuthModal('register')"
        @open-profile="isProfileModalOpen = true"
        @placeholder="handlePlaceholder"
      />

      <section class="content-area">
        <FeedTopPanel
          v-model:query="searchQuery"
          v-model:selectedTopic="selectedTopic"
          :loaded-count="visiblePosts.length"
          :can-interact="isAuthenticated"
          @update:sortMode="sortMode = $event"
          @search="handleSearch"
          @placeholder="handlePlaceholder"
          @auth-required="handleAuthRequired"
        />

        <section class="post-grid">
          <FeedPostCard
            v-for="post in visiblePosts"
            :key="post.id"
            :post="post"
            :liked="isPostLiked(post.id)"
            :can-interact="isAuthenticated"
            @open="openPost"
            @toggle-like="toggleLike"
            @placeholder="handlePlaceholder"
            @auth-required="handleAuthRequired"
          />
        </section>

        <div class="state-line">
          <LoadingIndicator v-if="isInitialLoading" label="Загружаем публикации..." />
          <LoadingIndicator v-else-if="isLoadingMore" label="Подгружаем еще..." />
          <p v-else-if="errorText" class="error-state">{{ errorText }}</p>
          <p v-else-if="!visiblePosts.length" class="empty-state">По текущему фильтру публикации не найдены</p>
          <p v-else-if="!hasMore" class="empty-state">Больше публикаций нет</p>
        </div>

        <div class="floating-actions">
          <button type="button" class="more-btn" @click="handleFindMoreClick">
            <img src="/assets/icons/Vector-5.png" alt="" />
            <span>Найти еще ролики</span>
          </button>
          <div class="counter-pill">
            <img src="/assets/icons/Vector-12.png" alt="" />
            <span>Видео: {{ visiblePosts.length }} из {{ estimatedTotal }}</span>
          </div>
        </div>
      </section>
    </div>

    <Transition name="modal-fade">
      <PostDetailsModal
        v-if="selectedPost"
        :post="selectedPost"
        :can-interact="isAuthenticated"
        @close="selectedPost = null"
        @placeholder="handlePlaceholder"
        @auth-required="handleAuthRequired"
      />
    </Transition>

    <Transition name="auth-fade">
      <AuthModal
        v-if="isAuthModalOpen"
        :is-loading="isAuthBusy"
        :error-text="authErrorText"
        :initial-mode="authMode"
        @register="handleRegister"
        @login="handleLogin"
        @close="isAuthModalOpen = false"
      />
    </Transition>

    <Transition name="auth-fade">
      <ProfileModal
        v-if="isProfileModalOpen && session?.user"
        :user="session.user"
        :is-loading="isProfileSaving"
        @close="isProfileModalOpen = false"
        @save="handleProfileSave"
        @logout="handleLogout"
      />
    </Transition>

    <Transition name="toast-fade">
      <div v-if="toastState" class="toast-wrap">
        <PlaceholderToast :title="toastState.title" :text="toastState.text" />
      </div>
    </Transition>
  </main>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

import AuthModal from "../components/AuthModal.vue";
import FeedPostCard from "../components/FeedPostCard.vue";
import FeedSidebar from "../components/FeedSidebar.vue";
import FeedTopPanel from "../components/FeedTopPanel.vue";
import LoadingIndicator from "../components/LoadingIndicator.vue";
import PlaceholderToast from "../components/PlaceholderToast.vue";
import PostDetailsModal from "../components/PostDetailsModal.vue";
import ProfileModal from "../components/ProfileModal.vue";
import { fetchDemoUser, fetchPostsByUser, loginUser, registerUser, seedDemoPosts, updateMyProfile } from "../services/postsApi";
import { clearSession, loadLikedPostIds, loadSession, saveLikedPostIds, saveSession } from "../services/localState";

const pageSize = 12;

const posts = ref([]);
const selectedPost = ref(null);
const viewerUserId = ref(null);
const publicViewer = ref(null);
const session = ref(loadSession());
const likedPostIds = ref(loadLikedPostIds());

const isInitialLoading = ref(false);
const isLoadingMore = ref(false);
const isAuthBusy = ref(false);
const isProfileSaving = ref(false);
const hasMore = ref(true);
const errorText = ref("");
const authErrorText = ref("");
const offset = ref(0);

const isSidebarCollapsed = ref(false);
const isCreativeExpanded = ref(false);
const isAuthModalOpen = ref(false);
const isProfileModalOpen = ref(false);
const authMode = ref("register");
const toastState = ref(null);

const searchQuery = ref("");
const selectedTopic = ref("Базы данных");
const sortMode = ref("all");

let toastTimerId = null;

const isAuthenticated = computed(() => Boolean(session.value?.accessToken));
const activeViewer = computed(() => session.value?.user || publicViewer.value || null);

const visiblePosts = computed(() => {
  const normalizedQuery = searchQuery.value.trim().toLowerCase();
  let result = [...posts.value];

  if (normalizedQuery) {
    result = result.filter((post) => {
      return `${post.title} ${post.text}`.toLowerCase().includes(normalizedQuery);
    });
  }

  if (sortMode.value === "likes") {
    result.sort((left, right) => right.id - left.id);
  }

  return result;
});

const profileName = computed(() => {
  if (isAuthenticated.value) {
    return session.value?.user?.name || "Пользователь";
  }

  return "Гость";
});

const profilePhone = computed(() => {
  if (isAuthenticated.value) {
    return session.value?.user?.email || "Аккаунт Trendsee";
  }

  return "Войдите или создайте аккаунт";
});

const profileAvatar = computed(() => session.value?.user?.avatar_data || "");
const avatarSeed = computed(() => session.value?.user?.id || 1);

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

    if (nextPosts.length < pageSize) {
      hasMore.value = false;
    }
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

  if (viewportBottom >= threshold) {
    loadNextBatch();
  }
}

async function reloadFeed() {
  if (!viewerUserId.value) return;

  posts.value = [];
  selectedPost.value = null;
  offset.value = 0;
  hasMore.value = true;
  await loadNextBatch();
}

async function loadPublicFeed() {
  publicViewer.value = await fetchDemoUser();
  viewerUserId.value = publicViewer.value.id;
}

function openPost(post) {
  selectedPost.value = post;
}

function openAuthModal(mode = "register") {
  authErrorText.value = "";
  authMode.value = mode;
  isAuthModalOpen.value = true;
}

function isPostLiked(postId) {
  return likedPostIds.value.has(postId);
}

function toggleLike(postId) {
  const nextLikedPostIds = new Set(likedPostIds.value);

  if (nextLikedPostIds.has(postId)) {
    nextLikedPostIds.delete(postId);
    showToast("Публикация убрана из избранного", "Список сохранится в вашем аккаунте на этом устройстве.");
  } else {
    nextLikedPostIds.add(postId);
    showToast("Публикация добавлена в избранное", "Избранное доступно только авторизованному пользователю.");
  }

  likedPostIds.value = nextLikedPostIds;
  saveLikedPostIds(nextLikedPostIds);
}

async function handleRegister(form) {
  isAuthBusy.value = true;
  authErrorText.value = "";

  try {
    const response = await registerUser({
      name: form.name,
      email: form.email,
      password: form.password,
      avatarData: form.avatarData,
    });

    const nextSession = {
      accessToken: response.access_token,
      tokenType: response.token_type,
      user: response.user,
      email: response.user.email,
    };

    saveSession(nextSession);
    session.value = nextSession;
    publicViewer.value = null;
    viewerUserId.value = response.user.id;

    await seedDemoPosts({
      token: nextSession.accessToken,
      count: 18,
      append: false,
    });

    isAuthModalOpen.value = false;
    await reloadFeed();
    showToast("Аккаунт создан", "Теперь доступны избранное, профиль и работа с подборкой.");
  } catch (error) {
    authErrorText.value = error.message;
  } finally {
    isAuthBusy.value = false;
  }
}

async function handleLogin(form) {
  isAuthBusy.value = true;
  authErrorText.value = "";

  try {
    const response = await loginUser({
      email: form.email,
      password: form.password,
    });

    const nextSession = {
      accessToken: response.access_token,
      tokenType: response.token_type,
      user: response.user,
      email: response.user.email,
    };

    saveSession(nextSession);
    session.value = nextSession;
    publicViewer.value = null;
    viewerUserId.value = response.user.id;

    isAuthModalOpen.value = false;
    await reloadFeed();
    showToast("Вход выполнен", "Можно продолжать работу с личной лентой.");
  } catch (error) {
    authErrorText.value = error.message;
  } finally {
    isAuthBusy.value = false;
  }
}

async function handleProfileSave(payload) {
  if (!session.value?.accessToken) return;

  isProfileSaving.value = true;

  try {
    const updatedUser = await updateMyProfile({
      token: session.value.accessToken,
      name: payload.name,
      avatarData: payload.avatarData,
    });

    const nextSession = {
      ...session.value,
      user: updatedUser,
      email: updatedUser.email,
    };

    saveSession(nextSession);
    session.value = nextSession;
    showToast("Профиль сохранен", "Новые данные сразу применены в интерфейсе.");
    isProfileModalOpen.value = false;
  } catch (error) {
    showToast("Не удалось сохранить профиль", error.message);
  } finally {
    isProfileSaving.value = false;
  }
}

async function handleFindMoreClick() {
  if (!session.value?.accessToken) {
    handleAuthRequired("Найти еще ролики");
    return;
  }

  try {
    await seedDemoPosts({
      token: session.value.accessToken,
      count: 8,
      append: true,
    });
    await reloadFeed();
    showToast("Подборка обновлена", "Мы добавили новую пачку роликов в ленту.");
  } catch (error) {
    errorText.value = error.message;
  }
}

async function handleLogout() {
  clearSession();
  session.value = null;
  likedPostIds.value = new Set();
  saveLikedPostIds(new Set());
  isCreativeExpanded.value = false;
  isProfileModalOpen.value = false;

  try {
    await loadPublicFeed();
    await reloadFeed();
    showToast("Вы вышли из аккаунта", "Избранное и расширенные действия снова недоступны.");
  } catch (error) {
    errorText.value = error.message;
  }
}

function handlePlaceholder(label) {
  const payload = {
    title: `${label} пока в разработке`,
    text: "Элемент сохранен как интерактивная заглушка, чтобы сценарий страницы читался как полноценный продукт.",
  };

  showToast(payload.title, payload.text);
}

function handleAuthRequired(reason) {
  openAuthModal("login");
  showToast("Нужно войти в аккаунт", `${reason} доступно только после регистрации или входа.`);
}

function handleSearch() {
  showToast("Фильтр обновлен", `Показано ${visiblePosts.value.length} публикаций по вашему запросу.`);
}

function showToast(title, text = "") {
  toastState.value = { title, text };

  if (toastTimerId) {
    window.clearTimeout(toastTimerId);
  }

  toastTimerId = window.setTimeout(() => {
    toastState.value = null;
    toastTimerId = null;
  }, 2600);
}

async function bootstrap() {
  try {
    if (isAuthenticated.value && session.value?.user?.id) {
      viewerUserId.value = session.value.user.id;
    } else {
      await loadPublicFeed();
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

  if (toastTimerId) {
    window.clearTimeout(toastTimerId);
  }
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
  background: #f8fafc;
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
  transition: transform 0.2s ease;
}

.more-btn:hover {
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

.toast-wrap {
  position: fixed;
  left: 50%;
  bottom: 84px;
  transform: translateX(-50%);
  z-index: 130;
}

.modal-fade-enter-active,
.modal-fade-leave-active,
.auth-fade-enter-active,
.auth-fade-leave-active,
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition:
    opacity 0.22s ease,
    transform 0.22s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to,
.auth-fade-enter-from,
.auth-fade-leave-to,
.toast-fade-enter-from,
.toast-fade-leave-to {
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

  .toast-wrap {
    left: 10px;
    right: 10px;
    transform: none;
    bottom: 74px;
  }
}
</style>
