<template>
  <section class="top-panel">
    <div class="hero-card">
      <div class="hero-bg">
        <span class="hero-shape hero-shape--one"></span>
        <span class="hero-shape hero-shape--two"></span>
        <span class="hero-shape hero-shape--three"></span>
      </div>

      <button type="button" class="back-btn" @click="$emit('placeholder', 'Назад')">Назад</button>

      <div class="hero-head">
        <div>
          <h2>Business history</h2>
          <button type="button" class="radar-btn" @click="handleRestrictedAction('Добавить в радар')">
            Добавить в радар
          </button>
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
            @click="$emit('update:selectedTopic', topic)"
          >
            {{ topic }}
          </button>
        </div>
      </div>

      <div class="search-shell">
        <label class="search-input">
          <input :value="query" type="text" placeholder="Новый поиск" @input="$emit('update:query', $event.target.value)" />
        </label>
        <button type="button" class="select-pill" @click="handleRestrictedAction('Тип видео')">
          Reels
        </button>
        <button type="button" class="select-pill" @click="handleRestrictedAction('Язык видео')">
          Русский
        </button>
        <button type="button" class="submit-btn" @click="handleSearch">Найти</button>
      </div>
    </div>

    <div class="results-card">
      <div class="results-head">
        <div class="results-query">Business history</div>
        <div class="results-count">Загружено: {{ loadedCount }} видео</div>
      </div>

      <div class="hint-row">
        Ролики собираются напрямую из поиска соцсетей. После регистрации можно сохранять результаты, добавлять в радар и
        работать с подборкой.
      </div>

      <div class="filters-row">
        <button type="button" class="filter-btn" @click="$emit('update:sortMode', 'all')">За все время</button>
        <button type="button" class="filter-btn" @click="$emit('update:sortMode', 'likes')">По лайкам</button>
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
    default: "Базы данных",
  },
  loadedCount: {
    type: Number,
    default: 0,
  },
  canInteract: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["update:query", "update:selectedTopic", "update:sortMode", "search", "placeholder", "auth-required"]);

const topics = ["Базы данных", "ИИ", "Чат-боты", "Программирование", "Айти", "Макбук", "Кофе"];

function handleSearch() {
  if (!props.canInteract) {
    emit("auth-required", "Поиск по ленте");
    return;
  }

  emit("search");
}

function handleRestrictedAction(label) {
  if (!props.canInteract) {
    emit("auth-required", label);
    return;
  }

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
  padding: 20px 18px 18px;
  background: linear-gradient(135deg, #6f5bff 0%, #5e36df 48%, #7b61ff 100%);
}

.hero-bg {
  position: absolute;
  inset: 0;
}

.hero-shape {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}

.hero-shape--one {
  width: 420px;
  height: 420px;
  top: -210px;
  right: 120px;
  background: rgba(18, 27, 83, 0.65);
}

.hero-shape--two {
  width: 380px;
  height: 380px;
  left: 140px;
  bottom: -230px;
  background: radial-gradient(circle at 30% 30%, #7fe5ff 0%, #7fe5ff 20%, #5c84f0 65%, rgba(92, 132, 240, 0.05) 100%);
}

.hero-shape--three {
  width: 520px;
  height: 240px;
  right: -120px;
  bottom: -90px;
  background: linear-gradient(180deg, rgba(188, 226, 255, 0.95) 0%, rgba(118, 175, 255, 0.75) 100%);
  border-radius: 56% 44% 0 0;
}

.back-btn,
.radar-btn,
.topic-chip,
.filter-btn {
  border: 0;
  cursor: pointer;
}

.back-btn {
  position: relative;
  z-index: 1;
  background: transparent;
  color: rgba(255, 255, 255, 0.85);
  font-size: 13px;
  font-weight: 700;
}

.hero-head {
  position: relative;
  z-index: 1;
  margin-top: 12px;
}

.hero-head h2 {
  margin: 0;
  color: #ffffff;
  font-size: 28px;
  font-weight: 800;
}

.radar-btn {
  margin-top: 10px;
  height: 32px;
  padding: 0 14px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.92);
  color: #4c4f67;
  font-size: 13px;
  font-weight: 700;
}

.topic-row,
.search-shell {
  position: relative;
  z-index: 1;
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
  background: rgba(255, 255, 255, 0.95);
  color: #4b5563;
  font-size: 12px;
  font-weight: 700;
}

.topic-chip--active {
  color: #2b31b3;
}

.search-shell {
  margin-top: 18px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 150px 150px 112px;
  gap: 10px;
}

.search-input,
.select-pill {
  height: 50px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
}

.search-input input {
  width: 100%;
  height: 100%;
  border: 0;
  outline: none;
  background: transparent;
  padding: 0 16px;
  color: #ffffff;
  font-size: 14px;
}

.search-input input::placeholder {
  color: rgba(255, 255, 255, 0.62);
}

.select-pill {
  justify-content: center;
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
}

.submit-btn {
  height: 50px;
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

.results-query {
  color: #101827;
  font-size: 22px;
  font-weight: 800;
}

.results-count {
  color: #7b8794;
  font-size: 13px;
  font-weight: 600;
}

.hint-row {
  margin-top: 12px;
  border-radius: 12px;
  background: #eef0ff;
  color: #6b71a8;
  padding: 12px 14px;
  font-size: 13px;
  line-height: 1.4;
}

.filters-row {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

.filter-btn {
  height: 34px;
  padding: 0 14px;
  border-radius: 10px;
  background: #f4f6fa;
  color: #4f5f70;
  font-size: 12px;
  font-weight: 700;
}

@media (max-width: 1180px) {
  .search-shell {
    grid-template-columns: 1fr;
  }

  .results-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
