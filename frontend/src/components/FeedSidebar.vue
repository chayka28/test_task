<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': collapsed }">
    <div class="sidebar-scroll">
      <header class="logo-row">
        <div class="brand-lockup">
          <div class="logo-mark" aria-hidden="true">
            <img class="logo-outline" src="/assets/logo/logo-outline.png" alt="" />
            <img class="logo-center" src="/assets/logo/logo-center.png" alt="" />
          </div>
          <span class="logo-text">trendsee</span>
          <span class="logo-tag">Beta</span>
        </div>

        <button class="collapse-btn" type="button" aria-label="Свернуть меню" @click="$emit('toggle-sidebar')">
          <img src="/assets/icons/Vector-13.png" alt="" />
        </button>
      </header>

      <p class="section-title">Поиск контента</p>
      <nav class="menu-list" aria-label="Главное меню">
        <button
          v-for="item in mainItems"
          :key="item.label"
          type="button"
          class="menu-item"
          :title="collapsed ? item.label : ''"
        >
          <img :src="item.icon" alt="" class="menu-icon" />
          <span class="menu-label">{{ item.label }}</span>
          <span v-if="item.badge" class="menu-badge">{{ item.badge }}</span>
        </button>
      </nav>

      <p class="section-title">Работа с соцсетями</p>
      <nav class="menu-list" aria-label="Соцсети">
        <button
          v-for="item in socialItems"
          :key="item.label"
          type="button"
          class="menu-item"
          :title="collapsed ? item.label : ''"
        >
          <img :src="item.icon" alt="" class="menu-icon" />
          <span class="menu-label">{{ item.label }}</span>
        </button>
      </nav>

      <p class="section-title">Инструменты</p>
      <nav class="menu-list" aria-label="Инструменты">
        <button
          v-for="item in toolsItems"
          :key="item.label"
          type="button"
          class="menu-item"
          :title="collapsed ? item.label : ''"
        >
          <img :src="item.icon" alt="" class="menu-icon" />
          <span class="menu-label">{{ item.label }}</span>
          <span v-if="item.badge" class="menu-badge badge-soft">{{ item.badge }}</span>
        </button>
      </nav>

      <section class="token-card">
        <div class="token-head">
          <span class="token-title">
            <img src="/assets/icons/Vector-15.png" alt="" class="token-icon" />
            <span class="token-title-text">Токены</span>
          </span>
          <strong class="token-value">{{ formattedTokenValue }}</strong>
        </div>

        <div class="token-bar">
          <span class="token-progress" :style="{ width: `${tokenProgress}%` }"></span>
        </div>

        <button type="button" class="creative-row" @click="$emit('toggle-creative')">
          <span>Creative +</span>
          <span class="creative-arrow" :class="{ 'creative-arrow--open': creativeExpanded }">›</span>
        </button>

        <Transition name="creative-panel">
          <div v-if="creativeExpanded && !collapsed" class="creative-panel">
            <p class="creative-copy">Пробная версия</p>
            <button type="button" class="upgrade-btn">Улучшить подписку</button>
          </div>
        </Transition>

        <button v-if="!isAuthenticated && !collapsed" type="button" class="auth-btn" @click="$emit('open-auth')">
          Создать аккаунт
        </button>
      </section>

      <section class="profile-row">
        <img src="/assets/avatar-feed.png" alt="Профиль" class="profile-avatar" />
        <div class="profile-meta">
          <p class="profile-name">{{ profileName }}</p>
          <p class="profile-phone">{{ profilePhone }}</p>
        </div>
        <button
          type="button"
          class="profile-action"
          :title="isAuthenticated ? 'Выйти' : 'Зарегистрироваться'"
          @click="handleProfileAction"
        >
          {{ isAuthenticated ? "↪" : "+" }}
        </button>
      </section>

      <div class="locale-row">
        <span class="locale-flag">🇷🇺</span>
        <span class="locale-code">RU</span>
        <span class="locale-arrow">⌄</span>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
  creativeExpanded: {
    type: Boolean,
    default: false,
  },
  isAuthenticated: {
    type: Boolean,
    default: false,
  },
  radarCount: {
    type: Number,
    default: 0,
  },
  tokenUsed: {
    type: Number,
    default: 0,
  },
  tokenTotal: {
    type: Number,
    default: 5000,
  },
  profileName: {
    type: String,
    default: "Гостевой режим",
  },
  profilePhone: {
    type: String,
    default: "Создайте аккаунт",
  },
});

const emit = defineEmits(["toggle-sidebar", "toggle-creative", "open-auth", "logout"]);

const mainItems = computed(() => [
  { label: "Главная", icon: "/assets/icons/Vector-12.png" },
  { label: "Видео", icon: "/assets/icons/Vector.png" },
  { label: "Шпионаж", icon: "/assets/icons/Vector-1.png" },
  { label: "Контент радар", icon: "/assets/icons/Vector-2.png", badge: String(props.radarCount) },
]);

