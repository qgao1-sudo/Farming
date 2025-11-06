"""
Gloria's Magic Farm - 月度指标系统
处理市政厅发布的月度任务和结算
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class MonthlyTarget:
    """月度指标类"""

    # 指标类型定义
    TARGET_TYPES = {
        "harvest": {
            "name": "产量指标",
            "emoji": "🌾",
            "difficulty": 1
        },
        "quality": {
            "name": "品质指标",
            "emoji": "⭐",
            "difficulty": 2
        },
        "sell": {
            "name": "经济指标",
            "emoji": "💰",
            "difficulty": 2
        },
        "variety": {
            "name": "多样性指标",
            "emoji": "🌈",
            "difficulty": 2
        },
        "special": {
            "name": "奇迹指标",
            "emoji": "✨",
            "difficulty": 3
        }
    }

    def __init__(self):
        self.current_target = None
        self.target_type = None
        self.target_value = 0
        self.target_crop = None  # 指定的作物（如果有）
        self.reward = {}
        self.penalty = 0
        self.start_date = None
        self.end_date = None
        self.description = ""
        self.is_completed = False

    def generate_new_target(self, difficulty_level: int = 1, current_date: datetime = None):
        """
        生成新的月度指标

        Args:
            difficulty_level: 难度等级 (1-5)
            current_date: 当前日期（默认为今天）
        """
        if current_date is None:
            current_date = datetime.now()

        self.start_date = current_date
        # 月底是截止日期
        if current_date.month == 12:
            self.end_date = datetime(current_date.year + 1, 1, 1) - timedelta(days=1)
        else:
            self.end_date = datetime(current_date.year, current_date.month + 1, 1) - timedelta(days=1)

        # 根据难度选择指标类型
        available_types = ["harvest", "sell", "variety"]
        if difficulty_level >= 2:
            available_types.append("quality")
        if difficulty_level >= 3:
            available_types.append("special")

        self.target_type = random.choice(available_types)

        # 根据类型生成具体指标
        if self.target_type == "harvest":
            self._generate_harvest_target(difficulty_level)
        elif self.target_type == "quality":
            self._generate_quality_target(difficulty_level)
        elif self.target_type == "sell":
            self._generate_sell_target(difficulty_level)
        elif self.target_type == "variety":
            self._generate_variety_target(difficulty_level)
        elif self.target_type == "special":
            self._generate_special_target(difficulty_level)

        return self._format_target_announcement()

    def _generate_harvest_target(self, difficulty: int):
        """生成产量指标"""
        crops = {
            1: [("小麦", 300, 400), ("胡萝卜", 200, 300), ("白萝卜", 200, 300)],
            2: [("番茄", 100, 150), ("草莓", 80, 120)],
            3: [("蓝莓", 60, 100), ("向日葵", 50, 80)]
        }

        crop_list = crops.get(min(difficulty, 3), crops[1])
        crop_name, min_amount, max_amount = random.choice(crop_list)

        self.target_crop = crop_name
        self.target_value = random.randint(min_amount, max_amount)
        self.description = f"收获 {self.target_value} 个 {crop_name}"

        # 设置奖励
        self.reward = {
            "gold": self.target_value * 10,
            "diamond": 5 * difficulty,
            "reputation": 10
        }
        self.penalty = self.target_value * 3

    def _generate_quality_target(self, difficulty: int):
        """生成品质指标"""
        crops = ["番茄", "草莓", "蓝莓", "玫瑰"]
        qualities = {
            1: ("good", "良好", 20, 30),
            2: ("excellent", "优秀", 15, 25),
            3: ("perfect", "完美", 10, 15)
        }

        self.target_crop = random.choice(crops)
        quality_en, quality_cn, min_amount, max_amount = qualities.get(difficulty, qualities[1])

        self.target_value = random.randint(min_amount, max_amount)
        self.description = f"上交 {self.target_value} 个 {quality_cn}品质的 {self.target_crop}"

        self.reward = {
            "gold": self.target_value * 50,
            "diamond": 10 * difficulty,
            "reputation": 15,
            "item": "优质种子礼包"
        }
        self.penalty = self.target_value * 15

    def _generate_sell_target(self, difficulty: int):
        """生成经济指标"""
        targets = {
            1: (5000, 8000),
            2: (10000, 15000),
            3: (20000, 30000)
        }

        min_amount, max_amount = targets.get(difficulty, targets[1])
        self.target_value = random.randint(min_amount, max_amount)
        self.description = f"实现单日农场收入达到 {self.target_value} 金币"

        self.reward = {
            "gold": self.target_value // 3,
            "diamond": 8 * difficulty,
            "reputation": 12,
            "item": "商店折扣券"
        }
        self.penalty = self.target_value // 5

    def _generate_variety_target(self, difficulty: int):
        """生成多样性指标"""
        categories = {
            1: ("flower", "花卉", 3, 5),
            2: ("flower", "花卉", 5, 7),
            3: ("fruit", "水果", 4, 6)
        }

        category, category_cn, min_types, max_types = categories.get(difficulty, categories[1])
        self.target_value = random.randint(min_types, max_types)
        self.target_crop = category
        self.description = f"种植 {self.target_value} 种不同的 {category_cn}"

        self.reward = {
            "gold": self.target_value * 500,
            "diamond": 12 * difficulty,
            "reputation": 20,
            "item": "稀有种子礼包"
        }
        self.penalty = self.target_value * 100

    def _generate_special_target(self, difficulty: int):
        """生成奇迹指标"""
        special_crops = {
            1: ("黄金南瓜", 1, 2),
            2: ("魔法蘑菇", 1, 3),
            3: ("水晶葡萄", 1, 2),
            4: ("樱花树苗", 1, 1)
        }

        crop_name, min_amount, max_amount = special_crops.get(difficulty, special_crops[1])
        self.target_crop = crop_name
        self.target_value = random.randint(min_amount, max_amount)
        self.description = f"成功培育出 {self.target_value} 株 {crop_name}"

        self.reward = {
            "gold": 5000 * difficulty,
            "diamond": 30 * difficulty,
            "reputation": 50,
            "item": "传奇种子",
            "title": f"{crop_name}大师"
        }
        self.penalty = 2000 * difficulty

    def _format_target_announcement(self) -> str:
        """格式化指标公告"""
        target_info = self.TARGET_TYPES.get(self.target_type, {})
        emoji = target_info.get("emoji", "📋")
        type_name = target_info.get("name", "未知指标")

        announcement = f"""
