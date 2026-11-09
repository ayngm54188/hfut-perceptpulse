<template>
  <header class="navbar-wrapper">
    <div class="navbar-container">
      <!-- Brand & Title -->
      <div class="brand-section">
        <div class="logo-box">
          <span class="logo-icon">📡</span>
        </div>
        <div class="title-box">
          <div class="main-title">
            <span class="gradient-text">HFUT-PerceptPulse</span>
            <span class="system-tag">v0.1</span>
          </div>
          <div class="sub-title">合工大校园学术与竞赛情报感知系统</div>
        </div>
      </div>

      <!-- Right Section: Campus Badge & Engine Status -->
      <div class="status-section">
        <div class="campus-selector">
          <span class="label">当前校区:</span>
          <el-select
            v-model="currentCampus"
            placeholder="校区选择"
            size="small"
            style="width: 110px"
            @change="handleCampusChange"
          >
            <el-option label="全部校区" value="全部" />
            <el-option label="翡翠湖校区" value="翡翠湖" />
            <el-option label="屯溪路校区" value="屯溪路" />
            <el-option label="宣城校区" value="宣城" />
          </el-select>
        </div>

        <div class="engine-badge">
          <span class="pulse-dot"></span>
          <span class="pulse-text">情报感知引擎在线</span>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  campus: {
    type: String,
    default: '全部'
  }
})

const emit = defineEmits(['update:campus'])

const currentCampus = ref(props.campus)

function handleCampusChange(val) {
  emit('update:campus', val)
}
</script>

<style scoped>
.navbar-wrapper {
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 50;
}

.navbar-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand-section {
  display: flex;
  align-items: center;
  gap: 0.875rem;
}

.logo-box {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
}

.logo-icon {
  font-size: 1.35rem;
}

.title-box {
  display: flex;
  flex-direction: column;
}

.main-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: -0.025em;
}

.gradient-text {
  background: linear-gradient(120deg, #1e3a8a 0%, #2563eb 60%, #0284c7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.system-tag {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 0.1rem 0.4rem;
  background-color: #eff6ff;
  color: #2563eb;
  border-radius: 9999px;
  border: 1px solid #dbeafe;
}

.sub-title {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: -1px;
}

.status-section {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.campus-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.campus-selector .label {
  font-size: 0.8rem;
  color: #475569;
  font-weight: 500;
}

.engine-badge {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  padding: 0.3rem 0.7rem;
  border-radius: 9999px;
}

.pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: #16a34a;
  box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7);
  animation: pulse-ring 1.8s infinite;
}

@keyframes pulse-ring {
  0% {
    box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7);
  }
  70% {
    box-shadow: 0 0 0 6px rgba(22, 163, 74, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(22, 163, 74, 0);
  }
}

.pulse-text {
  font-size: 0.72rem;
  font-weight: 600;
  color: #15803d;
}

@media (max-width: 640px) {
  .sub-title {
    display: none;
  }
  .engine-badge {
    display: none;
  }
}
</style>
