<template>
  <div class="app-container">
    <!-- Navbar -->
    <Navbar v-model:campus="currentCampus" @update:campus="onCampusChange" />

    <!-- Main Content Area -->
    <main class="main-content">
      <!-- Filter and Stats Bar -->
      <FilterBar
        :stats="statsData"
        :campus="currentCampus"
        @filter-change="onFilterChange"
      />

      <!-- Content Status & Result Counter -->
      <div class="result-header">
        <div class="result-count">
          共感知到 <span class="highlight">{{ totalItems }}</span> 条学术与竞赛情报
          <span v-if="activeFilterDesc" class="filter-hint">({{ activeFilterDesc }})</span>
        </div>
        <div class="actions-group">
          <el-button
            size="small"
            type="primary"
            :loading="crawling"
            @click="handleTriggerCrawl"
            title="实时联网爬取合工大各学院官网最新通知与讲座"
          >
            📡 联网感知采集
          </el-button>
          <el-button size="small" :loading="loading" @click="loadData">
            🔄 刷新看板
          </el-button>
        </div>
      </div>

      <!-- Loading Skeleton -->
      <div v-if="loading" class="card-grid">
        <el-skeleton
          v-for="n in 6"
          :key="n"
          animated
          class="skeleton-card"
        >
          <template #template>
            <div style="padding: 1.25rem;">
              <el-skeleton-item variant="text" style="width: 30%; margin-bottom: 12px;" />
              <el-skeleton-item variant="h3" style="width: 85%; margin-bottom: 12px;" />
              <el-skeleton-item variant="text" style="width: 50%; margin-bottom: 16px;" />
              <el-skeleton-item variant="p" style="width: 100%; margin-bottom: 8px;" />
              <el-skeleton-item variant="p" style="width: 70%;" />
            </div>
          </template>
        </el-skeleton>
      </div>

      <!-- Empty State -->
      <div v-else-if="items.length === 0" class="empty-state">
        <el-empty description="未检索到符合条件的学术或竞赛情报，可尝试更换关键词或校区">
          <el-button type="primary" @click="resetFilters">清空筛选条件</el-button>
        </el-empty>
      </div>

      <!-- Cards Grid -->
      <div v-else class="card-grid">
        <ItemCard
          v-for="item in items"
          :key="item.id"
          :item="item"
          @select="handleOpenDetail"
        />
      </div>

      <!-- Pagination -->
      <div class="pagination-wrapper" v-if="totalItems > pageSize">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="totalItems"
          layout="prev, pager, next, jumper"
          background
          @current-change="onPageChange"
        />
      </div>
    </main>

    <!-- Detail Dialog Modal -->
    <DetailModal
      v-model="detailVisible"
      :item="selectedItem"
    />

    <!-- Footer -->
    <footer class="app-footer">
      <div class="footer-inner">
        <div>HFUT-PerceptPulse 校园学术与竞赛情报感知系统 · 计算机与信息学院 & 管理学院创新实践</div>
        <div class="footer-sub">面向合肥工业大学翡翠湖、屯溪路与宣城校区 · 自动化感知与截止日期预警</div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import Navbar from './components/Navbar.vue'
import FilterBar from './components/FilterBar.vue'
import ItemCard from './components/ItemCard.vue'
import DetailModal from './components/DetailModal.vue'
import { getItems, getItemDetail, getStatsSummary, triggerCrawler } from './api/client'
import { ElMessage, ElNotification } from 'element-plus'

// State
const loading = ref(false)
const crawling = ref(false)
const items = ref([])
const totalItems = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)
const currentCampus = ref('全部')

const statsData = ref({
  total_items: 0,
  competition_count: 0,
  academic_count: 0,
  upcoming_deadlines: 0
})

const filterParams = reactive({
  category: '',
  campus: '全部',
  search: '',
  upcoming_only: false
})

// Modal state
const detailVisible = ref(false)
const selectedItem = ref(null)

