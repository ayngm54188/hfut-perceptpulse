<template>
  <el-dialog
    v-model="visible"
    :title="null"
    width="680px"
    class="custom-detail-dialog"
    destroy-on-close
  >
    <div v-if="item" class="modal-body">
      <!-- Header Area -->
      <div class="modal-header">
        <div class="header-top-row">
          <div class="badges-group">
            <span class="badge cat-badge">{{ categoryLabel }}</span>
            <span class="badge campus-badge">📍 {{ item.campus || '全部校区' }}</span>
            <span class="badge source-badge">🏛️ {{ item.source_site }}</span>
          </div>

          <!-- Favorite Button in Modal -->
          <button
            :class="['modal-fav-btn', { active: isStarred }]"
            :title="isStarred ? '取消关注' : '加入我的关注'"
            @click="handleToggleFav"
          >
            <span>{{ isStarred ? '★ 已关注' : '☆ 关注' }}</span>
          </button>
        </div>

        <h2 class="modal-title">{{ item.title }}</h2>
      </div>

      <!-- Info Meta Grid -->
      <div class="meta-grid">
        <div class="meta-item">
          <span class="meta-label">📅 发布日期:</span>
          <span class="meta-value">{{ item.publish_date || '近期' }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">⏰ 截止/开始时间:</span>
          <span class="meta-value highlight">{{ formatDeadline(item.deadline) }}</span>
        </div>
        <div class="meta-item" v-if="item.location">
          <span class="meta-label">📍 地点/形式:</span>
          <span class="meta-value">{{ item.location }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">👁️ 热度浏览:</span>
          <span class="meta-value">{{ item.view_count || 0 }} 次</span>
        </div>
      </div>

      <!-- Tags Section -->
      <div class="tags-section" v-if="tags.length">
        <span class="tags-title">主题标签:</span>
        <div class="tags-list">
          <el-tag v-for="tag in tags" :key="tag" size="small" effect="plain" class="tag-item">
            #{{ tag }}
          </el-tag>
        </div>
      </div>

      <!-- Summary Box -->
      <div class="summary-box" v-if="item.summary">
        <div class="summary-title">💡 情报摘要感知</div>
        <p class="summary-content">{{ item.summary }}</p>
      </div>

      <!-- Full Content -->
      <div class="content-section">
        <div class="section-title">📄 通知详情全文</div>
        <div class="raw-content">{{ item.content_raw || '无正文内容' }}</div>
      </div>

      <!-- Footer Buttons -->
      <div class="modal-actions">
        <el-button @click="visible = false">关闭</el-button>

        <!-- Export to Calendar -->
        <el-button
          type="warning"
          plain
          @click="handleExportCalendar"
        >
          📅 加入系统日历 (.ics)
        </el-button>

        <el-button
          v-if="item.url"
          type="primary"
          @click="openOriginalUrl"
        >
          前往工大官网原文 ↗
        </el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'
import { isFavorite, toggleFavorite } from '../utils/storage'
import { exportToCalendar } from '../utils/calendar'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  item: {
    type: Object,
    default: () => null
  }
})

const emit = defineEmits(['update:modelValue'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const isStarred = computed(() => {
  return props.item ? isFavorite(props.item.id) : false
})

function handleToggleFav() {
  if (!props.item) return
  const added = toggleFavorite(props.item.id)
  if (added) {
    ElMessage.success('已加入“我的关注”！可在顶部 Tab 快速查看')
  } else {
    ElMessage.info('已取消关注')
  }
}

function handleExportCalendar() {
  if (!props.item) return
  const success = exportToCalendar(props.item)
  if (success) {
    ElMessage.success({
      message: '已导出 .ics 日历文件，支持 iOS/安卓/Mac/Windows 日历打开提醒！',
      duration: 3500
    })
  }
}

const categoryLabel = computed(() => {
  if (!props.item) return ''
  const map = {
    academic: '🎓 学术讲座',
    competition: '🏆 竞赛选拔',
    scholarship: '📜 奖助评优',
    notice: '📢 综合公告'
  }
  return map[props.item.category] || '📌 情报条目'
})

const tags = computed(() => {
  if (!props.item || !props.item.tags) return []
  return props.item.tags.split(',').map(t => t.trim()).filter(Boolean)
})

function formatDeadline(dt) {
  if (!dt) return '常规进行 / 无硬性截止'
  const date = new Date(dt)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function openOriginalUrl() {
  if (props.item && props.item.url) {
    window.open(props.item.url, '_blank')
  }
}
</script>

<style scoped>
.modal-body {
  padding: 0.5rem 0.25rem;
}

.modal-header {
  margin-bottom: 1.25rem;
}

.header-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.badges-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.modal-fav-btn {
  background: #fffbeb;
  border: 1px solid #fef3c7;
  color: #b45309;
  border-radius: 9999px;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.15s;
}

.modal-fav-btn:hover {
  background: #fef3c7;
  transform: translateY(-1px);
}

.modal-fav-btn.active {
  background: #f59e0b;
  color: #ffffff;
  border-color: #f59e0b;
  box-shadow: 0 2px 4px rgba(245, 158, 11, 0.25);
}

.badge {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
}

.cat-badge {
  background: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #dbeafe;
}

.campus-badge {
  background: #f0fdfa;
  color: #0d9488;
  border: 1px solid #ccfbf1;
}

.source-badge {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #e2e8f0;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.4;
  margin: 0;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 0.75rem;
  background: #f8fafc;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1.25rem;
  border: 1px solid #f1f5f9;
}

.meta-item {
  font-size: 0.82rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-label {
  color: #64748b;
  font-weight: 500;
}

.meta-value {
  color: #1e293b;
  font-weight: 600;
}

.meta-value.highlight {
  color: #ea580c;
}

.tags-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.tags-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: #64748b;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.tag-item {
  border-radius: 4px;
}

.summary-box {
  background: #eff6ff;
  border-left: 4px solid #3b82f6;
  border-radius: 6px;
  padding: 0.85rem 1rem;
  margin-bottom: 1.25rem;
}

.summary-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: #1d4ed8;
  margin-bottom: 0.25rem;
}

.summary-content {
  margin: 0;
  font-size: 0.85rem;
  color: #1e40af;
  line-height: 1.55;
}

.content-section {
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: #334155;
  margin-bottom: 0.5rem;
}

.raw-content {
  font-size: 0.88rem;
  color: #334155;
  line-height: 1.7;
  white-space: pre-line;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  max-height: 260px;
  overflow-y: auto;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}
</style>
