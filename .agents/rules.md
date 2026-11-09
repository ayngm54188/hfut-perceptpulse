# HFUT-PerceptPulse 合工大信管创新班工程规约

> **适用范围**：合肥工业大学管理学院信息管理与信息系统（信管创新班）及计算机全栈联合项目。  
> **核心原则**：高内聚低耦合、强类型约束、防御式数据清洗、严格代码文档化。

---

## 一、 统一 API 响应设计规约

所有对外暴露的 RESTful API 必须遵守统一的数据契约，杜绝直接裸露原始异常或返回不规范的字典结构。

### 1. 成功响应结构 (Unified Success Envelope)
对于所有非纯文件流的 API 响应，推荐或遵守统一结构：
```json
{
  "code": 200,
  "message": "success",
  "data": { ... },
  "timestamp": "2026-11-10T01:45:00Z"
}
```
- **列表响应**：必须包含 `total`（总计数）、`items`（数组）及分页元信息，禁止在前端硬编码假分页。
- **时间戳字段**：统一采用标准 ISO 8601 格式输出（`YYYY-MM-DDTHH:MM:SS`）。

### 2. 异常响应与 HTTP 状态码映射
- `400 Bad Request`：参数校验不合规或业务前置条件不满足（如 URL 已存在）。
- `404 Not Found`：请求实体（如情报 ID）不存在。
- `422 Unprocessable Entity`：Pydantic 模式校验失败，必须返回精准的字段级错误定位。
- `500 Internal Server Error`：服务端未捕获异常，生产环境禁止泄露原始 Traceback，应记入日志并返回通用错误描述。

---

## 二、 Pydantic 严格校验与类型约束规约

后端全量采用 Pydantic V2 构建输入输出数据模型，严格遵循以下规则：

### 1. 类型提示与非空约束
- **严禁裸写 `dict` 或 `Any`**：字段必须使用具体的 Python 类型（`str`, `int`, `datetime`, `date`, `List[T]`）。
- **可选字段声明**：显式使用 `Optional[T] = None`，并附带默认值。
- **字符串清洗**：字符串类型的字段应开启 `str_strip_whitespace=True`，防止首尾多余空格污染检索索引。

### 2. 长度与边界限制
```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, date

class PulseItemBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=255, description="情报通知完整标题")
    category: str = Field(..., max_length=32, description="分类：academic/competition/notice")
    source_site: str = Field(..., max_length=64, description="发布学院或部门")
    campus: Optional[str] = Field("全部", max_length=32, description="翡翠湖/屯溪路/宣城/全部")
    url: str = Field(..., min_length=8, max_length=512, description="原文唯一URL")
```

### 3. ORM 映射模式
Schema 响应模型必须启用 `ConfigDict(from_attributes=True)`，严禁手动遍历 SQLAlchemy Model 属性组装字典。

---

## 三、 SQLite CRUD 分层与会话工程规范

系统采用清晰的三层架构：**API 路由层 $\rightarrow$ 业务服务层 $\rightarrow$ ORM 模型/持久化层**。

### 1. 数据库会话（Session）生命周期管理
- **禁止全局单例 Session**：必须通过 FastAPI 的 `Depends(get_db)` 依赖注入机制为每个 HTTP 请求分配独立的局部 Session。
- **自动回收与连接释放**：
  ```python
  def get_db():
      db = SessionLocal()
      try:
          yield db
      finally:
          db.close()
  ```
- **SQLite 并发设置**：连接引擎必须配置 `connect_args={"check_same_thread": False}`，防止多线程请求互斥报锁错误。

### 2. 事务与写入规范
- **批量插入优化**：在感知层批量入库时，必须在一个事务内执行 `db.add_all(items)` 后统一 `db.commit()`，禁止在循环体内频繁 commit。
- **失败回滚**：所有包含写操作的代码块必须包裹 `try...except`，发生异常时显式触发 `db.rollback()`。
- **唯一键幂等性**：以 `url` 作为唯一去重依据，在执行写入前必须执行 `db.query(...).filter(PulseItem.url == url).first()` 验证。

---

## 四、 中文分词与特征抽取算法注释规范

在情报感知层、文本清洗与信息抽取模块中，所有涉及正则表达式、模式匹配与文本分词的代码必须满足以下注释规范：

### 1. 正则表达式模式的“自解释注释”
对于提取日期、截止时间、校区或地点的正则表达式，必须在模式上方声明：
1. **模式意图**：该模式匹配的具体文本语义；
2. **正向匹配用例 (Positive Cases)**：列出至少 2 组工大官网的典型文本样本；
3. **捕获组说明 (Capturing Groups)**：标明每个括号对应提取的语义（如年份、月份、日期、小时）。

**示例标准**：
```python
# =========================================================================
# 算法函数: extract_deadline
# 业务语义: 智能感知工大通知正文中的报名/提交截止时间与答辩时刻
# 匹配用例:
#   - "请各项目负责人于11月30日前在大创系统中提交中期检查表"
#   - "答辩时间定于12月2日下午2点30分开始"
# 捕获组:
#   Group 1: 月份 (1~12)
#   Group 2: 日期 (1~31)
#   Group 3: 小时 (可选, 0~23)
# 复杂度: 时间 O(N), 空间 O(1), N 为正文字符长度
# =========================================================================
```

### 2. 工大校区与专有名词词典维护
针对合肥工业大学多校区办学特点，文本挖掘算法必须维护专用词库：
- **翡翠湖校区**：`翡翠科教楼`、`建工馆`、`翠竹苑`、`翡翠湖校区图书馆`、`合工大新区`。
- **屯溪路校区**：`科教楼A座/B座`、`斛兵大讲堂`、`学术会议中心`、`主楼`、`微机所`。
- **宣城校区**：`宣创杯`、`敬亭学堂`、`宣城校区行政楼`、`新戏斋`。
- **顶级赛事白名单**：`挑战杯`、`蓝桥杯`、`大学生计算机设计大赛`、`互联网+`、`大创`、`三创赛`、`企业竞争模拟`。

### 3. 代码演进与提交纪律
- 遵循 Conventional Commits 规范（`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`）。
- 新增感知源（学院官网）必须继承 `BaseCrawler` 并实现抽象方法 `crawl()`。
- 任何破坏数据库现有字段的变更，需同步更新 `schemas/`、`models/` 以及数据初始化脚本。