const activeFilterDesc = computed(() => {
  const parts = []
  if (filterParams.category === 'academic') parts.push('学术讲座')
  if (filterParams.category === 'competition') parts.push('竞赛选拔')
  if (filterParams.campus && filterParams.campus !== '全部') parts.push(filterParams.campus)
  if (filterParams.upcoming_only) parts.push('未截止')
  if (filterParams.search) parts.push(`"${filterParams.search}"`)
  return parts.join(' · ')
})

async function loadStats() {
  try {
    const data = await getStatsSummary()
    statsData.value = data
  } catch (err) {
    console.error('Failed to load stats:', err)
  }
}

async function loadData() {
  loading.value = true
  try {
    const res = await getItems({
      category: filterParams.category || undefined,
      campus: filterParams.campus !== '全部' ? filterParams.campus : undefined,
      search: filterParams.search || undefined,
      upcoming_only: filterParams.upcoming_only || undefined,
      page: currentPage.value,
      limit: pageSize.value
    })
    items.value = res.items || []
    totalItems.value = res.total || 0
  } catch (err) {
    console.error('Failed to load items:', err)
    ElMessage.error('无法连接后端 API 服务，请确认后端已启动在 8000 端口')
  } finally {
    loading.value = false
  }
}

async function handleTriggerCrawl() {
  crawling.value = true
  ElMessage.info('正在联网抓取合工大学院官网最新学术与竞赛公告...')
  try {
    const res = await triggerCrawler()
    ElNotification({
      title: '情报感知完成',
      message: `本次扫描发现 ${res.total_scraped} 篇公告，新增入库 ${res.new_inserted} 条，跳过重复 ${res.skipped_existing} 条。`,
      type: 'success',
      duration: 5000
    })
    await loadStats()
    await loadData()
  } catch (err) {
    console.error('Crawler failed:', err)
    ElMessage.error('感知采集失败，请检查网络连接或后端日志')
  } finally {
    crawling.value = false
  }
}

function onFilterChange(filters) {
  filterParams.category = filters.category
  filterParams.campus = filters.campus
  filterParams.search = filters.search
  filterParams.upcoming_only = filters.upcoming_only
  currentPage.value = 1
  loadData()
}

function onCampusChange(val) {
  currentCampus.value = val
  filterParams.campus = val
  currentPage.value = 1
  loadData()
}

function onPageChange(page) {
  currentPage.value = page
  loadData()
  window.scrollTo({ top: 120, behavior: 'smooth' })
}

function resetFilters() {
  filterParams.category = ''
  filterParams.campus = '全部'
  filterParams.search = ''
  filterParams.upcoming_only = false
  currentCampus.value = '全部'
  currentPage.value = 1
  loadData()
}

async function handleOpenDetail(item) {
  try {
    const detail = await getItemDetail(item.id)
    selectedItem.value = detail
    item.view_count = detail.view_count
  } catch {
    selectedItem.value = item
  }
  detailVisible.value = true
}

onMounted(() => {
  loadStats()
  loadData()
})
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 3rem 1.25rem;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.result-count {
  font-size: 0.88rem;
  color: #475569;
}

.result-count .highlight {
  font-weight: 700;
  color: #2563eb;
}

.filter-hint {
  color: #94a3b8;
  font-size: 0.8rem;
  margin-left: 0.5rem;
}

.actions-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 1.25rem;
}

.skeleton-card {
  background: #ffffff;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
}

.empty-state {
  background: #ffffff;
  border-radius: 14px;
  border: 1px dashed #cbd5e1;
  padding: 3rem 1rem;
  margin-top: 1rem;
}

.pagination-wrapper {
  margin-top: 2.5rem;
  display: flex;
  justify-content: center;
}

.app-footer {
  background: #ffffff;
  border-top: 1px solid #e2e8f0;
  padding: 1.5rem;
  text-align: center;
}

.footer-inner {
  font-size: 0.8rem;
  color: #64748b;
  line-height: 1.6;
}

.footer-sub {
  font-size: 0.75rem;
  color: #94a3b8;
}

@media (max-width: 640px) {
  .result-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>
