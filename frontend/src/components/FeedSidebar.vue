<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': collapsed }">
    <div class="sidebar-scroll">
      <header class="logo-row">
        <BrandLogo :icon-only="collapsed" :show-tag="!collapsed" compact />

        <button class="collapse-btn" type="button" aria-label="Свернуть меню" @click="$emit('toggle-sidebar')">
          <img
            src="/assets/icons/Vector-28.png"
            alt=""
            class="collapse-icon"
            :class="{ 'collapse-icon--collapsed': collapsed }"
          />
        </button>
      </header>

      <template v-if="collapsed">
        <div class="collapsed-layout">
          <nav class="shortcut-list" aria-label="Быстрые действия">
            <button
              v-for="item in shortcutItems"
              :key="item.label"
              type="button"
              class="shortcut-item"
              :class="{ 'shortcut-item--active': isRouteActive(item.route, item.isActive) }"
              :title="item.label"
              @click="handleMenuAction(item)"
            >
              <img :src="item.icon" :alt="item.label" class="shortcut-icon" />
            </button>
          </nav>

          <div class="collapsed-bottom">
            <button
              v-for="item in collapsedBottomItems"
              :key="item.label"
              type="button"
              class="shortcut-item"
              :title="item.label"
              @click="handleMenuAction(item)"
            >
              <img :src="item.icon" :alt="item.label" class="shortcut-icon" />
            </button>

            <button type="button" class="collapsed-avatar" @click="handleProfileAction">
              <AppAvatar :avatar="profileAvatar" :size="34" :seed="avatarSeed" alt="Профиль" />
            </button>
          </div>
        </div>
      </template>

      <template v-else>
        <section v-for="section in sections" :key="section.title" class="menu-section">
          <p class="section-title">{{ section.title }}</p>
          <nav class="menu-list" :aria-label="section.title">
            <button
              v-for="item in section.items"
              :key="item.label"
              type="button"
              class="menu-item"
              :class="{ 'menu-item--active': isRouteActive(item.route) }"
              @click="handleMenuAction(item)"
            >
              <img :src="item.icon" :alt="item.label" class="menu-icon" />
              <span class="menu-label">{{ item.label }}</span>
              <span v-if="item.badge" class="menu-badge" :class="{ 'menu-badge--soft': item.badgeSoft }">
                {{ item.badge }}
              </span>
              <img
                v-if="item.chevron"
                :src="item.chevronIcon || '/assets/icons/Vector-27.png'"
                alt=""
                class="menu-chevron"
                :class="{ 'menu-chevron--lightning': !!item.chevronIcon }"
              />
            </button>
          </nav>
        </section>
      </template>

      <section v-if="!collapsed" class="token-card">
        <div class="token-head">
          <span class="token-title">
            <img src="/assets/icons/Vector-25.png" alt="" class="token-icon" />
            <span v-if="!collapsed" class="token-title-text">Токены</span>
          </span>
          <strong v-if="!collapsed" class="token-value">{{ formattedTokenValue }}</strong>
        </div>

        <div v-if="!collapsed" class="token-bar">
          <span class="token-progress" :style="{ width: `${tokenProgress}%` }"></span>
        </div>

        <button v-if="!collapsed" type="button" class="creative-row" @click="$emit('toggle-creative')">
          <span>Creative +</span>
          <img src="/assets/icons/Vector-27.png" alt="" class="creative-arrow" :class="{ 'creative-arrow--open': creativeExpanded }" />
        </button>

        <Transition name="creative-panel">
          <div v-if="creativeExpanded && !collapsed" class="creative-panel">
            <p class="creative-copy">Пробная версия</p>
            <button type="button" class="upgrade-btn" @click="$emit('placeholder', 'Улучшить подписку')">
              Улучшить подписку
            </button>
          </div>
        </Transition>
      </section>

      <button v-if="!collapsed" type="button" class="profile-row" :class="{ 'profile-row--collapsed': collapsed }" @click="handleProfileAction">
        <AppAvatar :avatar="profileAvatar" :size="34" :seed="avatarSeed" alt="Профиль" class="profile-avatar" />
        <div v-if="!collapsed" class="profile-meta">
          <p class="profile-name">{{ profileName }}</p>
          <p class="profile-phone">{{ profilePhone }}</p>
        </div>
        <img v-if="!collapsed" src="/assets/icons/Vector-26.png" alt="" class="profile-action" />
      </button>

      <div v-if="!collapsed" class="locale-row">
        <span class="locale-flag">🇷🇺</span>
        <span class="locale-code">RU</span>
        <img src="/assets/icons/Vector-27.png" alt="" class="locale-arrow" />
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from "vue";

