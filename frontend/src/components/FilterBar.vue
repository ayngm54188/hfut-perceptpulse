<template>
  <div class="filter-panel">
    <!-- Top Stats Row -->
    <div class="stats-row" v-if="stats">
      <div class="stat-card">
        <div class="stat-icon-box blue">
          <span class="icon">📊</span>
        </div>
        <div class="stat-info">
          <div class="stat-label">感知情报总量</div>
          <div class="stat-value">{{ stats.total_items ?? 0 }} <span class="unit">条</span></div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-box purple">
          <span class="icon">🏆</span>
        </div>
        <div class="stat-info">
          <div class="stat-label">学科与双创竞赛</div>
          <div class="stat-value">{{ stats.competition_count ?? 0 }} <span class="unit">项</span></div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-box emerald">
          <span class="icon">🎓</span>
        </div>
        <div class="stat-info">
          <div class="stat-label">前沿学术讲座</div>
          <div class="stat-value">{{ stats.academic_count ?? 0 }} <span class="unit">场</span></div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-box amber">
          <span class="icon">⏳</span>
        </div>
        <div class="stat-info">
          <div class="stat-label">近期进行/待截止</div>
          <div class="stat-value">{{ stats.upcoming_deadlines ?? 0 }} <span class="unit">个</span></div>
        </div>
      </div>
    </div>

    <!-- Filter Controls Card -->
    <div class="controls-card">
      <!-- Search Input -->
      <div class="search-section">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索学术讲座、赛事名称、大创、指导老师或标签..."
          clearable
          size="default"
          @keyup.enter="handleSearch"
          @clear="handleSearch"
        >
          <template #prefix>
            <span class="search-icon">🔍</span>
          </template>
        </el-input>
        <el-button type="primary" @click="handleSearch">检索情报</el-button>
        <el-button @click="handleReset">重置</el-button>
      </div>

      <div class="divider"></div>

      <!-- Filter Tags Row -->
      <div class="tags-row">
        <!-- Category & Favorites Filter -->
        <div class="filter-group">
          <span class="group-title">情报分类:</span>
          <div class="pill-group">
            <button
              :class="['filter-pill', { active: !onlyFavorites && selectedCategory === '' }]"
              @click="changeCategory('')"
            >
              全部类型
            </button>
            <button
              :class="['filter-pill', { active: !onlyFavorites && selectedCategory === 'academic' }]"
              @click="changeCategory('academic')"
            >
              🎓 学术讲座
            </button>
            <button
              :class="['filter-pill', { active: !onlyFavorites && selectedCategory === 'competition' }]"
              @click="changeCategory('competition')"
            >
              🏆 竞赛选拔
            </button>
            <!-- My Favorites Pill -->
            <button
              :class="['filter-pill fav-pill', { active: onlyFavorites }]"
              @click="toggleFavoritesTab"
            >
              ⭐ 我的关注
              <span class="fav-count" v-if="favCount > 0">{{ favCount }}</span>
            </button>
          </div>
        </div>

        <!-- Campus Filter -->
        <div class="filter-group">
          <span class="group-title">归属校区:</span>
          <div class="pill-group">
            <button
              v-for="c in campuses"
              :key="c.value"
              :class="['filter-pill', { active: selectedCampus === c.value }]"
              @click="changeCampus(c.value)"
            >
              {{ c.label }}
            </button>
          </div>
        </div>

        <!-- Upcoming Toggle -->
        <div class="filter-group upcoming-toggle">
          <el-checkbox v-model="upcomingOnly" @change="handleFilterChange">
            🔥 仅展示未截止 / 进行中
          </el-checkbox>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { favoriteIds } from '../utils/storage'

const props = defineProps({
  stats: {
    type: Object,
    default: () => null
  },
  campus: {
    type: String,
    default: '全部'
  }
})

const emit = defineEmits(['filter-change'])

const searchKeyword = ref('')
const selectedCategory = ref('')
const selectedCampus = ref(props.campus)
const upcomingOnly = ref(false)
const onlyFavorites = ref(false)

const favCount = computed(() => favoriteIds.value.length)

const campuses = [
  { label: '全部校区', value: '全部' },
  { label: '翡翠湖', value: '翡翠湖' },
  { label: '屯溪路', value: '屯溪路' },
  { label: '宣城校区', value: '宣城' }
]

watch(() => props.campus, (newVal) => {
  selectedCampus.value = newVal
  emitChange()
})

function changeCategory(cat) {
  onlyFavorites.value = false
  selectedCategory.value = cat
  emitChange()
}

function toggleFavoritesTab() {
  onlyFavorites.value = !onlyFavorites.value
  emitChange()
}

function changeCampus(campusVal) {
  selectedCampus.value = campusVal
  emitChange()
}

function handleSearch() {
  emitChange()
}

function handleFilterChange() {
  emitChange()
}

function handleReset() {
  searchKeyword.value = ''
  selectedCategory.value = ''
  selectedCampus.value = '全部'
  upcomingOnly.value = false
  onlyFavorites.value = false
  emitChange()
}

function emitChange() {
  emit('filter-change', {
    search: searchKeyword.value.trim(),
    category: selectedCategory.value,
    campus: selectedCampus.value,
    upcoming_only: upcomingOnly.value,
    only_favorites: onlyFavorites.value
  })
}
</script>

<style scoped>
.filter-panel {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-bottom: 1.75rem;
}

/* Stats Row */
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.06);
}

.stat-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.stat-icon-box.blue { background: #eff6ff; color: #2563eb; }
.stat-icon-box.purple { background: #faf5ff; color: #9333ea; }
.stat-icon-box.emerald { background: #f0fdf4; color: #16a34a; }
.stat-icon-box.amber { background: #fffbeb; color: #d97706; }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

.stat-value {
  font-size: 1.35rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.2;
}

.stat-value .unit {
  font-size: 0.75rem;
  font-weight: 400;
  color: #94a3b8;
  margin-left: 2px;
}

/* Controls Card */
.controls-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
}

.search-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.search-icon {
  margin-right: 4px;
}

.divider {
  height: 1px;
  background: #f1f5f9;
  margin: 1rem 0;
}

.tags-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1.5rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.group-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: #475569;
}

.pill-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.filter-pill {
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  color: #475569;
  padding: 0.3rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.78rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
}

.filter-pill:hover {
  background: #f1f5f9;
  color: #1e293b;
  border-color: #cbd5e1;
}

.filter-pill.active {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
  font-weight: 600;
  box-shadow: 0 2px 4px 0 rgba(37, 99, 235, 0.2);
}

.fav-pill {
  border-color: #fde68a;
  background: #fffbeb;
  color: #b45309;
}

.fav-pill:hover {
  background: #fef3c7;
  color: #92400e;
  border-color: #fcd34d;
}

.fav-pill.active {
  background: #f59e0b;
  color: #ffffff;
  border-color: #f59e0b;
  box-shadow: 0 2px 4px 0 rgba(245, 158, 11, 0.3);
}

.fav-count {
  font-size: 0.68rem;
  background: rgba(255, 255, 255, 0.3);
  padding: 1px 5px;
  border-radius: 9999px;
  margin-left: 2px;
}

.fav-pill:not(.active) .fav-count {
  background: #fef3c7;
  color: #b45309;
  border: 1px solid #fde68a;
}

.upcoming-toggle {
  margin-left: auto;
}

@media (max-width: 768px) {
  .tags-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.85rem;
  }
  .upcoming-toggle {
    margin-left: 0;
  }
}
</style>
