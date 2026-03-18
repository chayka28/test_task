<template>
  <section class="top-panel">
    <div class="hero-card">
      <div class="hero-bg" aria-hidden="true">
        <span class="hero-shape hero-shape--dark"></span>
        <span class="hero-shape hero-shape--cyan"></span>
        <span class="hero-shape hero-shape--black"></span>
        <span class="hero-shape hero-shape--light"></span>
      </div>

      <button type="button" class="back-btn" @click="$emit('placeholder', 'Назад')">← Назад</button>

      <div class="hero-head">
        <div class="hero-title-row">
          <h2>{{ resultsTitle }}</h2>

          <div class="hero-actions">
            <button type="button" class="radar-btn" @click="handleRestrictedAction('Добавить в радар')">
              <img src="/assets/icons/top-plus.svg" alt="" />
              <span>Добавить в радар</span>
            </button>
            <button type="button" class="icon-badge" @click="$emit('placeholder', 'Информация о подборке')">
              <img src="/assets/icons/top-info.svg" alt="" />
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
              <img src="/assets/icons/top-search-dark.svg" alt="" class="search-icon search-icon--light" />
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
              <img src="/assets/icons/top-reels.svg" alt="" class="pill-icon" />
              <span>Reels</span>
            </span>
            <span class="input-sub">Тип видео</span>
            <img src="/assets/icons/top-chevron.svg" alt="" class="chevron chevron--light" />
          </button>

          <button type="button" class="select-pill" @click="handleRestrictedAction('Язык видео')">
            <span class="input-main">
              <span class="flag-ru" aria-hidden="true"></span>
              <span>Русский</span>
            </span>
            <span class="input-sub">Язык видео</span>
            <img src="/assets/icons/top-chevron.svg" alt="" class="chevron chevron--light" />
          </button>

          <button type="button" class="submit-btn" @click="handleSearch">Найти</button>
        </div>
      </div>
    </div>

    <div class="results-card">
      <div class="results-head">
        <div class="results-left">
          <img src="/assets/icons/top-search-blue.svg" alt="" class="results-search-icon" />
          <div class="results-query">{{ resultsTitle }}</div>

          <button type="button" class="results-radar-btn" @click="handleRestrictedAction('Добавить в радар')">
            <img src="/assets/icons/top-plus.svg" alt="" />
            <span>Добавить в радар</span>
          </button>

          <button type="button" class="results-info-btn" @click="$emit('placeholder', 'Информация о подборке')">
            <img src="/assets/icons/top-info.svg" alt="" />
          </button>
        </div>

        <div class="results-count">Загружено: {{ loadedCount }} видео</div>
      </div>

      <div class="hint-row">
        <span>
          Ролики собираются напрямую из поиска соц. сетей. Все видео из выдачи — актуальны и подгружаются прямо сейчас.
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
          <img src="/assets/icons/top-chevron.svg" alt="" class="chevron" />
        </button>
        <button
          type="button"
          class="filter-btn"
          :class="{ 'filter-btn--active': sortMode === 'likes' }"
          @click="$emit('update:sortMode', 'likes')"
        >
          По лайкам
          <img src="/assets/icons/top-chevron.svg" alt="" class="chevron" />
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
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
  gap: 14px;
  margin-bottom: 18px;
}

