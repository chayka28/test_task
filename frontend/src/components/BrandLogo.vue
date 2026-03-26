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
  gap: 8px;
  min-width: 0;
}

.brand--compact {
  gap: 8px;
}

.brand-icon {
  position: relative;
  width: 31px;
  height: 22px;
  flex: 0 0 31px;
}

.brand-outline,
.brand-center {
  position: absolute;
  display: block;
  pointer-events: none;
  user-select: none;
}

.brand-outline {
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: brightness(0);
}

.brand-center {
  left: 50%;
  top: 50%;
  width: auto;
  height: 54%;
  transform: translate(-50%, -48%);
  object-fit: contain;
  filter: brightness(0);
}

.brand-text {
  color: #16181f;
  font-size: 21px;
  line-height: 1;
  font-weight: 800;
  letter-spacing: -0.052em;
  font-family: Inter, Arial, sans-serif;
}

.brand-tag {
  border-radius: 12px;
  background: #e8edf2;
  color: #6d7c88;
  font-size: 10px;
  line-height: 1;
  font-weight: 700;
  padding: 6px 9px;
}
</style>
