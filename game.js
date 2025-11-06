// Gloria's Magic Farm - JavaScript Game Logic
// 开罗游戏风格的农场经营游戏

// ==================== 作物数据库 ====================
const CROPS_DATABASE = {
    "小麦": {
        name: "小麦",
        icon: "🌾",
        seedPrice: 10,
        growthDays: 2,
        baseYield: 30,
        basePrice: 5,
        season: ["春", "秋"],
        category: "vegetable",
        rarity: "common",
        description: "周期短，适合冲刺数量指标"
    },
    "番茄": {
        name: "番茄",
        icon: "🍅",
        seedPrice: 30,
        growthDays: 4,
        baseYield: 10,
        basePrice: 15,
        season: ["夏"],
        category: "fruit",
        rarity: "common",
        description: "单价高，适合经济指标"
    },
    "彩虹菊": {
        name: "彩虹菊",
        icon: "🌸",
        seedPrice: 100,
        growthDays: 6,
        baseYield: 5,
        basePrice: 50,
        season: ["春"],
        category: "flower",
        rarity: "rare",
        description: "花卉，用于多样性指标"
    },
    "黄金南瓜": {
        name: "黄金南瓜",
        icon: "🎃",
        seedPrice: 200,
        growthDays: 8,
        baseYield: 1,
        basePrice: 300,
        season: ["秋"],
        category: "special",
        rarity: "epic",
        description: "稀有作物，用于奇迹指标"
    },
    "胡萝卜": {
        name: "胡萝卜",
        icon: "🥕",
        seedPrice: 15,
        growthDays: 3,
        baseYield: 20,
        basePrice: 8,
        season: ["春", "秋", "冬"],
        category: "vegetable",
        rarity: "common",
        description: "生命力顽强，三季可种"
    },
    "草莓": {
        name: "草莓",
        icon: "🍓",
        seedPrice: 50,
        growthDays: 5,
        baseYield: 15,
        basePrice: 20,
        season: ["春", "夏"],
        category: "fruit",
        rarity: "common",
        description: "香甜可口，市场需求大"
    },
    "薰衣草": {
        name: "薰衣草",
        icon: "💜",
        seedPrice: 80,
        growthDays: 7,
        baseYield: 8,
        basePrice: 45,
        season: ["夏"],
        category: "flower",
        rarity: "rare",
        description: "紫色浪漫，可制作香薰"
    },
    "蓝莓": {
        name: "蓝莓",
        icon: "🫐",
        seedPrice: 60,
        growthDays: 6,
        baseYield: 12,
        basePrice: 25,
        season: ["夏", "秋"],
        category: "fruit",
        rarity: "rare",
        description: "富含花青素"
    },
    "向日葵": {
        name: "向日葵",
        icon: "🌻",
        seedPrice: 40,
        growthDays: 5,
        baseYield: 10,
        basePrice: 18,
        season: ["夏"],
        category: "flower",
        rarity: "common",
        description: "阳光的象征"
    },
    "水晶葡萄": {
        name: "水晶葡萄",
        icon: "🍇",
        seedPrice: 300,
        growthDays: 10,
        baseYield: 3,
        basePrice: 400,
        season: ["夏", "秋"],
        category: "special",
        rarity: "legendary",
        description: "传说中的奇迹作物"
    },
    "玫瑰": {
        name: "玫瑰",
        icon: "🌹",
        seedPrice: 120,
        growthDays: 8,
        baseYield: 6,
        basePrice: 60,
        season: ["春", "夏"],
        category: "flower",
        rarity: "rare",
        description: "爱情的象征"
    },
    "白萝卜": {
        name: "白萝卜",
        icon: "🥬",
        seedPrice: 12,
        growthDays: 3,
        baseYield: 25,
        basePrice: 6,
        season: ["秋", "冬"],
        category: "vegetable",
        rarity: "common",
        description: "冬季的主力蔬菜"
    },
    "魔法蘑菇": {
        name: "魔法蘑菇",
        icon: "🍄",
        seedPrice: 250,
        growthDays: 9,
        baseYield: 2,
        basePrice: 350,
        season: ["秋"],
        category: "special",
        rarity: "epic",
        description: "月光下会发光"
    },
    "樱花树苗": {
        name: "樱花树苗",
        icon: "🌸",
        seedPrice: 500,
        growthDays: 15,
        baseYield: 1,
        basePrice: 800,
        season: ["春"],
        category: "special",
        rarity: "legendary",
        description: "开花时美不胜收"
    }
};

