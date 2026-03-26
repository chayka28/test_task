<template>
  <section class="top-panel">
    <div class="hero-card">
      <div class="hero-bg" aria-hidden="true">
        <span class="hero-shape hero-shape--top"></span>
        <span class="hero-shape hero-shape--center"></span>
        <span class="hero-shape hero-shape--dark"></span>
        <span class="hero-shape hero-shape--cyan"></span>
        <span class="hero-shape hero-shape--light"></span>
      </div>

      <button type="button" class="back-btn" @click="$emit('placeholder', 'Назад')">
        <img src="/assets/icons/Vector-29.png" alt="" class="back-arrow" />
        <span>Назад</span>
      </button>

      <div class="hero-query-line">
        <img src="/assets/icons/Vector-32.png" alt="" class="hero-query-icon" />
        <span>{{ resultsTitle }}</span>
      </div>

      <div class="hero-head">
        <div class="hero-title-row">
          <h2>{{ resultsTitle }}</h2>

          <div class="hero-actions">
            <button type="button" class="radar-btn" @click="handleRestrictedAction('Добавить в радар')">
              <img src="/assets/icons/Vector-31.png" alt="" />
              <span>Добавить в радар</span>
              <img src="/assets/icons/Vector-37.png" alt="" class="radar-target" />
            </button>
            <button type="button" class="icon-badge" @click="$emit('placeholder', 'Информация о подборке')">
              <img src="/assets/icons/Vector-38.png" alt="" />
            </button>
          </div>
        </div>
      </div>

      <div class="topic-row">
        <span class="topic-caption">Рекомендуем по теме</span>
        <div class="topic-list">
          <button
            v-for="topic in topics"
            :key="topic"
            type="button"
            class="topic-chip"
            :class="{ 'topic-chip--active': selectedTopic === topic }"
            @click="$emit('update:selectedTopic', selectedTopic === topic ? '' : topic)"
          >
            {{ topic }}
          </button>
        </div>
      </div>

      <div class="search-row">
        <p class="search-label">Новый поиск</p>

        <div class="search-shell">
          <label class="search-input search-input--wide">
            <span class="input-main">
              <img src="/assets/icons/Vector-32.png" alt="" class="search-icon search-icon--light" />
              <input
                :value="query"
                type="text"
                placeholder="Новый поиск"
                @input="$emit('update:query', $event.target.value)"
                @keydown.enter.prevent="handleSearch"
              />
            </span>
            <span class="input-sub">Введите ключевое слово, а мы найдем для вас видео</span>
          </label>

          <button type="button" class="select-pill" @click="handleRestrictedAction('Тип видео')">
            <span class="input-main">
              <img src="/assets/icons/Vector-33.png" alt="" class="pill-icon" />
              <span>Reels</span>
            </span>
            <span class="input-sub">Тип видео</span>
            <img src="/assets/icons/Vector-34.png" alt="" class="chevron chevron--light" />
          </button>

          <button type="button" class="select-pill" @click="handleRestrictedAction('Язык видео')">
            <span class="input-main">
              <span class="flag-ru" aria-hidden="true"></span>
              <span>Русский</span>
            </span>
            <span class="input-sub">Язык видео</span>
            <img src="/assets/icons/Vector-34.png" alt="" class="chevron chevron--light" />
          </button>

          <button type="button" class="submit-btn" @click="handleSearch">Найти</button>
        </div>
      </div>
    </div>

    <div class="results-card">
      <div class="results-head">
        <div class="results-left">
          <img src="/assets/icons/Vector-35.png" alt="" class="results-search-icon" />
          <div class="results-query">{{ resultsTitle }}</div>

          <button type="button" class="results-radar-btn" @click="handleRestrictedAction('Добавить в радар')">
            <img src="/assets/icons/Vector-31.png" alt="" />
            <span>Добавить в радар</span>
            <img src="/assets/icons/Vector-37.png" alt="" class="radar-target" />
          </button>

          <button type="button" class="results-info-btn" @click="$emit('placeholder', 'Информация о подборке')">
            <img src="/assets/icons/Vector-38.png" alt="" />
          </button>
        </div>

        <div class="results-count">Загружено: {{ loadedCount }} видео</div>
      </div>

      <div class="hint-row">
        <span>
          Ролики собираются напрямую из поиска соц. сети. Все видео из выдачи — актуальны и продвигаются прямо сейчас.
        </span>
        <button type="button" class="hint-close" @click="$emit('placeholder', 'Скрыть подсказку')">×</button>
      </div>

      <div class="filters-row">
        <button
          type="button"
          class="filter-btn"
          :class="{ 'filter-btn--active': sortMode === 'all' }"
          @click="$emit('update:sortMode', 'all')"
        >
          За все время
          <img src="/assets/icons/Vector-27.png" alt="" class="chevron" />
        </button>
        <button
          type="button"
          class="filter-btn"
          :class="{ 'filter-btn--active': sortMode === 'likes' }"
          @click="$emit('update:sortMode', 'likes')"
        >
          По лайкам
          <img src="/assets/icons/Vector-27.png" alt="" class="chevron" />
        </button>
      </div>

      <div class="results-body">
        <slot />
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  query: {
    type: String,
    default: "",
  },
  selectedTopic: {
    type: String,
    default: "",
  },
  loadedCount: {
    type: Number,
    default: 0,
  },
  sortMode: {
    type: String,
    default: "all",
  },
  resultsTitle: {
    type: String,
    default: "Business history",
  },
});

