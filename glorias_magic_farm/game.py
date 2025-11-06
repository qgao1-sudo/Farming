"""
Gloria's Magic Farm - 主游戏类
整合所有系统，提供游戏主循环
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .core import Farm, Player, MonthlyTarget
from .data import get_crop_info, CROPS_DATABASE


class GloriaMagicFarm:
    """Gloria's Magic Farm 游戏主类"""

    def __init__(self, player_name: str = "Gloria"):
        self.player = Player(player_name)
        self.farm = Farm(player_name)
        self.monthly_target = MonthlyTarget()

        # 游戏时间
        self.current_date = datetime(2024, 5, 1)  # 从5月1日开始
        self.game_day = 1

        # 游戏状态
        self.is_running = False

        # 初始化：生成第一个月度指标
        difficulty = self._calculate_difficulty()
        self.monthly_target.generate_new_target(difficulty, self.current_date)

    def _calculate_difficulty(self) -> int:
        """根据玩家信誉度计算指标难度"""
        if self.player.reputation >= 90:
            return 3
        elif self.player.reputation >= 70:
            return 2
        else:
            return 1

    def advance_day(self):
        """推进一天"""
        self.current_date += timedelta(days=1)
        self.game_day += 1

        # 更新所有地块
        self.farm.update_all_plots(self.current_date)

        # 检查是否到了月底
        if self._is_month_end():
            self._settle_month()

    def _is_month_end(self) -> bool:
        """检查是否到了月底"""
        tomorrow = self.current_date + timedelta(days=1)
        return tomorrow.day == 1

    def _settle_month(self):
        """月底结算"""
        print("\n" + "="*50)
        print("🗓️  月底到了！开始结算...")
        print("="*50 + "\n")

        # 获取玩家月度统计数据
        player_stats = self.player.get_monthly_stats()

        # 进行结算
        result = self.monthly_target.settle_month(player_stats)

        print(result["message"])
        print()

        if result["success"]:
            # 完成指标
            rewards = self.player.complete_target(result["rewards"])
            for reward in rewards:
                print(reward["message"])
        else:
            # 未完成指标
            penalties = self.player.fail_target(result["penalty"])
            for penalty in penalties:
                print(penalty["message"])

        print()

        # 重置月度统计
        self.player.reset_monthly_stats()

        # 生成下个月的指标
        difficulty = self._calculate_difficulty()
        announcement = self.monthly_target.generate_new_target(difficulty, self.current_date + timedelta(days=1))
        print(announcement)

    def buy_and_plant_crop(self, crop_name: str) -> dict:
        """购买种子并种植"""
        crop_data = get_crop_info(crop_name)
        if not crop_data:
            return {"success": False, "message": f"未找到作物: {crop_name}"}

        # 检查金币
        seed_price = crop_data["seed_price"]
        if self.player.gold < seed_price:
            return {
                "success": False,
                "message": f"金币不足！需要 {seed_price} 金币，当前只有 {self.player.gold} 金币"
            }

        # 扣除金币
        spend_result = self.player.spend_gold(seed_price, f"购买 {crop_name} 种子")
        if not spend_result["success"]:
            return spend_result

        # 种植
        plant_result = self.farm.plant_crop(crop_name, self.current_date)

        if plant_result["success"]:
            # 记录种植（用于多样性指标）
            self.player.record_planting(crop_name, crop_data["category"])
            return {
                "success": True,
                "message": f"成功购买并种植 {crop_name}！{plant_result['message']}",
                "plot_id": plant_result["plot_id"],
                "harvest_date": plant_result["harvest_date"]
            }
        else:
            # 种植失败，退款
            self.player.add_gold(seed_price, "种植失败退款")
            return plant_result

    def harvest_and_sell(self, plot_id: int) -> dict:
        """收获并自动出售"""
        harvest_result = self.farm.harvest_plot(plot_id)

        if not harvest_result["success"]:
            return harvest_result

        # 记录收获
        crop_name = harvest_result["crop_name"]
        quantity = harvest_result["quantity"]
        quality = harvest_result["quality"]
        value = harvest_result["value"]

        self.player.record_harvest(crop_name, quantity, quality)

        # 自动出售，获得金币
        self.player.add_gold(value, f"出售 {quantity} 个 {quality} 品质的 {crop_name}")

        # 记录销售额（用于经济指标）
        self.player.record_daily_sale(value)

        return {
            "success": True,
            "message": f"成功收获并出售！",
            "crop_name": crop_name,
            "quantity": quantity,
            "quality": quality,
            "value": value,
            "current_gold": self.player.gold
        }

    def harvest_all_and_sell(self) -> List[dict]:
        """收获所有成熟作物并出售"""
        results = []
        harvestable_plots = [
            i for i, plot in enumerate(self.farm.plots)
            if plot.is_occupied and plot.crop and plot.crop.is_harvestable
        ]

        for plot_id in harvestable_plots:
            result = self.harvest_and_sell(plot_id)
            if result["success"]:
                results.append(result)

        return results

    def water_all_crops(self):
        """给所有作物浇水"""
        count = 0
        for i, plot in enumerate(self.farm.plots):
            if plot.is_occupied and plot.crop:
                self.farm.water_plot(i)
                count += 1

        return {"success": True, "message": f"已给 {count} 块地浇水"}

    def fertilize_all_crops(self):
        """给所有作物施肥"""
        cost_per_plot = 20  # 每块地施肥成本
        occupied_plots = sum(1 for plot in self.farm.plots if plot.is_occupied)
        total_cost = cost_per_plot * occupied_plots

        if self.player.gold < total_cost:
            return {"success": False, "message": f"金币不足！需要 {total_cost} 金币"}

        self.player.spend_gold(total_cost, "购买肥料")

        count = 0
        for i, plot in enumerate(self.farm.plots):
            if plot.is_occupied and plot.crop:
                self.farm.fertilize_plot(i)
                count += 1

        return {"success": True, "message": f"已给 {count} 块地施肥"}

    def show_farm_status(self):
        """显示农场状态"""
        farm_status = self.farm.get_farm_status(self.current_date)

        print("\n" + "="*50)
        print(f"🌾 {farm_status['owner']} 的农场 (Lv.{farm_status['level']})")
        print("="*50)
        print(f"📅 日期: {self.current_date.strftime('%Y年%m月%d日')} (第 {self.game_day} 天)")
        print(f"🏞️  地块: {farm_status['occupied_plots']}/{farm_status['total_plots']} 已使用")
        print(f"✅ 可收获: {farm_status['harvestable_plots']} 块地")
        print()

        # 显示作物列表
        if farm_status['crops']:
            print("🌱 当前作物:")
            for crop_info in farm_status['crops']:
                crop_status = crop_info['crop_status']
                status_icon = "✅" if crop_status['is_harvestable'] else "⏳"
                days_left = crop_status['days_until_harvest']
                print(f"  {status_icon} 地块 {crop_info['plot_id']}: {crop_status['name']} "
                      f"(还需 {days_left} 天, 健康度: {crop_status['health']}%, "
                      f"水分: {crop_status['water_level']}%)")
        else:
            print("🌱 当前没有作物")

        print("="*50 + "\n")

    def show_player_status(self):
        """显示玩家状态"""
        print(self.player.display_profile())

    def show_target_progress(self):
        """显示月度指标进度"""
        player_stats = self.player.get_monthly_stats()
        progress = self.monthly_target.get_progress(player_stats)

        print("\n" + "="*50)
        print("📋 月度指标进度")
        print("="*50)
        print(f"📝 {progress['description']}")
        print(f"📊 进度: {progress['current_value']}/{progress['target_value']} "
              f"({progress['progress_percent']:.1f}%)")
        print(f"⏰ 剩余天数: {progress['days_remaining']} 天")

        # 进度条
        bar_length = 30
        filled = int(bar_length * progress['progress_percent'] / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"[{bar}] {progress['progress_percent']:.1f}%")

        print("="*50 + "\n")

    def show_planting_suggestions(self):
        """显示种植建议"""
        # 计算月底日期
        if self.current_date.month == 12:
            month_end = datetime(self.current_date.year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = datetime(self.current_date.year, self.current_date.month + 1, 1) - timedelta(days=1)

        suggestions = self.farm.get_planting_suggestions(month_end, self.current_date)

        print("\n" + "="*50)
        print("💡 种植建议（基于月底截止日期）")
        print("="*50)
        print(f"📅 当前日期: {self.current_date.strftime('%Y-%m-%d')}")
        print(f"📅 月底日期: {month_end.strftime('%Y-%m-%d')}")
        print()

        if not suggestions:
            print("⚠️  警告：没有作物能在本月内收获！")
        else:
            print("推荐种植（按推荐度排序）:\n")
            for i, suggestion in enumerate(suggestions[:10], 1):  # 只显示前10个
                print(f"{i}. {suggestion['crop_name']}")
                print(f"   生长天数: {suggestion['growth_days']} 天")
                print(f"   收获日期: {suggestion['harvest_date']}")
                print(f"   时间余量: {suggestion['days_margin']} 天")
                print(f"   预计利润: {suggestion['profit_per_plot']} 金币/地块")
                print(f"   投资回报率: {suggestion['roi']:.1f}%")
                print(f"   稀有度: {suggestion['rarity']}")
                print(f"   推荐分数: {suggestion['recommendation_score']:.1f}")
                print()

        print("="*50 + "\n")
