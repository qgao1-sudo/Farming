// Gloria's Magic Farm - English Version
// Kairosoft-style Farming Game

// ==================== CROPS DATABASE ====================
const CROPS_DATABASE = {
    "Wheat": {
        name: "Wheat",
        icon: "🌾",
        seedPrice: 10,
        growthDays: 2,
        baseYield: 30,
        basePrice: 5,
        season: ["Spring", "Fall"],
        category: "vegetable",
        rarity: "common",
        description: "Fast growth, perfect for quantity goals"
    },
    "Tomato": {
        name: "Tomato",
        icon: "🍅",
        seedPrice: 30,
        growthDays: 4,
        baseYield: 10,
        basePrice: 15,
        season: ["Summer"],
        category: "fruit",
        rarity: "common",
        description: "High price, great for income goals"
    },
    "Rainbow Daisy": {
        name: "Rainbow Daisy",
        icon: "🌸",
        seedPrice: 100,
        growthDays: 6,
        baseYield: 5,
        basePrice: 50,
        season: ["Spring"],
        category: "flower",
        rarity: "rare",
        description: "Flower for diversity goals"
    },
    "Golden Pumpkin": {
        name: "Golden Pumpkin",
        icon: "🎃",
        seedPrice: 200,
        growthDays: 8,
        baseYield: 1,
        basePrice: 300,
        season: ["Fall"],
        category: "special",
        rarity: "epic",
        description: "Rare crop for miracle goals"
    },
    "Carrot": {
        name: "Carrot",
        icon: "🥕",
        seedPrice: 15,
        growthDays: 3,
        baseYield: 20,
        basePrice: 8,
        season: ["Spring", "Fall", "Winter"],
        category: "vegetable",
        rarity: "common",
        description: "Hardy, grows in three seasons"
    },
    "Strawberry": {
        name: "Strawberry",
        icon: "🍓",
        seedPrice: 50,
        growthDays: 5,
        baseYield: 15,
        basePrice: 20,
        season: ["Spring", "Summer"],
        category: "fruit",
        rarity: "common",
        description: "Sweet and popular"
    },
    "Lavender": {
        name: "Lavender",
        icon: "💜",
        seedPrice: 80,
        growthDays: 7,
        baseYield: 8,
        basePrice: 45,
        season: ["Summer"],
        category: "flower",
        rarity: "rare",
        description: "Purple romance, aromatherapy"
    },
    "Blueberry": {
        name: "Blueberry",
        icon: "🫐",
        seedPrice: 60,
        growthDays: 6,
        baseYield: 12,
        basePrice: 25,
        season: ["Summer", "Fall"],
        category: "fruit",
        rarity: "rare",
        description: "Rich in antioxidants"
    },
    "Sunflower": {
        name: "Sunflower",
        icon: "🌻",
        seedPrice: 40,
        growthDays: 5,
        baseYield: 10,
        basePrice: 18,
        season: ["Summer"],
        category: "flower",
        rarity: "common",
        description: "Symbol of sunshine"
    },
    "Crystal Grape": {
        name: "Crystal Grape",
        icon: "🍇",
        seedPrice: 300,
        growthDays: 10,
        baseYield: 3,
        basePrice: 400,
        season: ["Summer", "Fall"],
        category: "special",
        rarity: "legendary",
        description: "Legendary miracle crop"
    },
    "Rose": {
        name: "Rose",
        icon: "🌹",
        seedPrice: 120,
        growthDays: 8,
        baseYield: 6,
        basePrice: 60,
        season: ["Spring", "Summer"],
        category: "flower",
        rarity: "rare",
        description: "Symbol of love"
    },
    "Radish": {
        name: "Radish",
        icon: "🥬",
        seedPrice: 12,
        growthDays: 3,
        baseYield: 25,
        basePrice: 6,
        season: ["Fall", "Winter"],
        category: "vegetable",
        rarity: "common",
        description: "Winter staple vegetable"
    },
    "Magic Mushroom": {
        name: "Magic Mushroom",
        icon: "🍄",
        seedPrice: 250,
        growthDays: 9,
        baseYield: 2,
        basePrice: 350,
        season: ["Fall"],
        category: "special",
        rarity: "epic",
        description: "Glows under moonlight"
    },
    "Cherry Blossom": {
        name: "Cherry Blossom",
        icon: "🌸",
        seedPrice: 500,
        growthDays: 15,
        baseYield: 1,
        basePrice: 800,
        season: ["Spring"],
        category: "special",
        rarity: "legendary",
        description: "Beautiful when blooming"
    }
};

