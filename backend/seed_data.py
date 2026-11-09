import sys
from pathlib import Path
from datetime import datetime, date, timedelta

# Ensure backend directory is in python search path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.core.database import SessionLocal, engine, Base
from app.models.item import PulseItem, CrawlSource

def seed():
    print("[Seed] Initializing SQLite database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check existing items
        count = db.query(PulseItem).count()
        if count > 0:
            print(f"[Seed] Database already contains {count} items. Skipping initial seed.")
            return

        print("[Seed] Populating initial HFUT intelligence samples...")
        
        today = date.today()
        now = datetime.now()

        sample_items = [
            PulseItem(
                title="【斛兵学术大讲堂】大模型与具身智能前沿进展学术报告",
                category="academic",
                source_site="计算机与信息学院",
                campus="屯溪路",
                url="http://ci.hfut.edu.cn/info/1024/academic-llm-2026.htm",
                content_raw="报告主题：大模型与具身智能前沿进展\n主讲人：IEEE Fellow / 知名学者\n地点：屯溪路校区科教楼A座二楼报告厅\n欢迎全校感兴趣的本科生、研究生踊跃参与！",
                summary="围绕大模型与具身智能在多模态感知、自主决策领域的最新学术进展进行深度拆解，提供现场答疑交流互动环节。",
                publish_date=today - timedelta(days=1),
                deadline=now + timedelta(days=3, hours=4),
                location="屯溪路校区科教楼A座二楼报告厅",
                tags="大模型,具身智能,人工智能,讲座",
                view_count=86
            ),
            PulseItem(
                title="关于举办第十六届“蓝桥杯”全国软件和信息技术专业人才大赛合工大选拔赛的通知",
                category="competition",
                source_site="计算机与信息学院",
                campus="翡翠湖",
                url="http://ci.hfut.edu.cn/info/1025/lanqiao-2026.htm",
                content_raw="第十六届蓝桥杯软件赛（C/C++、Java、Python、Web应用开发）校赛报名正式启动！校内将组织赛前模拟训练营，成绩优异者由学校统一资助参加省赛。",
                summary="涵盖软件类与软件开发全组别，翡翠湖与屯溪路机房统一组织机试选拔，校赛前30%选手可入选省赛特训营并获学校资助。",
                publish_date=today - timedelta(days=3),
                deadline=now + timedelta(days=14, hours=12),
                location="翡翠湖校区建工馆机房 / 线上报名系统",
                tags="蓝桥杯,算法竞赛,程序设计,国家级A类",
                view_count=342
            ),
            PulseItem(
                title="【翡翠湖学术论坛】从信息管理到智能决策：现代数据资产运营新视角",
                category="academic",
                source_site="管理学院",
                campus="翡翠湖",
                url="http://som.hfut.edu.cn/info/2024/data-assets-forum.htm",
                content_raw="本次论坛聚焦信管专业与企业数字化转型结合点，邀请业界专家与校友分享数据治理、企业BI分析系统建设与现代信息组织方法。",
                summary="探讨信管专业在数字化转型中的核心竞争壁垒，涵盖数据治理、智能BI看板构建与数据资产评估实践案例分享。",
                publish_date=today - timedelta(days=2),
                deadline=now + timedelta(days=5, hours=2),
                location="翡翠湖校区图书馆学术报告厅",
                tags="信管,数据资产,数字化转型,管理科学",
                view_count=120
            ),
            PulseItem(
                title="关于组织参加2026年中国大学生计算机设计大赛校内预选赛的通知",
                category="competition",
                source_site="校本科生院",
                campus="全部",
                url="http://bkjy.hfut.edu.cn/info/1033/jsjsj-2026.htm",
                content_raw="大赛分为软件应用与开发、微课与教学辅助、物联网应用、大数据应用、人工智能实践赛等大类。作品需在校赛系统提交演示视频与设计说明书。",
                summary="全国高校顶级计算机实践赛事，跨学院组队（计信+信管+设计尤佳），初赛提交软著材料或原型Demo即可，校赛一二等奖推荐省赛。",
                publish_date=today - timedelta(days=5),
                deadline=now + timedelta(days=20),
                location="合肥工业大学大学生创新创业中心",
                tags="计算机设计大赛,软件开发,人机交互,双创赛事",
                view_count=521
            ),
            PulseItem(
                title="宣城校区“宣创杯”大学生创新创业挑战赛暨三创赛校区选拔赛通知",
                category="competition",
                source_site="宣城校区管委会",
                campus="宣城",
                url="http://xc.hfut.edu.cn/info/3021/xc-chuangye-2026.htm",
                content_raw="本次选拔赛面向宣城校区全体大一至大四学生，重点支持结合物联网、电子商务、智慧农业与区域经济发展的交叉学科项目。",
                summary="宣城校区专属选拔赛道，提供孵化基金与校内导师一对一指导，重点考核项目可行性与商业策划书完整度。",
                publish_date=today - timedelta(days=4),
                deadline=now + timedelta(days=10, hours=8),
                location="宣城校区行政楼报告厅 / 敬亭学堂",
                tags="宣城校区,三创赛,创业实践,学科交叉",
                view_count=215
            ),
            PulseItem(
                title="【斛兵研学】国家自然科学基金青年学者学术沙龙：图深度学习前沿",
                category="academic",
                source_site="科研院",
                campus="屯溪路",
                url="http://keyan.hfut.edu.cn/info/1089/graph-deep-learning.htm",
                content_raw="特邀青年骨干教师分享图神经网络（GNN）、知识图谱与复杂网络建模在社交网络和生物信息感知中的应用探索。",
                summary="聚焦图神经网络与知识图谱融合研究，适合对学术科研、保研夏令营与研究生论文方向感兴趣的高年级与大一科研先锋同学。",
                publish_date=today - timedelta(days=6),
                deadline=now + timedelta(days=1, hours=6),
                location="屯溪路校区学术会议中心小报告厅",
                tags="知识图谱,图神经网络,学术沙龙,科研训练",
                view_count=98
            ),
        ]

        # Sources
        sources = [
            CrawlSource(
                name="计算机与信息学院官网-通知公告",
                base_url="http://ci.hfut.edu.cn/1024/list.htm",
                category_default="all"
            ),
            CrawlSource(
                name="本科生院实践教学与创新创业网",
                base_url="http://bkjy.hfut.edu.cn/1033/list.htm",
                category_default="competition"
            ),
            CrawlSource(
                name="宣城校区综合信息网",
                base_url="http://xc.hfut.edu.cn/3021/list.htm",
                category_default="all"
            )
        ]

        db.add_all(sample_items)
        db.add_all(sources)
        db.commit()
        print(f"[Seed] Successfully populated {len(sample_items)} items and {len(sources)} sources into SQLite!")

    except Exception as e:
        db.rollback()
        print(f"[Seed] Error seeding data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
