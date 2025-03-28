import re

# 全局变量
predicate = ""  # 谓语
subject = ""    # 主语
object_ = ""    # 宾语
adverbial = ""  # 状语

# 数字程度映射
degree_map = {
    '0': '不',
    '1': '略微',
    '2': '有点',
    '3': '稍',
    '4': '一般',
    '5': '',
    '6': '比较',
    '7': '相当',
    '8': '非常',
    '9': '极其'
}

# 代词映射
pronoun_map = {
    '吾': '我的',
    '汝': '你的',
    '其': '他的',
    '彼': '那个'
}

# 时间标记映射
tense_map = {
    'ed': '了',
    'ing': '正在',
    'will': '将要'
}

def parse_sentence(sentence):
    global predicate, subject, object_, adverbial
    predicate = subject = object_ = adverbial = ""
    
    # 分离句末标点
    punctuation = ""
    if sentence[-1] in ".!?":
        punctuation = sentence[-1]
        sentence = sentence[:-1]
    
    # 拆分句法结构 [谓语]:[主语]=[宾语] [状语]
    parts = re.split(r'[:= ]', sentence)
    if len(parts) < 4:
        raise ValueError("无效的牛语句子结构")
    
    pred_part = parts[0]
    subj_part = parts[1]
    obj_part = parts[2]
    adv_part = " ".join(parts[3:])  # 合并剩余的状语部分
    
    # 解析各部分
    parse_predicate(pred_part)
    parse_subject(subj_part)
    parse_object(obj_part)
    parse_adverbial(adv_part)
    
    # 组合结果
    result = f"{subject}{predicate}{object_}{adverbial}"
    
    # 根据标点调整语气
    if punctuation == "!":
        result += "！"
    elif punctuation == "?":
        result += "吗？"
    else:
        result += "。"
    
    return result

def parse_predicate(pred):
    global predicate
    # 匹配数字、动词和时间标记
    match = re.match(r'^(\d)(\w+)(ed|ing|will)$', pred)
    if not match:
        raise ValueError(f"无效的谓语格式: {pred}")
    
    degree, verb, tense = match.groups()
    
    # 构建谓语
    degree_word = degree_map.get(degree, '')
    tense_word = tense_map.get(tense, '')
    
    predicate = f"{tense_word}{degree_word}{verb}"

def parse_subject(subj):
    global subject
    subject = parse_complex_item(subj)

def parse_object(obj):
    global object_
    object_ = parse_complex_item(obj)

def parse_complex_item(item):
    if '-' not in item:
        return item  # 简单项直接返回
    
    parts = item.split('-')
    noun = parts[-1]  # 最后一个是被修饰的名词
    modifiers = parts[:-1]
    
    adv_modifiers = []
    adj_modifiers = []
    
    for mod in modifiers:
        if mod.startswith('于'):
            # 副词修饰项
            adv_mod = parse_adverb_modifier(mod[1:])  # 去掉'于'
            adv_modifiers.append(adv_mod)
        else:
            # 形容词修饰项
            adj_mod = parse_adjective_modifier(mod)
            adj_modifiers.append(adj_mod)
    
    # 组装修饰语
    modifiers_str = ""
    if adv_modifiers:
        modifiers_str += "".join(adv_modifiers)
    if adj_modifiers:
        modifiers_str += "".join(adj_modifiers)
    
    return f"{modifiers_str}{noun}"

def parse_adjective_modifier(adj):
    # 解析如"9美"这样的形容词修饰项
    match = re.match(r'^(\d)(\w+)$', adj)
    if not match:
        raise ValueError(f"无效的形容词修饰格式: {adj}")
    
    degree, word = match.groups()
    
    # 检查是否是代词形容词
    if word in pronoun_map:
        return pronoun_map[word]
    
    degree_word = degree_map.get(degree, '')
    return f"{degree_word}{word}"

def parse_adverb_modifier(adv):
    # 解析如"8快"这样的副词修饰项
    return parse_adjective_modifier(adv)

def parse_adverbial(adv):
    global predicate, adverbial
    if not adv:
        return
    
    adv_parts = [p.strip() for p in adv.split(',') if p.strip()]
    
    for part in adv_parts:
        if part.startswith('于'):
            if part.startswith('于P'):
                # 地点状语
                place = part[2:]
                adverbial += f"在{place}"
            elif part.startswith('于T'):
                # 时间状语
                time = part[2:]
                adverbial += f"在{time}"
            elif part.startswith('于U'):
                # 其他状语
                other = part[2:]
                adverbial += other
            else:
                # 谓语状语
                adv_mod = parse_adverb_modifier(part[1:])
                predicate = f"{adv_mod}地{predicate}"
        else:
            raise ValueError(f"无效的状语格式: {part}")

# 测试用例
test_cases = [
    "9学ed：他=7优-课 于8勤，于P教室，于T昨天。",
    "9写ed：我=8美-文 于7专，于P书房，于T上周。",
    "7做ing：她=6趣-手工 于6乐，于P活动室，于T此刻。",
    "9赞ed：老师=8优-生 于9诚，于P办公室，于T今天！",
    "9跑ed：运动员=5快-速 于8猛，于P操场，于T比赛时！",
    "9绘ed：画家=9绝-画 于8细，于P画室，于T上月！",
    "9玩ed：孩子们=6趣-游戏 于7欢，于P公园，于T前天？",
    "7唱ing：歌手=8美-曲 于8动，于P舞台，于T现在？",
    "9探ed：探险家=7奇-洞 于6勇，于P山洞，于T去年？",
    "9给ed：妈妈=5重-麦 于8信，于P家，于T晨。",
    "7驮ing：小马=5重-麦 于6慎，于P路，于T午。",
    "9笑ed：兔=5慢-龟 于8傲，于P起点，于T赛前！"
]

# 运行测试
for i, test_case in enumerate(test_cases, 1):
    try:
        print(f"测试用例 {i}: {test_case}")
        print("翻译结果:", parse_sentence(test_case))
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

# 交互式测试
print("牛语编译器交互模式(输入q退出)")
while True:
    user_input = input("请输入牛语句子: ").strip()
    if user_input.lower() == 'q':
        break
    try:
        print("翻译结果:", parse_sentence(user_input))
    except Exception as e:
        print(f"错误: {e}")