// ==================== 作物类 ====================
class Crop {
    constructor(cropData, plantedDate, plotId) {
        this.name = cropData.name;
        this.icon = cropData.icon;
        this.growthDays = cropData.growthDays;
        this.baseYield = cropData.baseYield;
        this.basePrice = cropData.basePrice;
        this.category = cropData.category;
        this.rarity = cropData.rarity;

        this.plantedDate = new Date(plantedDate);
        this.plotId = plotId;
        this.isHarvestable = false;
        this.isHarvested = false;
        this.quality = "normal";

        this.waterLevel = 100;
        this.fertilizerLevel = 0;
        this.health = 100;
    }

    updateGrowth(currentDate) {
        if (this.isHarvested) return false;

        const daysPassed = Math.floor((currentDate - this.plantedDate) / (1000 * 60 * 60 * 24));
        if (daysPassed >= this.growthDays) {
            this.isHarvestable = true;
        }
        return this.isHarvestable;
    }

    getDaysUntilHarvest(currentDate) {
        if (this.isHarvested) return -1;

        const daysPassed = Math.floor((currentDate - this.plantedDate) / (1000 * 60 * 60 * 24));
        const daysLeft = this.growthDays - daysPassed;
        return Math.max(0, daysLeft);
    }

    water() {
        this.waterLevel = Math.min(100, this.waterLevel + 30);
    }

    fertilize() {
        this.fertilizerLevel = Math.min(100, this.fertilizerLevel + 20);
    }

    updateHealth() {
        if (this.waterLevel < 30) {
            this.health = Math.max(0, this.health - 10);
        }
        this.waterLevel = Math.max(0, this.waterLevel - 15);
    }

    calculateYield() {
        let yieldMultiplier = 1.0;

        if (this.health >= 90) yieldMultiplier *= 1.2;
        else if (this.health >= 70) yieldMultiplier *= 1.0;
        else if (this.health >= 50) yieldMultiplier *= 0.8;
        else yieldMultiplier *= 0.5;

        if (this.fertilizerLevel >= 80) yieldMultiplier *= 1.3;
        else if (this.fertilizerLevel >= 50) yieldMultiplier *= 1.1;

        return Math.floor(this.baseYield * yieldMultiplier);
    }

    harvest() {
        if (!this.isHarvestable || this.isHarvested) {
            return null;
        }

        this.isHarvested = true;
        const quantity = this.calculateYield();

        if (this.health >= 95 && this.fertilizerLevel >= 80) {
            this.quality = "perfect";
        } else if (this.health >= 85 && this.fertilizerLevel >= 60) {
            this.quality = "excellent";
        } else if (this.health >= 70 && this.fertilizerLevel >= 40) {
            this.quality = "good";
        } else {
            this.quality = "normal";
        }

        const priceMultiplier = {
            "perfect": 2.0,
            "excellent": 1.5,
            "good": 1.2,
            "normal": 1.0
        }[this.quality];

        const totalValue = Math.floor(quantity * this.basePrice * priceMultiplier);

        return {
            cropName: this.name,
            quantity: quantity,
            quality: this.quality,
            value: totalValue,
            icon: this.icon
        };
    }
}