╔═══════════════════════════════════════╗
║       🏛️  市政厅月度指标公告  🏛️        ║
╠═══════════════════════════════════════╣
║                                       ║
║  指标类型: {emoji} {type_name:<20} ║
║  任务内容: {self.description:<28} ║
║  截止日期: {self.end_date.strftime('%Y年%m月%d日'):<28} ║
║                                       ║
║  【奖励】                             ║
║    💰 金币: {self.reward.get('gold', 0):<26} ║
║    💎 钻石: {self.reward.get('diamond', 0):<26} ║
║    ⭐ 信誉度: {self.reward.get('reputation', 0):<23} ║"""

        if "item" in self.reward:
            announcement += f"""
║    🎁 特殊奖励: {self.reward['item']:<21} ║"""

        if "title" in self.reward:
            announcement += f"""
║    🏆 称号: {self.reward['title']:<24} ║"""

        announcement += f"""
║                                       ║
║  【失败惩罚】                         ║
║    💸 罚款: {self.penalty} 金币               ║
║    📉 信誉度下降                      ║
║                                       ║
╚═══════════════════════════════════════╝
        """

        return announcement

    def check_completion(self, player_data: Dict) -> bool:
        """
        检查玩家是否完成指标

        Args:
            player_data: 玩家数据字典

        Returns:
            bool: 是否完成
        """
        if self.target_type == "harvest":
            crop_harvested = player_data.get('crops_harvested', {})
            return crop_harvested.get(self.target_crop, 0) >= self.target_value

        elif self.target_type == "quality":
            quality_harvested = player_data.get('quality_harvested', {})
            crop_quality = quality_harvested.get(self.target_crop, {})
            # 这里需要检查特定品质的数量
            return crop_quality.get('excellent', 0) + crop_quality.get('perfect', 0) >= self.target_value

        elif self.target_type == "sell":
            return player_data.get('max_daily_sale', 0) >= self.target_value

        elif self.target_type == "variety":
            category = self.target_crop  # 这里存的是类别
            planted_types = player_data.get('planted_variety', {})
            return len(planted_types.get(category, [])) >= self.target_value

        elif self.target_type == "special":
            crop_harvested = player_data.get('crops_harvested', {})
            return crop_harvested.get(self.target_crop, 0) >= self.target_value

        return False

    def settle_month(self, player_data: Dict) -> Dict:
        """
        进行月底结算

        Args:
            player_data: 玩家数据

        Returns:
            dict: 结算结果
        """
        is_completed = self.check_completion(player_data)
        self.is_completed = is_completed

        result = {
            "success": is_completed,
            "target_description": self.description,
            "target_type": self.target_type
        }

        if is_completed:
            result["message"] = f"🎉 恭喜！你成功完成了本月指标！\n{self.description}"
            result["rewards"] = self.reward
            result["reputation_change"] = self.reward.get('reputation', 0)
        else:
            result["message"] = f"💔 很遗憾，你未能完成本月指标。\n{self.description}"
            result["penalty"] = self.penalty
            result["reputation_change"] = -20

        return result

    def get_progress(self, player_data: Dict) -> Dict:
        """
        获取指标完成进度

        Args:
            player_data: 玩家数据

        Returns:
            dict: 进度信息
        """
        progress = {
            "target_type": self.target_type,
            "description": self.description,
            "target_value": self.target_value,
            "current_value": 0,
            "progress_percent": 0,
            "days_remaining": (self.end_date - datetime.now()).days
        }

        if self.target_type == "harvest":
            current = player_data.get('crops_harvested', {}).get(self.target_crop, 0)
            progress["current_value"] = current

        elif self.target_type == "sell":
            current = player_data.get('max_daily_sale', 0)
            progress["current_value"] = current

        elif self.target_type == "variety":
            category = self.target_crop
            planted_types = player_data.get('planted_variety', {})
            current = len(planted_types.get(category, []))
            progress["current_value"] = current

        elif self.target_type == "special":
            current = player_data.get('crops_harvested', {}).get(self.target_crop, 0)
            progress["current_value"] = current

        # 计算百分比
        if self.target_value > 0:
            progress["progress_percent"] = min(100, (progress["current_value"] / self.target_value) * 100)

        return progress