import AppAvatar from "./AppAvatar.vue";
import BrandLogo from "./BrandLogo.vue";

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
    default: "Trendsee user",
  },
  profilePhone: {
    type: String,
    default: "Создайте аккаунт",
  },
  profileAvatar: {
    type: String,
    default: "",
  },
  avatarSeed: {
    type: Number,
    default: 1,
  },
  activeView: {
    type: String,
    default: "feed",
  },
});

const emit = defineEmits(["toggle-sidebar", "toggle-creative", "open-auth", "open-profile", "placeholder", "navigate"]);

const sections = computed(() => [
  {
    title: "Поиск контента",
    items: [
      { label: "Главная", icon: "/assets/icons/Vector-5.png", route: "feed" },
      { label: "Видео", icon: "/assets/icons/Vector-6.png" },
      { label: "Шпионаж", icon: "/assets/icons/Vector-7.png" },
      { label: "Контент радар", icon: "/assets/icons/Vector-8.png", badge: String(props.radarCount) },
    ],
  },
  {
    title: "Работа с соцсетями",
    items: [
      { label: "Кросс-постинг", icon: "/assets/icons/Vector-9.png" },
      { label: "Чат боты", icon: "/assets/icons/Vector-10.png" },
    ],
  },
  {
    title: "Инструменты",
    items: [
      { label: "ИИ-сценарий", icon: "/assets/icons/Vector-11.png" },
      { label: "Карусели", icon: "/assets/icons/Vector-12.png" },
      { label: "Анализ видео", icon: "/assets/icons/Vector-13.png" },
      { label: "Анализ профиля", icon: "/assets/icons/Vector-14.png" },
      { label: "Черновик", icon: "/assets/icons/draft-note.png", badge: "Скоро", badgeSoft: true },
      { label: "Контент план", icon: "/assets/icons/Vector-16.png", badge: "Скоро", badgeSoft: true },
    ],
  },
  {
    title: "Идеи",
    items: [
      { label: "Избранные", icon: "/assets/icons/Vector-17.png", route: "favorites" },
      {
        label: "История",
        icon: "/assets/icons/Vector-18.png",
        badge: "Скоро",
        badgeSoft: true,
        chevron: true,
        chevronIcon: "/assets/icons/lightning-white.png",
      },
      { label: "Закладки", icon: "/assets/icons/Vector-20.png", badge: "Скоро", badgeSoft: true },
    ],
  },
  {
    title: "Еще",
    items: [
      { label: "Обучение", icon: "/assets/icons/Vector-21.png" },
      { label: "Рефералы", icon: "/assets/icons/Vector-22.png" },
      { label: "Предложить идею", icon: "/assets/icons/Vector-23.png" },
      { label: "Поддержка", icon: "/assets/icons/Vector-24.png" },
    ],
  },
]);

