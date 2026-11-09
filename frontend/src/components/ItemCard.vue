<template>
  <div class="item-card">
    <!-- Top Badges Row -->
    <div class="card-header">
      <div class="left-badges">
        <!-- Category Badge -->
        <span :class="['badge', categoryClass]">
          {{ categoryLabel }}
        </span>

        <!-- Campus Badge -->
        <span :class="['badge', campusClass]">
          📍 {{ item.campus || '全部校区' }}
        </span>
      </div>

      <!-- Deadline Countdown Badge -->
      <div class="deadline-badge-box">
        <span :class="['countdown-badge', countdownStatus.level]">
          <span class="icon">{{ countdownStatus.icon }}</span>
          <span>{{ countdownStatus.text }}</span>
        </span>
      </div>
    </div>

    <!-- Title -->
    <h3 class="card-title" @click="$emit('select', item)" :title="item.title">
      {{ item.title }}
    </h3>

    <!-- Source Department & Location -->
    <div class="meta-row">
      <span class="source-tag">
        🏛️ {{ item.source_site || '学校通知' }}
      </span>
      <span v-if="item.location" class="location-tag" :title="item.location">
        📌 {{ item.location }}
      </span>
    </div>

    <!-- Summary -->
    <p class="summary-text">
      {{ item.summary || item.content_raw || '暂无摘要' }}
    </p>

    <!-- Tags -->
    <div class="tags-row" v-if="tagList.length">
      <span v-for="tag in tagList" :key="tag" class="tag-pill">
        #{{ tag }}
      </span>
    </div>

    <!-- Card Footer -->
    <div class="card-footer">
      <div class="footer-meta">
        <span class="date" title="发布日期">
          📅 {{ item.publish_date || '近期' }}
        </span>
        <span class="views" title="热度/阅读量">
          👁️ {{ item.view_count || 0 }}
        </span>
      </div>

      <div class="footer-actions">
        <el-button size="small" type="primary" plain @click="$emit('select', item)">
          情报详情
        </el-button>
        <a
          v-if="item.url"
          :href="item.url"
          target="_blank"
          rel="noopener noreferrer"
          class="ext-link"
          title="跳转校园网原文"
        >
          原文 ↗
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

defineEmits(['select'])

const categoryLabel = computed(() => {
  const map = {
    academic: '🎓 学术讲座',
    competition: '🏆 竞赛选拔',
    scholarship: '📜 奖助评优',
    notice: '📢 综合公告'
  }
  return map[props.item.category] || '📌 情报条目'
})

const categoryClass = computed(() => {
  if (props.item.category === 'competition') return 'cat-competition'
  if (props.item.category === 'academic') return 'cat-academic'
  return 'cat-default'
})

const campusClass = computed(() => {
  const map = {
    翡翠湖: 'campus-fch',
    屯溪路: 'campus-txl',
    宣城: 'campus-xc'
  }
  return map[props.item.campus] || 'campus-all'
})

const tagList = computed(() => {
  if (!props.item.tags) return []
  return props.item.tags.split(',').map(t => t.trim()).filter(Boolean)
})

// Countdown computation
const countdownStatus = computed(() => {
  if (!props.item.deadline) {
    return { level: 'neutral', icon: '🔔', text: '日常进行' }
  }

  const deadline = new Date(props.item.deadline).getTime()
  const now = new Date().getTime()
  const diffMs = deadline - now

  if (diffMs <= 0) {
    return { level: 'expired', icon: '⏹️', text: '已截止' }
  }

  const hours = Math.floor(diffMs / (1000 * 60 * 60))
  const days = Math.floor(hours / 24)

  if (days === 0) {
    return { level: 'urgent', icon: '🔥', text: `距截止仅剩 ${hours} 小时` }
  } else if (days <= 3) {
    return { level: 'urgent', icon: '⚡', text: `距截止 ${days} 天 ${hours % 24} 时` }
  } else if (days <= 7) {
    return { level: 'warning', icon: '⏳', text: `距截止 ${days} 天` }
  } else {
    return { level: 'normal', icon: '📅', text: `距截止 ${days} 天` }
  }
})
</script>

<style scoped>
.item-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
}

.item-card:hover {
  transform: translateY(-3px);
  border-color: #cbd5e1;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.left-badges {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.badge {
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
}

.cat-competition {
  background: #faf5ff;
  color: #7e22ce;
  border: 1px solid #f3e8ff;
}

.cat-academic {
  background: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #dbeafe;
}

.cat-default {
  background: #f1f5f9;
  color: #475569;
}

.campus-fch {
  background: #f0fdfa;
  color: #0d9488;
  border: 1px solid #ccfbf1;
}

.campus-txl {
  background: #fffbeb;
  color: #b45309;
  border: 1px solid #fef3c7;
}

.campus-xc {
  background: #fdf2f8;
  color: #be185d;
  border: 1px solid #fce7f3;
}

.campus-all {
  background: #f8fafc;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.countdown-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: 9999px;
}

.countdown-badge.urgent {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  animation: pulse-badge 2s infinite;
}

.countdown-badge.warning {
  background: #fffbeb;
  color: #d97706;
  border: 1px solid #fef3c7;
}

.countdown-badge.normal {
  background: #f0fdf4;
  color: #16a34a;
  border: 1px solid #dcfce7;
}

.countdown-badge.neutral {
  background: #f1f5f9;
  color: #64748b;
}

.countdown-badge.expired {
  background: #f1f5f9;
  color: #94a3b8;
  text-decoration: line-through;
}

@keyframes pulse-badge {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.75; }
}

.card-title {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.45;
  cursor: pointer;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.15s;
}

.card-title:hover {
  color: #2563eb;
}

.meta-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
  font-size: 0.75rem;
  color: #64748b;
  margin-bottom: 0.65rem;
}

.source-tag {
  font-weight: 600;
  color: #334155;
}

.location-tag {
  color: #64748b;
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.summary-text {
  font-size: 0.82rem;
  color: #475569;
  line-height: 1.55;
  margin: 0 0 0.85rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-bottom: 1rem;
}

.tag-pill {
  font-size: 0.7rem;
  background: #f8fafc;
  color: #475569;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  padding: 0.1rem 0.4rem;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.75rem;
  border-top: 1px dashed #e2e8f0;
  font-size: 0.75rem;
  color: #94a3b8;
}

.footer-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.footer-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.ext-link {
  font-size: 0.75rem;
  color: #64748b;
  text-decoration: none;
  font-weight: 500;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
}

.ext-link:hover {
  color: #2563eb;
  background: #eff6ff;
}
</style>
