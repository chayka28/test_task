<template>
  <main class="feed-page">
    <div class="feed-shell">
      <FeedSidebar
        :collapsed="isSidebarCollapsed"
        :creative-expanded="isCreativeExpanded"
        :is-authenticated="isAuthenticated"
        :active-view="viewMode === 'favorites' ? 'favorites' : 'feed'"
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
            @open-user-posts="handleOpenUserPosts"
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
        @view-posts="handleOpenMyPosts"
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
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
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
  updatePost,
  updateUserName,
} from "../services/postsApi";
import { buildPostMetricValues, buildPostTopic, buildUserHandle } from "../services/postPresentation";
import { clearFavoritePostIds, clearSession, loadFavoritePostIds, loadSession, saveFavoritePostIds, saveSession } from "../services/localState";

const props = defineProps({
  viewMode: {
    type: String,
    default: "feed",
  },
  routeUserId: {
    type: Number,
    default: null,
  },
});

const router = useRouter();
const pageSize = 12;

const posts = ref([]);
const selectedPost = ref(null);
const session = ref(loadSession());
const ownPostsCount = ref(0);
const authorFeedName = ref("");

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
const isMobileLayout = ref(false);

let toastTimerId = null;

const isAuthenticated = computed(() => Boolean(session.value?.accessToken));
const isFavoritesView = computed(() => props.viewMode === "favorites");
const isOwnPostsView = computed(() => props.viewMode === "my-posts");
const isUserPostsView = computed(() => props.viewMode === "user");

const currentSource = computed(() => {
  if (isOwnPostsView.value) {
    if (!session.value?.user?.id) {
      return { type: "auth-required" };
    }

    return {
      type: "user",
      userId: session.value.user.id,
      label: session.value.user.name || "Мои публикации",
    };
  }

  if (isUserPostsView.value) {
    if (!props.routeUserId) {
      return { type: "empty" };
    }

    return {
      type: "user",
      userId: props.routeUserId,
      label: authorFeedName.value || "Публикации автора",
    };
  }

  return { type: "feed" };
});

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
      const authorHandle = buildUserHandle(post.user_name, post.user_id);
      return `${post.title} ${post.text} ${post.user_name || ""} ${authorHandle} ${buildPostTopic(post.id)}`
        .toLowerCase()
        .includes(normalizedQuery);
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

  if (isFavoritesView.value) {
    return "Избранные";
  }

  if (isOwnPostsView.value) {
    return "Мои публикации";
  }

  if (isUserPostsView.value) {
    return currentSource.value.label;
  }

  return "Business history";
});

