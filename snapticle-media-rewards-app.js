// State Management
let currentUser = null;
let userRewards = [];
let userHistory = [];

// Constants
const TIER_RULES = {
    BRONZE: { min: 0, max: 499, color: 'indigo' },
    SILVER: { min: 500, max: 1999, color: 'slate' },
    GOLD: { min: 2000, max: 4999, color: 'amber' },
    PLATINUM: { min: 5000, max: Infinity, color: 'purple' }
};

const SPIN_REWARDS = [
    { name: '5 Points', type: 'points', value: 5, icon: 'plus-circle' },
    { name: '10 Points', type: 'points', value: 10, icon: 'plus-circle' },
    { name: '20 Points', type: 'points', value: 20, icon: 'plus-circle' },
    { name: '25 Points', type: 'points', value: 25, icon: 'plus-circle' },
    { name: '30 Points', type: 'points', value: 30, icon: 'plus-circle' },
    { name: 'Free Sweet Dish', type: 'coupon', value: 'sweet-dish', icon: 'cake' },
    { name: 'Free Beverage', type: 'coupon', value: 'beverage', icon: 'coffee' },
    { name: '5% Discount', type: 'coupon', value: 'discount-5', icon: 'percent' },
    { name: 'Better Luck Next Time', type: 'luck', value: 0, icon: 'frown' }
];

// Initialize App
document.addEventListener('DOMContentLoaded', async () => {
    console.log("App Initializing...");
    
    try {
        // Check local storage for session
        const savedPhone = localStorage.getItem('loyalty_user_phone');
        console.log("Saved Phone:", savedPhone);
        
        if (savedPhone) {
            await loadUserData(savedPhone);
        } else {
            showOnboarding();
        }
    } catch (error) {
        console.error("Initialization Error:", error);
        showOnboarding();
    }
    
    initWheel();
    lucide.createIcons();
});

// Firebase Data Loading
async function loadUserData(phone) {
    try {
        if (typeof db === 'undefined') return;

        // Real-time listener for user document
        db.collection('customers').doc(phone).onSnapshot((doc) => {
            if (doc.exists) {
                currentUser = doc.data();
                localStorage.setItem('loyalty_user_phone', phone);
                showMainScreen();
                updateDashboard();
            } else {
                localStorage.removeItem('loyalty_user_phone');
                showOnboarding();
            }
        }, (error) => {
            console.error("Firestore error:", error);
            showOnboarding();
        });

        // Real-time listener for Rewards
        db.collection('customers').doc(phone).collection('rewards').onSnapshot((snapshot) => {
            userRewards = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
            if (document.getElementById('wallet-tab').classList.contains('hidden') === false) {
                renderRewards();
            }
        });

        // Real-time listener for History
        db.collection('customers').doc(phone).collection('history').orderBy('date', 'desc').limit(20).onSnapshot((snapshot) => {
            userHistory = snapshot.docs.map(doc => doc.data());
            if (document.getElementById('history-tab').classList.contains('hidden') === false) {
                renderHistory();
            }
        });

        checkExpirations();
    } catch (error) {
        console.error("Error loading user data:", error);
    }
}

// Navigation Functions
function showOnboarding() {
    document.getElementById('onboarding-screen').classList.remove('hidden');
    document.getElementById('app').classList.add('hidden');
}

function showMainScreen() {
    document.getElementById('onboarding-screen').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    document.getElementById('main-screen').classList.remove('hidden');
    
    if (currentUser) {
        document.getElementById('user-display-name').textContent = currentUser.name;
    }
}

