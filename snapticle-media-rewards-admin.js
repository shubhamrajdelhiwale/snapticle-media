// Admin State Management
let adminCustomers = [];
let adminSettings = {
    secretCode: '1234',
    pointValue: 10,
    maxDiscount: 20,
    restaurantName: ''
};

// Initialize Admin App
document.addEventListener('DOMContentLoaded', async () => {
    lucide.createIcons();
    await fetchSettings();
    
    // Check if already authenticated for this session
    if (sessionStorage.getItem('admin_authenticated') === 'true') {
        showAdminDashboard();
    }
});

async function fetchSettings() {
    if (typeof db === 'undefined') return;
    try {
        const settingsDoc = await db.collection('settings').doc('business').get();
        if (settingsDoc.exists) {
            const data = settingsDoc.data();
            adminSettings = {
                secretCode: data.secretCode || '1234',
                pointValue: data.pointValue || 10,
                maxDiscount: data.maxDiscount || 20,
                restaurantName: data.restaurantName || ''
            };
        }
    } catch (error) {
        console.error("Error fetching settings:", error);
    }
}

function handleAdminLogin() {
    const code = document.getElementById('admin-login-code').value;
    if (code === adminSettings.secretCode) {
        sessionStorage.setItem('admin_authenticated', 'true');
        showAdminDashboard();
    } else {
        alert("Invalid Secret Code!");
    }
}

async function showAdminDashboard() {
    document.getElementById('admin-login-overlay').classList.add('hidden');
    document.getElementById('admin-screen').classList.remove('hidden');
    
    // Update Date
    const dateEl = document.getElementById('admin-current-date');
    if (dateEl) {
        dateEl.textContent = new Date().toLocaleDateString('en-US', { 
            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
        });
    }

    // Load Data & Listeners
    db.collection('customers').onSnapshot((snapshot) => {
        adminCustomers = snapshot.docs.map(doc => doc.data());
        updateOverviewStats();
        fetchRecentRedemptions();
        if (!document.getElementById('admin-customers').classList.contains('hidden')) {
            renderCustomers();
        }
    });

    // Daily Spins (Today only)
    const today = new Date();
    today.setHours(0,0,0,0);
    db.collection('events')
        .where('type', '==', 'spin')
        .where('timestamp', '>=', today)
        .onSnapshot((snapshot) => {
            const el = document.getElementById('stat-daily-spins');
            if (el) el.textContent = snapshot.size.toLocaleString();
        });

    initCharts();
    
    // Fill Config Fields
    if (document.getElementById('config-point-value')) {
        document.getElementById('config-point-value').value = adminSettings.pointValue;
        document.getElementById('config-max-discount').value = adminSettings.maxDiscount;
        document.getElementById('settings-name').value = adminSettings.restaurantName;
        document.getElementById('settings-secret').value = adminSettings.secretCode;
    }
}

window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024) {
        const sidebar = document.getElementById('admin-sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        if (sidebar) sidebar.classList.remove('-translate-x-full');
        if (overlay) overlay.classList.add('hidden');
    } else {
        const sidebar = document.getElementById('admin-sidebar');
        if (sidebar) sidebar.classList.add('-translate-x-full');
    }
});

