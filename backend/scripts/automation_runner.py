import sys
import logging
from datetime import datetime, date, timedelta
from pathlib import Path

# Setup Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure backend root is in python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import SessionLocal
from app.models.item import PulseItem, CrawlSource
from app.services.crawlers.manager import CrawlerManager

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("AutomationRunner")

def generate_daily_markdown_report(crawl_stats: dict, db) -> Path:
    """
    Generates a daily intelligence briefing in Markdown format.
    """
    today_str = date.today().isoformat()
    now_dt = datetime.now()

    # Query statistics
    total_count = db.query(PulseItem).count()
    comp_count = db.query(PulseItem).filter(PulseItem.category == "competition").count()
    acad_count = db.query(PulseItem).filter(PulseItem.category == "academic").count()

    # Query upcoming deadlines within 14 days
    upcoming_items = db.query(PulseItem).filter(
        PulseItem.deadline >= now_dt,
        PulseItem.deadline <= now_dt + timedelta(days=14)
    ).order_by(PulseItem.deadline.asc()).limit(8).all()

    # Query latest competitions
    latest_competitions = db.query(PulseItem).filter(
        PulseItem.category == "competition"
    ).order_by(PulseItem.publish_date.desc(), PulseItem.id.desc()).limit(5).all()

    # Query latest academic lectures
    latest_lectures = db.query(PulseItem).filter(
        PulseItem.category == "academic"
    ).order_by(PulseItem.publish_date.desc(), PulseItem.id.desc()).limit(5).all()

    # Build Markdown document
    lines = [
        f"# 📡 HFUT-PerceptPulse 校园学术与竞赛情报每日感知简报",
        f"> **生成时间**：{now_dt.strftime('%Y-%m-%d %H:%M:%S')}  |  **感知范围**：合工大各学院官网、本科生院与双创网\n",
        "---",
        "## 📊 一、 今日数据感知概览\n",
        f"| 指标项 | 统计数值 | 状态与说明 |",
        f"| :--- | :--- | :--- |",
        f"| **系统情报总库** | **{total_count}** 条 | 覆盖翡翠湖、屯溪路与宣城校区 |",
        f"| **学科与双创赛事** | **{comp_count}** 项 | 涵盖校赛选拔、大创与A类学科竞赛 |",
        f"| **前沿学术动态** | **{acad_count}** 场 | 涵盖学术报告、斛兵大讲堂与研讨沙龙 |",
        f"| **本次扫描条目** | **{crawl_stats.get('total_scraped', 0)}** 篇 | 增量抓取学院通知公告与学术频道 |",
        f"| **本次新增入库** | **{crawl_stats.get('new_inserted', 0)}** 条 | 经严格 URL 幂等去重后的最新发布 |",
        f"| **去重保留条目** | **{crawl_stats.get('skipped_existing', 0)}** 条 | 保持本地浏览热度与元数据不变 |\n",
        "---",
        "## ⚡ 二、 近期截止与日程预警 (未来 14 天内)\n"
    ]

    if upcoming_items:
        lines.append("| 截止时间 | 类别 | 校区 | 赛事 / 讲座主题 | 主办部门 | 原文链接 |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for it in upcoming_items:
            deadline_str = it.deadline.strftime("%m-%d %H:%M") if it.deadline else "待定"
            cat_name = "🏆 竞赛" if it.category == "competition" else "🎓 学术"
            campus_name = it.campus or "全部"
            link = f"[查看原文]({it.url})" if it.url else "-"
            # Truncate title for clean table display
            clean_title = it.title.replace("|", "/")
            if len(clean_title) > 28:
                clean_title = clean_title[:28] + "..."
            lines.append(f"| **{deadline_str}** | {cat_name} | {campus_name} | {clean_title} | {it.source_site} | {link} |")
        lines.append("")
    else:
        lines.append("> 暂无 14 天内紧急截止事项，可放宽筛选条件查看常规通知。\n")

    lines.extend([
        "---",
        "## 🏆 三、 重点学科竞赛与双创选拔推荐\n"
    ])

    for comp in latest_competitions:
        lines.append(f"### 📍 {comp.title}")
        lines.append(f"- **主办单位**：`{comp.source_site}`  |  **适用校区**：`{comp.campus}`")
        if comp.deadline:
            lines.append(f"- **报名截止**：`{comp.deadline.strftime('%Y-%m-%d %H:%M')}`")
        if comp.tags:
            lines.append(f"- **主题标签**：`{comp.tags}`")
        if comp.summary:
            lines.append(f"- **情报摘要**：{comp.summary}")
        if comp.url:
            lines.append(f"- **原文直达**：<{comp.url}>")
        lines.append("")

    lines.extend([
        "---",
        "## 🎓 四、 前沿学术讲座与论坛精选\n"
    ])

    for acad in latest_lectures:
        lines.append(f"### 💡 {acad.title}")
        lines.append(f"- **举办学院**：`{acad.source_site}`  |  **校区/地点**：`{acad.campus} · {acad.location or '详见通知'}`")
        if acad.deadline:
            lines.append(f"- **活动时间**：`{acad.deadline.strftime('%Y-%m-%d %H:%M')}`")
        if acad.summary:
            lines.append(f"- **报告概要**：{acad.summary}")
        if acad.url:
            lines.append(f"- **原文直达**：<{acad.url}>")
        lines.append("")

    lines.extend([
        "---",
        "> *本简报由 HFUT-PerceptPulse 自动化调度引擎自动生成于合肥工业大学。*",
        "> *数据存储于本地 SQLite 数据库，支持在前端面板一键导出为 .ics 日历日程并设置提醒。*"
    ])

    # Target directory
    report_dir = backend_dir / "data" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"daily_briefing_{today_str}.md"

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path

def run():
    print("=" * 65)
    print("  🚀 [HFUT-PerceptPulse] 每日定时感知与情报简报自动化任务启动")
    print("=" * 65)

    db = SessionLocal()
    try:
        # Step 1: Run Web Crawlers
        logger.info("Executing campus intelligence crawlers...")
        manager = CrawlerManager(db=db)
        crawl_stats = manager.run_all()
        logger.info(f"Crawl completed. New: {crawl_stats['new_inserted']}, Existing: {crawl_stats['skipped_existing']}")

        # Step 2: Generate Daily Markdown Briefing
        logger.info("Generating daily intelligence Markdown briefing...")
        report_path = generate_daily_markdown_report(crawl_stats, db)
        logger.info(f"Report generated successfully at: {report_path}")

        print("\n" + "=" * 65)
        print("  🎉 自动化感知任务执行完毕！")
        print(f"  - 新增入库条目: {crawl_stats['new_inserted']}")
        print(f"  - 简报生成路径: {report_path.relative_to(backend_dir.parent)}")
        print("=" * 65)

    except Exception as e:
        logger.error(f"Error during automation run: {e}", exc_info=True)
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run()
