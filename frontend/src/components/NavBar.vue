<template>
  <nav class="top-bar">
    <div class="navbar-left">
      <!-- Space for logo -->
      <div class="logo-placeholder"></div>
      <span class="navbar-title">{{ title }}</span>
    </div>
  </nav>
</template>

<script setup>
// Define props
defineProps({
  title: {
    type: String,
    default: 'Soundseal Factory Application'
  }
});
</script>

<style scoped>
.top-bar {
  display: flex;
  align-items: center;
  padding: 16px 32px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.navbar-left {
  display: flex;
  align-items: center;
}

.logo-placeholder {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #64748b 0%, #475569 100%);
  border-radius: 8px;
  margin-right: 12px;
  box-shadow: 0 2px 8px rgba(100, 116, 139, 0.15);
  position: relative;
  overflow: hidden;
}

.logo-placeholder::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 16px;
  height: 16px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
}

.navbar-title {
  font-size: 20px;
  font-weight: 600;
  color: #334155;
  letter-spacing: 0.3px;
}
</style>