const emptyStateText = computed(() => {
  if (isFavoritesView.value && !isAuthenticated.value) {
    return "Войдите в аккаунт, чтобы сохранять публикации в избранное.";
  }

  if (isFavoritesView.value) {
    return "В избранном пока нет публикаций.";
  }

  if (isOwnPostsView.value && !isAuthenticated.value) {
    return "Войдите в аккаунт, чтобы открыть свои публикации.";
  }

  if (isOwnPostsView.value) {
    return "У вас пока нет публикаций.";
  }

  if (isUserPostsView.value) {
    return "У этого пользователя пока нет публикаций.";
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
  if (currentSource.value.type === "auth-required" || currentSource.value.type === "empty") {
    hasMore.value = false;
    return;
  }

  if (offset.value === 0) {
    isInitialLoading.value = true;
  } else {
    isLoadingMore.value = true;
  }

  errorText.value = "";

  try {
    const nextPosts =
      currentSource.value.type === "feed"
        ? await fetchFeedPosts({ limit: pageSize, offset: offset.value })
        : await fetchPostsByUser({
            userId: currentSource.value.userId,
            limit: pageSize,
            offset: offset.value,
          });

    if (currentSource.value.type === "user" && offset.value === 0) {
      authorFeedName.value = nextPosts[0]?.user_name || currentSource.value.label || "Публикации автора";
    }

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
  if (!isUserPostsView.value) {
    authorFeedName.value = "";
  }
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

function handleOpenUserPosts(post) {
  router.push(`/users/${post.user_id}/posts`);
}

function handleOpenMyPosts() {
  if (!session.value?.accessToken) {
    handleAuthRequired("Просмотр своих публикаций");
    return;
  }

  isProfileModalOpen.value = false;
  router.push("/my-posts");
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

    await refreshOwnPostsCount();
    isAuthModalOpen.value = false;
    await reloadFeed();
    showToast("Аккаунт создан", "Теперь доступны профиль, избранное и свои публикации.");
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

    await refreshOwnPostsCount();
    isAuthModalOpen.value = false;
    await reloadFeed();
    showToast("Вход выполнен", "Можно продолжать работу с публикациями.");
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
      nextPost = { ...nextPost, user_name: session.value.user.name };
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
      nextPost = { ...nextPost, user_name: session.value.user.name };
      showToast("Публикация обновлена", "Изменения сохранены и уже отображаются в ленте.");
    }

    isPostEditorOpen.value = false;
    postEditorInitialPost.value = null;
    await refreshOwnPostsCount();
    await reloadFeed();
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
    await refreshOwnPostsCount();
    await reloadFeed();
    showToast("Публикация удалена", "Карточка больше не отображается в ленте.");
  } catch (error) {
    showToast("Не удалось удалить публикацию", error.message);
  } finally {
    isPostDeleting.value = false;
  }
}

async function handleFindMoreClick() {
  try {
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
  ownPostsCount.value = 0;
  favoritePostIds.value = new Set();

  if (isFavoritesView.value || isOwnPostsView.value) {
    await router.push("/");
  }

  await reloadFeed();
  showToast("Вы вышли из аккаунта", "Доступны только публичные функции без авторизации.");
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
    ownPostsCount.value = 0;
    favoritePostIds.value = new Set();

    if (isFavoritesView.value || isOwnPostsView.value) {
      await router.push("/");
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
  showToast(`${label} недоступно`, "Функция пока недоступна.");
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

async function handleNavigate(target) {
  if (target === "favorites" && !isAuthenticated.value) {
    handleAuthRequired("Избранное");
    return;
  }

  if (target === "feed") {
    await router.push("/");
    return;
  }

  if (target === "favorites") {
    await router.push("/favorites");
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

function syncResponsiveLayout() {
  const nextIsMobileLayout = window.innerWidth <= 980;

  if (nextIsMobileLayout && !isMobileLayout.value) {
    isSidebarCollapsed.value = true;
  }

  isMobileLayout.value = nextIsMobileLayout;
}

async function bootstrap() {
  errorText.value = "";

  if (isAuthenticated.value && session.value?.user?.id) {
    favoritePostIds.value = loadFavoritePostIds(session.value.user.id);
    await refreshOwnPostsCount();
  } else {
    favoritePostIds.value = new Set();
    ownPostsCount.value = 0;
  }

  await reloadFeed();
  window.scrollTo({ top: 0, behavior: "auto" });
}

watch(
  () => [props.viewMode, props.routeUserId],
  async () => {
    await bootstrap();
  },
);

onMounted(async () => {
  syncResponsiveLayout();
  await bootstrap();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", syncResponsiveLayout, { passive: true });
  onScroll();
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", onScroll);
  window.removeEventListener("resize", syncResponsiveLayout);

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
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  justify-content: stretch;
  justify-items: center;
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
    padding: 8px 12px 92px;
  }

  .post-grid {
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 14px;
  }
}

@media (max-width: 980px) {
  .feed-shell {
    flex-direction: column;
  }

  .content-area {
    width: 100%;
    padding: 10px 10px 120px;
  }

  .post-grid {
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  }

  .floating-actions {
    right: 10px;
    left: 10px;
    bottom: 10px;
    justify-content: stretch;
    flex-direction: column;
    align-items: stretch;
  }

  .more-btn,
  .counter-pill {
    width: 100%;
    justify-content: center;
    font-size: 14px;
  }

  .toast-wrap {
    left: 10px;
    right: 10px;
    transform: none;
    bottom: 74px;
  }
}

@media (max-width: 640px) {
  .content-area {
    padding: 8px 8px 124px;
  }

  .post-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}
</style>
