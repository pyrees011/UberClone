document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.custom-menu');

    menuItems.forEach(function(item) {
        item.addEventListener('click', function() {
            // Remove 'active' class from all menu items
            menuItems.forEach(function(menuItem) {
                menuItem.classList.remove('active');
            });

            // Add 'active' class to the clicked menu item
            this.classList.add('active');
        });
    });
});