function toggleMobileSidebar() {
    const sidebar = document.getElementById('admin-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const isHidden = sidebar.classList.contains('-translate-x-full');

    if (isHidden) {
        sidebar.classList.remove('-translate-x-full');
        overlay.classList.remove('hidden');
    } else {
        sidebar.classList.add('-translate-x-full');
        overlay.classList.add('hidden');
    }
}

function switchAdminTab(tabId) {
    // Close sidebar on mobile after selection
    if (window.innerWidth < 1024) {
        toggleMobileSidebar();
    }
    const sections = ['overview', 'customers', 'rewards', 'analytics', 'settings'];
    sections.forEach(s => {
        const el = document.getElementById(`admin-${s}`);
        if (el) el.classList.add('hidden');
        const nav = document.getElementById(`nav-${s}`);
        if (nav) nav.classList.remove('bg-indigo-600', 'text-white');
    });

    document.getElementById(`admin-${tabId}`).classList.remove('hidden');
    document.getElementById(`nav-${tabId}`).classList.add('bg-indigo-600', 'text-white');
    document.getElementById('admin-page-title').textContent = tabId.charAt(0).toUpperCase() + tabId.slice(1);
    
    if (tabId === 'customers') renderCustomers();
    lucide.createIcons();
}

function updateOverviewStats() {
    const totalMembersEl = document.getElementById('stat-total-members');
    const redeemedEl = document.getElementById('stat-points-redeemed');
    const retentionEl = document.getElementById('stat-retention');

    if (totalMembersEl) totalMembersEl.textContent = adminCustomers.length.toLocaleString();
    
    const redeemed = adminCustomers.reduce((acc, c) => acc + (c.savings || 0), 0);
    if (redeemedEl) redeemedEl.textContent = `₹${redeemed.toLocaleString()}`;
    
    const repeats = adminCustomers.filter(c => c.visits > 1).length;
    const rate = adminCustomers.length > 0 ? Math.round((repeats / adminCustomers.length) * 100) : 0;
    if (retentionEl) retentionEl.textContent = `${rate}%`;
}

async function fetchRecentRedemptions() {
    const tableBody = document.getElementById('recent-redemptions-table');
    if (!tableBody) return;
    
    let allHistory = [];
    for (let c of adminCustomers.slice(0, 20)) {
        const snap = await db.collection('customers').doc(c.phone).collection('history')
            .where('type', '==', 'redemption')
            .limit(5)
            .get();
        snap.forEach(doc => allHistory.push({ ...doc.data(), customerName: c.name }));
    }
    
    allHistory.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    tableBody.innerHTML = allHistory.slice(0, 5).map(h => `
        <tr class="hover:bg-slate-50 transition-colors">
            <td class="px-8 py-6">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center text-slate-900 font-black text-xs">${h.customerName.charAt(0)}</div>
                    <span class="font-bold text-slate-900">${h.customerName}</span>
                </div>
            </td>
            <td class="px-8 py-6 font-black text-slate-900">₹${h.discount}</td>
            <td class="px-8 py-6 text-sm text-slate-500 font-medium">${new Date(h.date).toLocaleDateString()}</td>
            <td class="px-8 py-6">
                <span class="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest bg-green-50 text-green-600 border border-green-100">Completed</span>
            </td>
        </tr>
    `).join('');
}

function renderCustomers() {
    const tableBody = document.getElementById('customer-list-table');
    if (!tableBody) return;
    
    const searchTerm = document.getElementById('customer-search')?.value.toLowerCase() || '';
    const filtered = adminCustomers.filter(c => 
        c.name.toLowerCase().includes(searchTerm) || 
        c.phone.includes(searchTerm)
    );

    tableBody.innerHTML = filtered.map(c => `
        <tr class="hover:bg-slate-50 transition-colors">
            <td class="px-8 py-6">
                <div class="flex items-center space-x-4">
                    <div class="w-12 h-12 rounded-2xl bg-slate-100 flex items-center justify-center text-slate-900 font-black text-sm border border-slate-200">${c.name.charAt(0)}</div>
                    <div>
                        <p class="font-black text-slate-900 tracking-tight">${c.name}</p>
                        <p class="text-xs text-slate-500 font-medium">${c.phone}</p>
                    </div>
                </div>
            </td>
            <td class="px-8 py-6">
                <span class="px-4 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-[0.15em] ${getTierStyle(c.points)}">
                    ${calculateTier(c.points)}
                </span>
            </td>
            <td class="px-8 py-6 font-black text-slate-900 tracking-tighter text-lg">${c.points.toLocaleString()}</td>
            <td class="px-8 py-6 font-bold text-slate-500">${c.visits}</td>
            <td class="px-8 py-6 text-right">
                <div class="flex items-center justify-end space-x-2">
                    <button onclick="openVerifyModal('${c.id}')" class="p-3 bg-indigo-50 text-indigo-600 rounded-xl hover:bg-indigo-600 hover:text-white transition-all shadow-sm">
                        <i data-lucide="plus" class="w-5 h-5"></i>
                    </button>
                    <button onclick="viewCustomerDetails('${c.phone}')" class="p-3 bg-slate-50 text-slate-600 rounded-xl hover:bg-slate-900 hover:text-white transition-all shadow-sm">
                        <i data-lucide="eye" class="w-5 h-5"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
    lucide.createIcons();
}

function calculateTier(points) {
    if (points >= 5000) return 'platinum';
    if (points >= 2000) return 'gold';
    if (points >= 500) return 'silver';
    return 'bronze';
}

function getTierStyle(points) {
    if (points >= 5000) return 'bg-purple-50 text-purple-600 border border-purple-100';
    if (points >= 2000) return 'bg-amber-50 text-amber-600 border border-amber-100';
    if (points >= 500) return 'bg-slate-100 text-slate-600 border border-slate-200';
    return 'bg-indigo-50 text-indigo-600 border border-indigo-100';
}

function filterCustomers() { renderCustomers(); }

function openVerifyModal(id = '') {
    document.getElementById('verify-modal').classList.remove('hidden');
    document.getElementById('verify-id-input').value = id;
}

function closeVerifyModal() { document.getElementById('verify-modal').classList.add('hidden'); }

async function confirmVisit() {
    const id = document.getElementById('verify-id-input').value;
    const secret = document.getElementById('verify-secret-input').value;
    if (secret !== adminSettings.secretCode) return alert("Invalid Secret Code!");
    
    const snap = await db.collection('customers').where('id', '==', id).get();
    if (snap.empty) return alert("Customer not found!");
    
    const userData = snap.docs[0].data();
    await db.collection('customers').doc(userData.phone).update({
        visits: firebase.firestore.FieldValue.increment(1),
        points: firebase.firestore.FieldValue.increment(50),
        lifetimePoints: firebase.firestore.FieldValue.increment(50)
    });

    await db.collection('customers').doc(userData.phone).collection('history').add({
        type: 'visit',
        points: 50,
        date: new Date().toISOString()
    });

    alert("Visit verified!");
    closeVerifyModal();
}

function viewCustomerDetails(phone) {
    const customer = adminCustomers.find(c => c.phone === phone);
    if (!customer) return;
    alert(`Customer: ${customer.name}\nPhone: ${customer.phone}\nPoints: ${customer.points}\nVisits: ${customer.visits}`);
}

async function saveConfig() {
    const val = parseInt(document.getElementById('config-point-value').value);
    const max = parseInt(document.getElementById('config-max-discount').value);
    await db.collection('settings').doc('business').set({ pointValue: val, maxDiscount: max }, { merge: true });
    alert("Policy Updated!");
}

async function saveSettings() {
    const name = document.getElementById('settings-name').value;
    const secret = document.getElementById('settings-secret').value;
    await db.collection('settings').doc('business').set({ restaurantName: name, secretCode: secret }, { merge: true });
    alert("Settings Saved!");
}

function initCharts() {
    const ctx = document.getElementById('rewardsChart');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Sweet Dish', 'Discount', 'Points', 'Beverages'],
            datasets: [{ data: [30, 20, 40, 10], backgroundColor: ['#6366f1', '#a855f7', '#ec4899', '#f59e0b'], borderWidth: 0 }]
        },
        options: { cutout: '70%', plugins: { legend: { position: 'bottom' } } }
    });
}

async function exportCustomersCSV() {
    const headers = ['Name', 'Phone', 'Points', 'Visits', 'Tier'];
    const rows = adminCustomers.map(c => [c.name, c.phone, c.points, c.visits, calculateTier(c.points)]);
    let csvContent = "data:text/csv;charset=utf-8," + headers.join(",") + "\n" + rows.map(e => e.join(",")).join("\n");
    const link = document.createElement("a");
    link.setAttribute("href", encodeURI(csvContent));
    link.setAttribute("download", "customers.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}