const emit = defineEmits(["update:query", "update:selectedTopic", "update:sortMode", "search", "placeholder"]);

const topics = ["Базы данных", "ИИ", "Чат-боты", "Программирование", "Айти", "Макбук", "Кофе"];

function handleSearch() {
  emit("search");
}

function handleRestrictedAction(label) {
  emit("placeholder", label);
}
</script>

<style scoped>
.top-panel {
  display: grid;
  gap: 16px;
  margin-bottom: 16px;
}

.hero-card {
  position: relative;
  min-height: 342px;
  overflow: hidden;
  border-radius: 16px;
  padding: 20px 18px 18px;
  background: #6946ff url("/assets/hero-bg.svg") center/cover no-repeat;
}

.hero-bg {
  display: none;
}

.back-btn,
.radar-btn,
.topic-chip,
.filter-btn,
.icon-badge,
.results-radar-btn,
.results-info-btn,
.hint-close {
  border: 0;
  cursor: pointer;
}

.back-btn {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 0;
  background: transparent;
  color: rgba(255, 255, 255, 0.92);
  font-size: 12px;
  line-height: 1;
  font-weight: 700;
}

.back-arrow {
  width: 12px;
  height: 12px;
}

.hero-query-line,
.hero-head,
.topic-row,
.search-row {
  position: relative;
  z-index: 1;
}

.hero-query-line {
  margin-top: 18px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: rgba(255, 255, 255, 0.74);
  font-size: 14px;
  line-height: 1;
  font-weight: 500;
}

.hero-query-icon {
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.hero-head {
  margin-top: 8px;
}

.hero-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}

.hero-head h2 {
  margin: 0;
  color: #ffffff;
  font-size: 21px;
  line-height: 1.18;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.hero-actions,
.results-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.radar-btn,
.results-radar-btn {
  height: 32px;
  padding: 0 12px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.96);
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #303646;
  font-size: 13px;
  line-height: 1;
  font-weight: 700;
}

.radar-btn img,
.results-radar-btn img {
  width: 12px;
  height: 12px;
}

.radar-target {
  width: 14px !important;
  height: 14px !important;
  opacity: 0.84;
}

.icon-badge,
.results-info-btn {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: transparent;
  display: grid;
  place-items: center;
  padding: 0;
}

.icon-badge img,
.results-info-btn img {
  width: 14px;
  height: 14px;
}

.topic-row {
  margin-top: 16px;
}

.topic-caption {
  display: block;
  margin-bottom: 10px;
  color: #ffffff;
  font-size: 15px;
  line-height: 1.2;
  font-weight: 700;
}

.topic-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.topic-chip {
  min-height: 32px;
  padding: 0 15px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.97);
  color: #49535f;
  font-size: 11px;
  line-height: 1;
  font-weight: 700;
}

.topic-chip--active {
  color: #2b31b3;
}

.search-row {
  margin-top: 14px;
}

