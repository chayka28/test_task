<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card" role="dialog" aria-modal="true" aria-label="Просмотр публикации">
      <button class="close-btn" type="button" @click="$emit('close')">
        <img src="/assets/icons/close-button.png" alt="Закрыть" />
      </button>

      <div class="modal-layout">
        <aside class="left-column">
          <div class="preview-card">
            <div class="preview-media" :style="mediaStyle">
              <div v-if="post.poster_url" class="preview-poster" :style="previewPosterStyle"></div>
              <div class="preview-tags">
                <span class="preview-tag">
                  <img src="/assets/icons/Vector-33.png" alt="" />
                  <span>Reels</span>
                </span>
                <span class="preview-tag">
                  <img src="/assets/icons/Vector-1.png" alt="" />
                  <span>X{{ activityMultiplier }}</span>
                </span>
              </div>

              <button type="button" class="play-btn" @click="handleRestrictedAction('Просмотр видео')">
                <img src="/assets/icons/play-button.png" alt="Воспроизвести" />
              </button>
            </div>

            <div class="preview-meta-row">
              <time class="preview-date">{{ cardDate }}</time>
              <button type="button" class="preview-link" @click="openSource">
                <img src="/assets/icons/Vector-26.png" alt="Открыть источник" />
              </button>
            </div>

            <div class="author-row" role="button" tabindex="0" @click.stop="$emit('placeholder', 'Профиль автора')">
              <AppAvatar :avatar="post.poster_url || ''" :seed="post.id" :size="34" alt="Креатор" />
              <div class="author-copy">
                <p class="author-name">{{ authorHandle }}</p>
                <p class="author-followers">{{ followers }}</p>
              </div>
              <button type="button" class="author-tool-btn" @click.stop="handleRestrictedAction('Инструменты карточки')">
                <img src="/assets/icons/Icon-1.png" alt="" />
              </button>
            </div>

            <p class="preview-text">{{ excerptText }}</p>

            <div class="metric-list">
              <div class="metric-item">
                <span class="metric-label"><img src="/assets/icons/Vector (2).png" alt="" />Просмотры</span>
                <span>{{ metricRows.views }}</span>
              </div>
              <div class="metric-item">
                <span class="metric-label"><img src="/assets/icons/Vector-1 (2).png" alt="" />Лайки</span>
                <span>{{ metricRows.likes }}</span>
              </div>
              <div class="metric-item">
                <span class="metric-label"><img src="/assets/icons/Vector-2 (2).png" alt="" />Комментарии</span>
                <span>{{ metricRows.comments }}</span>
              </div>
              <div class="metric-item">
                <span class="metric-label"><img src="/assets/icons/Vector-3 (2).png" alt="" />Репосты</span>
                <span>{{ metricRows.shares }}</span>
              </div>
              <div class="metric-item">
                <span class="metric-label"><img src="/assets/icons/Vector-4 (2).png" alt="" />ER</span>
                <span>{{ metricRows.er }}</span>
              </div>
            </div>
          </div>
        </aside>

        <section class="right-column">
          <p class="section-overline">Тема видео</p>
          <h2 class="modal-title">{{ post.title }}</h2>

          <div class="title-meta-row">
            <span class="audio-pill">
              <img src="/assets/icons/music-icon.png" alt="" />
              <span>Tyga - Pop it off</span>
            </span>
            <span class="lang-copy">Язык:</span>
            <span class="lang-pill"><span class="lang-flag">🇬🇧</span><span>Английский</span></span>
          </div>

          <div class="chip-row">
            <span class="chip chip-blue">Туториал</span>
            <span class="chip chip-green">Энергичное видео</span>
            <span class="chip chip-orange">Изи монтаж</span>
            <span class="chip chip-pink">Трендовый звук</span>
            <span class="chip chip-yellow">Лид магнит</span>
            <span class="chip chip-violet">Красота и здоровье</span>
          </div>

          <section class="content-block">
            <div class="block-head">
              <h3>Транскрибация</h3>
              <div class="block-tools">
                <button type="button" class="translated-pill" @click="handleRestrictedAction('Перевод публикации')">
                  <img src="/assets/icons/Vector-5 (2).png" alt="" />
                  <span>Переведено</span>
                </button>
                <button type="button" class="copy-btn" @click="handleRestrictedAction('Скопировать блок')">
                  <img src="/assets/icons/copy-button.png" alt="" />
                </button>
              </div>
            </div>
            <div class="block-surface transcript-surface">
              <p>{{ transcriptParagraphs[0] }}</p>
              <p>{{ transcriptParagraphs[1] }}</p>
              <p>{{ transcriptParagraphs[2] }}</p>
              <button type="button" class="more-link" @click="handleRestrictedAction('Показать полный текст')">
                <img src="/assets/icons/chevron-down-black.png" alt="" />
                <span>Ещё</span>
              </button>
            </div>
          </section>

          <div class="action-row">
            <button type="button" class="adapt-btn" @click="handleRestrictedAction('Адаптировать')">
              <img src="/assets/icons/Vector-7 (2).png" alt="" />
              <span>Адаптировать</span>
            </button>

            <div v-if="canManagePost" class="manage-row">
              <button type="button" class="manage-btn" :disabled="isSaving" @click="$emit('edit', post)">
                {{ isSaving ? 'Сохраняем...' : 'Редактировать' }}
              </button>
              <button type="button" class="manage-btn manage-btn--danger" :disabled="isDeleting" @click="$emit('delete', post)">
                {{ isDeleting ? 'Удаляем...' : 'Удалить' }}
              </button>
            </div>
          </div>

          <section class="content-block">
            <h3>Суть</h3>
            <div class="block-surface">
              <p>{{ essenceText }}</p>
            </div>
          </section>

          <section class="structure-block">
            <h3>Структура</h3>
            <div class="structure-line">
              <div class="structure-track" aria-hidden="true"></div>
              <div class="structure-step">
                <div class="step-time"><span class="step-plus">+</span><span class="step-time-text">0-3 сек</span></div>
                <img src="/assets/icons/structure-dashed.png" alt="" class="structure-marker structure-marker--dashed" />
                <div class="step-copy">
                  <h4>Шок-сравнение</h4>
                  <p>Визуальный (Девушка с предметом) + Текст на экране: "Это спасет вашу зиму"</p>
                </div>
              </div>
              <div class="structure-step">
                <div class="step-time"><span class="step-plus">+</span><span class="step-time-text">3-15 сек</span></div>
                <img src="/assets/icons/structure-ring.png" alt="" class="structure-marker structure-marker--ring" />
                <div class="step-copy">
                  <h4>Сюжет</h4>
                  <p>[Герой] показывает проблему → Резкая смена кадра → Решение</p>
                </div>
              </div>
              <div class="structure-step">
                <div class="step-time"><span class="step-plus">+</span><span class="step-time-text step-time-text--multiline">15-120<br />сек</span></div>
                <img src="/assets/icons/structure-dot.png" alt="" class="structure-marker structure-marker--dot" />
                <div class="step-copy">
                  <h4>Финал / CTA</h4>
                  <p>Призыв: "Пиши слово \"ССЫЛКА\" в комменты"</p>
                </div>
              </div>
            </div>
          </section>

          <section class="content-block">
            <div class="block-head">
              <h3>Хук фраза</h3>
              <button type="button" class="copy-btn" @click="handleRestrictedAction('Скопировать блок')">
                <img src="/assets/icons/copy-button.png" alt="" />
              </button>
            </div>
            <div class="block-surface grouped-hook-surface">
              <div class="hook-entry">
                <p class="hook-text">Одна из них — пустышка. Угадаешь какая?</p>
              </div>

              <div class="hook-section">
                <div class="block-head block-head--sub">
                  <h3>Визуальный хук</h3>
                  <button type="button" class="copy-btn" @click="handleRestrictedAction('Скопировать блок')">
                    <img src="/assets/icons/copy-button.png" alt="" />
                  </button>
                </div>
                <div class="hook-entry">
                  <p class="hook-text">Одна из них — пустышка. Угадаешь какая?</p>
                </div>
              </div>

              <div class="hook-section">
                <div class="block-head block-head--sub">
                  <h3>Текстовый хук</h3>
                  <button type="button" class="copy-btn" @click="handleRestrictedAction('Скопировать блок')">
                    <img src="/assets/icons/copy-button.png" alt="" />
                  </button>
                </div>
                <div class="hook-entry">
                  <p class="hook-text">Одна из них — пустышка. Угадаешь какая?</p>
                </div>
              </div>
            </div>
          </section>

          <section class="content-block">
            <div class="block-head">
              <h3>Рабочие приемы</h3>
              <button type="button" class="copy-btn" @click="handleRestrictedAction('Скопировать блок')">
                <img src="/assets/icons/copy-button.png" alt="" />
              </button>
            </div>
            <div class="block-surface long-surface">
              <h4>2. Суть видео</h4>
              <p>Приём: "кому подходит / кому нет" двумя блоками.</p>
              <p>Почему сработало: это формат "диагноз → лечение → решение". Люди сохраняют не эмоции, а инструкцию. И это "обзор", а не философия.</p>

              <h4>3. Монтаж</h4>
              <p>Приём: смена планов каждые 1-2 секунды: лицо → продукт крупно → рука (демо) → снова лицо.</p>
              <p>Почему сработало: вертикалки смотрят на автопилоте. Частая смена планов держит внимание даже без звука.</p>
              <p>Приём: все доказательства — через B-roll вставки на 0.3-0.8 сек (катышки, блеск, этикетка, нанесение).</p>
              <p>Почему сработало: речь в кадре быстро утомляет. B-roll делает ощущение "я реально тестировал".</p>

              <h4>4. Реплики</h4>
              <p>Приём: "триггер доверия" одной фразой: "Я не продаю этот SPF, мне пох, скажу как есть."</p>
              <p>Почему сработало: снимает защиту "мне впаривают".</p>
              <p>Приём: "вилка выбора" в середине: "Если кожа жирная — делай так. Если сухая — так."</p>
              <p>Почему сработало: персонализация без долгого объяснения = удержание.</p>
            </div>
          </section>

          <section class="content-block">
            <div class="block-head">
              <h3>Воронка / Маркетинг</h3>
              <button type="button" class="copy-btn" @click="handleRestrictedAction('Скопировать блок')">
                <img src="/assets/icons/copy-button.png" alt="" />
              </button>
            </div>
            <div class="block-surface long-surface">
              <h4>CTA голос/визуал</h4>
              <p>Почему сработало: зритель узнаёт свой баг мгновенно. Это не "мнение", а физический факт в кадре, мозг цепляется.</p>
              <h4>Триггер</h4>
              <p>Почему сработало: зритель узнаёт свой баг мгновенно. Это не "мнение", а физический факт в кадре, мозг цепляется.</p>
              <h4>Куда ведет</h4>
              <p>Почему сработало: зритель узнаёт свой баг мгновенно. Это не "мнение", а физический факт в кадре, мозг цепляется.</p>
              <h4>Лид-магнит</h4>
              <p>Почему сработало: зритель узнаёт свой баг мгновенно. Это не "мнение", а физический факт в кадре, мозг цепляется.</p>
            </div>
          </section>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

