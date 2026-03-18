<template>
  <main class="feed-page">
    <div class="feed-shell">
      <FeedSidebar
        :collapsed="isSidebarCollapsed"
        :creative-expanded="isCreativeExpanded"
        :is-authenticated="isAuthenticated"
        :active-view="viewMode"
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
        @navigate="handleNavigate"
        @placeholder="handlePlaceholder"
      />

      <section class="content-area">
        <FeedTopPanel
          v-model:query="searchQuery"
          v-model:selectedTopic="selectedTopic"
          :loaded-count="visiblePosts.length"
          :sort-mode="sortMode"
          :results-title="resultsTitle"
          @update:sortMode="sortMode = $event"
          @search="handleSearch"
          @placeholder="handlePlaceholder"
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
            @auth-required="handleAuthRequired"
            @placeholder="handlePlaceholder"
          />
        </section>

        <div class="state-line">
          <LoadingIndicator v-if="isInitialLoading" label="Загружаем публикации..." />
          <LoadingIndicator v-else-if="isLoadingMore" label="Подгружаем еще..." />
          <p v-else-if="errorText" class="error-state">{{ errorText }}</p>
          <p v-else-if="!visiblePosts.length" class="empty-state">{{ emptyStateText }}</p>
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
        :can-manage-post="canManageSelectedPost"
        :is-saving="isPostSaving"
        :is-deleting="isPostDeleting"
        @close="selectedPost = null"
        @edit="openPostEditor('edit', $event)"
        @delete="handleDeletePost"
        @placeholder="handlePlaceholder"
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
        :posts-count="ownPostsCount"
        :is-loading="isProfileSaving"
        :is-deleting="isUserDeleting"
        @close="isProfileModalOpen = false"
        @save="handleProfileSave"
        @create-post="openPostEditor('create')"
        @delete-account="handleDeleteAccount"
        @logout="handleLogout"
      />
    </Transition>

    <Transition name="auth-fade">
      <PostEditorModal
        v-if="isPostEditorOpen"
        :mode="postEditorMode"
        :initial-post="postEditorInitialPost"
        :is-loading="isPostSaving"
        @close="closePostEditor"
        @submit="handlePostEditorSubmit"
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
import { useRouter } from "vue-router";

import AuthModal from "../components/AuthModal.vue";
import FeedPostCard from "../components/FeedPostCard.vue";
import FeedSidebar from "../components/FeedSidebar.vue";
import FeedTopPanel from "../components/FeedTopPanel.vue";
import LoadingIndicator from "../components/LoadingIndicator.vue";
import PlaceholderToast from "../components/PlaceholderToast.vue";
import PostEditorModal from "../components/PostEditorModal.vue";
import PostDetailsModal from "../components/PostDetailsModal.vue";
import ProfileModal from "../components/ProfileModal.vue";
import {
  createPost,
  deletePost,
  deleteUserById,
  fetchFeedPosts,
  fetchPostsByUser,
  loginUser,
  registerUser,
  seedDemoPosts,
  updatePost,
  updateUserName,
} from "../services/postsApi";
import { buildPostMetricValues, buildPostTopic } from "../services/postPresentation";
import { clearFavoritePostIds, clearSession, loadFavoritePostIds, loadSession, saveFavoritePostIds, saveSession } from "../services/localState";

const props = defineProps({
  viewMode: {
    type: String,
    default: "feed",
  },
});

const router = useRouter();

const pageSize = 12;

const posts = ref([]);
const selectedPost = ref(null);
const session = ref(loadSession());
const ownPostsCount = ref(0);

const isInitialLoading = ref(false);
const isLoadingMore = ref(false);
const isAuthBusy = ref(false);
const isProfileSaving = ref(false);
const isUserDeleting = ref(false);
const isPostSaving = ref(false);
const isPostDeleting = ref(false);
const hasMore = ref(true);
const errorText = ref("");
const authErrorText = ref("");
const offset = ref(0);

const isSidebarCollapsed = ref(false);
const isCreativeExpanded = ref(false);
const isAuthModalOpen = ref(false);
const isProfileModalOpen = ref(false);
const isPostEditorOpen = ref(false);
const authMode = ref("register");
const toastState = ref(null);
const postEditorMode = ref("create");
const postEditorInitialPost = ref(null);
const favoritePostIds = ref(loadFavoritePostIds(session.value?.user?.id));

const searchQuery = ref("");
const selectedTopic = ref("");
const sortMode = ref("all");

let toastTimerId = null;

const isAuthenticated = computed(() => Boolean(session.value?.accessToken));
const isFavoritesView = computed(() => props.viewMode === "favorites");