const socialItems = [
  { label: "Кросс-постинг", icon: "/assets/icons/Vector-3.png" },
  { label: "Чат боты", icon: "/assets/icons/Vector-4.png" },
];

const toolsItems = [
  { label: "ИИ-сценарий", icon: "/assets/icons/Vector-5.png" },
  { label: "Карусели", icon: "/assets/icons/Vector-6.png" },
  { label: "Анализ видео", icon: "/assets/icons/Vector-7.png" },
  { label: "Анализ профиля", icon: "/assets/icons/Vector-8.png" },
  { label: "Черновик", icon: "/assets/icons/Vector-9.png", badge: "Скоро" },
];

const formattedTokenValue = computed(() => {
  return `${props.tokenUsed.toLocaleString("ru-RU")} / ${props.tokenTotal.toLocaleString("ru-RU")}`;
});

const tokenProgress = computed(() => {
  if (!props.tokenTotal) return 0;
  return Math.max(0, Math.min(100, (props.tokenUsed / props.tokenTotal) * 100));
});

function handleProfileAction() {
  if (props.isAuthenticated) {
    emit("logout");
    return;
  }

  emit("open-auth");
}
</script>

<style scoped>
.sidebar {
  width: 282px;
  flex: 0 0 282px;
  height: 100vh;
  position: sticky;
  top: 0;
  background: #f4f5f6;
  padding: 10px 14px 12px;
  transition:
    width 0.28s ease,
    flex-basis 0.28s ease,
    padding 0.28s ease;
}

.sidebar--collapsed {
  width: 88px;
  flex-basis: 88px;
  padding-inline: 12px;
}

.sidebar-scroll {
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  scrollbar-width: none;
}

.sidebar-scroll::-webkit-scrollbar {
  display: none;
}

.logo-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.brand-lockup {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.logo-mark {
  position: relative;
  width: 34px;
  height: 28px;
  flex: 0 0 34px;
}

.logo-outline {
  position: absolute;
  left: 0;
  top: 5px;
  width: 34px;
  height: 22px;
  object-fit: contain;
}

.logo-center {
  position: absolute;
  left: 11px;
  top: 0;
  width: 14px;
  height: 17px;
  object-fit: contain;
}

.logo-text {
  color: #1f2230;
  font-size: 24px;
  line-height: 1;
  font-weight: 900;
  letter-spacing: -0.04em;
  transition:
    width 0.24s ease,
    opacity 0.2s ease,
    transform 0.24s ease;
}

.logo-tag {
  border-radius: 12px;
  background: #dce1e5;
  color: #6e7d89;
  font-size: 14px;
  line-height: 1;
  font-weight: 700;
  padding: 5px 8px;
  transition:
    opacity 0.2s ease,
    transform 0.24s ease;
}

.collapse-btn {
  border: 1px solid #c9cfd4;
  border-radius: 4px;
  width: 20px;
  height: 20px;
  display: grid;
  place-items: center;
  background: transparent;
  cursor: pointer;
  padding: 0;
  transition: transform 0.24s ease;
}

.collapse-btn img {
  width: 12px;
  height: 12px;
}

.section-title {
  margin: 18px 0 8px;
  color: #8393a0;
  font-size: 14px;
  line-height: 1.2;
  font-weight: 700;
  transition:
    opacity 0.2s ease,
    max-height 0.24s ease,
    margin 0.24s ease;
}

.menu-list {
  display: grid;
  gap: 4px;
}

.menu-item {
  border: 0;
  border-radius: 12px;
  background: transparent;
  color: #435968;
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 40px;
  padding: 8px 10px;
  text-align: left;
  cursor: pointer;
  transition: background 0.2s ease;
}

.menu-item:hover {
  background: #ebedf0;
}

.menu-icon {
  width: 20px;
  height: 20px;
  object-fit: contain;
  flex: 0 0 20px;
}

.menu-label,
.menu-badge,
.token-title-text,
.token-value,
.creative-row span:first-child,
.profile-meta,
.locale-code,
.locale-arrow {
  transition:
    opacity 0.2s ease,
    transform 0.24s ease,
    max-width 0.24s ease;
}

.menu-label {
  font-size: 15px;
  line-height: 1.2;
  font-weight: 500;
  margin-right: auto;
  white-space: nowrap;
}

.menu-badge {
  border-radius: 999px;
  background: #c6cbff;
  color: #2f3ace;
  font-size: 11px;
  line-height: 1;
  font-weight: 700;
  padding: 4px 8px;
}

.badge-soft {
  background: #d9dde2;
  color: #636f7a;
}

.token-card {
  margin-top: auto;
  border-radius: 18px;
  background: #ffffff;
  padding: 14px;
  transition:
    padding 0.24s ease,
    background 0.24s ease;
}

.token-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  color: #191c2b;
  font-size: 14px;
  font-weight: 700;
}

.token-title {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-width: 0;
}