function switchTab(tabId) {
    const tabs = ['dashboard', 'spin', 'wallet', 'redeem', 'history', 'profile'];
    tabs.forEach(t => {
        const el = document.getElementById(`${t}-tab`);
        if (el) el.classList.add('hidden');
        
        const navItem = document.getElementById(`nav-${t}`);
        if (navItem) {
            navItem.classList.remove('text-indigo-600');
            navItem.classList.add('text-gray-400');
        }
    });

    const activeTab = document.getElementById(`${tabId}-tab`);
    if (activeTab) activeTab.classList.remove('hidden');
    
    const activeNav = document.getElementById(`nav-${tabId}`);
    if (activeNav) {
        activeNav.classList.remove('text-gray-400');
        activeNav.classList.add('text-indigo-600');
    }

    if (tabId === 'wallet') renderRewards();
    if (tabId === 'history') renderHistory();
    if (tabId === 'spin') checkSpinAvailability();
}

function handleLogout() {
    if (confirm("Are you sure you want to logout?")) {
        localStorage.removeItem('loyalty_user_phone');
        location.reload();
    }
}

function calculateTier(points) {
    if (points >= 5000) return 'platinum';
    if (points >= 2000) return 'gold';
    if (points >= 500) return 'silver';
    return 'bronze';
}

function renderHistory() {
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = '';

    if (userHistory.length === 0) {
        historyList.innerHTML = '<div class="text-center py-10 text-gray-400">No history found</div>';
        return;
    }

    userHistory.forEach(item => {
        let icon = 'activity';
        let color = 'indigo';
        let title = '';
        let subtitle = '';
        let amount = '';

        if (item.type === 'redemption') {
            icon = 'shopping-bag';
            color = 'pink';
            title = 'Points Redeemed';
            subtitle = `Bill: ₹${item.billAmount}`;
            amount = `- ₹${item.discount}`;
        } else if (item.type === 'referral_bonus') {
            icon = 'share-2';
            color = 'green';
            title = 'Referral Bonus';
            subtitle = `${item.note || 'From Referral'}: ${item.fromUser}`;
            amount = `+ ${item.points} pts`;
        } else if (item.type === 'visit') {
            icon = 'map-pin';
            color = 'orange';
            title = 'Visit Verified';
            subtitle = 'Points earned for visit';
            amount = `+ ${item.points} pts`;
        } else if (item.type === 'reward_claim') {
            icon = 'gift';
            color = 'purple';
            title = 'Reward Claimed';
            subtitle = item.rewardName;
            amount = 'Used';
        }

        const date = new Date(item.date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });

        const html = `
            <div class="glass p-4 rounded-3xl flex items-center justify-between border-l-4 border-${color}-500">
                <div class="flex items-center space-x-4">
                    <div class="w-10 h-10 rounded-2xl bg-${color}-50 flex items-center justify-center text-${color}-600">
                        <i data-lucide="${icon}" class="w-5 h-5"></i>
                    </div>
                    <div>
                        <h4 class="font-bold text-gray-900 text-sm">${title}</h4>
                        <p class="text-[10px] text-gray-500">${subtitle} • ${date}</p>
                    </div>
                </div>
                <div class="text-right">
                    <p class="font-bold text-${color}-600 text-sm">${amount}</p>
                </div>
            </div>
        `;
        historyList.innerHTML += html;
    });

    lucide.createIcons();
}

function generateQR(containerId, text) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    new QRCode(container, {
        text: text,
        width: 128,
        height: 128,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    });
}

