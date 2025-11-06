"""
Gloria's Magic Farm - 作物数据库
包含所有作物的基础数据
"""

# 作物数据结构：
# {
#     "name": 作物名称,
#     "seed_price": 种子价格（金币）,
#     "growth_days": 生长周期（天）,
#     "base_yield": 基础产量,
#     "base_price": 基础售价（金币/个）,
#     "season": 适宜季节,
#     "category": 类别（vegetable/fruit/flower/special）,
#     "rarity": 稀有度（common/rare/epic/legendary）,
#     "description": 说明
# }

CROPS_DATABASE = {
    # 原有的4种作物
    "小麦": {
        "name": "小麦",
        "seed_price": 10,
        "growth_days": 2,
        "base_yield": 30,
        "base_price": 5,
        "season": ["春", "秋"],
        "category": "vegetable",
        "rarity": "common",
        "description": "周期短，适合冲刺数量指标"
    },
    "番茄": {
        "name": "番茄",
        "seed_price": 30,
        "growth_days": 4,
        "base_yield": 10,
        "base_price": 15,
        "season": ["夏"],
        "category": "fruit",
        "rarity": "common",
        "description": "单价高，适合经济指标"
    },
    "彩虹菊": {
        "name": "彩虹菊",
        "seed_price": 100,
        "growth_days": 6,
        "base_yield": 5,
        "base_price": 50,
        "season": ["春"],
        "category": "flower",
        "rarity": "rare",
        "description": "花卉，用于多样性指标"
    },
    "黄金南瓜": {
        "name": "黄金南瓜",
        "seed_price": 200,
        "growth_days": 8,
        "base_yield": 1,
        "base_price": 300,
        "season": ["秋"],
        "category": "special",
        "rarity": "epic",
        "description": "稀有作物，用于奇迹指标"
    },

    # 新增的10种作物
    "胡萝卜": {
        "name": "胡萝卜",
        "seed_price": 15,
        "growth_days": 3,
        "base_yield": 20,
        "base_price": 8,
        "season": ["春", "秋", "冬"],
        "category": "vegetable",
        "rarity": "common",
        "description": "生命力顽强，三季可种，适合新手"
    },
    "草莓": {
        "name": "草莓",
        "seed_price": 50,
        "growth_days": 5,
        "base_yield": 15,
        "base_price": 20,
        "season": ["春", "夏"],
        "category": "fruit",
        "rarity": "common",
        "description": "香甜可口，市场需求大"
    },
    "薰衣草": {
        "name": "薰衣草",
        "seed_price": 80,
        "growth_days": 7,
        "base_yield": 8,
        "base_price": 45,
        "season": ["夏"],
        "category": "flower",
        "rarity": "rare",
        "description": "紫色浪漫，可用于制作香薰产品"
    },
    "蓝莓": {
        "name": "蓝莓",
        "seed_price": 60,
        "growth_days": 6,
        "base_yield": 12,
        "base_price": 25,
        "season": ["夏", "秋"],
        "category": "fruit",
        "rarity": "rare",
        "description": "富含花青素，深受健康人士喜爱"
    },
    "向日葵": {
        "name": "向日葵",
        "seed_price": 40,
        "growth_days": 5,
        "base_yield": 10,
        "base_price": 18,
        "season": ["夏"],
        "category": "flower",
        "rarity": "common",
        "description": "阳光的象征，能提升农场美观度"
    },
    "水晶葡萄": {
        "name": "水晶葡萄",
        "seed_price": 300,
        "growth_days": 10,
        "base_yield": 3,
        "base_price": 400,
        "season": ["夏", "秋"],
        "category": "special",
        "rarity": "legendary",
        "description": "传说中的奇迹作物，晶莹剔透如宝石"
    },
    "玫瑰": {
        "name": "玫瑰",
        "seed_price": 120,
        "growth_days": 8,
        "base_yield": 6,
        "base_price": 60,
        "season": ["春", "夏"],
        "category": "flower",
        "rarity": "rare",
        "description": "爱情的象征，情人节期间价格翻倍"
    },
    "白萝卜": {
        "name": "白萝卜",
        "seed_price": 12,
        "growth_days": 3,
        "base_yield": 25,
        "base_price": 6,
        "season": ["秋", "冬"],
        "category": "vegetable",
        "rarity": "common",
        "description": "冬季的主力蔬菜，生长快速"
    },
    "魔法蘑菇": {
        "name": "魔法蘑菇",
        "seed_price": 250,
        "growth_days": 9,
        "base_yield": 2,
        "base_price": 350,
        "season": ["秋"],
        "category": "special",
        "rarity": "epic",
        "description": "在月光下会发光的神奇蘑菇"
    },
    "樱花树苗": {
        "name": "樱花树苗",
        "seed_price": 500,
        "growth_days": 15,
        "base_yield": 1,
        "base_price": 800,
        "season": ["春"],
        "category": "special",
        "rarity": "legendary",
        "description": "需要耐心培育，开花时美不胜收"
    }
}


def get_crop_info(crop_name):
    """获取作物信息"""
    return CROPS_DATABASE.get(crop_name, None)


def get_crops_by_category(category):
    """按类别获取作物列表"""
    return {name: data for name, data in CROPS_DATABASE.items() if data["category"] == category}


def get_crops_by_season(season):
    """按季节获取可种植的作物列表"""
    return {name: data for name, data in CROPS_DATABASE.items() if season in data["season"]}


def get_crops_by_rarity(rarity):
    """按稀有度获取作物列表"""
    return {name: data for name, data in CROPS_DATABASE.items() if data["rarity"] == rarity}


def calculate_profit(crop_name, quantity=1):
    """计算种植某作物的理论利润"""
    crop = get_crop_info(crop_name)
    if not crop:
        return None

    cost = crop["seed_price"] * quantity
    revenue = crop["base_price"] * crop["base_yield"] * quantity
    profit = revenue - cost

    return {
        "crop_name": crop_name,
        "quantity": quantity,
        "total_cost": cost,
        "total_revenue": revenue,
        "profit": profit,
        "roi": (profit / cost * 100) if cost > 0 else 0  # 投资回报率
    }