// Quality names
const QUALITY_NAMES = {
    "normal": "Normal",
    "good": "Good",
    "excellent": "Excellent",
    "perfect": "Perfect"
};

// ==================== CROP CLASS ====================
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

// ==================== GAME CLASS ====================
class GloriaMagicFarm {
    constructor() {
        // Player data
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

        // Game time
        this.currentDate = new Date(2024, 4, 1); // May 1st
        this.gameDay = 1;

        // Farm
        this.plots = Array(9).fill(null).map((_, i) => ({
            id: i,
            crop: null,
            isOccupied: false
        }));

        // Monthly target
        this.monthlyTarget = this.generateMonthlyTarget();

        // Initialize UI
        this.initUI();
        this.renderAll();
    }

    // ==================== MONTHLY TARGET ====================
    generateMonthlyTarget() {
        const types = ["harvest", "sell"];
        const type = types[Math.floor(Math.random() * types.length)];

        let target = { type: type };

        if (type === "harvest") {
            const crops = ["Wheat", "Carrot", "Tomato"];
            const crop = crops[Math.floor(Math.random() * crops.length)];
            const amount = Math.floor(Math.random() * 200) + 200;

            target.crop = crop;
            target.value = amount;
            target.description = `Harvest ${amount} ${crop}`;
            target.reward = { gold: amount * 10, diamond: 5, reputation: 10 };
        } else if (type === "sell") {
            const amount = Math.floor(Math.random() * 5000) + 5000;
            target.value = amount;
            target.description = `Earn ${amount} gold in a single day`;
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
            message = `🎉 CONGRATULATIONS!\nYou completed this month's goal!\n\n💰 Gold: +${this.monthlyTarget.reward.gold}\n💎 Gems: +${this.monthlyTarget.reward.diamond}\n⭐ Fame: +${this.monthlyTarget.reward.reputation}`;

            this.player.gold += this.monthlyTarget.reward.gold;
            this.player.diamond += this.monthlyTarget.reward.diamond;
            this.player.reputation = Math.min(100, this.player.reputation + this.monthlyTarget.reward.reputation);
        } else {
            message = `💔 GOAL FAILED\n\nTarget: ${this.monthlyTarget.description}\nProgress: ${progress.current}/${progress.total}\n\n💸 Penalty: -500 gold\n📉 Fame: -20`;

            this.player.gold = Math.max(0, this.player.gold - 500);
            this.player.reputation = Math.max(0, this.player.reputation - 20);
        }

        // Reset monthly stats
        this.player.cropsHarvested = {};
        this.player.maxDailySale = 0;

        // Generate new target
        this.monthlyTarget = this.generateMonthlyTarget();

        return { isCompleted, message };
    }

    // ==================== FARM OPERATIONS ====================
    plantCrop(cropName, plotId) {
        const cropData = CROPS_DATABASE[cropName];
        if (!cropData) {
            return { success: false, message: `Crop not found: ${cropName}` };
        }

        if (this.player.gold < cropData.seedPrice) {
            return { success: false, message: `Not enough gold! Need ${cropData.seedPrice}g` };
        }

        const plot = this.plots[plotId];
        if (plot.isOccupied) {
            return { success: false, message: "Plot already occupied" };
        }

        this.player.gold -= cropData.seedPrice;
        const crop = new Crop(cropData, this.currentDate, plotId);
        plot.crop = crop;
        plot.isOccupied = true;

        this.player.plantedVariety[cropData.category].add(cropName);

        this.addLog(`✅ Planted ${cropName} on plot ${plotId}`);
        return { success: true, message: `Planted ${cropName}!` };
    }

