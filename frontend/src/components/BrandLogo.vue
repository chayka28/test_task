<template>
  <div class="brand" :class="{ 'brand--compact': compact }">
    <svg class="brand-icon" viewBox="0 0 34 24" aria-hidden="true">
      <path
        d="M1.8 12C5.4 5.7 10.5 2.6 17 2.6C23.5 2.6 28.6 5.7 32.2 12C28.6 18.3 23.5 21.4 17 21.4C10.5 21.4 5.4 18.3 1.8 12Z"
        fill="none"
        stroke="#1c2030"
        stroke-width="3.2"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <circle cx="17" cy="12" r="7.2" fill="#1c2030" />
      <path
        d="M17 6.2C18.8 8.5 19.8 10.2 19.8 11.8C19.8 14 18.5 15.8 16.7 16.5C15.1 15.8 14 14.3 14 12.6C14 11 14.8 9.4 17 6.2Z"
        fill="#ffffff"
      />
    </svg>

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
  display: block;
}

.brand-text {
  color: #1f2230;
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
