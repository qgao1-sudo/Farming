"""
Gloria's Magic Farm - 农场管理系统
处理农场的地块、种植、收获等操作
"""

from datetime import datetime
from typing import Dict, List, Optional
from .crop import Crop, can_harvest_before_deadline
from ..data.crops_data import get_crop_info


class FarmPlot:
    """农场地块类"""

    def __init__(self, plot_id: int):
        self.plot_id = plot_id
        self.crop: Optional[Crop] = None
        self.is_occupied = False
        self.soil_quality = 100  # 土壤质量
        self.has_irrigation = False  # 是否有自动灌溉

    def plant(self, crop: Crop) -> bool:
        """种植作物"""
        if self.is_occupied:
            return False

        self.crop = crop
        self.is_occupied = True
        return True

    def harvest(self) -> Optional[dict]:
        """收获作物"""
        if not self.is_occupied or not self.crop:
            return None

        result = self.crop.harvest()
        self.crop = None
        self.is_occupied = False

        # 收获后土壤质量下降
        self.soil_quality = max(20, self.soil_quality - 10)

        return result

    def update(self, current_date: datetime):
        """更新地块状态"""
        if self.crop:
            self.crop.update_growth(current_date)
            self.crop.update_health()

            # 自动灌溉系统
            if self.has_irrigation and self.crop.water_level < 50:
                self.crop.water()

    def get_status(self, current_date: datetime) -> dict:
        """获取地块状态"""
        if not self.is_occupied or not self.crop:
            return {
                "plot_id": self.plot_id,
                "is_occupied": False,
                "soil_quality": self.soil_quality
            }

        return {
            "plot_id": self.plot_id,
            "is_occupied": True,
            "soil_quality": self.soil_quality,
            "crop_status": self.crop.get_status(current_date)
        }


