<template>
  <div class="brand" :class="{ 'brand--compact': compact }">
    <span class="brand-icon" aria-hidden="true">
      <img class="brand-outline" src="/assets/logo/logo-outline.png" alt="" />
      <img class="brand-center" src="/assets/logo/logo-center.png" alt="" />
    </span>

    <template v-if="!iconOnly">
      <span class="brand-text">trendsee</span>
      <span v-if="showTag" class="brand-tag">Beta</span>
    </template>
  </div>
</template>

<script setup>
defineProps({
  iconOnly: {
    type: Boolean,
    default: false,
  },
  showTag: {
    type: Boolean,
    default: false,
  },
  compact: {
    type: Boolean,
    default: false,
  },
});
</script>

<style scoped>
.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.brand--compact {
  gap: 8px;
}

.brand-icon {
  width: 34px;
  height: 24px;
  flex: 0 0 34px;
  display: inline-block;
  position: relative;
}

.brand-outline,
.brand-center {
  position: absolute;
  display: block;
  user-select: none;
  pointer-events: none;
}

.brand-outline {
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: brightness(0) saturate(100%);
}

.brand-center {
  left: 50%;
  top: 51%;
  height: 56%;
  width: auto;
  transform: translate(-49%, -51%);
  object-fit: contain;
  filter: brightness(0) saturate(100%);
}

.brand-text {
  color: #111111;
  font-size: 24px;
  line-height: 1;
  font-weight: 900;
  letter-spacing: -0.04em;
}

.brand-tag {
  border-radius: 12px;
  background: #dce1e5;
  color: #6e7d89;
  font-size: 14px;
  line-height: 1;
  font-weight: 700;
  padding: 5px 8px;
}
</style>
