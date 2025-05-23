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

# 常见名词映射
noun_map = {
    # 动物类（保留单字名称）
    "老虎": "虎", "狮子": "狮", "熊猫": "熊", "狐狸": "狐", "骆驼": "驼",
    "鲸鱼": "鲸", "鲨鱼": "鲨", "鳄鱼": "鳄", "蜘蛛": "蛛", "蝴蝶": "蝶",

    # 食物类
    "苹果": "苹", "香蕉": "蕉", "葡萄": "葡", "草莓": "莓", "西瓜": "瓜",
    "米饭": "饭", "面条": "面", "饺子": "饺", "面包": "包", "鸡蛋": "蛋",
    "牛奶": "奶", "咖啡": "咖", "啤酒": "啤", "酱油": "酱", "蜂蜜": "蜜",

    # 日常用品
    "手机": "机", "电脑": "脑", "电视": "视", "空调": "调", "冰箱": "箱",
    "洗衣机": "衣", "电梯": "梯", "自行车": "车", "汽车": "车", "飞机": "机",
    "书包": "包", "铅笔": "笔", "橡皮": "皮", "桌子": "桌", "椅子": "椅",
    "窗户": "窗", "门锁": "锁", "灯泡": "泡", "牙刷": "刷", "毛巾": "巾",

    # 自然景观
    "太阳": "阳", "月亮": "月", "星星": "星", "云朵": "云", "雪花": "雪",
    "暴雨": "雨", "雷电": "雷", "台风": "风", "沙漠": "漠", "森林": "林",
    "河流": "河", "海洋": "海", "湖泊": "湖", "山峰": "峰", "岛屿": "岛",

    # 身体部位
    "头发": "发", "眼睛": "眼", "鼻子": "鼻", "嘴巴": "嘴", "耳朵": "耳",
    "手臂": "臂", "手掌": "掌", "手指": "指", "大腿": "腿", "脚踝": "踝",

    # 社会场所
    "学校": "校", "医院": "院", "银行": "行", "超市": "超", "餐厅": "厅",
    "公园": "园", "广场": "场", "车站": "站", "机场": "场", "图书馆": "馆",

    # 抽象概念（特殊保留）
    "时间": "时", "空间": "空", "爱情": "情", "友谊": "谊", "知识": "知",
    "梦想": "梦", "希望": "望", "勇气": "勇", "和平": "和", "自由": "由",

    # 我的自定义
    "课": "课程", "信": "信件", "生": "学生", "师": "老师", "洞": "洞穴",
}

adj_map = {
    # ========== 基础视觉类 ==========
    "美": "美丽",    "帅": "帅气",    "酷": "酷炫",    "萌": "萌萌",
    "艳": "艳丽",    "雅": "优雅",    "精": "精致",    "华": "华丽",
    "丑": "丑陋",    "怪": "怪异",    "粗": "粗糙",    "细": "细腻",
    
    # ========== 科学测量类 ========== (新增重点)
    # 长度相关
    "长": "修长",    "短": "短小",    "高": "高大",    "矮": "矮小",
    "深": "深邃",    "浅": "浅显",    "远": "遥远",    "近": "邻近",
    
    # 体积/面积相关
    "大": "巨大",    "小": "微小",    "宽": "宽阔",    "窄": "狭窄",
    "厚": "厚重",    "薄": "薄脆",    "胖": "肥胖",    "瘦": "瘦削",
    
    # 重量/密度相关
    "重": "沉重",    "轻": "轻盈",    "密": "密集",    "疏": "稀疏",
    "硬": "坚硬",    "软": "柔软",    "强": "强大",    "弱": "微弱",
    
    # 时间相关
    "快": "快速",    "慢": "缓慢",    "早": "提早",    "晚": "延迟",
    "新": "崭新",    "旧": "陈旧",    "久": "长久",    "暂": "短暂",
    
    # ========== 智力/能力类 ==========
    "智": "智慧",    "聪": "聪明",    "慧": "聪慧",    "敏": "敏锐",
    "才": "才华",    "博": "博学",    "达": "通达",    "笨": "愚笨",
    "灵": "灵巧",    "拙": "笨拙",    "熟": "熟练",    "生": "生疏",
    
    # ========== 力量/强度类 ==========
    "力": "有力",    "劲": "强劲",    "猛": "威猛",    "刚": "刚强",
    "勇": "勇敢",    "悍": "强悍",    "坚": "坚固",    "韧": "韧性",
    "脆": "脆弱",    "稳": "稳定",    "牢": "牢固",    "松": "松散",
    
    # ========== 情感/态度类 ========== (仅正面)
    "乐": "快乐",    "欢": "欢乐",    "喜": "喜悦",    "愉": "愉快",
    "幸": "幸福",    "甜": "甜蜜",    "暖": "温暖",    "爱": "可爱",
    "静": "安静",    "和": "和谐",    "安": "安宁",    "慈": "慈祥",
    
    # ========== 质量/品质类 ==========
    "优": "优质",    "良": "良好",    "精": "精良",    "佳": "最佳",
    "上": "上等",    "顶": "顶级",    "高": "高级",    "特": "特殊",
    "差": "差劲",    "劣": "劣质",    "废": "废品",    "次": "次品",
    
    # ========== 状态/属性类 ==========
    "新": "崭新",    "鲜": "新鲜",    "活": "活泼",    "生": "生动",
    "清": "清新",    "亮": "明亮",    "净": "干净",    "纯": "纯净",
    "脏": "肮脏",    "乱": "混乱",    "暗": "阴暗",    "浊": "浑浊",
    
    # ========== 科学专用类 ========== (新增重点)
    # 光学相关
    "亮": "明亮",    "暗": "黑暗",    "透": "透明",    "反": "反光",
    "折": "折射",    "散": "散射",    "偏": "偏振",    "辐": "辐射",
    
    # 热力学相关
    "热": "炎热",    "冷": "寒冷",    "温": "温暖",    "凉": "凉爽",
    "沸": "沸腾",    "凝": "凝结",    "蒸": "蒸发",    "熔": "熔化",
    
    # 电学相关
    "电": "带电",    "导": "导电",    "绝": "绝缘",    "阻": "电阻",
    "压": "电压",    "流": "电流",    "频": "频率",    "波": "波动",
    
    # 力学相关
    "速": "速度",    "加": "加速",    "减": "减速",    "惯": "惯性",
    "弹": "弹性",    "塑": "塑性",    "粘": "粘性",    "摩": "摩擦",
    
    # 化学相关
    "酸": "酸性",    "碱": "碱性",    "氧": "氧化",    "还": "还原",
    "溶": "溶解",    "浓": "浓缩",    "挥": "挥发",    "腐": "腐蚀",

    # 自定义
    "趣": "有趣", "乐": "快乐", "勤": "勤奋"
}