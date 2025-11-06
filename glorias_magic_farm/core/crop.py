"""
Gloria's Magic Farm - 作物类
处理作物的种植、生长和收获
"""

from datetime import datetime, timedelta
from typing import Optional


class Crop:
    """作物类 - 代表农场中的一株作物"""

    def __init__(self, crop_data: dict, planted_date: datetime, plot_id: int = 0):
        """
        初始化作物

        Args:
            crop_data: 从 crops_data.py 中获取的作物数据字典
            planted_date: 种植日期
            plot_id: 地块ID（用于标识种植位置）
        """
        self.name = crop_data["name"]
        self.growth_days = crop_data["growth_days"]
        self.base_yield = crop_data["base_yield"]
        self.base_price = crop_data["base_price"]
        self.category = crop_data["category"]
        self.rarity = crop_data["rarity"]
        self.season = crop_data["season"]

        self.planted_date = planted_date
        self.plot_id = plot_id
        self.is_harvestable = False
        self.is_harvested = False
        self.quality = "normal"  # normal, good, excellent, perfect

        # 作物状态
        self.water_level = 100  # 水分等级
        self.fertilizer_level = 0  # 肥料等级
        self.health = 100  # 健康度

    def update_growth(self, current_date: datetime) -> bool:
        """
        更新作物生长状态

        Args:
            current_date: 当前日期

        Returns:
            bool: 是否可以收获
        """
        if self.is_harvested:
            return False

        days_passed = (current_date - self.planted_date).days
        if days_passed >= self.growth_days:
            self.is_harvestable = True

        return self.is_harvestable

    def get_days_until_harvest(self, current_date: datetime) -> int:
        """
        计算距离收获还有几天

        Args:
            current_date: 当前日期

        Returns:
            int: 剩余天数（0表示已可收获）
        """
        if self.is_harvested:
            return -1

        days_passed = (current_date - self.planted_date).days
        days_left = self.growth_days - days_passed
        return max(0, days_left)

    def get_harvest_date(self) -> datetime:
        """获取预计收获日期"""
        return self.planted_date + timedelta(days=self.growth_days)

    def water(self):
        """浇水"""
        self.water_level = min(100, self.water_level + 30)

    def fertilize(self):
        """施肥"""
        self.fertilizer_level = min(100, self.fertilizer_level + 20)

    def update_health(self):
        """更新健康度（每天调用）"""
        # 缺水会降低健康度
        if self.water_level < 30:
            self.health = max(0, self.health - 10)

        # 水分自然消耗
        self.water_level = max(0, self.water_level - 15)

    def calculate_yield(self) -> int:
        """
        根据作物状态计算实际产量

        Returns:
            int: 实际产量
        """
        yield_multiplier = 1.0

        # 健康度影响
        if self.health >= 90:
            yield_multiplier *= 1.2
        elif self.health >= 70:
            yield_multiplier *= 1.0
        elif self.health >= 50:
            yield_multiplier *= 0.8
        else:
            yield_multiplier *= 0.5

        # 肥料影响
        if self.fertilizer_level >= 80:
            yield_multiplier *= 1.3
        elif self.fertilizer_level >= 50:
            yield_multiplier *= 1.1

        return int(self.base_yield * yield_multiplier)

    def harvest(self) -> dict:
        """
        收获作物

        Returns:
            dict: 收获结果 {"crop_name": str, "quantity": int, "quality": str, "value": int}
        """
        if not self.is_harvestable or self.is_harvested:
            return {"error": "作物还未成熟或已被收获"}

        self.is_harvested = True
        quantity = self.calculate_yield()

        # 根据健康度和肥料等级决定品质
        if self.health >= 95 and self.fertilizer_level >= 80:
            self.quality = "perfect"
            price_multiplier = 2.0
        elif self.health >= 85 and self.fertilizer_level >= 60:
            self.quality = "excellent"
            price_multiplier = 1.5
        elif self.health >= 70 and self.fertilizer_level >= 40:
            self.quality = "good"
            price_multiplier = 1.2
        else:
            self.quality = "normal"
            price_multiplier = 1.0

        total_value = int(quantity * self.base_price * price_multiplier)

        return {
            "crop_name": self.name,
            "quantity": quantity,
            "quality": self.quality,
            "value": total_value,
            "base_price": self.base_price
        }

    def get_status(self, current_date: datetime) -> dict:
        """
        获取作物当前状态

        Args:
            current_date: 当前日期

        Returns:
            dict: 作物状态信息
        """
        return {
            "name": self.name,
            "plot_id": self.plot_id,
            "planted_date": self.planted_date.strftime("%Y-%m-%d"),
            "days_until_harvest": self.get_days_until_harvest(current_date),
            "is_harvestable": self.is_harvestable,
            "is_harvested": self.is_harvested,
            "water_level": self.water_level,
            "fertilizer_level": self.fertilizer_level,
            "health": self.health,
            "quality_prediction": self._predict_quality()
        }

    def _predict_quality(self) -> str:
        """预测当前状态下的收获品质"""
        if self.health >= 95 and self.fertilizer_level >= 80:
            return "perfect"
        elif self.health >= 85 and self.fertilizer_level >= 60:
            return "excellent"
        elif self.health >= 70 and self.fertilizer_level >= 40:
            return "good"
        else:
            return "normal"

    def __repr__(self):
        return f"<Crop: {self.name} (Plot {self.plot_id}, Health: {self.health}%)>"


def can_harvest_before_deadline(crop_data: dict, plant_date: datetime, deadline: datetime) -> dict:
    """
    判断某种作物在指定日期种植后，是否能在截止日期前收获

    这是用户要求的核心功能函数！

    Args:
        crop_data: 作物数据字典
        plant_date: 计划种植日期
        deadline: 截止日期（通常是月底）

    Returns:
        dict: {
            "can_harvest": bool,  # 是否能在截止日期前收获
            "harvest_date": datetime,  # 预计收获日期
            "days_margin": int,  # 距离截止日期的余量（负数表示来不及）
            "crop_name": str
        }
    """
    crop_name = crop_data["name"]
    growth_days = crop_data["growth_days"]

    harvest_date = plant_date + timedelta(days=growth_days)
    days_margin = (deadline - harvest_date).days
    can_harvest = harvest_date <= deadline

    return {
        "can_harvest": can_harvest,
        "harvest_date": harvest_date,
        "days_margin": days_margin,
        "crop_name": crop_name,
        "plant_date": plant_date,
        "deadline": deadline
    }


def calculate_max_harvests_in_period(crop_data: dict, start_date: datetime, end_date: datetime) -> dict:
    """
    计算在指定时间段内，某种作物最多能收获几次
    （考虑种植后再次种植的情况）

    Args:
        crop_data: 作物数据
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        dict: 包含最大收获次数等信息
    """
    growth_days = crop_data["growth_days"]
    total_days = (end_date - start_date).days

    max_harvests = total_days // growth_days

    # 计算每次收获的日期
    harvest_schedule = []
    current_plant_date = start_date

    for i in range(max_harvests):
        harvest_date = current_plant_date + timedelta(days=growth_days)
        if harvest_date <= end_date:
            harvest_schedule.append({
                "cycle": i + 1,
                "plant_date": current_plant_date,
                "harvest_date": harvest_date
            })
            current_plant_date = harvest_date
        else:
            break

    return {
        "crop_name": crop_data["name"],
        "max_harvests": len(harvest_schedule),
        "total_yield": len(harvest_schedule) * crop_data["base_yield"],
        "harvest_schedule": harvest_schedule,
        "period_days": total_days
    }
