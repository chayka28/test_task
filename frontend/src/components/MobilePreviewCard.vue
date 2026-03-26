<template>
  <article class="mobile-card">
    <div class="media" :style="mediaStyle">
      <div v-if="sourcePost.poster_url" class="media-poster" :style="mediaPosterStyle"></div>

      <div class="media-header">
        <div class="tags">
          <span class="tag"><img src="/assets/icons/Vector-33.png" alt="" /><span>Reels</span></span>
          <span class="tag"><img src="/assets/icons/Vector-1.png" alt="" /><span>X{{ activityMultiplier }}</span></span>
        </div>

        <div class="actions">
          <span class="action"><img src="/assets/icons/Heart.png" alt="" /></span>
          <span class="action"><img src="/assets/icons/external-link.png" alt="" /></span>
        </div>
      </div>

      <div class="stats">
        <div class="cell"><img src="/assets/icons/Vector-2.png" alt="" /><span>{{ metrics.views }}</span></div>
        <div class="cell"><img src="/assets/icons/Heart.png" alt="" /><span>{{ metrics.likes }}</span></div>
        <div class="cell"><img src="/assets/icons/Vector-4.png" alt="" /><span>{{ metrics.comments }}</span></div>
        <div class="cell"><img src="/assets/icons/Icon.png" alt="" /><span>{{ metrics.shares }}</span></div>
      </div>
    </div>

    <div class="author-row">
      <AppAvatar :avatar="sourcePost.poster_url || ''" :seed="sourcePost.id" :size="40" alt="Креатор" />
      <div class="author-meta">
        <p class="name">{{ handle }}</p>
        <p class="subs">{{ followers }}</p>
      </div>
      <img src="/assets/icons/Icon-1.png" alt="" class="tool" />
    </div>

    <p class="title">{{ sourcePost.title }}</p>
    <p class="description">{{ previewText }}</p>
    <time class="date">{{ formattedCreatedAt }}</time>
    <button type="button" class="action-btn">Анализ</button>
  </article>
</template>

<script setup>
import { computed } from 'vue';

import AppAvatar from './AppAvatar.vue';
import { buildFollowers, buildMediaPalette, buildPostMetrics, buildUserHandle } from '../services/postPresentation';

const props = defineProps({
  post: {
    type: Object,
    default: null,
  },
});

const sourcePost = computed(() => {
  return (
    props.post || {
      id: 1,
      user_id: 1,
      title: 'Разбор ролика: почему это видео зашло',
      text: '500 000 лайков на ютубе делаем, разберем механику удержания и лид-магнит.',
      created_at: new Date().toISOString(),
    }
  );
});

const metrics = computed(() => buildPostMetrics(sourcePost.value.id));
const handle = computed(() => buildUserHandle(sourcePost.value.user_name, sourcePost.value.user_id));
const followers = computed(() => buildFollowers(sourcePost.value.user_id));
const activityMultiplier = computed(() => ((sourcePost.value.id % 12) + 3).toString());

const mediaStyle = computed(() => {
  const palette = buildMediaPalette(sourcePost.value.id);

  return {
    '--media-start': palette.start,
    '--media-end': palette.end,
    '--media-glow': palette.glow,
    '--media-surface': palette.surface,
  };
});

const mediaPosterStyle = computed(() => {
  if (!sourcePost.value.poster_url) return {};

  return {
    backgroundImage: `url(${sourcePost.value.poster_url})`,
  };
});

const previewText = computed(() => {
  const raw = sourcePost.value.text || '';
  if (raw.length <= 68) return raw;
  return `${raw.slice(0, 68)}...`;
});

const formattedCreatedAt = computed(() => {
  const date = new Date(sourcePost.value.created_at);
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(date);
});
</script>

<style scoped>
.mobile-card {
  width: 262px;
  border-radius: 16px;
  background: #ffffff;
  padding: 4px 4px 8px;
}

.media {
  width: 254px;
  aspect-ratio: 254 / 400;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  background: linear-gradient(160deg, var(--media-start) 0%, var(--media-end) 100%);
}

.media-poster {
  position: absolute;
  inset: 0;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  opacity: 0.9;
}

.media-header {
  position: absolute;
  inset: 12px 12px auto;
  display: flex;
  justify-content: space-between;
}

.tags {
  display: grid;
  gap: 6px;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  color: #ffffff;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
  padding: 4px 8px;
}

.tag img,
.action img {
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.actions {
  display: grid;
  gap: 8px;
}

.action {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  display: grid;
  place-items: center;
}

.stats {
  position: absolute;
  left: 12px;
  right: 12px;
  bottom: 8px;
  border-radius: 12px;
  background: rgba(60, 27, 28, 0.74);
  backdrop-filter: blur(4px);
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  padding: 8px 4px;
}

.cell {
  display: grid;
  justify-items: center;
  gap: 4px;
  color: #ffffff;
  font-size: 12px;
  line-height: 1;
}

.cell img {
  width: 16px;
  height: 16px;
  object-fit: contain;
}

.author-row {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-meta {
  min-width: 0;
}

.name {
  margin: 0;
  color: #2f38c7;
  font-size: 14px;
  line-height: 1.1;
  font-weight: 700;
}

.subs {
  margin: 2px 0 0;
  color: #7d8a96;
  font-size: 12px;
  line-height: 1.2;
}

.tool {
  width: 24px;
  height: 24px;
  margin-left: auto;
  object-fit: contain;
}

.title,
.description {
  margin: 8px 0 0;
  color: #536875;
  font-size: 12px;
  line-height: 15px;
}

.title {
  color: #202b38;
  font-weight: 500;
}

.date {
  display: block;
  margin: 10px 0 9px;
  color: #a3aeb8;
  font-size: 12px;
  line-height: 1;
}

.action-btn {
  width: 100%;
  height: 40px;
  border: 0;
  border-radius: 11px;
  background: #3138c8;
  color: #ffffff;
  font-size: 14px;
  line-height: 1;
  font-weight: 700;
}
</style>