.search-label {
  margin: 0 0 10px;
  color: #ffffff;
  font-size: 14px;
  line-height: 1.2;
  font-weight: 700;
}

.search-shell {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 136px 144px 122px;
  gap: 12px;
}

.search-input,
.select-pill {
  min-height: 78px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.22);
  padding: 14px 16px 12px;
  display: grid;
  align-content: space-between;
  position: relative;
  text-align: left;
  color: #ffffff;
}

.search-input--wide {
  gap: 10px;
}

.input-main {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  color: #ffffff;
  font-size: 14px;
  line-height: 1.1;
  font-weight: 500;
}

.search-input input {
  width: 100%;
  border: 0;
  outline: none;
  background: transparent;
  color: #ffffff;
  font: inherit;
  min-width: 0;
}

.search-input input::placeholder {
  color: rgba(255, 255, 255, 0.54);
}

.input-sub {
  color: rgba(255, 255, 255, 0.58);
  font-size: 11px;
  line-height: 1.2;
}

.search-icon,
.pill-icon {
  width: 18px;
  height: 18px;
  flex: 0 0 18px;
}

.flag-ru {
  width: 20px;
  height: 14px;
  border-radius: 2px;
  background:
    linear-gradient(180deg, #ffffff 0 33%, #1e50d8 33% 66%, #db4437 66% 100%);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.24);
}

.chevron {
  width: 12px;
  height: 8px;
}

.chevron--light {
  position: absolute;
  top: 22px;
  right: 16px;
}

.submit-btn {
  min-height: 78px;
  border-radius: 16px;
  background: #ffffff;
  color: #2f3644;
  font-size: 14px;
  line-height: 1;
  font-weight: 700;
}

.results-card {
  border-radius: 16px;
  background: #ffffff;
  padding: 14px 16px 16px;
  box-shadow: 0 10px 26px rgba(18, 27, 52, 0.05);
}

.results-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.results-left {
  min-width: 0;
  flex-wrap: wrap;
}

.results-search-icon {
  width: 24px;
  height: 24px;
}

.results-query {
  color: #1f2632;
  font-size: 16px;
  line-height: 1.2;
  font-weight: 800;
}

.results-count {
  color: #7b8794;
  font-size: 13px;
  line-height: 1.2;
  font-weight: 500;
  white-space: nowrap;
}

.hint-row {
  margin-top: 16px;
  min-height: 42px;
  border-radius: 16px;
  background: #ddd9ff;
  padding: 13px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  color: #5b62cc;
  font-size: 13px;
  line-height: 1.2;
}

.hint-close {
  background: transparent;
  color: #646ee1;
  font-size: 20px;
  line-height: 1;
  padding: 0;
}

.filters-row {
  margin-top: 12px;
  display: flex;
  gap: 10px;
}

.filter-btn {
  height: 40px;
  padding: 0 13px;
  border-radius: 12px;
  border: 1px solid #d9dfe8;
  background: #ffffff;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #222b37;
  font-size: 12px;
  line-height: 1;
  font-weight: 700;
}

.filter-btn--active {
  box-shadow: inset 0 0 0 1px #c9d2df;
}

.results-body {
  margin-top: 16px;
}

@media (max-width: 1180px) {
  .hero-title-row,
  .results-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-shell {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 980px) {
  .hero-card,
  .results-card {
    border-radius: 14px;
  }

  .hero-card {
    min-height: auto;
    padding: 18px 16px 18px;
  }

  .hero-head {
    margin-top: 20px;
  }

  .hero-head h2 {
    font-size: 28px;
  }

  .hero-shape--top {
    left: 240px;
  }

  .hero-shape--dark {
    right: 20px;
  }
}

@media (max-width: 640px) {
  .top-panel {
    gap: 12px;
    margin-bottom: 14px;
  }

  .hero-card,
  .results-card {
    padding: 14px 12px;
  }

  .hero-head h2 {
    font-size: 24px;
  }

  .hero-actions,
  .results-left,
  .filters-row {
    width: 100%;
    flex-wrap: wrap;
  }

  .hint-row {
    align-items: flex-start;
  }

  .results-query {
    font-size: 18px;
  }

  .results-count {
    white-space: normal;
  }
}
</style>