const shortcutItems = [
  { label: "Главная", icon: "/assets/icons/Vector-5.png", route: "feed" },
  { label: "Поиск", icon: "/assets/icons/Vector-35.png", isActive: true, route: "feed" },
  { label: "Контент радар", icon: "/assets/icons/Vector-8.png" },
  { label: "Шпионаж", icon: "/assets/icons/Vector-7.png" },
  { label: "Анализ видео", icon: "/assets/icons/Vector-13.png" },
  { label: "Анализ профиля", icon: "/assets/icons/Vector-14.png" },
  { label: "Черновик", icon: "/assets/icons/draft-note.png" },
  { label: "Контент план", icon: "/assets/icons/Vector-16.png" },
  { label: "Избранные", icon: "/assets/icons/Vector-17.png", route: "favorites" },
  { label: "Закладки", icon: "/assets/icons/Vector-20.png" },
];

const collapsedBottomItems = [
  { label: "Предложить идею", icon: "/assets/icons/Vector-23.png" },
  { label: "Поддержка", icon: "/assets/icons/Vector-24.png" },
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
    emit("open-profile");
    return;
  }

  emit("open-auth");
}

function handleMenuAction(item) {
  if (item.route) {
    emit("navigate", item.route);
    return;
  }

  emit("placeholder", item.label);
}

function isRouteActive(routeName, fallback = false) {
  if (!routeName) return Boolean(fallback);
  return props.activeView === routeName;
}
</script>

<style scoped>
.sidebar {
  width: 246px;
  flex: 0 0 246px;
  height: 100vh;
  position: sticky;
  top: 0;
  background: #f5f6f8;
  padding: 0 12px;
  transition:
    width 0.28s ease,
    flex-basis 0.28s ease,
    padding 0.28s ease;
}

.sidebar--collapsed {
  width: 64px;
  flex-basis: 64px;
  padding: 0 6px;
}

.sidebar-scroll {
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  padding: 10px 0 16px;
  scrollbar-width: none;
}

.sidebar-scroll::-webkit-scrollbar {
  display: none;
}

.logo-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  min-height: 38px;
}

.collapse-btn {
  width: 16px;
  height: 16px;
  border-radius: 3px;
  border: 1px solid #c7d5e3;
  background: transparent;
  padding: 0;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.collapse-icon {
  width: 12px;
  height: 12px;
  object-fit: contain;
  transition: transform 0.22s ease;
}

.collapse-icon--collapsed {
  transform: rotate(180deg);
}

.menu-section {
  margin-top: 12px;
}

.section-title {
  margin: 0 0 10px;
  color: #98a5b0;
  font-size: 11px;
  line-height: 1.2;
  font-weight: 700;
}

.menu-list {
  display: grid;
  gap: 6px;
}

.menu-item {
  min-height: 44px;
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  border: 0;
  background: transparent;
  padding: 8px 12px;
  border-radius: 14px;
  text-align: left;
  cursor: pointer;
  color: #5d6f7d;
}

.menu-item:hover,
.menu-item--active {
  background: rgba(236, 239, 243, 0.9);
}

.menu-icon {
  width: 24px;
  height: 24px;
  flex: 0 0 24px;
  object-fit: contain;
}

.menu-label {
  font-size: 12px;
  line-height: 1.2;
  font-weight: 500;
}

.menu-badge {
  margin-left: auto;
  min-width: 34px;
  padding: 5px 9px;
  border-radius: 999px;
  background: #d8d7ff;
  color: #4f59d7;
  font-size: 10px;
  line-height: 1;
  font-weight: 700;
  text-align: center;
}

.menu-badge--soft {
  background: #eceff2;
  color: #7f8d99;
}

.menu-chevron {
  margin-left: auto;
  width: 12px;
  height: 8px;
}

.menu-chevron--lightning {
  width: 10px;
  height: 14px;
  margin-right: 2px;
}

.collapsed-layout {
  display: flex;
  flex: 1;
  flex-direction: column;
}

.shortcut-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  padding-top: 18px;
}