class Farm:
    """农场类"""

    def __init__(self, owner_name: str, initial_plots: int = 9):
        self.owner_name = owner_name
        self.plots: List[FarmPlot] = [FarmPlot(i) for i in range(initial_plots)]
        self.total_plots = initial_plots
        self.level = 1

        # 设施
        self.has_greenhouse = False  # 温室
        self.has_processing_plant = False  # 种子加工厂
        self.has_planning_house = False  # 智能规划屋
        self.irrigation_coverage = 0  # 灌溉系统覆盖的地块数

    def get_empty_plot(self) -> Optional[FarmPlot]:
        """获取一个空闲地块"""
        for plot in self.plots:
            if not plot.is_occupied:
                return plot
        return None

    def plant_crop(self, crop_name: str, current_date: datetime) -> dict:
        """
        种植作物

        Args:
            crop_name: 作物名称
            current_date: 当前日期

        Returns:
            dict: 种植结果
        """
        crop_data = get_crop_info(crop_name)
        if not crop_data:
            return {"success": False, "message": f"未找到作物: {crop_name}"}

        plot = self.get_empty_plot()
        if not plot:
            return {"success": False, "message": "没有空闲的地块了！"}

        crop = Crop(crop_data, current_date, plot.plot_id)
        if plot.plant(crop):
            return {
                "success": True,
                "message": f"成功在地块 {plot.plot_id} 种植了 {crop_name}",
                "plot_id": plot.plot_id,
                "harvest_date": crop.get_harvest_date().strftime("%Y-%m-%d")
            }

        return {"success": False, "message": "种植失败"}

    def harvest_plot(self, plot_id: int) -> dict:
        """收获指定地块"""
        if plot_id >= len(self.plots):
            return {"success": False, "message": "地块不存在"}

        plot = self.plots[plot_id]
        if not plot.is_occupied:
            return {"success": False, "message": "地块上没有作物"}

        if not plot.crop.is_harvestable:
            return {"success": False, "message": "作物还未成熟"}

        result = plot.harvest()
        if result:
            result["success"] = True
            result["plot_id"] = plot_id
            return result

        return {"success": False, "message": "收获失败"}

    def harvest_all_ready(self) -> List[dict]:
        """收获所有已成熟的作物"""
        results = []
        for plot in self.plots:
            if plot.is_occupied and plot.crop and plot.crop.is_harvestable:
                result = plot.harvest()
                if result:
                    result["plot_id"] = plot.plot_id
                    results.append(result)
        return results

    def water_plot(self, plot_id: int) -> dict:
        """给指定地块浇水"""
        if plot_id >= len(self.plots):
            return {"success": False, "message": "地块不存在"}

        plot = self.plots[plot_id]
        if not plot.is_occupied or not plot.crop:
            return {"success": False, "message": "地块上没有作物"}

        plot.crop.water()
        return {
            "success": True,
            "message": f"已给地块 {plot_id} 浇水",
            "water_level": plot.crop.water_level
        }

    def fertilize_plot(self, plot_id: int) -> dict:
        """给指定地块施肥"""
        if plot_id >= len(self.plots):
            return {"success": False, "message": "地块不存在"}

        plot = self.plots[plot_id]
        if not plot.is_occupied or not plot.crop:
            return {"success": False, "message": "地块上没有作物"}

        plot.crop.fertilize()
        return {
            "success": True,
            "message": f"已给地块 {plot_id} 施肥",
            "fertilizer_level": plot.crop.fertilizer_level
        }

    def update_all_plots(self, current_date: datetime):
        """更新所有地块状态（每日调用）"""
        for plot in self.plots:
            plot.update(current_date)

    def get_farm_status(self, current_date: datetime) -> dict:
        """获取农场整体状态"""
        occupied_plots = sum(1 for plot in self.plots if plot.is_occupied)
        harvestable_plots = sum(
            1 for plot in self.plots
            if plot.is_occupied and plot.crop and plot.crop.is_harvestable
        )

        crop_list = []
        for plot in self.plots:
            if plot.is_occupied and plot.crop:
                crop_list.append(plot.get_status(current_date))

        return {
            "owner": self.owner_name,
            "level": self.level,
            "total_plots": self.total_plots,
            "occupied_plots": occupied_plots,
            "empty_plots": self.total_plots - occupied_plots,
            "harvestable_plots": harvestable_plots,
            "facilities": {
                "greenhouse": self.has_greenhouse,
                "processing_plant": self.has_processing_plant,
                "planning_house": self.has_planning_house,
                "irrigation_coverage": self.irrigation_coverage
            },
            "crops": crop_list
        }

    def expand_farm(self, additional_plots: int = 3) -> dict:
        """扩建农场，增加地块"""
        new_plots = [FarmPlot(self.total_plots + i) for i in range(additional_plots)]
        self.plots.extend(new_plots)
        self.total_plots += additional_plots

        return {
            "success": True,
            "message": f"农场扩建成功！新增 {additional_plots} 块地",
            "total_plots": self.total_plots
        }

    def upgrade_irrigation(self, plots_count: int) -> dict:
        """升级灌溉系统"""
        if plots_count > self.total_plots:
            plots_count = self.total_plots

        for i in range(plots_count):
            self.plots[i].has_irrigation = True

        self.irrigation_coverage = plots_count

        return {
            "success": True,
            "message": f"灌溉系统升级成功！覆盖 {plots_count} 块地",
            "coverage": self.irrigation_coverage
        }

    def build_facility(self, facility_name: str) -> dict:
        """建造设施"""
        facilities = {
            "greenhouse": "温室",
            "processing_plant": "种子加工厂",
            "planning_house": "智能规划屋"
        }

        if facility_name not in facilities:
            return {"success": False, "message": "未知的设施类型"}

        if facility_name == "greenhouse":
            self.has_greenhouse = True
        elif facility_name == "processing_plant":
            self.has_processing_plant = True
        elif facility_name == "planning_house":
            self.has_planning_house = True

        return {
            "success": True,
            "message": f"{facilities[facility_name]} 建造完成！"
        }

    def get_planting_suggestions(self, deadline: datetime, current_date: datetime) -> List[dict]:
        """
        获取种植建议（基于月底截止日期）
        使用我们实现的核心函数 can_harvest_before_deadline

        Args:
            deadline: 截止日期（通常是月底）
            current_date: 当前日期

        Returns:
            list: 建议列表
        """
        from ..data.crops_data import CROPS_DATABASE

        suggestions = []

        for crop_name, crop_data in CROPS_DATABASE.items():
            check_result = can_harvest_before_deadline(crop_data, current_date, deadline)

            if check_result["can_harvest"]:
                profit_info = self._calculate_profit(crop_data)

                suggestions.append({
                    "crop_name": crop_name,
                    "can_harvest": True,
                    "harvest_date": check_result["harvest_date"].strftime("%Y-%m-%d"),
                    "days_margin": check_result["days_margin"],
                    "growth_days": crop_data["growth_days"],
                    "profit_per_plot": profit_info["profit"],
                    "roi": profit_info["roi"],
                    "rarity": crop_data["rarity"],
                    "recommendation_score": self._calculate_recommendation_score(
                        check_result["days_margin"],
                        profit_info["roi"],
                        crop_data["rarity"]
                    )
                })

        # 按推荐分数排序
        suggestions.sort(key=lambda x: x["recommendation_score"], reverse=True)

        return suggestions

    def _calculate_profit(self, crop_data: dict) -> dict:
        """计算作物利润"""
        cost = crop_data["seed_price"]
        revenue = crop_data["base_price"] * crop_data["base_yield"]
        profit = revenue - cost
        roi = (profit / cost * 100) if cost > 0 else 0

        return {"profit": profit, "roi": roi}

    def _calculate_recommendation_score(self, days_margin: int, roi: float, rarity: str) -> float:
        """计算推荐分数"""
        score = 0

        # 时间余量分数（更多余量更好）
        score += min(days_margin * 2, 50)

        # ROI分数
        score += min(roi / 10, 30)

        # 稀有度分数
        rarity_scores = {
            "common": 5,
            "rare": 10,
            "epic": 15,
            "legendary": 20
        }
        score += rarity_scores.get(rarity, 0)

        return score
