"""
Gloria's Magic Farm - 玩家系统
处理玩家的资源、信誉度、成就等
"""

from datetime import datetime
from typing import Dict, List


class Player:
    """玩家类"""

    def __init__(self, name: str):
        self.name = name
        self.gold = 1000  # 初始金币
        self.diamond = 10  # 初始钻石
        self.reputation = 50  # 市政厅信誉度（0-100）
        self.level = 1
        self.exp = 0

        # 统计数据（用于月度指标检查）
        self.crops_harvested = {}  # {作物名: 数量}
        self.quality_harvested = {}  # {作物名: {品质: 数量}}
        self.planted_variety = {
            "vegetable": set(),
            "fruit": set(),
            "flower": set(),
            "special": set()
        }  # 记录种植过的品种

        self.max_daily_sale = 0  # 单日最高销售额
        self.total_income = 0  # 总收入
        self.total_expense = 0  # 总支出

        # 月度表现
        self.consecutive_success = 0  # 连续完成月度指标的次数
        self.total_targets_completed = 0
        self.total_targets_failed = 0

        # 库存
        self.inventory = {}  # {物品名: 数量}

        # 成就和称号
        self.achievements = []
        self.titles = []
        self.current_title = None

    def add_gold(self, amount: int, description: str = ""):
        """增加金币"""
        self.gold += amount
        self.total_income += amount
        return {
            "success": True,
            "message": f"获得 {amount} 金币！{description}",
            "current_gold": self.gold
        }

    def spend_gold(self, amount: int, description: str = "") -> dict:
        """花费金币"""
        if self.gold < amount:
            return {
                "success": False,
                "message": "金币不足！",
                "current_gold": self.gold,
                "required": amount
            }

        self.gold -= amount
        self.total_expense += amount
        return {
            "success": True,
            "message": f"花费 {amount} 金币。{description}",
            "current_gold": self.gold
        }

    def add_diamond(self, amount: int):
        """增加钻石"""
        self.diamond += amount
        return {"success": True, "message": f"获得 {amount} 钻石！"}

    def record_harvest(self, crop_name: str, quantity: int, quality: str = "normal"):
        """
        记录收获（用于月度指标统计）

        Args:
            crop_name: 作物名称
            quantity: 数量
            quality: 品质
        """
        # 记录总数
        if crop_name not in self.crops_harvested:
            self.crops_harvested[crop_name] = 0
        self.crops_harvested[crop_name] += quantity

        # 记录品质
        if crop_name not in self.quality_harvested:
            self.quality_harvested[crop_name] = {}
        if quality not in self.quality_harvested[crop_name]:
            self.quality_harvested[crop_name][quality] = 0
        self.quality_harvested[crop_name][quality] += quantity

    def record_planting(self, crop_name: str, category: str):
        """
        记录种植（用于多样性指标）

        Args:
            crop_name: 作物名称
            category: 类别（vegetable/fruit/flower/special）
        """
        if category in self.planted_variety:
            self.planted_variety[category].add(crop_name)

    def record_daily_sale(self, amount: int):
        """记录单日销售额"""
        if amount > self.max_daily_sale:
            self.max_daily_sale = amount

    def add_reputation(self, amount: int) -> dict:
        """增加信誉度"""
        old_reputation = self.reputation
        self.reputation = min(100, self.reputation + amount)

        message = f"信誉度 +{amount}！当前信誉度: {self.reputation}"

        # 信誉度等级
        if old_reputation < 70 <= self.reputation:
            message += "\n🎉 信誉等级提升至【良好】！"
        elif old_reputation < 90 <= self.reputation:
            message += "\n🎉 信誉等级提升至【优秀】！"

        return {"success": True, "message": message, "reputation": self.reputation}

    def decrease_reputation(self, amount: int) -> dict:
        """降低信誉度"""
        old_reputation = self.reputation
        self.reputation = max(0, self.reputation - amount)

        message = f"信誉度 -{amount}。当前信誉度: {self.reputation}"

        # 信誉度等级
        if old_reputation >= 70 > self.reputation:
            message += "\n⚠️ 信誉等级降至【普通】。"
        elif old_reputation >= 50 > self.reputation:
            message += "\n⚠️ 信誉等级降至【较差】。"

        return {"success": True, "message": message, "reputation": self.reputation}

    def complete_target(self, reward: dict):
        """完成月度指标"""
        self.consecutive_success += 1
        self.total_targets_completed += 1

        # 发放奖励
        results = []

        if "gold" in reward:
            # 连续完成奖励加成
            bonus_multiplier = 1.0 + (self.consecutive_success - 1) * 0.1
            gold_amount = int(reward["gold"] * bonus_multiplier)
            results.append(self.add_gold(gold_amount, f"（连胜加成 x{bonus_multiplier:.1f}）"))

        if "diamond" in reward:
            results.append(self.add_diamond(reward["diamond"]))

        if "reputation" in reward:
            results.append(self.add_reputation(reward["reputation"]))

        if "item" in reward:
            self.add_to_inventory(reward["item"], 1)
            results.append({"success": True, "message": f"获得物品: {reward['item']}"})

        if "title" in reward:
            self.unlock_title(reward["title"])
            results.append({"success": True, "message": f"解锁称号: {reward['title']}"})

        # 连续完成成就
        if self.consecutive_success == 3:
            self.unlock_achievement("三连胜")
        elif self.consecutive_success == 5:
            self.unlock_achievement("五连胜大师")

        return results

    def fail_target(self, penalty: int):
        """未完成月度指标"""
        self.consecutive_success = 0  # 重置连胜
        self.total_targets_failed += 1

        results = []
        results.append(self.spend_gold(penalty, "月度指标失败罚款"))
        results.append(self.decrease_reputation(20))

        return results

    def add_to_inventory(self, item_name: str, quantity: int = 1):
        """添加物品到库存"""
        if item_name not in self.inventory:
            self.inventory[item_name] = 0
        self.inventory[item_name] += quantity

    def use_item(self, item_name: str, quantity: int = 1) -> dict:
        """使用物品"""
        if item_name not in self.inventory or self.inventory[item_name] < quantity:
            return {"success": False, "message": f"物品不足: {item_name}"}

        self.inventory[item_name] -= quantity
        return {"success": True, "message": f"使用了 {quantity} 个 {item_name}"}

    def unlock_achievement(self, achievement_name: str):
        """解锁成就"""
        if achievement_name not in self.achievements:
            self.achievements.append(achievement_name)
            return {"success": True, "message": f"🏆 解锁成就: {achievement_name}！"}
        return {"success": False, "message": "已拥有该成就"}

    def unlock_title(self, title_name: str):
        """解锁称号"""
        if title_name not in self.titles:
            self.titles.append(title_name)
            self.current_title = title_name
            return {"success": True, "message": f"✨ 解锁称号: {title_name}！"}
        return {"success": False, "message": "已拥有该称号"}

    def reset_monthly_stats(self):
        """重置月度统计（每月初调用）"""
        self.crops_harvested = {}
        self.quality_harvested = {}
        self.planted_variety = {
            "vegetable": set(),
            "fruit": set(),
            "flower": set(),
            "special": set()
        }
        self.max_daily_sale = 0

    def get_player_info(self) -> dict:
        """获取玩家信息"""
        return {
            "name": self.name,
            "level": self.level,
            "exp": self.exp,
            "gold": self.gold,
            "diamond": self.diamond,
            "reputation": self.reputation,
            "reputation_level": self._get_reputation_level(),
            "current_title": self.current_title,
            "consecutive_success": self.consecutive_success,
            "total_targets_completed": self.total_targets_completed,
            "total_targets_failed": self.total_targets_failed,
            "total_income": self.total_income,
            "total_expense": self.total_expense,
            "achievements_count": len(self.achievements),
            "titles_count": len(self.titles)
        }

    def _get_reputation_level(self) -> str:
        """获取信誉等级"""
        if self.reputation >= 90:
            return "优秀 ⭐⭐⭐"
        elif self.reputation >= 70:
            return "良好 ⭐⭐"
        elif self.reputation >= 50:
            return "普通 ⭐"
        elif self.reputation >= 30:
            return "较差"
        else:
            return "糟糕"

    def get_monthly_stats(self) -> dict:
        """获取本月统计数据（用于检查月度指标）"""
        return {
            "crops_harvested": self.crops_harvested,
            "quality_harvested": self.quality_harvested,
            "planted_variety": {k: list(v) for k, v in self.planted_variety.items()},
            "max_daily_sale": self.max_daily_sale
        }

    def display_profile(self) -> str:
        """显示玩家档案（格式化输出）"""
        info = self.get_player_info()

        profile = f"""
╔═══════════════════════════════════════╗
║          🧑‍🌾 玩家档案 🧑‍🌾              ║
╠═══════════════════════════════════════╣
║  姓名: {info['name']:<31} ║
║  等级: Lv.{info['level']:<28} ║
║  称号: {info['current_title'] or '无':<31} ║
║                                       ║
║  💰 金币: {info['gold']:<28} ║
║  💎 钻石: {info['diamond']:<28} ║
║  ⭐ 信誉度: {info['reputation']}/100 ({info['reputation_level']:<14}) ║
║                                       ║
║  📊 月度表现                          ║
║    连续完成: {info['consecutive_success']} 次              ║
║    总完成: {info['total_targets_completed']} 次 | 总失败: {info['total_targets_failed']} 次   ║
║                                       ║
║  🏆 成就数: {info['achievements_count']:<26} ║
║  ✨ 称号数: {info['titles_count']:<26} ║
╚═══════════════════════════════════════╝
        """

        return profile
