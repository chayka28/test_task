<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': collapsed }">
    <div class="sidebar-scroll">
      <header class="logo-row">
        <div class="brand-lockup">
          <div class="logo-mark" aria-hidden="true">
            <img class="logo-outline" src="/assets/logo/logo-outline.png" alt="" />
            <img class="logo-center" src="/assets/logo/logo-center.png" alt="" />
          </div>
          <span v-if="!collapsed" class="logo-text">trendsee</span>
          <span v-if="!collapsed" class="logo-tag">Beta</span>
        </div>

        <button class="collapse-btn" type="button" aria-label="Свернуть меню" @click="$emit('toggle-sidebar')">
          <span class="collapse-arrow" :class="{ 'collapse-arrow--collapsed': collapsed }">→</span>
        </button>
      </header>

      <template v-if="collapsed">
        <nav class="shortcut-list" aria-label="Быстрые действия">
          <button
            v-for="item in shortcutItems"
            :key="item.label"
            type="button"
            class="shortcut-item"
            :class="{ 'shortcut-item--active': item.isActive }"
            :title="item.label"
            @click="$emit('placeholder', item.label)"
          >
            <img :src="item.icon" :alt="item.label" class="shortcut-icon" />
          </button>
        </nav>
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
              @click="$emit('placeholder', item.label)"
            >
              <img :src="item.icon" :alt="item.label" class="menu-icon" />
              <span class="menu-label">{{ item.label }}</span>
              <span v-if="item.badge" class="menu-badge" :class="{ 'menu-badge--soft': item.badgeSoft }">
                {{ item.badge }}
              </span>
              <span v-if="item.chevron" class="menu-chevron">›</span>
            </button>
          </nav>
        </section>
      </template>

      <section class="token-card">
        <div class="token-head">
          <span class="token-title">
            <img src="/assets/icons/Vector-15.png" alt="" class="token-icon" />
            <span v-if="!collapsed" class="token-title-text">Токены</span>
          </span>
          <strong v-if="!collapsed" class="token-value">{{ formattedTokenValue }}</strong>
        </div>

        <div v-if="!collapsed" class="token-bar">
          <span class="token-progress" :style="{ width: `${tokenProgress}%` }"></span>
        </div>

        <button v-if="!collapsed" type="button" class="creative-row" @click="$emit('toggle-creative')">
          <span>Creative +</span>
          <span class="creative-arrow" :class="{ 'creative-arrow--open': creativeExpanded }">›</span>
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

      <button type="button" class="profile-row" :class="{ 'profile-row--collapsed': collapsed }" @click="handleProfileAction">
        <AppAvatar :avatar="profileAvatar" :size="34" :seed="avatarSeed" alt="Профиль" class="profile-avatar" />
        <div v-if="!collapsed" class="profile-meta">
          <p class="profile-name">{{ profileName }}</p>
          <p class="profile-phone">{{ profilePhone }}</p>
        </div>
        <span v-if="!collapsed" class="profile-action">{{ isAuthenticated ? "↗" : "+" }}</span>
      </button>

      <div v-if="!collapsed" class="locale-row">
        <span class="locale-flag">🇷🇺</span>
        <span class="locale-code">RU</span>
        <span class="locale-arrow">⌄</span>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from "vue";

import AppAvatar from "./AppAvatar.vue";

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
});

const emit = defineEmits(["toggle-sidebar", "toggle-creative", "open-auth", "open-profile", "placeholder"]);

const sections = computed(() => [
  {
    title: "Поиск контента",
    items: [
      { label: "Главная", icon: "/assets/icons/home.svg" },
      { label: "Видео", icon: "/assets/icons/Vector.png" },
      { label: "Шпионаж", icon: "/assets/icons/Vector-1.png" },
      { label: "Контент радар", icon: "/assets/icons/Vector-2.png", badge: String(props.radarCount) },
    ],
  },
  {
    title: "Работа с соцсетями",
    items: [
      { label: "Кросс-постинг", icon: "/assets/icons/Vector-3.png" },
      { label: "Чат боты", icon: "/assets/icons/Vector-4.png" },
    ],
  },
  {
    title: "Инструменты",
    items: [
      { label: "ИИ-сценарий", icon: "/assets/icons/Vector-5.png" },
      { label: "Карусели", icon: "/assets/icons/Vector-6.png" },
      { label: "Анализ видео", icon: "/assets/icons/Vector-7.png" },
      { label: "Анализ профиля", icon: "/assets/icons/Vector-8.png" },
      { label: "Черновик", icon: "/assets/icons/Vector-9.png", badge: "Скоро", badgeSoft: true },
      { label: "Контент план", icon: "/assets/icons/Vector-10.png", badge: "Скоро", badgeSoft: true },
    ],
  },
  {
    title: "Идеи",
    items: [
      { label: "Избранные", icon: "/assets/icons/menu-favorites.png" },
      { label: "История", icon: "/assets/icons/menu-history.png", badge: "Скоро", badgeSoft: true, chevron: true },
      { label: "Закладки", icon: "/assets/icons/menu-bookmark.png", badge: "Скоро", badgeSoft: true },
    ],
  },
  {
    title: "Еще",
    items: [
      { label: "Обучение", icon: "/assets/icons/education.svg" },
      { label: "Рефералы", icon: "/assets/icons/referrals.svg" },
      { label: "Предложить идею", icon: "/assets/icons/idea.svg" },
      { label: "Поддержка", icon: "/assets/icons/support.svg" },
    ],
  },
]);