import AppAvatar from './AppAvatar.vue';
import { buildFollowers, buildMediaPalette, buildPostMetrics, buildUserHandle } from '../services/postPresentation';

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
  canManagePost: {
    type: Boolean,
    default: false,
  },
  isSaving: {
    type: Boolean,
    default: false,
  },
  isDeleting: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['close', 'placeholder', 'edit', 'delete']);

const palette = computed(() => buildMediaPalette(props.post.id));
const metricRows = computed(() => buildPostMetrics(props.post.id));
const authorHandle = computed(() => buildUserHandle(props.post.user_name, props.post.user_id));
const followers = computed(() => buildFollowers(props.post.user_id));
const activityMultiplier = computed(() => ((props.post.id % 12) + 3).toString());

const mediaStyle = computed(() => ({
  '--preview-start': palette.value.start,
  '--preview-end': palette.value.end,
}));

const previewPosterStyle = computed(() => {
  if (!props.post.poster_url) return {};
  return {
    backgroundImage: `url(${props.post.poster_url})`,
  };
});

const cardDate = computed(() => {
  if (!props.post.created_at) return '—';
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(new Date(props.post.created_at));
});

const excerptText = computed(() => shortText(props.post.text, 110));
const essenceText = computed(() => shortText(props.post.text, 220));
const transcriptParagraphs = computed(() => {
  const text = props.post.text || 'SPF скатывается? Смотри — вот эти катышки. И нет, это не всегда плохой SPF.';
  return [
    shortText(text, 110),
    'Скатывается по трём причинам.',
    'Первая — ты намазал под SPF слишком много всего: сыворотка, крем, база... сверху SPF — и оно начинает конфликтовать. Чем больше слоёв, тем выше шанс, что всё свернётся в катышки....',
  ];
});

