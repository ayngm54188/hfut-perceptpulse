import re
from datetime import datetime, date

def extract_publish_date(text: str) -> date:
    """Extract publish date formatted like 2026-11-09, 2026/11/09 or 2026年11月9日"""
    if not text:
        return date.today()
    
    # Try YYYY-MM-DD or YYYY/MM/DD
    match = re.search(r'(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})', text)
    if match:
        year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
        try:
            return date(year, month, day)
        except ValueError:
            pass
    return date.today()

def extract_deadline(text: str, default_year: int = None) -> datetime:
    """
    Intelligently extracts deadline or event datetime from announcement text.
    e.g. '请各项目负责人于11月30日前在大创系统中提交', '答辩时间定于12月2日下午2点30分'
    """
    if not text:
        return None
    
    if default_year is None:
        default_year = date.today().year

    # Pattern 1: 2026年11月30日 23:59 or 2026-11-30
    match1 = re.search(r'(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})[日\s]*(\d{1,2})?[:点时]?(\d{1,2})?', text)
    if match1:
        y, m, d = int(match1.group(1)), int(match1.group(2)), int(match1.group(3))
        hr = int(match1.group(4)) if match1.group(4) else 23
        mi = int(match1.group(5)) if match1.group(5) else 59
        try:
            return datetime(y, m, d, min(hr, 23), min(mi, 59))
        except ValueError:
            pass

    # Pattern 2: 于X月X日前 / 截止至X月X日 / 答辩时间定于X月X日
    deadline_keywords = [
        r'(?:截止|前|截至|时间为|定于|举办时间)[^\d]{0,8}(\d{1,2})月(\d{1,2})日[^\d]{0,6}(\d{1,2})?[点时:]?(\d{1,2})?',
        r'(\d{1,2})月(\d{1,2})日[^\d]{0,6}(?:前|截止|前提交|前完成)'
    ]

    for pat in deadline_keywords:
        match = re.search(pat, text)
        if match:
            m = int(match.group(1))
            d = int(match.group(2))
            hr = 23
            mi = 59
            if len(match.groups()) >= 4 and match.group(3):
                try:
                    hr = int(match.group(3))
                    mi = int(match.group(4)) if match.group(4) else 0
                except (ValueError, TypeError):
                    pass
            try:
                return datetime(default_year, m, d, hr, mi)
            except ValueError:
                pass

    return None

def categorize_item(title: str, text: str) -> str:
    """Classifies an item into competition, academic, or notice"""
    combined = (title + " " + (text[:300] if text else "")).lower()
    
    comp_keywords = ["竞赛", "大赛", "选拔赛", "挑战杯", "蓝桥杯", "创客", "大创", "创新创业", "院赛", "校赛", "三创"]
    for kw in comp_keywords:
        if kw in combined:
            return "competition"

    acad_keywords = ["讲座", "学术报告", "论坛", "研讨会", "学术年会", "报告会", "学术动态", "沙龙"]
    for kw in acad_keywords:
        if kw in combined:
            return "academic"

    return "notice"

def infer_campus(title: str, text: str) -> str:
    """Infers the HFUT campus from text"""
    combined = title + " " + (text or "")
    if "宣城校区" in combined or "敬亭学堂" in combined:
        return "宣城"
    if "翡翠湖校区" in combined or "建工馆" in combined or "翡翠科教楼" in combined:
        return "翡翠湖"
    if "屯溪路校区" in combined or "斛兵" in combined or "主楼" in combined:
        return "屯溪路"
    return "全部"

def extract_location(text: str) -> str:
    """Extracts physical location or online meeting platform"""
    if not text:
        return None
    patterns = [
        r'(地点[：:\s]*[^\n，。；]+)',
        r'(腾讯会议[：:\s]*[^\n，。；]+)',
        r'(报告厅[^\n，。；]*)',
        r'(科教楼[^\n，。；]*)',
        r'(学术会议中心[^\n，。；]*)',
        r'(建工馆[^\n，。；]*)'
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            clean = m.group(1).replace("地点", "").replace("：", "").replace(":", "").strip()
            return clean[:60]
    return None

def generate_tags(title: str, text: str) -> str:
    """Generates relevant tags based on keyword frequency"""
    combined = title + " " + (text or "")
    candidate_tags = [
        "挑战杯", "大创", "蓝桥杯", "创新创业", "人工智能", "大数据",
        "学术报告", "竞赛选拔", "信管", "企业模拟", "软件设计", "双创",
        "职业规划", "国家级A类", "具身智能", "研究生", "本科生"
    ]
    matched = [tag for tag in candidate_tags if tag in combined]
    if not matched:
        matched = ["通知公告"]
    return ",".join(matched[:5])