.shortcut-item {
  width: 44px;
  height: 44px;
  border: 0;
  border-radius: 14px;
  background: transparent;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.shortcut-item--active,
.shortcut-item:hover {
  background: #ecebe7;
}

.shortcut-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.collapsed-bottom {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  padding-bottom: 8px;
}

.collapsed-avatar {
  width: 44px;
  height: 44px;
  border: 0;
  border-radius: 50%;
  background: transparent;
  padding: 0;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.token-card {
  margin-top: auto;
  border-radius: 16px;
  background: #ffffff;
  padding: 10px 12px;
  box-shadow: 0 8px 20px rgba(23, 32, 56, 0.04);
}

.token-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.token-title {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #171a21;
  font-size: 13px;
  line-height: 1;
  font-weight: 800;
}

.token-icon {
  width: 14px;
  height: 14px;
}

.token-value {
  color: #1b1d26;
  font-size: 13px;
  line-height: 1;
  font-weight: 500;
}

.token-bar {
  margin-top: 10px;
  height: 8px;
  border-radius: 999px;
  background: #d9dde2;
  overflow: hidden;
}

.token-progress {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: #2f37c6;
}

.creative-row {
  margin-top: 12px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 0;
  padding: 0;
  background: transparent;
  color: #8a97a0;
  font-size: 13px;
  line-height: 1;
  cursor: pointer;
}

.creative-arrow {
  width: 12px;
  height: 8px;
  transition: transform 0.22s ease;
}

.creative-arrow--open {
  transform: rotate(-90deg);
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
  color: #7f8b95;
  font-size: 13px;
  line-height: 1.2;
}

.upgrade-btn {
  margin-top: 10px;
  width: 100%;
  height: 38px;
  border: 0;
  border-radius: 14px;
  background: #f3f4f6;
  color: #2f37c6;
  font-size: 14px;
  line-height: 1;
  font-weight: 700;
  cursor: pointer;
}

.profile-row {
  margin-top: 14px;
  width: 100%;
  min-height: 56px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px 8px 8px;
  border: 0;
  border-radius: 16px;
  background: #ffffff;
  box-shadow: 0 8px 20px rgba(23, 32, 56, 0.04);
  text-align: left;
  cursor: pointer;
}

.profile-row--collapsed {
  justify-content: center;
  padding-inline: 0;
}

.profile-meta {
  min-width: 0;
}

.profile-name {
  margin: 0;
  color: #6b7b89;
  font-size: 13px;
  line-height: 1.2;
  font-weight: 700;
}

.profile-phone {
  margin: 2px 0 0;
  color: #a2aab3;
  font-size: 11px;
  line-height: 1.2;
}

.profile-action {
  margin-left: auto;
  width: 16px;
  height: 16px;
}

.locale-row {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 7px;
  padding-left: 4px;
  color: #6a7988;
  font-size: 12px;
  line-height: 1;
}

.locale-flag {
  font-size: 16px;
}

.locale-arrow {
  width: 12px;
  height: 8px;
}

.sidebar--collapsed .token-card {
  padding: 12px 10px;
}

.sidebar--collapsed .token-head {
  justify-content: center;
}

@media (max-width: 720px) {
  .sidebar,
  .sidebar--collapsed {
    width: 100%;
    flex-basis: auto;
    height: auto;
    position: sticky;
    z-index: 30;
    padding: 0 10px;
    border-bottom: 1px solid #e5e9ef;
  }

  .sidebar-scroll {
    height: auto;
    overflow: visible;
    padding: 10px 0 14px;
  }

  .shortcut-list {
    flex-direction: row;
    justify-content: flex-start;
    overflow-x: auto;
    gap: 10px;
    padding: 14px 0 0;
  }

  .token-card,
  .profile-row,
  .locale-row {
    margin-top: 12px;
  }
}

@media (max-width: 560px) {
  .menu-label {
    font-size: 14px;
  }

  .menu-badge {
    font-size: 11px;
    padding-inline: 8px;
  }
}
</style>