function shortText(text, maxLength) {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}...`;
}

function handleRestrictedAction(label) {
  emit('placeholder', label);
}

function openSource() {
  if (!props.post.source_url) {
    handleRestrictedAction('Открыть источник');
    return;
  }

  window.open(props.post.source_url, '_blank', 'noopener,noreferrer');
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(7, 9, 15, 0.62);
  backdrop-filter: blur(2px);
  display: flex;
  justify-content: flex-end;
}

.modal-card {
  width: min(1042px, calc(100vw - 12px));
  height: 100vh;
  overflow: auto;
  background: #ffffff;
  border-radius: 20px 0 0 20px;
  padding: 18px 22px 28px 18px;
  position: relative;
}

.close-btn {
  position: absolute;
  right: 16px;
  top: 16px;
  width: 40px;
  height: 40px;
  border: 0;
  background: transparent;
  padding: 0;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.close-btn img {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.modal-layout {
  display: grid;
  grid-template-columns: 194px minmax(0, 1fr);
  gap: 28px;
}

.left-column {
  padding-top: 2px;
}

.preview-card {
  padding-right: 2px;
}

.preview-media {
  position: relative;
  aspect-ratio: 176 / 296;
  border-radius: 18px;
  overflow: hidden;
  background: linear-gradient(160deg, var(--preview-start) 0%, var(--preview-end) 100%);
}

.preview-poster {
  position: absolute;
  inset: 0;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.preview-tags {
  position: absolute;
  left: 12px;
  top: 12px;
  display: grid;
  gap: 8px;
}

.preview-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 30px;
  padding: 0 10px;
  border-radius: 10px;
  background: rgba(65, 55, 45, 0.68);
  color: #ffffff;
  font-size: 12px;
  line-height: 1;
  font-weight: 500;
  backdrop-filter: blur(8px);
}

.preview-tag img {
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.play-btn {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 64px;
  height: 64px;
  border: 0;
  background: transparent;
  padding: 0;
  cursor: pointer;
}

.play-btn img {
  width: 64px;
  height: 64px;
  object-fit: contain;
}

.preview-meta-row {
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.preview-date {
  color: #99a7b8;
  font-size: 12px;
  line-height: 1;
  font-weight: 500;
}

.preview-link {
  border: 0;
  background: transparent;
  width: 18px;
  height: 18px;
  padding: 0;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.preview-link img {
  width: 18px;
  height: 18px;
  object-fit: contain;
}

.author-row {
  margin-top: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.author-copy {
  min-width: 0;
}

.author-name {
  margin: 0;
  color: #3240db;
  font-size: 13px;
  line-height: 1.1;
  font-weight: 700;
}

.author-followers {
  margin: 2px 0 0;
  color: #6d7e8e;
  font-size: 12px;
  line-height: 1.2;
}

.author-tool-btn {
  margin-left: auto;
  border: 0;
  background: transparent;
  padding: 0;
  width: 24px;
  height: 24px;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.author-tool-btn img {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.preview-text {
  margin: 10px 0 0;
  color: #384854;
  font-size: 12px;
  line-height: 1.35;
  font-weight: 500;
}

.metric-list {
  margin-top: 14px;
  display: grid;
  gap: 8px;
}

.metric-item {
  min-height: 31px;
  border-radius: 10px;
  background: #f3f4f8;
  padding: 0 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  color: #474f5a;
  font-size: 13px;
  line-height: 1;
  font-weight: 500;
}

.metric-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.metric-label img {
  width: 14px;
  height: 14px;
  object-fit: contain;
}

.right-column {
  padding-top: 2px;
  padding-right: 24px;
}

.section-overline {
  margin: 0;
  color: #6e8094;
  font-size: 14px;
  line-height: 1.2;
  font-weight: 600;
}

.modal-title {
  margin: 8px 0 0;
  color: #181d24;
  font-family: "Inter", Arial, sans-serif;
  font-size: 22px;
  line-height: 1.18;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.title-meta-row {
  margin-top: 14px;
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}

.audio-pill,
.lang-pill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  color: #6c7a88;
  font-size: 15px;
  line-height: 1;
}

.audio-pill img {
  width: 14px;
  height: 14px;
  object-fit: contain;
}

.lang-copy {
  color: #7b8893;
  font-size: 15px;
  line-height: 1;
}

.lang-flag {
  font-size: 18px;
  line-height: 1;
}

.chip-row {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chip {
  min-height: 30px;
  padding: 0 14px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  color: #4d5765;
  font-size: 14px;
  line-height: 1;
  font-weight: 600;
}

.chip-blue { background: #d9d8ff; color: #5d61e1; }
.chip-green { background: #ddf2c5; color: #64a933; }
.chip-orange { background: #ffe3bd; color: #d9871d; }
.chip-pink { background: #ffd7e5; color: #f14a82; }
.chip-yellow { background: #ffe2ba; color: #d29038; }
.chip-violet { background: #d9d9ff; color: #5a69d8; }

.content-block,
.structure-block {
  margin-top: 22px;
}

.block-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
}

.block-head--sub {
  margin-top: 18px;
}

.block-head h3,
.structure-block h3,
.content-block h3 {
  margin: 0;
  color: #171d24;
  font-size: 16px;
  line-height: 1.2;
  font-weight: 800;
}

.block-tools {
  display: flex;
  align-items: center;
  gap: 8px;
}

.translated-pill {
  min-height: 32px;
  border: 0;
  border-radius: 12px;
  background: #f3f4fb;
  padding: 0 12px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #5865de;
  font-size: 13px;
  line-height: 1;
  font-weight: 700;
  cursor: pointer;
}

.translated-pill img {
  width: 14px;
  height: 14px;
}

.copy-btn {
  width: 32px;
  height: 32px;
  border: 0;
  background: transparent;
  padding: 0;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.copy-btn img {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.block-surface {
  border-radius: 10px;
  background: #f3f5f8;
  padding: 15px 18px;
  color: #6a7987;
  font-size: 14px;
  line-height: 1.5;
}

.transcript-surface {
  min-height: 162px;
}

.transcript-surface p,
.long-surface p {
  margin: 0 0 12px;
}

.transcript-surface p:last-of-type,
.long-surface p:last-of-type {
  margin-bottom: 0;
}

.more-link {
  margin-top: 8px;
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 0;
  background: transparent;
  color: #31353b;
  font-size: 13px;
  line-height: 1;
  cursor: pointer;
}

.more-link img {
  width: 10px;
  height: 6px;
  object-fit: contain;
}

.action-row {
  margin-top: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
}

.adapt-btn {
  min-width: 178px;
  height: 50px;
  border: 0;
  border-radius: 12px;
  background: #3239ce;
  padding: 0 18px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #ffffff;
  font-size: 15px;
  line-height: 1;
  font-weight: 700;
  cursor: pointer;
}

.adapt-btn img {
  width: 18px;
  height: 18px;
}

.manage-row {
  display: flex;
  gap: 8px;
}

.manage-btn {
  height: 38px;
  border: 0;
  border-radius: 10px;
  background: #eff1f7;
  padding: 0 14px;
  color: #29303c;
  font-size: 13px;
  line-height: 1;
  font-weight: 700;
  cursor: pointer;
}

.manage-btn--danger {
  background: #fde8eb;
  color: #d64558;
}

.structure-line {
  margin-top: 12px;
  position: relative;
  display: grid;
  gap: 22px;
  padding-left: 104px;
}

.structure-track {
  position: absolute;
  left: 125px;
  top: 5px;
  bottom: 8px;
  width: 4px;
  background: url("/assets/icons/structure-line-full.png") center top / 4px 240px repeat-y;
}

.structure-step {
  display: grid;
  grid-template-columns: 94px 18px minmax(0, 1fr);
  gap: 14px;
  align-items: start;
  position: relative;
  z-index: 1;
}

.step-time {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #8d98a3;
  font-size: 13px;
  line-height: 1;
  font-weight: 500;
}

.step-plus {
  color: #7f8690;
  font-size: 24px;
  line-height: 1;
  font-weight: 300;
}

.step-time-text {
  display: inline-block;
  line-height: 1.08;
}

.step-time-text--multiline {
  line-height: 1.02;
}

.structure-marker {
  width: 18px;
  height: 18px;
  object-fit: contain;
  margin-top: 1px;
}

.step-copy h4,
.long-surface h4 {
  margin: 0 0 6px;
  color: #1a2027;
  font-size: 14px;
  line-height: 1.2;
  font-weight: 800;
}

.step-copy p {
  margin: 0;
  color: #73808b;
  font-size: 14px;
  line-height: 1.45;
}

.grouped-hook-surface {
  padding-top: 14px;
  padding-bottom: 18px;
}

.hook-entry {
  color: #798591;
  font-size: 14px;
  line-height: 1.45;
  padding-bottom: 8px;
}

.hook-text {
  margin: 0;
}

.hook-section + .hook-section {
  margin-top: 8px;
}

.long-surface h4:not(:first-child) {
  margin-top: 16px;
}

@media (max-width: 960px) {
  .modal-card {
    width: 100vw;
    border-radius: 0;
    padding-right: 12px;
  }

  .modal-layout {
    grid-template-columns: 1fr;
  }

  .right-column {
    padding-right: 8px;
  }
}
</style>
