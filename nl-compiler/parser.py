import re
from data import *

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
    global pre_to_predicate
    predicate = f"{tense_str}{pre_to_predicate}{verb}"
    return predicate

def parse_core_item(core):
    """解析核心项（被修饰项）"""
    extended_core = noun_map.get(core)
    if extended_core is not None:
        return extended_core
    else:
        return core

def parse_adj_item(adj):
    """解析修饰项"""
    extend_adj = adj_map.get(adj)
    if extend_adj is not None:
        return extend_adj
    else:
        return adj

def parse_complex_item(item_str):
    """解析复合项（包含-连接的修饰关系）"""
    parts = item_str.split("-")
    core = parts[-1]  # 最后一个元素是核心词(被修饰项)
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
                word = parse_adj_item(word)
                adv_modifiers.append(f"{degree}{word}")
            continue
        
        # 处理普通修饰项
        if mod and mod[0] in degree_map:
            degree = degree_map[mod[0]]
            word = mod[1:] if len(mod) > 1 else ""
            word = parse_adj_item(word)
            adj_modifiers.append(f"{degree}{word}")
    
    # 处理被修饰项，对它进行映射扩展
    core = parse_core_item(core)

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
            global pre_to_predicate
            part = part.replace("于", "")  # 直接删除"于"
            if part and part[0] in degree_map:
                degree = degree_map[part[0]]
                adj = part[1:] if len(part) > 1 else ""
                adj = parse_adj_item(adj)
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