const visiblePosts = computed(() => {
  const normalizedQuery = searchQuery.value.trim().toLowerCase();
  let result = [...posts.value];

  if (isFavoritesView.value) {
    result = result.filter((post) => favoritePostIds.value.has(post.id));
  }

  if (selectedTopic.value) {
    result = result.filter((post) => buildPostTopic(post.id) === selectedTopic.value);
  }

  if (normalizedQuery) {
    result = result.filter((post) => {
      return `${post.title} ${post.text} ${buildPostTopic(post.id)}`.toLowerCase().includes(normalizedQuery);
    });
  }

  if (sortMode.value === "likes") {
    result.sort((left, right) => buildPostMetricValues(right.id).likes - buildPostMetricValues(left.id).likes);
  } else {
    result.sort((left, right) => new Date(right.created_at) - new Date(left.created_at));
  }

  return result;
});

const resultsTitle = computed(() => {
  if (searchQuery.value.trim()) {
    return searchQuery.value.trim();
  }

  return isFavoritesView.value ? "Избранные" : "Business history";
});

const emptyStateText = computed(() => {
  if (isFavoritesView.value && !isAuthenticated.value) {
    return "Войдите в аккаунт, чтобы сохранять публикации в избранное.";
  }

  if (isFavoritesView.value) {
    return "В избранном пока нет публикаций.";
  }

  return "По текущему фильтру публикации не найдены";
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
const tokenTotal = computed(() => 4200 + (session.value?.user?.id || 1) * 37);
const tokenUsed = computed(() => Math.min(tokenTotal.value, 680 + posts.value.length * 19));
const estimatedTotal = computed(() => (hasMore.value ? Math.max(3000, posts.value.length * 120) : posts.value.length));
const canManageSelectedPost = computed(() => {
  return Boolean(
    isAuthenticated.value &&
      session.value?.user?.id &&
      selectedPost.value &&
      session.value.user.id === selectedPost.value.user_id,
  );
});

async function loadNextBatch() {
  if (!hasMore.value || isInitialLoading.value || isLoadingMore.value) return;

  if (offset.value === 0) {
    isInitialLoading.value = true;
  } else {
    isLoadingMore.value = true;
  }

  errorText.value = "";

  try {
    const nextPosts = await fetchFeedPosts({
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
  const viewportBottom = window.scrollY + window.innerHeight;
  const threshold = document.documentElement.scrollHeight - 500;

  if (viewportBottom >= threshold) {
    loadNextBatch();
  }
}

async function reloadFeed() {
  posts.value = [];
  selectedPost.value = null;
  offset.value = 0;
  hasMore.value = true;
  await loadNextBatch();
}

async function refreshOwnPostsCount() {
  if (!session.value?.user?.id) {
    ownPostsCount.value = 0;
    return;
  }

  try {
    const ownPosts = await fetchPostsByUser({
      userId: session.value.user.id,
      limit: 50,
      offset: 0,
    });
    ownPostsCount.value = ownPosts.length;
  } catch {
    ownPostsCount.value = posts.value.filter((post) => post.user_id === session.value?.user?.id).length;
  }
}

function openPost(post) {
  selectedPost.value = post;
}

function openPostEditor(mode, post = null) {
  if (!session.value?.accessToken) {
    handleAuthRequired(mode === "create" ? "Создание публикации" : "Редактирование публикации");
    return;
  }

  if (mode === "edit" && post?.user_id !== session.value?.user?.id) {
    showToast("Редактирование недоступно", "Изменять можно только свои публикации.");
    return;
  }

  isProfileModalOpen.value = false;
  postEditorMode.value = mode;
  postEditorInitialPost.value = post ? { ...post } : null;
  isPostEditorOpen.value = true;
}

function closePostEditor() {
  if (isPostSaving.value) return;
  isPostEditorOpen.value = false;
  postEditorInitialPost.value = null;
}

function openAuthModal(mode = "register") {
  authErrorText.value = "";
  authMode.value = mode;
  isAuthModalOpen.value = true;
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
    favoritePostIds.value = loadFavoritePostIds(response.user.id);

    await seedDemoPosts({
      token: nextSession.accessToken,
      count: 4,
      append: false,
    });

    isAuthModalOpen.value = false;
    await reloadFeed();
    await refreshOwnPostsCount();
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
    favoritePostIds.value = loadFavoritePostIds(response.user.id);

    isAuthModalOpen.value = false;
    await reloadFeed();
    await refreshOwnPostsCount();
    showToast("Вход выполнен", "Можно продолжать работу с личной лентой.");
  } catch (error) {
    authErrorText.value = error.message;
  } finally {
    isAuthBusy.value = false;
  }
}

async function handleProfileSave(payload) {
  if (!session.value?.user?.id) return;

  isProfileSaving.value = true;

  try {
    const updatedUser = await updateUserName({
      userId: session.value.user.id,
      name: payload.name,
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

async function handlePostEditorSubmit(payload) {
  if (!session.value?.accessToken) return;

  isPostSaving.value = true;

  try {
    let nextPost;

    if (postEditorMode.value === "create") {
      nextPost = await createPost({
        token: session.value.accessToken,
        title: payload.title,
        text: payload.text,
        videoUrl: payload.videoUrl,
        posterUrl: payload.posterUrl,
        sourceUrl: payload.sourceUrl,
      });
      showToast("Публикация создана", "Новая карточка добавлена в вашу ленту.");
    } else {
      nextPost = await updatePost({
        token: session.value.accessToken,
        postId: postEditorInitialPost.value.id,
        title: payload.title,
        text: payload.text,
        videoUrl: payload.videoUrl,
        posterUrl: payload.posterUrl,
        sourceUrl: payload.sourceUrl,
      });
      showToast("Публикация обновлена", "Изменения сохранены и уже отображаются в ленте.");
    }

    isPostEditorOpen.value = false;
    postEditorInitialPost.value = null;
    await reloadFeed();
    await refreshOwnPostsCount();
    selectedPost.value = nextPost;
  } catch (error) {
    showToast("Не удалось сохранить публикацию", error.message);
  } finally {
    isPostSaving.value = false;
  }
}

async function handleDeletePost(post) {
  if (!session.value?.accessToken || !post?.id) return;
  if (post.user_id !== session.value?.user?.id) {
    showToast("Удаление недоступно", "Удалять можно только свои публикации.");
    return;
  }
  if (!window.confirm("Удалить эту публикацию?")) return;

  isPostDeleting.value = true;

  try {
    await deletePost({
      token: session.value.accessToken,
      postId: post.id,
    });
    selectedPost.value = null;
    await reloadFeed();
    await refreshOwnPostsCount();
    showToast("Публикация удалена", "Карточка больше не отображается в вашей ленте.");
  } catch (error) {
    showToast("Не удалось удалить публикацию", error.message);
  } finally {
    isPostDeleting.value = false;
  }
}

async function handleFindMoreClick() {
  try {
    if (isLoadingMore.value || isInitialLoading.value) {
      return;
    }

    if (!hasMore.value) {
      showToast("Больше публикаций нет", "Нижняя граница ленты уже достигнута.");
      return;
    }

    await loadNextBatch();
    showToast("Лента обновлена", "Загружена следующая порция публикаций.");
  } catch (error) {
    showToast("Не удалось загрузить новые ролики", error.message);
  }
}

async function handleLogout() {
  clearSession();
  session.value = null;
  isProfileModalOpen.value = false;
  favoritePostIds.value = new Set();
  ownPostsCount.value = 0;

  if (isFavoritesView.value) {
    router.push("/");
  }

  try {
    await reloadFeed();
    showToast("Вы вышли из аккаунта", "На главной странице остались только функции, доступные без авторизации.");
  } catch (error) {
    errorText.value = error.message;
  }
}

async function handleDeleteAccount() {
  if (!session.value?.user?.id) return;
  if (!window.confirm("Удалить аккаунт и связанные публикации?")) return;

  isUserDeleting.value = true;

  try {
    const currentUserId = session.value.user.id;
    await deleteUserById(currentUserId);
    clearFavoritePostIds(currentUserId);
    clearSession();
    session.value = null;
    isProfileModalOpen.value = false;
    selectedPost.value = null;
    favoritePostIds.value = new Set();
    ownPostsCount.value = 0;

    if (isFavoritesView.value) {
      router.push("/");
    }

    await reloadFeed();
    showToast("Аккаунт удален", "Вы вернулись в публичный режим просмотра.");
  } catch (error) {
    showToast("Не удалось удалить аккаунт", error.message);
  } finally {
    isUserDeleting.value = false;
  }
}

function handlePlaceholder(label) {
  const payload = {
    title: `${label} недоступно`,
    text: "Функция пока недоступна.",
  };

  showToast(payload.title, payload.text);
}

function handleAuthRequired(reason) {
  openAuthModal("login");
  showToast("Нужно войти в аккаунт", `${reason} доступно только после регистрации или входа.`);
}

function isPostLiked(postId) {
  return favoritePostIds.value.has(postId);
}

function toggleLike(post) {
  if (!session.value?.user?.id) {
    handleAuthRequired("Избранное");
    return;
  }

  const nextSet = new Set(favoritePostIds.value);

  if (nextSet.has(post.id)) {
    nextSet.delete(post.id);
    showToast("Удалено из избранного", "Публикация убрана из сохраненного списка.");
  } else {
    nextSet.add(post.id);
    showToast("Добавлено в избранное", "Публикация сохранена в избранном.");
  }

  favoritePostIds.value = nextSet;
  saveFavoritePostIds(session.value.user.id, nextSet);
}

function handleNavigate(target) {
  if (target === "favorites" && !isAuthenticated.value) {
    handleAuthRequired("Избранное");
    return;
  }

  if (target === "feed") {
    router.push("/");
    return;
  }

  if (target === "favorites") {
    router.push("/favorites");
  }
}

function handleSearch() {
  if (!visiblePosts.value.length && hasMore.value && !isInitialLoading.value && !isLoadingMore.value) {
    requestAnimationFrame(onScroll);
  }

  showToast("Лента обновлена", `По текущим фильтрам показано ${visiblePosts.value.length} публикаций.`);
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
      favoritePostIds.value = loadFavoritePostIds(session.value.user.id);
      await refreshOwnPostsCount();
    } else {
      favoritePostIds.value = new Set();
      ownPostsCount.value = 0;
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


