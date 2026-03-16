<template>
  <div class="loading" role="status" aria-live="polite">
    <span class="spinner"></span>
    <span class="text">{{ label }}</span>
  </div>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    default: "Загружаем публикации...",
  },
});
</script>

<style scoped>
.loading {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 11px;
  color: #495474;
  background: #e9edf6;
  border: 1px solid #d6dcee;
}

.spinner {
  width: 12px;
  height: 12px;
  border: 2px solid #8f9bc9;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
