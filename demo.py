"""
Gloria's Magic Farm - 游戏演示
展示游戏的核心功能和玩法
"""

import sys
import os

# 添加项目路径到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from glorias_magic_farm.game import GloriaMagicFarm
from glorias_magic_farm.data import CROPS_DATABASE, get_crops_by_category, calculate_profit
from glorias_magic_farm.core import can_harvest_before_deadline
from datetime import datetime, timedelta


def print_banner():
    """打印游戏横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║      ✨ Gloria's Magic Farm - 魔法农场 ✨                  ║
║                                                           ║
║           一个关于效率和规划的农场经营游戏                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def demo_crop_database():
    """演示：作物数据库"""
    print("\n" + "="*60)
    print("📚 演示 1: 作物数据库")
    print("="*60 + "\n")

    print(f"游戏共有 {len(CROPS_DATABASE)} 种作物:\n")

    # 按类别展示
    categories = {
        "vegetable": "蔬菜",
        "fruit": "水果",
        "flower": "花卉",
        "special": "特殊作物"
    }

    for category_en, category_cn in categories.items():
        crops = get_crops_by_category(category_en)
        print(f"【{category_cn}】({len(crops)}种)")
        for crop_name, crop_data in crops.items():
            print(f"  • {crop_name}: "
                  f"{crop_data['growth_days']}天成熟, "
                  f"种子{crop_data['seed_price']}金币, "
                  f"产量{crop_data['base_yield']}, "
                  f"售价{crop_data['base_price']}金币/个")

            # 计算利润
            profit_info = calculate_profit(crop_name)
            print(f"    💰 利润: {profit_info['profit']} 金币, "
                  f"ROI: {profit_info['roi']:.1f}%")
        print()


def demo_harvest_calculation():
    """演示：收获日期计算（核心功能）"""
    print("\n" + "="*60)
    print("🧮 演示 2: 收获日期计算（用户要求的核心功能）")
    print("="*60 + "\n")

    # 模拟场景：现在是5月15日，月底是5月31日
    plant_date = datetime(2024, 5, 15)
    deadline = datetime(2024, 5, 31)

    print(f"📅 场景: 今天是 {plant_date.strftime('%Y-%m-%d')}")
    print(f"📅 月底截止日期: {deadline.strftime('%Y-%m-%d')}")
    print(f"📅 可用时间: {(deadline - plant_date).days} 天\n")

    print("分析各种作物是否能在月底前收获:\n")

    can_harvest_list = []
    cannot_harvest_list = []

    for crop_name, crop_data in CROPS_DATABASE.items():
        result = can_harvest_before_deadline(crop_data, plant_date, deadline)

        if result["can_harvest"]:
            can_harvest_list.append(result)
        else:
            cannot_harvest_list.append(result)

    print(f"✅ 可以在月底前收获的作物 ({len(can_harvest_list)}种):")
    for result in sorted(can_harvest_list, key=lambda x: x["days_margin"], reverse=True):
        print(f"  • {result['crop_name']}: "
              f"预计 {result['harvest_date'].strftime('%m-%d')} 收获, "
              f"时间余量 {result['days_margin']} 天")

    print(f"\n❌ 来不及在月底前收获的作物 ({len(cannot_harvest_list)}种):")
    for result in cannot_harvest_list[:5]:  # 只显示前5个
        print(f"  • {result['crop_name']}: "
              f"预计 {result['harvest_date'].strftime('%m-%d')} 收获, "
              f"超出 {-result['days_margin']} 天")


def demo_game_simulation():
    """演示：游戏模拟运行"""
    print("\n" + "="*60)
    print("🎮 演示 3: 游戏模拟（完整流程）")
    print("="*60 + "\n")

    # 创建游戏实例
    game = GloriaMagicFarm(player_name="Gloria")

    print("🎬 游戏开始！\n")

    # 显示初始状态
    game.show_player_status()
    game.show_farm_status()
    game.show_target_progress()

    # 获取种植建议
    game.show_planting_suggestions()

    # 模拟游戏流程
    print("\n" + "="*60)
    print("📝 开始执行游戏操作...")
    print("="*60 + "\n")

    # 第1天：种植一些快速生长的作物
    print("【第1天】种植作物\n")

    crops_to_plant = ["小麦", "小麦", "胡萝卜", "番茄", "草莓"]

    for crop_name in crops_to_plant:
        result = game.buy_and_plant_crop(crop_name)
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   预计收获日期: {result['harvest_date']}")
        else:
            print(f"❌ {result['message']}")

    print()
    game.show_farm_status()

    # 模拟几天的照料
    print("\n【第2-3天】照料作物\n")

    for day in range(2):
        game.advance_day()
        water_result = game.water_all_crops()
        print(f"第{game.game_day}天: {water_result['message']}")

    # 施肥
    fertilize_result = game.fertilize_all_crops()
    print(f"施肥: {fertilize_result['message']}\n")

    game.show_farm_status()

    # 第4天：小麦应该可以收获了（2天生长周期）
    print("\n【第4天】收获成熟作物\n")

    game.advance_day()

    harvest_results = game.harvest_all_and_sell()
    if harvest_results:
        for result in harvest_results:
            print(f"✅ 收获成功！")
            print(f"   作物: {result['crop_name']}")
            print(f"   数量: {result['quantity']} 个")
            print(f"   品质: {result['quality']}")
            print(f"   获得: {result['value']} 金币")
            print()
    else:
        print("还没有作物可以收获。")

    game.show_player_status()
    game.show_target_progress()

    # 继续种植
    print("\n【第4天】继续种植\n")

    more_crops = ["小麦", "白萝卜", "向日葵"]
    for crop_name in more_crops:
        result = game.buy_and_plant_crop(crop_name)
        if result["success"]:
            print(f"✅ {result['message']}")

    print()
    game.show_farm_status()

    # 模拟到第10天
    print("\n【第5-10天】持续经营...\n")

    for _ in range(6):
        game.advance_day()
        game.water_all_crops()

        # 每隔一天收获
        if game.game_day % 2 == 0:
            harvest_results = game.harvest_all_and_sell()
            if harvest_results:
                total_value = sum(r['value'] for r in harvest_results)
                print(f"第{game.game_day}天: 收获并出售，获得 {total_value} 金币")

                # 继续种植
                for _ in range(len(harvest_results)):
                    if game.player.gold >= 30:
                        game.buy_and_plant_crop("番茄")

    print("\n【第10天】查看农场状态\n")
    game.show_farm_status()
    game.show_player_status()
    game.show_target_progress()

    print("\n🎉 演示完成！")
    print("\n提示：实际游戏中还有更多功能，如：")
    print("  • 建造温室、加工厂等设施")
    print("  • 农场扩建，增加地块")
    print("  • 解锁成就和称号")
    print("  • 月底结算和连续完成奖励")
    print("  • 培育稀有作物（黄金南瓜、水晶葡萄、樱花树等）")


def demo_advanced_features():
    """演示：高级功能"""
    print("\n" + "="*60)
    print("🔬 演示 4: 高级功能")
    print("="*60 + "\n")

    from glorias_magic_farm.core import calculate_max_harvests_in_period
    from glorias_magic_farm.data import get_crop_info

    # 计算一个月内最多能收获几次
    print("【功能】计算一个月内某作物的最大收获次数\n")

    start_date = datetime(2024, 5, 1)
    end_date = datetime(2024, 5, 31)

    test_crops = ["小麦", "番茄", "黄金南瓜"]

    for crop_name in test_crops:
        crop_data = get_crop_info(crop_name)
        result = calculate_max_harvests_in_period(crop_data, start_date, end_date)

        print(f"📊 {result['crop_name']}:")
        print(f"   生长周期: {crop_data['growth_days']} 天")
        print(f"   时间段: {result['period_days']} 天")
        print(f"   最大收获次数: {result['max_harvests']} 次")
        print(f"   总产量: {result['total_yield']} 个")
        print(f"   收获时间表:")
        for schedule in result['harvest_schedule']:
            print(f"     第{schedule['cycle']}次: "
                  f"{schedule['plant_date'].strftime('%m-%d')} 种植 -> "
                  f"{schedule['harvest_date'].strftime('%m-%d')} 收获")
        print()


def main():
    """主函数"""
    print_banner()

    print("\n欢迎来到 Gloria's Magic Farm！")
    print("这是一个关于效率和规划的农场经营游戏。\n")

    demos = [
        ("1", "作物数据库", demo_crop_database),
        ("2", "收获日期计算（核心功能）", demo_harvest_calculation),
        ("3", "游戏模拟运行", demo_game_simulation),
        ("4", "高级功能", demo_advanced_features),
        ("all", "运行所有演示", None)
    ]

    print("请选择要运行的演示:\n")
    for code, name, _ in demos:
        print(f"  [{code}] {name}")

    print()
    choice = input("请输入选项 (直接回车运行所有演示): ").strip() or "all"

    if choice == "all":
        # 运行所有演示
        demo_crop_database()
        input("\n按回车继续下一个演示...")

        demo_harvest_calculation()
        input("\n按回车继续下一个演示...")

        demo_game_simulation()
        input("\n按回车继续下一个演示...")

        demo_advanced_features()
    else:
        # 运行指定演示
        for code, name, func in demos:
            if code == choice and func:
                func()
                break
        else:
            print("❌ 无效的选项！")

    print("\n" + "="*60)
    print("感谢体验 Gloria's Magic Farm！")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
