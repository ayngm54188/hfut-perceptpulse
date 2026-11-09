import sys
import logging
from pathlib import Path

# Configure stdout encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Ensure backend root is in python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from app.services.crawlers.manager import CrawlerManager

def main():
    print("=" * 65)
    print("  [PerceptPulse] 校园学术与竞赛情报感知采集引擎启动")
    print("  目标源: 计算机与信息学院、管理学院（学术动态与竞赛通知）")
    print("=" * 65)

    manager = CrawlerManager()
    stats = manager.run_all()

    print("\n" + "=" * 65)
    print("  [PerceptPulse] 感知与数据持久化任务完成！")
    print(f"  - 发现网页条目数: {stats['total_scraped']}")
    print(f"  - 新增入库情报数: {stats['new_inserted']}")
    print(f"  - 存在且去重跳过: {stats['skipped_existing']}")
    print(f"  - 覆盖学院源: {', '.join(stats['sources'])}")
    print("=" * 65)

if __name__ == "__main__":
    main()
