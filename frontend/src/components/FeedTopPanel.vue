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

      <button type="button" class="back-btn" @click="$emit('back')">
        <img src="/assets/icons/Vector-29.png" alt="" class="back-arrow" />
        <span>Назад</span>
      </button>

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
          <div class="search-field search-field--wide">
            <label class="search-input">
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
            </label>
            <span class="field-sub">Введите ключевое слово, а мы найдем для вас видео</span>
          </div>

          <div class="search-field">
            <button type="button" class="select-pill" @click="handleRestrictedAction('Тип видео')">
              <span class="input-main">
                <img src="/assets/icons/Vector-33.png" alt="" class="pill-icon" />
                <span>Reels</span>
              </span>
              <img src="/assets/icons/Vector-34.png" alt="" class="chevron chevron--light" />
            </button>
            <span class="field-sub">Тип видео</span>
          </div>

          <div class="search-field">
            <button type="button" class="select-pill" @click="handleRestrictedAction('Язык видео')">
              <span class="input-main">
                <span class="flag-ru" aria-hidden="true"></span>
                <span>Русский</span>
              </span>
              <img src="/assets/icons/Vector-34.png" alt="" class="chevron chevron--light" />
            </button>
            <span class="field-sub">Язык видео</span>
          </div>

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

const emit = defineEmits(["update:query", "update:selectedTopic", "update:sortMode", "search", "placeholder", "back"]);

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
  min-height: 344px;
  overflow: hidden;
  border-radius: 20px;
  padding: 19px 24px 22px;
  background: #6946ff url("/assets/dark-hero.png") center/100% 100% no-repeat;
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
  gap: 9px;
  padding: 0;
  background: transparent;
  color: rgba(255, 255, 255, 0.92);
  font-size: 13px;
  line-height: 1;
  font-weight: 700;
}

.back-arrow {
  width: 12px;
  height: 12px;
}

.hero-head,
.topic-row,
.search-row {
  position: relative;
  z-index: 1;
}

.hero-head {
  margin-top: 36px;
}

.hero-title-row {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 16px;
}

.hero-head h2 {
  margin: 0;
  color: #ffffff;
  font-family: "Inter", Arial, sans-serif;
  font-size: 24px;
  line-height: 29px;
  font-weight: 700;
  letter-spacing: 0;
}

.hero-actions,
.results-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.radar-btn,
.results-radar-btn {
  height: 39px;
  padding: 0 16px;
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
  margin-top: 20px;
}

.topic-caption {
  display: block;
  margin-bottom: 12px;
  color: #ffffff;
  font-size: 14px;
  line-height: 1.2;
  font-weight: 700;
}

.topic-list {
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
}

.topic-chip {
  min-height: 38px;
  padding: 0 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.97);
  color: #49535f;
  font-size: 13px;
  line-height: 1;
  font-weight: 700;
}

.topic-chip--active {
  color: #2b31b3;
}

.search-row {
  margin-top: 17px;
}

.search-label {
  margin: 0 0 11px;
  color: #ffffff;
  font-size: 14px;
  line-height: 1.2;
  font-weight: 700;
}

.search-shell {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 166px 194px 132px;
  gap: 12px;
  align-items: start;
}

.search-field {
  display: grid;
  gap: 7px;
}

.search-field--wide {
  min-width: 0;
}

.search-input,
.select-pill {
  min-height: 50px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.22);
  padding: 0 17px;
  display: flex;
  align-items: center;
  width: 100%;
  position: relative;
  text-align: left;
  color: #ffffff;
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

.field-sub {
  color: rgba(255, 255, 255, 0.58);
  font-size: 12px;
  line-height: 1.15;
  padding-left: 0;
}

.search-icon,
.pill-icon {
  width: 21px;
  height: 21px;
  flex: 0 0 21px;
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
  top: 21px;
  right: 16px;
}

.submit-btn {
  min-height: 50px;
  align-self: start;
  border-radius: 16px;
  background: #ffffff;
  color: #2f3644;
  font-size: 16px;
  line-height: 1;
  font-weight: 800;
  box-shadow: inset 0 0 0 1px rgba(69, 78, 90, 0.2);
}

.results-card {
  border-radius: 22px;
  background: #ffffff;
  padding: 20px 22px 20px;
  box-shadow: 0 14px 34px rgba(18, 27, 52, 0.05);
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
  font-family: "Inter", Arial, sans-serif;
  font-size: 18px;
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.results-count {
  color: #7b8794;
  font-size: 14px;
  line-height: 1.2;
  font-weight: 500;
  white-space: nowrap;
}

.hint-row {
  margin-top: 16px;
  min-height: 70px;
  border-radius: 16px;
  background: #ddd9ff;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  color: #5b62cc;
  font-size: 14px;
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
  margin-top: 18px;
  display: flex;
  gap: 10px;
}

.filter-btn {
  height: 46px;
  padding: 0 16px;
  border-radius: 14px;
  border: 1px solid #d9dfe8;
  background: #ffffff;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #222b37;
  font-size: 14px;
  line-height: 1;
  font-weight: 700;
}

.filter-btn--active {
  box-shadow: inset 0 0 0 1px #c9d2df;
}

.results-body {
  margin-top: 18px;
}

@media (max-width: 860px) {
  .hero-title-row,
  .results-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-shell {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
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

@media (max-width: 560px) {
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