    harvestPlot(plotId) {
        const plot = this.plots[plotId];
        if (!plot.isOccupied || !plot.crop) {
            return { success: false, message: "No crop on this plot" };
        }

        if (!plot.crop.isHarvestable) {
            return { success: false, message: "Crop not ready yet" };
        }

        const result = plot.crop.harvest();
        if (!result) {
            return { success: false, message: "Harvest failed" };
        }

        // Record harvest
        if (!this.player.cropsHarvested[result.cropName]) {
            this.player.cropsHarvested[result.cropName] = 0;
        }
        this.player.cropsHarvested[result.cropName] += result.quantity;

        // Gain gold
        this.player.gold += result.value;

        // Record sales
        if (result.value > this.player.maxDailySale) {
            this.player.maxDailySale = result.value;
        }

        // Clear plot
        plot.crop = null;
        plot.isOccupied = false;

        this.addLog(`🌾 Harvested ${result.quantity} ${QUALITY_NAMES[result.quality]} ${result.cropName} (+${result.value}g)`);

        return { success: true, message: `Harvested! +${result.value}g`, result };
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
                return { success: false, message: "Not enough gold" };
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
        this.addLog(`💧 Watered ${count} plots`);
        this.renderAll();
    }

    fertilizeAll() {
        const occupiedCount = this.plots.filter(p => p.isOccupied).length;
        const cost = occupiedCount * 20;

        if (this.player.gold < cost) {
            alert(`Not enough gold! Need ${cost}g`);
            return;
        }

        let count = 0;
        this.plots.forEach(plot => {
            if (this.fertilizePlot(plot.id).success) count++;
        });

        this.addLog(`🌱 Fertilized ${count} plots (-${cost}g)`);
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
            this.addLog(`🎉 Harvested ${count} plots! Total: +${totalValue}g`);
        } else {
            this.addLog(`⚠️ No crops ready to harvest`);
        }