.token-icon {
  width: 10px;
  height: 11px;
  flex: 0 0 10px;
}

.token-bar {
  margin-top: 9px;
  height: 8px;
  border-radius: 999px;
  background: #d9dde2;
  overflow: hidden;
}

.token-progress {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: #2b31b3;
}

.creative-row {
  margin-top: 12px;
  width: 100%;
  border: 0;
  background: transparent;
  color: #748592;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
}

.creative-arrow {
  font-size: 22px;
  line-height: 1;
  color: #8a96a0;
  transition: transform 0.22s ease;
}

.creative-arrow--open {
  transform: rotate(90deg);
}

.creative-panel-enter-active,
.creative-panel-leave-active {
  transition:
    opacity 0.24s ease,
    max-height 0.24s ease,
    margin-top 0.24s ease;
}

.creative-panel-enter-from,
.creative-panel-leave-to {
  opacity: 0;
  max-height: 0;
  margin-top: 0;
}

.creative-panel-enter-to,
.creative-panel-leave-from {
  opacity: 1;
  max-height: 140px;
  margin-top: 12px;
}

.creative-copy {
  margin: 0;
  color: #7b8794;
  font-size: 13px;
  line-height: 1.2;
}

.upgrade-btn,
.auth-btn {
  width: 100%;
  height: 40px;
  border: 0;
  border-radius: 14px;
  background: #eef0f4;
  color: #2b31b3;
  font-size: 14px;
  line-height: 1;
  font-weight: 700;
  cursor: pointer;
}

.upgrade-btn {
  margin-top: 10px;
}

.auth-btn {
  margin-top: 12px;
  background: #2b31b3;
  color: #ffffff;
}

.profile-row {
  margin-top: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.profile-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  object-fit: cover;
  flex: 0 0 34px;
}

.profile-meta {
  min-width: 0;
}

.profile-name {
  margin: 0;
  color: #5d6f7d;
  font-size: 14px;
  font-weight: 700;
  line-height: 1.2;
}

.profile-phone {
  margin: 2px 0 0;
  color: #9aa5b2;
  font-size: 12px;
  line-height: 1.2;
}

.profile-action {
  margin-left: auto;
  width: 26px;
  height: 26px;
  border: 0;
  border-radius: 50%;
  background: transparent;
  color: #8e98a6;
  font-size: 18px;
  cursor: pointer;
}

.locale-row {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #6d7c89;
  font-size: 12px;
  line-height: 1;
}

.locale-flag {
  font-size: 14px;
}

.sidebar--collapsed .logo-text,
.sidebar--collapsed .logo-tag,
.sidebar--collapsed .section-title,
.sidebar--collapsed .menu-label,
.sidebar--collapsed .menu-badge,
.sidebar--collapsed .token-title-text,
.sidebar--collapsed .token-value,
.sidebar--collapsed .creative-row span:first-child,
.sidebar--collapsed .profile-meta,
.sidebar--collapsed .locale-code,
.sidebar--collapsed .locale-arrow {
  opacity: 0;
  transform: translateX(-8px);
  max-width: 0;
  overflow: hidden;
}

.sidebar--collapsed .section-title {
  max-height: 0;
  margin: 0;
}

.sidebar--collapsed .collapse-btn {
  transform: rotate(180deg);
}

.sidebar--collapsed .menu-item {
  justify-content: center;
  padding-inline: 0;
}

.sidebar--collapsed .token-card {
  background: transparent;
  padding-inline: 0;
  padding-block: 10px 0;
}

.sidebar--collapsed .token-bar,
.sidebar--collapsed .creative-row,
.sidebar--collapsed .creative-panel,
.sidebar--collapsed .auth-btn {
  display: none;
}

.sidebar--collapsed .token-head {
  justify-content: center;
}

.sidebar--collapsed .profile-row,
.sidebar--collapsed .locale-row {
  justify-content: center;
}

@media (max-width: 980px) {
  .sidebar {
    width: 100%;
    flex-basis: auto;
    height: auto;
    position: static;
  }

  .sidebar--collapsed {
    width: 100%;
    flex-basis: auto;
  }

  .sidebar-scroll {
    overflow: visible;
  }

  .sidebar--collapsed .logo-text,
  .sidebar--collapsed .logo-tag,
  .sidebar--collapsed .section-title,
  .sidebar--collapsed .menu-label,
  .sidebar--collapsed .menu-badge,
  .sidebar--collapsed .token-title-text,
  .sidebar--collapsed .token-value,
  .sidebar--collapsed .creative-row span:first-child,
  .sidebar--collapsed .profile-meta,
  .sidebar--collapsed .locale-code,
  .sidebar--collapsed .locale-arrow {
    opacity: 1;
    transform: none;
    max-width: none;
  }

  .sidebar--collapsed .token-bar,
  .sidebar--collapsed .creative-row,
  .sidebar--collapsed .creative-panel,
  .sidebar--collapsed .auth-btn {
    display: block;
  }
}
</style>
