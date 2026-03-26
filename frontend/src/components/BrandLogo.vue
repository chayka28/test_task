<template>
  <div class="brand" :class="{ 'brand--compact': compact }">
    <span class="brand-icon" aria-hidden="true">
      <img class="brand-mark" src="/assets/logo/loogo.png" alt="" />
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
  width: 30px;
  height: 21px;
  flex: 0 0 30px;
}

.brand-mark {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  pointer-events: none;
  user-select: none;
}

.brand-text {
  color: #131721;
  font-size: 17px;
  line-height: 1;
  font-weight: 700;
  letter-spacing: -0.03em;
  font-family: "Unbounded", "Inter", Arial, sans-serif;
}

.brand-tag {
  border-radius: 12px;
  background: #e8edf2;
  color: #667480;
  font-size: 10px;
  line-height: 1;
  font-weight: 700;
  padding: 6px 9px;
}
</style>
