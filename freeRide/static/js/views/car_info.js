document.addEventListener('DOMContentLoaded', function() {
    const carItems = document.querySelectorAll('.car-card');
    const car_type = document.getElementById('car_type')

    carItems.forEach(function(item) {
        item.addEventListener('click', function() {
            // Remove 'active' class from all menu items
            carItems.forEach(function(menuItem) {
                menuItem.classList.remove('active');
            });

            // Add 'active' class to the clicked menu item
            this.classList.add('active');
            const car_option = this.getAttribute('data-value');
            car_type.value = car_option;
        });
    });
});