// ==================== 游戏类 ====================
class GloriaMagicFarm {
    constructor() {
        // 玩家数据
        this.player = {
            name: "Gloria",
            gold: 1000,
            diamond: 10,
            reputation: 50,
            level: 1,
            cropsHarvested: {},
            plantedVariety: { vegetable: new Set(), fruit: new Set(), flower: new Set(), special: new Set() },
            maxDailySale: 0
        };

        // 游戏时间
        this.currentDate = new Date(2024, 4, 1); // 5月1日
        this.gameDay = 1;

        // 农场
        this.plots = Array(9).fill(null).map((_, i) => ({
            id: i,
            crop: null,
            isOccupied: false
        }));

        // 月度指标
        this.monthlyTarget = this.generateMonthlyTarget();

        // 初始化UI
        this.initUI();
        this.renderAll();
    }

    // ==================== 月度指标 ====================
    generateMonthlyTarget() {
        const types = ["harvest", "sell"];
        const type = types[Math.floor(Math.random() * types.length)];

        let target = { type: type };

        if (type === "harvest") {
            const crops = ["小麦", "胡萝卜", "番茄"];
            const crop = crops[Math.floor(Math.random() * crops.length)];
            const amount = Math.floor(Math.random() * 200) + 200;

            target.crop = crop;
            target.value = amount;
            target.description = `收获 ${amount} 个 ${crop}`;
            target.reward = { gold: amount * 10, diamond: 5, reputation: 10 };
        } else if (type === "sell") {
            const amount = Math.floor(Math.random() * 5000) + 5000;
            target.value = amount;
            target.description = `实现单日农场收入达到 ${amount} 金币`;
            target.reward = { gold: Math.floor(amount / 3), diamond: 10, reputation: 12 };
        }

        target.startDate = new Date(this.currentDate);
        target.endDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 0);