// Registration
async function handleRegistration() {
    const name = document.getElementById('reg-name').value;
    const phone = document.getElementById('reg-phone').value;
    const whatsapp = document.getElementById('reg-whatsapp').value;
    const email = document.getElementById('reg-email').value;
    const referralCode = document.getElementById('reg-referral').value;

    if (!name || !phone || !whatsapp) {
        alert('Please fill in all required fields');
        return;
    }

    const newUser = {
        name,
        phone,
        whatsapp,
        email,
        id: 'REST-' + Math.floor(1000 + Math.random() * 9000) + '-' + Math.floor(1000 + Math.random() * 9000),
        points: 50,
        lifetimePoints: 50,
        referredBy: referralCode || null,
        visits: 0,
        savings: 0,
        lastSpin: null,
        joinedAt: firebase.firestore.FieldValue.serverTimestamp()
    };

    try {
        await db.collection('customers').doc(phone).set(newUser);
        
        // Referral Signup Bonus for Referrer
        if (referralCode) {
            const referrerSnap = await db.collection('customers').where('id', '==', referralCode).get();
            if (!referrerSnap.empty) {
                const referrerDoc = referrerSnap.docs[0];
                await db.collection('customers').doc(referrerDoc.id).update({
                    points: firebase.firestore.FieldValue.increment(50),
                    lifetimePoints: firebase.firestore.FieldValue.increment(50)
                });
                
                await db.collection('customers').doc(referrerDoc.id).collection('history').add({
                    type: 'referral_bonus',
                    points: 50,
                    fromUser: name,
                    note: 'Referral Signup Bonus',
                    date: new Date().toISOString()
                });
            }
        }

        await loadUserData(phone);
    } catch (error) {
        console.error("Firebase Error:", error);
        alert("Registration failed: " + error.message);
    }
}

// Dashboard Logic
function updateDashboard() {
    if (!currentUser) return;
    
    const setSafeText = (id, text) => {
        const el = document.getElementById(id);
        if (el) el.textContent = text;
    };

    setSafeText('points-balance', currentUser.points.toLocaleString());
    setSafeText('membership-id', `ID: ${currentUser.id}`);
    setSafeText('lifetime-points', `${currentUser.lifetimePoints.toLocaleString()} pts`);
    setSafeText('visit-count', currentUser.visits);
    setSafeText('total-savings', `₹${currentUser.savings}`);
    setSafeText('wallet-points', currentUser.points.toLocaleString());
    setSafeText('available-points-calc', `${currentUser.points.toLocaleString()} pts`);

    // Tier Progress
    let currentTier = 'BRONZE';
    let nextTier = 'SILVER';
    let pointsToNext = 0;
    let progress = 0;

    if (currentUser.points >= 5000) {
        currentTier = 'PLATINUM';
        nextTier = 'MAX';
        progress = 100;
    } else if (currentUser.points >= 2000) {
        currentTier = 'GOLD';
        nextTier = 'PLATINUM';
        pointsToNext = 5000 - currentUser.points;
        progress = ((currentUser.points - 2000) / 3000) * 100;
    } else if (currentUser.points >= 500) {
        currentTier = 'SILVER';
        nextTier = 'GOLD';
        pointsToNext = 2000 - currentUser.points;
        progress = ((currentUser.points - 500) / 1500) * 100;
    } else {
        currentTier = 'BRONZE';
        nextTier = 'SILVER';
        pointsToNext = 500 - currentUser.points;
        progress = (currentUser.points / 500) * 100;
    }

    const tierBadge = document.getElementById('user-tier-badge');
    if (tierBadge) {
        tierBadge.innerHTML = currentTier;
    }

    setSafeText('membership-tier-name', `${currentTier.charAt(0) + currentTier.slice(1).toLowerCase()} Member`);
    setSafeText('membership-tier-name-display', currentTier.charAt(0) + currentTier.slice(1).toLowerCase());
    
    const progressBar = document.getElementById('tier-progress-bar');
    if (progressBar) {
        progressBar.style.width = `${progress}%`;
    }

    setSafeText('points-to-next', nextTier === 'MAX' ? 'Top Tier Reached!' : `${pointsToNext} pts to ${nextTier}`);
    
    lucide.createIcons();
}

// Spin Wheel Logic
let isSpinning = false;
let currentRotation = 0;

function initWheel() {
    const canvas = document.getElementById('wheel');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = canvas.width / 2 - 10;
    const angleStep = (2 * Math.PI) / SPIN_REWARDS.length;

    SPIN_REWARDS.forEach((reward, i) => {
        const startAngle = i * angleStep;
        const endAngle = (i + 1) * angleStep;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.fillStyle = i % 2 === 0 ? '#6366f1' : '#a855f7';
        ctx.fill();
        ctx.stroke();
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(startAngle + angleStep / 2);
        ctx.fillStyle = 'white';
        ctx.font = 'bold 10px sans-serif';
        ctx.textAlign = 'right';
        ctx.fillText(reward.name, radius - 15, 5);
        ctx.restore();
    });
}

