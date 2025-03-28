from parser import *

def compile_niuyu(sentence):
    """主编译函数"""
    reset_globals()
    
    try:
        # 提取句子类型
        sentence_type = "陈述"
        if "？" in sentence:
            sentence_type = "疑问"
        elif "！" in sentence:
            sentence_type = "感叹"
        
        # 拆分句法结构 [谓语]:[主语]=[宾语] [状语]
        # 先按空格分割出状语部分
        parts = sentence.strip(" 。？！").split(" ", 1)
        main_part = parts[0]
        adv_part = parts[1] if len(parts) > 1 else ""
        
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
        global subject, object_, adverbial, predicate
        subject = parse_subject_object(subj_part)
        object_ = parse_subject_object(obj_part)
        adverbial = parse_adverbial(adv_part)
        predicate = parse_predicate(pred_part)

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
     "在教室，在昨天，他极其勤奋地学了比较优质的课程。"),
    
    ("7做ing：她=6趣-手工 于6乐，于P活动室，于T此刻？",
     "在活动室，在此刻，她正打算做较为趣的手工吗？")
    
    # ("9探ed：探险家=7奇-洞 于6勇，于P山洞，于T去年！",
    #  "在山洞，在去年，探险家极其探了很奇的洞！"),
    
    # # 新增测试案例
    # ("9赞ed：老师=8优-生 于9诚，于P办公室，于T今天！",
    #  "在办公室，在今天，老师极其赞了非常优的生！"),
    
    # ("5写will：我=3长-信 于4专，于P家，于T明晚。",
    #  "在家，在明晚，我将要写有点长的信。")
]


for index, (niuyu, expected) in enumerate(test_cases):
    result = compile_niuyu(niuyu)
    print(f"------------测试用例{index + 1}-------------")
    print(f"输入: {niuyu}")
    print(f"输出: {result}")
    # print(f"期望: {expected}")