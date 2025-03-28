import re

# 全局变量
predicate = ""     # 谓语
subject = ""       # 主语
object_ = ""       # 宾语
adverbial = ""     # 状语
pre_to_predicate = ""

# 程度映射 (0-9)
degree_map = {
    "0": "不",
    "1": "略微",
    "2": "稍",
    "3": "有点",
    "4": "一般",
    "5": "比较",
    "6": "较为",
    "7": "很",
    "8": "非常",
    "9": "极其"
}

# 时态映射
tense_map = {
    "ed": "曾经",
    "ing": "正打算",
    "will": "将要"
}

def reset_globals():
    """重置全局变量"""
    global predicate, subject, object_, adverbial
    predicate = ""
    subject = ""
    object_ = ""
    adverbial = ""

def parse_predicate(pred_str):
    """解析谓语部分"""
    # 匹配模式：数字(倾向)+动词+时态
    match = re.match(r"^(\d)(.+?)(ed|ing|will)$", pred_str)
    if not match:
        raise ValueError(f"无效的谓语格式: {pred_str}")
    
    tendency, verb, tense = match.groups()
    tendency_str = degree_map.get(tendency, "")
    tense_str = tense_map.get(tense, "")
    
    # 组合谓语
    global predicate, pre_to_predicate
    predicate = pre_to_predicate + f"{tense_str}{tendency_str}{verb}"

def parse_complex_item(item_str):
    """解析复合项（包含-连接的修饰关系）"""
    parts = item_str.split("-")
    core = parts[-1]  # 最后一个元素是核心词
    modifiers = parts[:-1]
    
    adj_modifiers = []
    adv_modifiers = []
    
    for mod in modifiers:
        # 处理副词修饰项（包含于）
        if mod.startswith("于"):
            adv = mod[1:]
            if adv and adv[0] in degree_map:
                degree = degree_map[adv[0]]
                word = adv[1:] if len(adv) > 1 else ""
                adv_modifiers.append(f"{degree}{word}")
            continue
        
        # 处理普通修饰项
        if mod and mod[0] in degree_map:
            degree = degree_map[mod[0]]
            word = mod[1:] if len(mod) > 1 else ""
            adj_modifiers.append(f"{degree}{word}")
    
    # 组合修饰语：副词在前，形容词在后
    return "的".join(adv_modifiers + adj_modifiers + [core])

def parse_subject_object(item_str):
    """解析主语或宾语"""
    if "-" in item_str:
        return parse_complex_item(item_str)
    return item_str

def parse_adverbial(adv_str):
    """解析状语部分"""
    adv_parts = []
    for part in adv_str.split("，"):
        part = part.strip()
        if not part:
            continue
        
        # 处理谓语状语（于+形容词）
        if part.startswith("于") and not part.startswith(("于P", "于T", "于U")):
            # print("me:", part)
            global pre_to_predicate
            part = part.replace("于", "")  # 直接删除"于"
            if part and part[0] in degree_map:
                degree = degree_map[part[0]]
                adj = part[1:] if len(part) > 1 else ""
                pre_to_predicate = f"{degree}{adj}地"
            else:
                degree = ""
                adj = part
                pre_to_predicate = f"{degree}{adj}地"
            
        # 处理地点状语
        elif part.startswith("于P"):
            place = part.replace("于P", "")  # 直接删除"于P"
            adv_parts.append(f"在{place}")
        
        # 处理时间状语
        elif part.startswith("于T"):
            time = part.replace("于T", "")  # 直接删除"于T"
            adv_parts.append(f"在{time}")
    
    # 按顺序组合：方式→地点→时间
    return "，".join(adv_parts)

def compile_niuyu(sentence):
    """主编译函数"""
    reset_globals()
    
    try:
        # print(f"\n原始输入: {sentence}")  # 调试输出
        
        # 提取句子类型
        sentence_type = "陈述"
        if "？" in sentence:
            sentence_type = "疑问"
        elif "！" in sentence:
            sentence_type = "感叹"
        # print(f"句子类型: {sentence_type}")  # 调试输出
        
        # 拆分句法结构 [谓语]:[主语]=[宾语] [状语]
        # 先按空格分割出状语部分
        parts = sentence.strip(" 。？！").split(" ", 1)
        main_part = parts[0]
        adv_part = parts[1] if len(parts) > 1 else ""
        # print(f"主部分: {main_part}")  # 调试输出
        # print(f"状部分: {adv_part}")   # 调试输出
        
        # 分割主谓宾部分
        main_parts = main_part.split("：")
        if len(main_parts) < 2:
            raise ValueError("缺少冒号分隔符")
        
        pred_part = main_parts[0]
        subj_obj_part = main_parts[1].split("=")
        if len(subj_obj_part) < 2:
            raise ValueError("缺少等号分隔符")
        
        subj_part = subj_obj_part[0]
        obj_part = subj_obj_part[1]
        # print(f"谓部分: {pred_part}")  # 调试输出
        # print(f"主部分: {subj_part}")  # 调试输出
        # print(f"宾部分: {obj_part}")   # 调试输出
        
        # 处理各组成部分
        parse_predicate(pred_part)
        global subject, object_, adverbial
        subject = parse_subject_object(subj_part)
        object_ = parse_subject_object(obj_part)
        adverbial = parse_adverbial(adv_part)
        # print(f"解析后谓语: {predicate}")  # 调试输出
        # print(f"解析后主语: {subject}")    # 调试输出
        # print(f"解析后宾语: {object_}")    # 调试输出
        # print(f"解析后状语: {adverbial}")  # 调试输出
        
        # 组合最终结果
        adv_clause = f"{adverbial}，" if adverbial else ""
        base = f"{adv_clause}{subject}{predicate}{object_}".strip("，")
        
        # 根据句子类型添加标点
        if sentence_type == "疑问":
            return base + "吗？"
        elif sentence_type == "感叹":
            return base + "！"
        return base + "。"
    
    except Exception as e:
        return f"编译错误: {str(e)}"

# 测试用例
test_cases = [
    ("9学ed：他=7优-课 于8勤，于P教室，于T昨天。", 
     "在教室，在昨天，他极其学了比较优的课。"),
    
    ("7做ing：她=6趣-手工 于6乐，于P活动室，于T此刻？",
     "在活动室，在此刻，她正打算做较为趣的手工吗？"),
    
    ("9探ed：探险家=7奇-洞 于6勇，于P山洞，于T去年！",
     "在山洞，在去年，探险家极其探了很奇的洞！"),
    
    # 新增测试案例
    ("9赞ed：老师=8优-生 于9诚，于P办公室，于T今天！",
     "在办公室，在今天，老师极其赞了非常优的生！"),
    
    ("5写will：我=3长-信 于4专，于P家，于T明晚。",
     "在家，在明晚，我将要写有点长的信。")
]

for niuyu, expected in test_cases:
    print(f"输入: {niuyu}")
    result = compile_niuyu(niuyu)
    print(f"输出: {result}")
    print(f"期望: {expected}")
    print("---")