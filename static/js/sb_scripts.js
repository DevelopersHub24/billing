// Track active menu item
let activeMenuItem = null;

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    sidebar.classList.toggle('-translate-x-full');
    overlay.classList.toggle('show');

    // Add/remove body overflow when sidebar is open/closed
    if (sidebar.classList.contains('-translate-x-full')) {
        document.body.style.overflow = 'auto';
    } else {
        document.body.style.overflow = 'hidden';
    }
}

function logout() {
    alert('Logging out...');
    window.location.href = '/logout';
}

function toggleDropdown(type) {
    const dropdown = document.getElementById(`${type}Dropdown`);
    const arrow = document.getElementById(`${type}DropdownArrow`);

    dropdown.classList.toggle('show');
    arrow.classList.toggle('rotate-180');

    // Close other dropdowns when opening a new one
    if (dropdown.classList.contains('show')) {
        document.querySelectorAll('.dropdown-content').forEach(el => {
            if (el.id !== `${type}Dropdown` && el.classList.contains('show')) {
                el.classList.remove('show');
                document.getElementById(el.id.replace('Dropdown', 'DropdownArrow')).classList.remove('rotate-180');
            }
        });
    }
}

function navigateTo(page) {
    // Update active menu item
    if (activeMenuItem) {
        activeMenuItem.classList.remove('active');
    }

    // Find the clicked item and mark it as active
    const clickedItem = event.currentTarget;
    clickedItem.classList.add('active');
    activeMenuItem = clickedItem;

    // Also mark parent menu item as active
    const parentMenu = clickedItem.closest('.relative');
    if (parentMenu) {
        parentMenu.querySelector('.sidebar-item').classList.add('active');
    }

    // Navigate to the corresponding page
        const routes = {
            'sales-bill': '/home/billing/sales',
            'purchase-bill': '/home/billing/purchase',
            'credit-note': '/home/billing/credit-note',
            'debit-note': '/home/billing/debit-note', // Add this line
            'proforma-invoice': '/home/billing/proforma',
            'asn': '/home/billing/asn',
            'inventory': '/home/inventory'
        };
    
        if (routes[page]) {
            window.location.href = routes[page];
        } else {
            console.log(`Navigating to: ${page}`);
        }
    }

// Close dropdowns when clicking outside
document.addEventListener('click', function (event) {
    if (!event.target.closest('.relative')) {
        document.querySelectorAll('.dropdown-content').forEach(el => {
            el.classList.remove('show');
        });
        document.querySelectorAll('.dropdown-arrow').forEach(el => {
            el.classList.remove('rotate-180');
        });
    }
});

// Initialize with dashboard as active
document.addEventListener('DOMContentLoaded', function () {
    activeMenuItem = document.querySelector('.sidebar-item.active');
});