function spinWheel() {
    if (isSpinning) return;
    const now = new Date().getTime();
    if (currentUser.lastSpin && now - currentUser.lastSpin < 24 * 60 * 60 * 1000) {
        alert('You can only spin once every 24 hours!');
        return;
    }
    isSpinning = true;
    const wheel = document.getElementById('wheel');
    const randomSpins = 5 + Math.floor(Math.random() * 5);
    const randomAngle = Math.floor(Math.random() * 360);
    currentRotation += randomSpins * 360 + randomAngle;
    wheel.style.transform = `rotate(${currentRotation}deg)`;
    setTimeout(async () => {
        isSpinning = false;
        const actualAngle = currentRotation % 360;
        const rewardIndex = Math.floor((360 - actualAngle) / (360 / SPIN_REWARDS.length)) % SPIN_REWARDS.length;
        const reward = SPIN_REWARDS[rewardIndex];
        await db.collection('customers').doc(currentUser.phone).update({ lastSpin: new Date().getTime() });
        await db.collection('events').add({ type: 'spin', timestamp: firebase.firestore.FieldValue.serverTimestamp(), reward: reward.name, phone: currentUser.phone });
        currentUser.lastSpin = new Date().getTime();
        if (reward.type !== 'luck') handleWin(reward);
        else alert('Better luck next time!');
        checkSpinAvailability();
    }, 4000);
}

async function handleWin(reward) {
    confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 }, colors: ['#6366f1', '#a855f7', '#ec4899'] });
    const newReward = { name: reward.name, type: reward.type, value: reward.value, icon: reward.icon, earnedDate: new Date().toISOString(), expiryDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(), status: 'active' };
    if (reward.type === 'points') {
        const newPoints = currentUser.points + reward.value;
        const newLifetime = currentUser.lifetimePoints + reward.value;
        await db.collection('customers').doc(currentUser.phone).update({ points: newPoints, lifetimePoints: newLifetime });
        currentUser.points = newPoints;
        currentUser.lifetimePoints = newLifetime;
        updateDashboard();
    }
    const rewardRef = await db.collection('customers').doc(currentUser.phone).collection('rewards').add(newReward);
    newReward.id = rewardRef.id;
    userRewards.push(newReward);
    showRewardModal(newReward);
}

function showRewardModal(reward) {
    const modal = document.getElementById('reward-modal');
    document.getElementById('modal-reward-name').textContent = reward.name;
    document.getElementById('modal-reward-icon').setAttribute('data-lucide', reward.icon);
    document.getElementById('modal-reward-code').textContent = reward.id.substring(0, 8).toUpperCase();
    document.getElementById('modal-reward-title').textContent = "You've won a reward!";
    generateQR('modal-qr-container', reward.id);
    modal.classList.remove('hidden');
    lucide.createIcons();
}

function closeModal() { document.getElementById('reward-modal').classList.add('hidden'); }