        this.renderAll();
    }

    // ==================== TIME ADVANCE ====================
    advanceDay() {
        this.currentDate = new Date(this.currentDate.getTime() + 24 * 60 * 60 * 1000);
        this.gameDay++;

        // Update all crops
        this.plots.forEach(plot => {
            if (plot.isOccupied && plot.crop) {
                plot.crop.updateGrowth(this.currentDate);
                plot.crop.updateHealth();
            }
        });

        this.addLog(`📅 New day! Day ${this.gameDay}`);

        // Check for month end
        const tomorrow = new Date(this.currentDate.getTime() + 24 * 60 * 60 * 1000);
        if (tomorrow.getDate() === 1) {
            const settlement = this.settleMonth();
            this.showSettlement(settlement);
        }

        this.renderAll();
    }

    // ==================== PLANTING SUGGESTIONS ====================
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

    // ==================== UI RENDERING ====================
    initUI() {
        // Render farm plots
        const farmGrid = document.getElementById('farm-grid');
        farmGrid.innerHTML = '';

        for (let i = 0; i < 9; i++) {
            const plotDiv = document.createElement('div');
            plotDiv.className = 'plot';
            plotDiv.id = `plot-${i}`;
            plotDiv.onclick = () => this.showPlotModal(i);
            farmGrid.appendChild(plotDiv);
        }

        // Render shop
        this.renderShop('all');

        // Bind events
        document.getElementById('advance-day-btn').onclick = () => this.advanceDay();
        document.getElementById('water-all-btn').onclick = () => this.waterAll();
        document.getElementById('fertilize-all-btn').onclick = () => this.fertilizeAll();
        document.getElementById('harvest-all-btn').onclick = () => this.harvestAll();
        document.getElementById('show-suggestions-btn').onclick = () => this.toggleSuggestions();

        // Shop filters
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.onclick = () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.renderShop(btn.dataset.category);
            };
        });

        // Modal close
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
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        const dateStr = `${months[this.currentDate.getMonth()]} ${this.currentDate.getDate()}, ${this.currentDate.getFullYear()}`;
        document.getElementById('game-date').textContent = dateStr;
        document.getElementById('game-day').textContent = `Day ${this.gameDay}`;
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

        const progressBar = document.getElementById('target-progress');
        progressBar.style.width = `${progress.percent}%`;
        progressBar.querySelector('.progress-text').textContent = `${Math.floor(progress.percent)}%`;

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
                const statusText = plot.crop.isHarvestable ? '✅ READY' : `⏳ ${daysLeft}d`;

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
                        <div class="plot-empty-text">CLICK TO<br>PLANT</div>
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
                    📅 ${crop.growthDays} days | Yield: ${crop.baseYield}<br>
                    💰 Profit: ${profit}g | ROI: ${roi}%
                </div>
                <div class="shop-item-price">💰 ${crop.seedPrice} GOLD</div>
            `;

            shopItems.appendChild(itemDiv);
        }
    }

    buyAndPlant(cropName) {
        const emptyPlot = this.plots.find(p => !p.isOccupied);
        if (!emptyPlot) {
            alert('No empty plots available!');
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

            if (suggestions.length === 0) {
                suggestionsDiv.innerHTML = '<div class="suggestion-item">⚠️ No crops can be harvested before month end!</div>';
            } else {
                suggestions.forEach((s, i) => {
                    const div = document.createElement('div');
                    div.className = 'suggestion-item';
                    div.innerHTML = `
                        <strong>${i + 1}. ${s.icon} ${s.name}</strong><br>
                        Growth: ${s.growthDays}d | Margin: ${s.margin}d<br>
                        Profit: ${s.profit}g | ROI: ${s.roi.toFixed(0)}%
                    `;
                    suggestionsDiv.appendChild(div);
                });
            }

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
                <div class="stat-row"><span class="stat-label">Status:</span> <span class="stat-value">${plot.crop.isHarvestable ? '✅ READY' : `⏳ ${daysLeft} days left`}</span></div>
                <div class="stat-row"><span class="stat-label">Health:</span> <span class="stat-value">${Math.floor(plot.crop.health)}%</span></div>
                <div class="stat-row"><span class="stat-label">Water:</span> <span class="stat-value">${Math.floor(plot.crop.waterLevel)}%</span></div>
                <div class="stat-row"><span class="stat-label">Fertilizer:</span> <span class="stat-value">${Math.floor(plot.crop.fertilizerLevel)}%</span></div>
                <div class="stat-row"><span class="stat-label">Est. Yield:</span> <span class="stat-value">${plot.crop.calculateYield()} units</span></div>
                <div style="margin-top: 20px;">
                    ${plot.crop.isHarvestable ?
                        `<button class="pixel-btn btn-yellow" onclick="game.harvestPlot(${plotId}); game.renderAll(); document.getElementById('plot-modal').style.display='none';">🌾 HARVEST</button>` :
                        `<button class="pixel-btn btn-blue" onclick="game.waterPlot(${plotId}); game.renderAll(); document.getElementById('plot-modal').style.display='none';">💧 WATER</button>
                         <button class="pixel-btn btn-green" onclick="game.fertilizePlot(${plotId}); game.renderAll(); document.getElementById('plot-modal').style.display='none';">🌱 FERTILIZE (20g)</button>`
                    }
                </div>
            `;
        } else {
            modalBody.innerHTML = `
                <p style="text-align: center; margin: 20px 0; font-size: 12px;">Empty plot! Choose a crop to plant:</p>
                <div id="plant-options"></div>
            `;

            const plantOptions = document.getElementById('plant-options');
            for (const [name, crop] of Object.entries(CROPS_DATABASE)) {
                const btn = document.createElement('button');
                btn.className = 'pixel-btn btn-info';
                btn.style.marginTop = '8px';
                btn.innerHTML = `${crop.icon} ${name} (${crop.seedPrice}g)`;
                btn.onclick = () => {
                    this.plantCrop(name, plotId);
                    this.renderAll();
                    modal.style.display = 'none';
                };
                plantOptions.appendChild(btn);
            }
        }

        document.getElementById('modal-title').textContent = `PLOT #${plotId}`;
        modal.style.display = 'block';
    }

    showSettlement(settlement) {
        const modal = document.getElementById('settlement-modal');
        const body = document.getElementById('settlement-body');

        body.innerHTML = `
            <div style="font-size: 48px; margin: 20px 0;">
                ${settlement.isCompleted ? '🎉' : '💔'}
            </div>
            <div style="white-space: pre-line; line-height: 2;">
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

        // Keep max 20 logs
        while (logContent.children.length > 20) {
            logContent.removeChild(logContent.lastChild);
        }
    }
}

// Start the game
let game;
window.onload = () => {
    game = new GloriaMagicFarm();
    game.addLog('🎮 Welcome to Gloria\'s Magic Farm!');
    game.addLog('💡 Plant crops and complete monthly goals!');
};
