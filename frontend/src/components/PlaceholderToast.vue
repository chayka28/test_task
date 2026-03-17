<template>
  <div class="toast" role="status" aria-live="polite">
    <span class="toast-title">{{ title }}</span>
    <span v-if="text" class="toast-text">{{ text }}</span>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  text: {
    type: String,
    default: "",
  },
});
</script>

<style scoped>
.toast {
  min-width: 240px;
  max-width: 420px;
  border-radius: 18px;
  background: rgba(25, 30, 44, 0.92);
  box-shadow: 0 20px 48px rgba(13, 18, 32, 0.24);
  color: #ffffff;
  padding: 14px 16px;
  display: grid;
  gap: 4px;
}

.toast-title {
  font-size: 14px;
  line-height: 1.2;
  font-weight: 700;
}

.toast-text {
  font-size: 13px;
  line-height: 1.4;
  color: rgba(255, 255, 255, 0.78);
}
</style>