function checkSpinAvailability() {
    const timerEl = document.getElementById('spin-timer');
    const btn = document.getElementById('spin-btn');
    const countdownEl = document.getElementById('countdown');
    if (!currentUser.lastSpin) { timerEl.classList.add('hidden'); btn.disabled = false; btn.classList.remove('opacity-50'); return; }
    const now = new Date().getTime();
    const timeLeft = (24 * 60 * 60 * 1000) - (now - currentUser.lastSpin);
    if (timeLeft > 0) {
        timerEl.classList.remove('hidden'); btn.disabled = true; btn.classList.add('opacity-50');
        const hours = Math.floor(timeLeft / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
        countdownEl.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        setTimeout(checkSpinAvailability, 1000);
    } else { timerEl.classList.add('hidden'); btn.disabled = false; btn.classList.remove('opacity-50'); }
}

function renderRewards() {
    const activeList = document.getElementById('active-rewards-list');
    const expiredList = document.getElementById('expired-rewards-list');
    activeList.innerHTML = ''; expiredList.innerHTML = '';
    const activeRewards = userRewards.filter(r => r.status === 'active');
    const expiredRewards = userRewards.filter(r => r.status === 'expired');
    if (activeRewards.length === 0) activeList.innerHTML = '<div class="text-center py-10 text-gray-400">No active rewards found</div>';
    activeRewards.forEach(reward => {
        const expiryDate = new Date(reward.expiryDate);
        const daysLeft = Math.ceil((expiryDate - new Date()) / (1000 * 60 * 60 * 24));
        activeList.innerHTML += `<div class="glass p-5 rounded-3xl relative overflow-hidden border-l-4 border-indigo-500"><div class="flex justify-between items-start"><div class="flex space-x-4"><div class="w-12 h-12 rounded-2xl bg-indigo-50 flex items-center justify-center text-indigo-600"><i data-lucide="${reward.icon}" class="w-6 h-6"></i></div><div><h4 class="font-bold text-gray-900">${reward.name}</h4><p class="text-[10px] text-gray-500 uppercase tracking-wider">Expires in ${daysLeft} days</p></div></div><button onclick="redeemReward('${reward.id}')" class="px-4 py-2 bg-gray-900 text-white rounded-xl text-xs font-bold">Redeem</button></div></div>`;
    });
    expiredRewards.forEach(reward => {
        expiredList.innerHTML += `<div class="glass p-5 rounded-3xl opacity-60 grayscale"><div class="flex justify-between items-center"><div class="flex space-x-4"><div class="w-12 h-12 rounded-2xl bg-gray-100 flex items-center justify-center text-gray-400"><i data-lucide="${reward.icon}" class="w-6 h-6"></i></div><div><h4 class="font-bold text-gray-900">${reward.name}</h4><p class="text-[10px] text-red-500 uppercase tracking-wider">Expired</p></div></div></div></div>`;
    });
    lucide.createIcons();
}

function toggleWalletTab(type) {
    const btnActive = document.getElementById('btn-active-rewards'); const btnExpired = document.getElementById('btn-expired-rewards');
    const listActive = document.getElementById('active-rewards-list'); const listExpired = document.getElementById('expired-rewards-list');
    if (type === 'active') { btnActive.classList.add('bg-white', 'shadow-sm', 'text-indigo-600'); btnActive.classList.remove('text-gray-500'); btnExpired.classList.remove('bg-white', 'shadow-sm', 'text-indigo-600'); btnExpired.classList.add('text-gray-500'); listActive.classList.remove('hidden'); listExpired.classList.add('hidden'); }
    else { btnExpired.classList.add('bg-white', 'shadow-sm', 'text-indigo-600'); btnExpired.classList.remove('text-gray-500'); btnActive.classList.remove('bg-white', 'shadow-sm', 'text-indigo-600'); btnActive.classList.add('text-gray-500'); listExpired.classList.remove('hidden'); listActive.classList.add('hidden'); }
}

async function checkExpirations() {
    let changed = false; const now = new Date();
    for (let reward of userRewards) {
        if (reward.status === 'active' && new Date(reward.expiryDate) < now) {
            reward.status = 'expired'; await db.collection('customers').doc(currentUser.phone).collection('rewards').doc(reward.id).update({ status: 'expired' });
            changed = true;
        }
    }
    if (changed) renderRewards();
}

function calculateRedemption() {
    const bill = parseFloat(document.getElementById('bill-amount').value) || 0;
    const maxDiscount = bill * 0.20;
    const availableDiscountFromPoints = currentUser.points; 
    const actualDiscount = Math.min(maxDiscount, availableDiscountFromPoints);
    const pointsToUse = actualDiscount;
    const finalBill = bill - actualDiscount;
    document.getElementById('max-discount').textContent = `₹${maxDiscount.toFixed(2)}`;
    document.getElementById('points-to-use').textContent = `${Math.floor(pointsToUse)} pts`;
    document.getElementById('discount-value').textContent = `- ₹${actualDiscount.toFixed(2)}`;
    document.getElementById('final-bill').textContent = `₹${finalBill.toFixed(2)}`;
}

async function redeemPoints() {
    const bill = parseFloat(document.getElementById('bill-amount').value) || 0;
    if (bill <= 0) return alert('Please enter a valid bill amount');
    const maxDiscount = bill * 0.20; const availableDiscountFromPoints = currentUser.points;
    const actualDiscount = Math.min(maxDiscount, availableDiscountFromPoints);
    const pointsToUse = Math.floor(actualDiscount);
    if (pointsToUse <= 0) return alert('No points available for discount');
    if (confirm(`Confirm redemption of ${pointsToUse} points for ₹${actualDiscount.toFixed(2)} discount?`)) {
        const newPoints = currentUser.points - pointsToUse; const newSavings = currentUser.savings + pointsToUse;
        const historyItem = { type: 'redemption', points: pointsToUse, discount: actualDiscount, billAmount: bill, date: new Date().toISOString() };
        await db.collection('customers').doc(currentUser.phone).update({ points: newPoints, savings: newSavings });
        await db.collection('customers').doc(currentUser.phone).collection('history').add(historyItem);
        if (currentUser.referredBy) {
            const referralPoints = Math.floor(bill * 0.10);
            if (referralPoints > 0) {
                const referrerSnap = await db.collection('customers').where('id', '==', currentUser.referredBy).get();
                if (!referrerSnap.empty) {
                    const referrerDoc = referrerSnap.docs[0];
                    await db.collection('customers').doc(referrerDoc.id).update({ points: firebase.firestore.FieldValue.increment(referralPoints), lifetimePoints: firebase.firestore.FieldValue.increment(referralPoints) });
                    await db.collection('customers').doc(referrerDoc.id).collection('history').add({ type: 'referral_bonus', points: referralPoints, fromUser: currentUser.name, date: new Date().toISOString() });
                }
            }
        }
        currentUser.points = newPoints; currentUser.savings = newSavings; userHistory.unshift(historyItem);
        updateDashboard(); alert('Redemption successful!'); switchTab('dashboard');
        document.getElementById('bill-amount').value = ''; calculateRedemption();
    }
}

async function redeemReward(rewardId) {
    const reward = userRewards.find(r => r.id === rewardId);
    if (reward) {
        if (confirm(`Redeem "${reward.name}"? This will mark it as used.`)) {
            await db.collection('customers').doc(currentUser.phone).collection('rewards').doc(rewardId).update({ status: 'redeemed' });
            const historyItem = { type: 'reward_claim', rewardName: reward.name, date: new Date().toISOString() };
            await db.collection('customers').doc(currentUser.phone).collection('history').add(historyItem);
            reward.status = 'redeemed'; userHistory.unshift(historyItem);
            renderRewards(); alert('Reward redeemed successfully!');
        }
    }
}

function showVerificationQR() {
    const modal = document.getElementById('reward-modal'); 
    document.getElementById('modal-reward-name').textContent = "Verify Visit";
    document.getElementById('modal-reward-desc').textContent = "Show this ID to the restaurant staff to verify your visit and earn points.";
    document.getElementById('modal-reward-icon').setAttribute('data-lucide', 'qr-code');
    document.getElementById('modal-reward-code').textContent = currentUser.id;
    document.getElementById('modal-reward-title').textContent = "Verification QR";
    generateQR('modal-qr-container', currentUser.id);
    modal.classList.remove('hidden');
    lucide.createIcons();
}