        return target;
    }

    checkTargetProgress() {
        const target = this.monthlyTarget;
        let current = 0;

        if (target.type === "harvest") {
            current = this.player.cropsHarvested[target.crop] || 0;
        } else if (target.type === "sell") {
            current = this.player.maxDailySale;
        }

        return {
            current: current,
            total: target.value,
            percent: Math.min(100, (current / target.value) * 100)
        };
    }

    settleMonth() {
        const progress = this.checkTargetProgress();
        const isCompleted = progress.current >= progress.total;

        let message = "";
        if (isCompleted) {
            message = `🎉 恭喜！你成功完成了本月指标！\n\n获得奖励：\n💰 金币: ${this.monthlyTarget.reward.gold}\n💎 钻石: ${this.monthlyTarget.reward.diamond}\n⭐ 信誉度: +${this.monthlyTarget.reward.reputation}`;

            this.player.gold += this.monthlyTarget.reward.gold;
            this.player.diamond += this.monthlyTarget.reward.diamond;
            this.player.reputation = Math.min(100, this.player.reputation + this.monthlyTarget.reward.reputation);
        } else {
            message = `💔 很遗憾，你未能完成本月指标。\n\n目标: ${this.monthlyTarget.description}\n完成: ${progress.current}/${progress.total}\n\n罚款 500 金币，信誉度 -20`;

            this.player.gold = Math.max(0, this.player.gold - 500);
            this.player.reputation = Math.max(0, this.player.reputation - 20);
        }

        // 重置月度统计
        this.player.cropsHarvested = {};
        this.player.maxDailySale = 0;

        // 生成新指标
        this.monthlyTarget = this.generateMonthlyTarget();

        return { isCompleted, message };
    }

    // ==================== 农场操作 ====================
    plantCrop(cropName, plotId) {
        const cropData = CROPS_DATABASE[cropName];
        if (!cropData) {
            return { success: false, message: `未找到作物: ${cropName}` };
        }

        if (this.player.gold < cropData.seedPrice) {
            return { success: false, message: `金币不足！需要 ${cropData.seedPrice} 金币` };
        }

        const plot = this.plots[plotId];
        if (plot.isOccupied) {
            return { success: false, message: "该地块已被占用" };
        }

        this.player.gold -= cropData.seedPrice;
        const crop = new Crop(cropData, this.currentDate, plotId);
        plot.crop = crop;
        plot.isOccupied = true;

        this.player.plantedVariety[cropData.category].add(cropName);

        this.addLog(`✅ 在地块 ${plotId} 种植了 ${cropName}`);
        return { success: true, message: `成功种植 ${cropName}` };
    }

    harvestPlot(plotId) {
        const plot = this.plots[plotId];
        if (!plot.isOccupied || !plot.crop) {
            return { success: false, message: "该地块没有作物" };
        }

        if (!plot.crop.isHarvestable) {
            return { success: false, message: "作物还未成熟" };
        }

        const result = plot.crop.harvest();
        if (!result) {
            return { success: false, message: "收获失败" };
        }

        // 记录收获
        if (!this.player.cropsHarvested[result.cropName]) {
            this.player.cropsHarvested[result.cropName] = 0;
        }
        this.player.cropsHarvested[result.cropName] += result.quantity;

        // 获得金币
        this.player.gold += result.value;

        // 记录销售额
        if (result.value > this.player.maxDailySale) {
            this.player.maxDailySale = result.value;
        }

        // 清空地块
        plot.crop = null;
        plot.isOccupied = false;

        this.addLog(`🌾 收获 ${result.quantity} 个 ${result.quality} 品质的 ${result.cropName}，获得 ${result.value} 金币`);

        return { success: true, message: `成功收获！获得 ${result.value} 金币`, result };
    }

    waterPlot(plotId) {
        const plot = this.plots[plotId];
        if (plot.isOccupied && plot.crop) {
            plot.crop.water();
            return { success: true };
        }
        return { success: false };
    }

    fertilizePlot(plotId) {
        const plot = this.plots[plotId];
        if (plot.isOccupied && plot.crop) {
            if (this.player.gold < 20) {
                return { success: false, message: "金币不足" };
            }
            this.player.gold -= 20;
            plot.crop.fertilize();
            return { success: true };
        }
        return { success: false };
    }

    waterAll() {
        let count = 0;
        this.plots.forEach(plot => {
            if (this.waterPlot(plot.id).success) count++;
        });
        this.addLog(`💧 给 ${count} 块地浇水`);
        this.renderAll();
    }

    fertilizeAll() {
        const occupiedCount = this.plots.filter(p => p.isOccupied).length;
        const cost = occupiedCount * 20;

        if (this.player.gold < cost) {
            alert(`金币不足！需要 ${cost} 金币`);
            return;
        }

        let count = 0;
        this.plots.forEach(plot => {
            if (this.fertilizePlot(plot.id).success) count++;
        });

        this.addLog(`🌱 给 ${count} 块地施肥，花费 ${cost} 金币`);
        this.renderAll();
    }

    harvestAll() {
        let totalValue = 0;
        let count = 0;

        this.plots.forEach(plot => {
            if (plot.isOccupied && plot.crop && plot.crop.isHarvestable) {
                const result = this.harvestPlot(plot.id);
                if (result.success) {
                    totalValue += result.result.value;
                    count++;
                }
            }
        });

        if (count > 0) {
            this.addLog(`🎉 收获 ${count} 块地，总共获得 ${totalValue} 金币`);
        } else {
            this.addLog(`⚠️ 没有可收获的作物`);
        }

        this.renderAll();
    }

    // ==================== 时间推进 ====================
    advanceDay() {
        this.currentDate = new Date(this.currentDate.getTime() + 24 * 60 * 60 * 1000);
        this.gameDay++;

        // 更新所有作物
        this.plots.forEach(plot => {
            if (plot.isOccupied && plot.crop) {
                plot.crop.updateGrowth(this.currentDate);
                plot.crop.updateHealth();
            }
        });

        this.addLog(`📅 新的一天！第 ${this.gameDay} 天`);

        // 检查是否月底
        const tomorrow = new Date(this.currentDate.getTime() + 24 * 60 * 60 * 1000);
        if (tomorrow.getDate() === 1) {
            const settlement = this.settleMonth();
            this.showSettlement(settlement);
        }

        this.renderAll();
    }

    // ==================== 智能建议 ====================
    getPlantingSuggestions() {
        const monthEnd = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 0);
        const daysLeft = Math.floor((monthEnd - this.currentDate) / (1000 * 60 * 60 * 24));

        const suggestions = [];

        for (const [name, crop] of Object.entries(CROPS_DATABASE)) {
            if (crop.growthDays <= daysLeft) {
                const profit = crop.basePrice * crop.baseYield - crop.seedPrice;
                const roi = (profit / crop.seedPrice) * 100;
                const margin = daysLeft - crop.growthDays;

                suggestions.push({
                    name: name,
                    icon: crop.icon,
                    growthDays: crop.growthDays,
                    margin: margin,
                    profit: profit,
                    roi: roi,
                    score: margin * 2 + roi / 10
                });
            }
        }

        suggestions.sort((a, b) => b.score - a.score);
        return suggestions.slice(0, 5);
    }

    // ==================== UI渲染 ====================
    initUI() {
        // 渲染农场地块
        const farmGrid = document.getElementById('farm-grid');
        farmGrid.innerHTML = '';

        for (let i = 0; i < 9; i++) {
            const plotDiv = document.createElement('div');
            plotDiv.className = 'plot';
            plotDiv.id = `plot-${i}`;
            plotDiv.onclick = () => this.showPlotModal(i);
            farmGrid.appendChild(plotDiv);
        }

        // 渲染商店
        this.renderShop('all');

        // 绑定事件
        document.getElementById('advance-day-btn').onclick = () => this.advanceDay();
        document.getElementById('water-all-btn').onclick = () => this.waterAll();
        document.getElementById('fertilize-all-btn').onclick = () => this.fertilizeAll();
        document.getElementById('harvest-all-btn').onclick = () => this.harvestAll();
        document.getElementById('show-suggestions-btn').onclick = () => this.toggleSuggestions();

        // 商店过滤按钮
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.onclick = () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.renderShop(btn.dataset.category);
            };
        });

        // 模态窗口关闭
        document.querySelector('.close').onclick = () => {
            document.getElementById('plot-modal').style.display = 'none';
        };

        document.getElementById('close-settlement-btn').onclick = () => {
            document.getElementById('settlement-modal').style.display = 'none';
        };

        window.onclick = (event) => {
            const modal = document.getElementById('plot-modal');
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        };
    }

    renderAll() {
        this.renderPlayerInfo();
        this.renderTimeInfo();
        this.renderTargetInfo();
        this.renderFarm();
        this.renderFarmStats();
    }

    renderPlayerInfo() {
        document.getElementById('player-name').textContent = this.player.name;
        document.getElementById('player-level').textContent = this.player.level;
        document.getElementById('player-gold').textContent = this.player.gold;
        document.getElementById('player-diamond').textContent = this.player.diamond;
        document.getElementById('player-reputation').textContent = `${this.player.reputation}/100`;
    }

    renderTimeInfo() {
        const dateStr = `${this.currentDate.getFullYear()}年${this.currentDate.getMonth() + 1}月${this.currentDate.getDate()}日`;
        document.getElementById('game-date').textContent = dateStr;
        document.getElementById('game-day').textContent = `第 ${this.gameDay} 天`;
    }

    renderTargetInfo() {
        const target = this.monthlyTarget;
        const progress = this.checkTargetProgress();
        const monthEnd = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 0);
        const daysLeft = Math.floor((monthEnd - this.currentDate) / (1000 * 60 * 60 * 24));

        document.getElementById('target-description').textContent = target.description;
        document.getElementById('target-current').textContent = progress.current;
        document.getElementById('target-total').textContent = progress.total;
        document.getElementById('target-percent').textContent = Math.floor(progress.percent);
        document.getElementById('target-progress').style.width = `${progress.percent}%`;
        document.getElementById('days-remaining').textContent = daysLeft;
    }

    renderFarm() {
        this.plots.forEach((plot, i) => {
            const plotDiv = document.getElementById(`plot-${i}`);
            plotDiv.className = 'plot';

            if (plot.isOccupied && plot.crop) {
                plot.crop.updateGrowth(this.currentDate);

                if (plot.crop.isHarvestable) {
                    plotDiv.classList.add('harvestable');
                } else {
                    plotDiv.classList.add('occupied');
                }

                const daysLeft = plot.crop.getDaysUntilHarvest(this.currentDate);
                const statusText = plot.crop.isHarvestable ? '✅ 可收获' : `⏳ ${daysLeft}天`;

                plotDiv.innerHTML = `
                    <div class="plot-id">#${i}</div>
                    <div class="plot-content">
                        <div class="crop-icon">${plot.crop.icon}</div>
                        <div class="crop-name">${plot.crop.name}</div>
                        <div class="crop-status">${statusText}</div>
                        <div class="crop-status">💧${Math.floor(plot.crop.waterLevel)}%</div>
                    </div>
                `;
            } else {
                plotDiv.innerHTML = `
                    <div class="plot-id">#${i}</div>
                    <div class="plot-content">
                        <div class="plot-empty-text">点击种植</div>
                    </div>
                `;
            }
        });
    }

    renderFarmStats() {
        const occupied = this.plots.filter(p => p.isOccupied).length;
        const harvestable = this.plots.filter(p => p.isOccupied && p.crop && p.crop.isHarvestable).length;

        document.getElementById('occupied-plots').textContent = occupied;
        document.getElementById('harvestable-plots').textContent = harvestable;
    }

    renderShop(category) {
        const shopItems = document.getElementById('shop-items');
        shopItems.innerHTML = '';

        for (const [name, crop] of Object.entries(CROPS_DATABASE)) {
            if (category !== 'all' && crop.category !== category) continue;

            const itemDiv = document.createElement('div');
            itemDiv.className = `shop-item rarity-${crop.rarity}`;
            itemDiv.onclick = () => this.buyAndPlant(name);

            const profit = crop.basePrice * crop.baseYield - crop.seedPrice;
            const roi = ((profit / crop.seedPrice) * 100).toFixed(0);

            itemDiv.innerHTML = `
                <div class="shop-item-header">
                    <span class="shop-item-name">${name}</span>
                    <span class="shop-item-icon">${crop.icon}</span>
                </div>
                <div class="shop-item-info">
                    📅 ${crop.growthDays}天成熟 | 产量: ${crop.baseYield}<br>
                    💰 利润: ${profit}金币 | ROI: ${roi}%
                </div>
                <div class="shop-item-price">💰 ${crop.seedPrice} 金币</div>
            `;

            shopItems.appendChild(itemDiv);
        }
    }

    buyAndPlant(cropName) {
        // 找到第一个空地块
        const emptyPlot = this.plots.find(p => !p.isOccupied);
        if (!emptyPlot) {
            alert('没有空闲的地块了！');
            return;
        }

        const result = this.plantCrop(cropName, emptyPlot.id);
        if (result.success) {
            this.renderAll();
        } else {
            alert(result.message);
        }
    }

    toggleSuggestions() {
        const suggestionsDiv = document.getElementById('suggestions-list');

        if (suggestionsDiv.style.display === 'none') {
            const suggestions = this.getPlantingSuggestions();
            suggestionsDiv.innerHTML = '';

            suggestions.forEach((s, i) => {
                const div = document.createElement('div');
                div.className = 'suggestion-item';
                div.innerHTML = `
                    <strong>${i + 1}. ${s.icon} ${s.name}</strong><br>
                    生长: ${s.growthDays}天 | 余量: ${s.margin}天<br>
                    利润: ${s.profit}金币 | ROI: ${s.roi.toFixed(0)}%
                `;
                suggestionsDiv.appendChild(div);
            });

            suggestionsDiv.style.display = 'block';
        } else {
            suggestionsDiv.style.display = 'none';
        }
    }

    showPlotModal(plotId) {
        const plot = this.plots[plotId];
        const modal = document.getElementById('plot-modal');
        const modalBody = document.getElementById('modal-body');

        if (plot.isOccupied && plot.crop) {
            const daysLeft = plot.crop.getDaysUntilHarvest(this.currentDate);

            modalBody.innerHTML = `
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 64px;">${plot.crop.icon}</div>
                    <h3>${plot.crop.name}</h3>
                </div>
                <div class="info-item"><span>状态:</span> <span>${plot.crop.isHarvestable ? '✅ 可收获' : `⏳ 还需 ${daysLeft} 天`}</span></div>
                <div class="info-item"><span>健康度:</span> <span>${Math.floor(plot.crop.health)}%</span></div>
                <div class="info-item"><span>水分:</span> <span>${Math.floor(plot.crop.waterLevel)}%</span></div>
                <div class="info-item"><span>肥料:</span> <span>${Math.floor(plot.crop.fertilizerLevel)}%</span></div>
                <div class="info-item"><span>预计产量:</span> <span>${plot.crop.calculateYield()} 个</span></div>
                <div style="margin-top: 20px;">
                    ${plot.crop.isHarvestable ?
                        `<button class="btn btn-success" onclick="game.harvestPlot(${plotId}); game.renderAll(); document.getElementById('plot-modal').style.display='none';">🌾 收获</button>` :
                        `<button class="btn btn-action" onclick="game.waterPlot(${plotId}); game.renderAll(); document.getElementById('plot-modal').style.display='none';">💧 浇水</button>
                         <button class="btn btn-warning" onclick="game.fertilizePlot(${plotId}); game.renderAll(); document.getElementById('plot-modal').style.display='none';">🌱 施肥 (20金币)</button>`
                    }
                </div>
            `;
        } else {
            modalBody.innerHTML = `
                <p style="text-align: center; margin: 20px 0;">这是一块空地，选择一个作物种植吧！</p>
                <div id="plant-options"></div>
            `;

            const plantOptions = document.getElementById('plant-options');
            for (const [name, crop] of Object.entries(CROPS_DATABASE)) {
                const btn = document.createElement('button');
                btn.className = 'btn btn-info';
                btn.style.marginTop = '8px';
                btn.innerHTML = `${crop.icon} ${name} (${crop.seedPrice}金币)`;
                btn.onclick = () => {
                    this.plantCrop(name, plotId);
                    this.renderAll();
                    modal.style.display = 'none';
                };
                plantOptions.appendChild(btn);
            }
        }

        document.getElementById('modal-title').textContent = `地块 #${plotId}`;
        modal.style.display = 'block';
    }

    showSettlement(settlement) {
        const modal = document.getElementById('settlement-modal');
        const body = document.getElementById('settlement-body');

        body.innerHTML = `
            <div style="font-size: 24px; margin: 20px 0;">
                ${settlement.isCompleted ? '🎉' : '💔'}
            </div>
            <div style="white-space: pre-line; margin: 20px 0; line-height: 1.8;">
                ${settlement.message}
            </div>
        `;

        modal.style.display = 'block';
    }

    addLog(message) {
        const logContent = document.getElementById('log-content');
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        entry.textContent = message;
        logContent.insertBefore(entry, logContent.firstChild);

        // 保持最多20条日志
        while (logContent.children.length > 20) {
            logContent.removeChild(logContent.lastChild);
        }
    }
}

// 启动游戏
let game;
window.onload = () => {
    game = new GloriaMagicFarm();
    game.addLog('🎮 游戏开始！祝你玩得开心！');
};
