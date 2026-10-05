#!/usr/bin/env python3
"""Nosurvey Lab · 构念替代分级判定器

输入一个或多个构念（名称 + 测量类型），输出替代可行性级别与推荐策略。
确定性规则，无随机。用法：

    python3 grade_construct.py --construct "工作满意度:心理" "收入水平:事实"

或交互式逐行输入："构念名:类型"，类型 ∈ 事实/行为/心理。
"""

import sys
import re

# 测量类型 → 替代级别映射（规则基准）
TYPE_RULES = {
    "事实": "S",   # 客观事实：行政/统计/交易数据直接替代
    "行为": "A",   # 可观察行为：数字足迹/平台日志替代
    "心理": "B",   # 内在状态：文本/痕迹代理 + 校准
}

# 类型内细分的提升/降级词（可选：通过构念名关键词微调）
UPGRADE_KEYWORDS = {  # 更容易替代 → 级别上调
    "收入": "S", "消费": "S", "就业": "S", "支出": "S",
    "使用": "A", "参与": "A", "互动": "A", "购买": "A",
    "时长": "A", "频率": "A", "行为": "A",
}
DOWNGRADE_KEYWORDS = {  # 更难替代 → 级别下调
    "幸福感": "C", "内在动机": "C", "心流": "C", "自我效能": "C",
    "私密": "D", "性": "D", "信仰": "D", "深层": "C",
}

STRATEGY = {
    "S": ("直接替代", "全网替代，问卷不推荐"),
    "A": ("高度可替代", "全网替代，问卷不推荐"),
    "B": ("可替代·需校准", "替代为主 + 小样本校准（100-300份效度锚点）"),
    "C": ("部分替代·三角验证", "多源三角（文本×行为×情境），问卷降级辅助"),
    "D": ("兜底·实验/问卷", "推荐行为实验任务替代自报"),
}


def parse_constructs(args):
    """解析 ["名称:类型", ...] 或交互输入"""
    constructs = []
    if args:
        for a in args:
            if a.startswith("-"):
                continue
            m = re.match(r"^(.+?)[:：](事实|行为|心理)$", a.strip())
            if m:
                constructs.append((m.group(1).strip(), m.group(2)))
            else:
                print(f"⚠ 无法解析（应为 '名称:类型'）：{a}", file=sys.stderr)
    else:
        print("交互模式：输入 '构念名:类型'（事实/行为/心理），空行结束")
        for line in sys.stdin:
            line = line.strip()
            if not line:
                break
            m = re.match(r"^(.+?)[:：](事实|行为|心理)$", line)
            if m:
                constructs.append((m.group(1).strip(), m.group(2)))
            else:
                print(f"⚠ 跳过无法解析的行：{line}", file=sys.stderr)
    return constructs


def grade(name, mtype):
    """返回 (级别, 依据)"""
    level = TYPE_RULES[mtype]
    notes = [f"类型『{mtype}』基础级别 {level}"]

    # 关键词微调（同一大类内微调）：
    # - 事实类：命中可观察词 → 保持/确认 S
    # - 行为类：命中可观察行为词 → 保持/确认 A
    # - 心理类：命中行为代理词 → 最多升到 A（意愿→行为有 gap，需说明）；
    #           命中难替代词 → 降到 C/D
    if mtype == "心理":
        for kw, lv in DOWNGRADE_KEYWORDS.items():
            if kw in name:
                level = lv
                notes.append(f"命中难替代词『{kw}』→ 下调至 {level}")
                return level, notes
        for kw, lv in UPGRADE_KEYWORDS.items():
            if kw in name:
                level = "A" if lv == "S" else lv  # 心理类最高升到 A
                notes.append(f"命中行为代理词『{kw}』→ 上调至 {level}（意愿≠行为，需校准或说明 gap）")
                return level, notes
    else:
        for kw, lv in UPGRADE_KEYWORDS.items():
            if kw in name:
                level = lv if lv == mtype or lv == "S" else level
                if lv != level:
                    notes.append(f"命中可替代词『{kw}』→ 确认 {level}")
                break
    return level, notes


def main():
    constructs = parse_constructs(sys.argv[1:])
    if not constructs:
        print("未输入有效构念。用法：grade_construct.py --construct '名称:事实|行为|心理'")
        return 1

    print("\n" + "=" * 62)
    print("问卷替代可行性分级结果")
    print("=" * 62)
    for name, mtype in constructs:
        level, notes = grade(name, mtype)
        label, strat = STRATEGY[level]
        print(f"\n【{name}】类型={mtype}")
        print(f"  级别：{level}级 · {label}")
        print(f"  策略：{strat}")
        print(f"  依据：{'；'.join(notes)}")
    print("\n" + "=" * 62)
    print("注：分级是初筛。最终方案需按 SKILL.md Step 4 匹配数据源并做效度论证。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
