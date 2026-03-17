<template>
  <div class="avatar-shell" :style="shellStyle">
    <img v-if="avatarVisual.kind === 'image' && !blurred" :src="avatarVisual.value" :alt="alt" class="avatar-image" />
    <div
      v-else
      class="avatar-fill"
      :class="{ 'avatar-fill--blurred': blurred }"
      :style="{ background: avatarVisual.value }"
      :aria-label="alt"
    ></div>
  </div>
</template>

<script setup>
import { computed } from "vue";

import { buildMediaPalette } from "../services/postPresentation";
import { resolveAvatarVisual } from "../services/avatarPresets";

const props = defineProps({
  avatar: {
    type: String,
    default: "",
  },
  seed: {
    type: Number,
    default: 1,
  },
  size: {
    type: Number,
    default: 40,
  },
  alt: {
    type: String,
    default: "Аватар",
  },
  blurred: {
    type: Boolean,
    default: false,
  },
});

const shellStyle = computed(() => ({
  width: `${props.size}px`,
  height: `${props.size}px`,
}));

const avatarVisual = computed(() => {
  if (props.blurred) {
    const palette = buildMediaPalette(props.seed);
    return {
      kind: "gradient",
      value: `linear-gradient(160deg, ${palette.start} 0%, ${palette.end} 100%)`,
    };
  }

  return resolveAvatarVisual(props.avatar, props.seed);
});
</script>

<style scoped>
.avatar-shell {
  border-radius: 50%;
  overflow: hidden;
  flex: 0 0 auto;
  background: #e5e7eb;
}

.avatar-image,
.avatar-fill {
  width: 100%;
  height: 100%;
  display: block;
}

.avatar-image {
  object-fit: cover;
}

.avatar-fill {
  position: relative;
}

.avatar-fill--blurred {
  filter: blur(1.5px) saturate(1.1);
  transform: scale(1.08);
}

.avatar-fill::after {
  content: "";
  position: absolute;
  inset: 8% 10% auto auto;
  width: 38%;
  height: 38%;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.18);
}
</style>
