<template>
  <article class="mobile-card">
    <div class="media" :style="mediaStyle">
      <div class="media-glow media-glow--first"></div>
      <div class="media-glow media-glow--second"></div>
      <div class="media-grid"></div>

      <div class="media-header">
        <div class="tags">
          <span class="tag">
            <img src="/assets/icons/Vector.png" alt="" />
            <span>Reels</span>
          </span>
          <span class="tag">
            <img src="/assets/icons/Vector-15.png" alt="" />
            <span>X{{ activityMultiplier }}</span>
          </span>
        </div>

        <div class="actions">
          <span class="action"><img src="/assets/icons/heart-outline.png" alt="" /></span>
          <span class="action"><span>↗</span></span>
        </div>
      </div>

      <div class="media-copy">
        <p class="media-overline">Разбор ролика</p>
        <p class="media-title">{{ posterCopy.headline }}</p>
        <div class="media-note">{{ posterCopy.note }}</div>
      </div>

      <div class="stats">
        <div class="cell">
          <img src="/assets/icons/Vector-14.png" alt="" />
          <span>{{ metrics.views }}</span>
        </div>
        <div class="cell">
          <img src="/assets/icons/Vector-11.png" alt="" />
          <span>{{ metrics.likes }}</span>
        </div>
        <div class="cell">
          <img src="/assets/icons/Vector-4.png" alt="" />
          <span>{{ metrics.comments }}</span>
        </div>
        <div class="cell">
          <img src="/assets/icons/Vector-3.png" alt="" />
          <span>{{ metrics.shares }}</span>
        </div>
      </div>
    </div>

    <div class="author-row">
      <img src="/assets/avatar-feed.png" alt="" class="avatar" />
      <div class="author-meta">
        <p class="name">{{ handle }}</p>
        <p class="subs">{{ followers }}</p>
      </div>
      <img src="/assets/icons/Vector-5.png" alt="" class="tool" />
    </div>

    <p class="title">{{ sourcePost.title }}</p>
    <p class="description">{{ previewText }}</p>
    <time class="date">{{ formattedCreatedAt }}</time>
    <button type="button" class="action-btn">Анализ</button>
  </article>
</template>

<script setup>
import { computed } from "vue";

import { buildFollowers, buildHandle, buildMediaPalette, buildPosterCopy, buildPostMetrics } from "../services/postPresentation";

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
      title: "Разбор ролика: почему это видео зашло",
      text: "500 000 лайков на ютубе делаем, разберем механику удержания и лид-магнит.",
      created_at: new Date().toISOString(),
    }
  );
});

const metrics = computed(() => buildPostMetrics(sourcePost.value.id));
const handle = computed(() => buildHandle(sourcePost.value.user_id));
const followers = computed(() => buildFollowers(sourcePost.value.user_id));
const posterCopy = computed(() => buildPosterCopy(sourcePost.value));
const activityMultiplier = computed(() => ((sourcePost.value.id % 12) + 3).toString());

const mediaStyle = computed(() => {
  const palette = buildMediaPalette(sourcePost.value.id);

  return {
    "--media-start": palette.start,
    "--media-end": palette.end,
    "--media-glow": palette.glow,
    "--media-surface": palette.surface,
  };
});

const previewText = computed(() => {
  const raw = sourcePost.value.text || "";
  if (raw.length <= 68) return raw;
  return `${raw.slice(0, 68)}...`;
});

const formattedCreatedAt = computed(() => {
  const date = new Date(sourcePost.value.created_at);
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
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
  height: 400px;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  background:
    radial-gradient(circle at 24% 22%, var(--media-glow) 0, transparent 34%),
    linear-gradient(160deg, var(--media-start) 0%, var(--media-end) 100%);
}

.media-glow {
  position: absolute;
  border-radius: 999px;
  filter: blur(12px);
}

.media-glow--first {
  width: 168px;
  height: 168px;
  right: -18px;
  top: 64px;
  background: var(--media-glow);
}

.media-glow--second {
  width: 126px;
  height: 126px;
  left: -22px;
  bottom: 110px;
  background: rgba(255, 255, 255, 0.16);
}

.media-grid {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 22px 22px;
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

.tag img {
  width: 16px;
  height: 16px;
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
  color: #ffffff;
}

.action img {
  width: 20px;
  height: 20px;
  filter: brightness(0) invert(1);
}

.action span {
  font-size: 22px;
  line-height: 1;
  transform: translateY(-1px);
}

.media-copy {
  position: absolute;
  left: 16px;
  right: 16px;
  bottom: 74px;
}

.media-overline {
  margin: 0;
  color: rgba(255, 255, 255, 0.72);
  font-size: 11px;
  line-height: 1.2;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.media-title {
  margin: 10px 0 0;
  color: #ffffff;
  font-size: 28px;
  line-height: 0.95;
  font-weight: 700;
  letter-spacing: -0.04em;
  text-shadow: 0 4px 24px rgba(0, 0, 0, 0.26);
  max-width: 190px;
}

.media-note {
  margin-top: 12px;
  width: fit-content;
  max-width: 176px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  color: #111827;
  padding: 8px 10px;
  box-shadow: 0 8px 20px rgba(22, 22, 22, 0.15);
  font-size: 11px;
  line-height: 1.15;
  font-weight: 600;
}

.stats {
  position: absolute;
  left: 12px;
  right: 12px;
  bottom: 8px;
  border-radius: 12px;
  background: var(--media-surface);
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
  line-height: 14.5px;
  letter-spacing: 0.4px;
}

.cell img {
  width: 20px;
  height: 20px;
}

.author-row {
  margin-top: 4px;
  padding: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.name {
  margin: 0;
  color: #2b31b3;
  font-size: 14px;
  line-height: 21px;
  letter-spacing: 0.1px;
  font-weight: 600;
}

.subs {
  margin: 0;
  color: #4e616b;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.4px;
}

.tool {
  margin-left: auto;
  width: 24px;
  height: 24px;
}

.title {
  margin: 0;
  padding: 0 4px;
  color: #25303d;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
  font-weight: 600;
}

.description {
  margin: 2px 0 0;
  padding: 0 4px;
  min-height: 44px;
  color: #4e616b;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
}

.date {
  display: block;
  margin-top: 4px;
  padding: 0 4px;
  color: #a0adb4;
  font-size: 12px;
  line-height: 14.5px;
  letter-spacing: 0.4px;
}

.action-btn {
  margin: 8px 4px 0;
  width: calc(100% - 8px);
  height: 40px;
  border: 0;
  border-radius: 12px;
  background: #2b31b3;
  color: #ffffff;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.4px;
  font-weight: 600;
}
</style>