const shortcutItems = [
  { label: "Главная", icon: "/assets/icons/home.svg" },
  { label: "Поиск", icon: "/assets/icons/search.svg", isActive: true },
  { label: "Контент радар", icon: "/assets/icons/Vector-2.png" },
  { label: "Идеи", icon: "/assets/icons/ghost.svg" },
  { label: "Анализ видео", icon: "/assets/icons/Vector-7.png" },
  { label: "Анализ профиля", icon: "/assets/icons/Vector-8.png" },
  { label: "Черновик", icon: "/assets/icons/Vector-9.png" },
  { label: "Контент план", icon: "/assets/icons/Vector-10.png" },
  { label: "Избранные", icon: "/assets/icons/menu-favorites.png" },
  { label: "Закладки", icon: "/assets/icons/menu-bookmark.png" },
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
</script>

<style scoped>
.sidebar {
  width: 252px;
  flex: 0 0 252px;
  height: 100vh;
  position: sticky;
  top: 0;
  background: #f5f6f8;
  padding: 10px 12px 12px;
  transition:
    width 0.28s ease,
    flex-basis 0.28s ease,
    padding 0.28s ease;
}

.sidebar--collapsed {
  width: 84px;
  flex-basis: 84px;
  padding-inline: 10px;
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

.logo-outline,
.logo-center {
  filter: brightness(0) saturate(100%);
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
}

.logo-tag {
  border-radius: 12px;
  background: #dce1e5;
  color: #6e7d89;
  font-size: 14px;
  line-height: 1;
  font-weight: 700;
  padding: 5px 8px;
}

.collapse-btn {
  border: 1px solid #bad9ec;
  border-radius: 4px;
  width: 22px;
  height: 22px;
  display: grid;
  place-items: center;
  background: transparent;
  cursor: pointer;
  padding: 0;
}

.collapse-arrow {
  color: #7a8a97;
  font-size: 12px;
  line-height: 1;
  transition: transform 0.24s ease;
}

.collapse-arrow--collapsed {
  transform: rotate(180deg);
}

.menu-section + .menu-section {
  margin-top: 4px;
}

.section-title {
  margin: 18px 0 8px;
  color: #95a2ad;
  font-size: 14px;
  line-height: 1.2;
  font-weight: 700;
}

.menu-list {
  display: grid;
  gap: 4px;
}

.menu-item {
  border: 0;
  border-radius: 12px;
  background: transparent;
  color: #526878;
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
  background: #eceef2;
}

.menu-icon {
  width: 20px;
  height: 20px;
  object-fit: contain;
  flex: 0 0 20px;
}

.menu-label {
  font-size: 15px;
  line-height: 1.25;
  font-weight: 500;
  margin-right: auto;
  white-space: nowrap;
}

.menu-badge {
  border-radius: 999px;
  background: #d7dbff;
  color: #3640cb;
  font-size: 11px;
  line-height: 1;
  font-weight: 700;
  padding: 4px 8px;
}

.menu-badge--soft {
  background: #e4e7eb;
  color: #6d7680;
}

.menu-chevron {
  color: #838b92;
  font-size: 20px;
  line-height: 1;
}

.shortcut-list {
  margin-top: 16px;
  display: grid;
  gap: 18px;
  justify-items: center;
  padding-top: 8px;
}

.shortcut-item {
  width: 42px;
  height: 42px;
  border: 0;
  border-radius: 14px;
  background: transparent;
  display: grid;
  place-items: center;
  cursor: pointer;
  transition: background 0.2s ease;
}

.shortcut-item:hover {
  background: #eceef2;
}

.shortcut-item--active {
  background: #ecebe7;
}

.shortcut-icon {
  width: 22px;
  height: 22px;
  object-fit: contain;
}

.token-card {
  margin-top: auto;
  border-radius: 14px;
  background: #ffffff;
  padding: 12px 14px;
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
  color: #8a96a0;
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

.upgrade-btn {
  margin-top: 10px;
  width: 100%;
  height: 38px;
  border: 0;
  border-radius: 13px;
  background: #f0f1f4;
  color: #2b31b3;
  font-size: 14px;
  line-height: 1;
  font-weight: 700;
  cursor: pointer;
}

.profile-row {
  margin-top: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  border: 0;
  background: transparent;
  padding: 0;
  text-align: left;
  cursor: pointer;
}

.profile-row--collapsed {
  justify-content: center;
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
  color: #8e98a6;
  font-size: 18px;
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

.sidebar--collapsed .token-card {
  padding-inline: 10px;
}

.sidebar--collapsed .token-head {
  justify-content: center;
}

@media (max-width: 980px) {
  .sidebar,
  .sidebar--collapsed {
    width: 100%;
    flex-basis: auto;
    height: auto;
    position: static;
  }

  .sidebar-scroll {
    overflow: visible;
  }

  .shortcut-list {
    grid-template-columns: repeat(5, 40px);
    justify-content: flex-start;
  }
}
</style>