.hero-card {
  position: relative;
  overflow: hidden;
  border-radius: 16px;
  padding: 18px 16px 18px;
  background: linear-gradient(135deg, #6c5cff 0%, #5f3ce3 42%, #7a66ff 100%);
}

.hero-bg {
  position: absolute;
  inset: 0;
}

.hero-shape {
  position: absolute;
  pointer-events: none;
}

.hero-shape--dark {
  width: 460px;
  height: 460px;
  border-radius: 50%;
  top: -290px;
  right: 180px;
  background: rgba(25, 42, 118, 0.58);
}

.hero-shape--cyan {
  width: 390px;
  height: 390px;
  border-radius: 50%;
  left: 120px;
  bottom: -250px;
  background: radial-gradient(circle at 25% 25%, #8fe7ff 0%, #7fdfff 30%, #5b83f2 74%, rgba(91, 131, 242, 0.08) 100%);
}

.hero-shape--black {
  width: 400px;
  height: 240px;
  right: 140px;
  top: -4px;
  background: radial-gradient(circle at 50% 50%, rgba(18, 12, 47, 0.98) 0%, rgba(20, 13, 52, 0.97) 62%, rgba(28, 18, 66, 0.94) 100%);
  clip-path: ellipse(50% 44% at 50% 50%);
}

.hero-shape--light {
  width: 520px;
  height: 240px;
  right: -150px;
  bottom: -90px;
  background: linear-gradient(180deg, rgba(192, 225, 255, 0.94) 0%, rgba(125, 181, 255, 0.72) 100%);
  border-radius: 60% 40% 0 0;
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
  background: transparent;
  color: rgba(255, 255, 255, 0.88);
  font-size: 12px;
  line-height: 1;
  font-weight: 700;
}

.hero-head,
.topic-row,
.search-row {
  position: relative;
  z-index: 1;
}

.hero-head {
  margin-top: 18px;
}

.hero-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.hero-head h2 {
  margin: 0;
  color: #ffffff;
  font-size: 31px;
  line-height: 1.1;
  font-weight: 800;
}

.hero-actions,
.results-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.radar-btn,
.results-radar-btn {
  height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.96);
  color: #454b63;
  font-size: 12px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.radar-btn img,
.results-radar-btn img {
  width: 12px;
  height: 12px;
}

.icon-badge,
.results-info-btn {
  width: 18px;
  height: 18px;
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
  margin-top: 18px;
}

.topic-caption {
  display: block;
  color: rgba(255, 255, 255, 0.84);
  font-size: 13px;
  font-weight: 700;
}

.topic-list {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.topic-chip {
  min-height: 30px;
  padding: 0 12px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.96);
  color: #4b5563;
  font-size: 12px;
  font-weight: 700;
}

.topic-chip--active {
  color: #2b31b3;
}

.search-row {
  margin-top: 16px;
}

.search-label {
  margin: 0 0 10px;
  color: #ffffff;
  font-size: 13px;
  font-weight: 700;
}

.search-shell {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 142px 142px 104px;
  gap: 10px;
}

.search-input,
.select-pill {
  min-height: 62px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.16);
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: center;
  padding: 10px 14px;
  position: relative;
}

.search-input--wide {
  justify-content: space-between;
}

.input-main {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 18px;
}

.search-icon {
  width: 18px;
  height: 18px;
}

.search-icon--light {
  filter: brightness(0) invert(1);
}

.search-input input {
  width: 100%;
  border: 0;
  outline: none;
  background: transparent;
  padding: 0;
  color: #ffffff;
  font-size: 14px;
  line-height: 1;
}

.search-input input::placeholder {
  color: rgba(255, 255, 255, 0.8);
}

.select-pill {
  padding-right: 28px;
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
  text-align: left;
}

.pill-icon {
  width: 18px;
  height: 18px;
}

.input-sub {
  display: block;
  margin-top: 9px;
  color: rgba(255, 255, 255, 0.58);
  font-size: 11px;
  line-height: 1.1;
  white-space: nowrap;
}

.chevron {
  width: 12px;
  height: 8px;
}

.chevron--light {
  position: absolute;
  right: 12px;
  top: 19px;
  filter: brightness(0) invert(1);
  opacity: 0.85;
}

.flag-ru {
  width: 16px;
  height: 12px;
  border-radius: 2px;
  display: inline-block;
  background: linear-gradient(180deg, #ffffff 0 33.33%, #2749d8 33.33% 66.66%, #d43838 66.66% 100%);
}

.submit-btn {
  height: 62px;
  border-radius: 12px;
  background: #ffffff;
  color: #2b31b3;
  font-size: 15px;
  font-weight: 800;
}

.results-card {
  border-radius: 16px;
  background: #ffffff;
  padding: 16px;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.results-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.results-left {
  min-width: 0;
  flex-wrap: wrap;
}

.results-search-icon {
  width: 18px;
  height: 18px;
}

.results-query {
  color: #101827;
  font-size: 22px;
  font-weight: 800;
}

.results-count {
  color: #7b8794;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

.hint-row {
  margin-top: 12px;
  border-radius: 12px;
  background: #eef0ff;
  color: #6b71a8;
  padding: 12px 14px;
  font-size: 13px;
  line-height: 1.4;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.hint-close {
  background: transparent;
  color: #8791d0;
  font-size: 18px;
  line-height: 1;
}

.filters-row {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

.filter-btn {
  height: 34px;
  padding: 0 12px;
  border-radius: 10px;
  background: #f4f6fa;
  color: #4f5f70;
  font-size: 12px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.filter-btn--active {
  background: #e6e9ff;
  color: #2b31b3;
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
    padding: 16px 14px;
  }

  .hero-head {
    margin-top: 14px;
  }

  .hero-head h2 {
    font-size: 26px;
  }

  .hero-shape--dark {
    width: 340px;
    height: 340px;
    top: -220px;
    right: 60px;
  }

  .hero-shape--cyan {
    width: 280px;
    height: 280px;
    left: 40px;
    bottom: -170px;
  }

  .hero-shape--black {
    width: 280px;
    height: 180px;
    right: 40px;
    top: 20px;
  }

  .hero-shape--light {
    width: 360px;
    height: 180px;
    right: -120px;
    bottom: -70px;
  }

  .input-sub {
    white-space: normal;
  }

  .submit-btn {
    width: 100%;
  }

  .hint-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .filters-row {
    flex-wrap: wrap;
  }
}

@media (max-width: 640px) {
  .top-panel {
    gap: 12px;
    margin-bottom: 14px;
  }

  .hero-card {
    padding: 14px 12px;
  }

  .hero-head h2 {
    font-size: 22px;
  }

  .hero-actions,
  .results-left {
    width: 100%;
    flex-wrap: wrap;
  }

  .radar-btn,
  .results-radar-btn {
    max-width: 100%;
  }

  .search-input,
  .select-pill,
  .submit-btn {
    min-height: 58px;
  }

  .results-card {
    padding: 14px 12px;
  }

  .results-query {
    font-size: 18px;
  }

  .results-count {
    white-space: normal;
  }
}
</style>
