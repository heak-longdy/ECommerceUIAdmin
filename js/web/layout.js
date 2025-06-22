// Topbar scroll effect
// Listen for scroll events on the main-content div (correct approach for your layout)
document.addEventListener('DOMContentLoaded', function() {
    const mainContent = document.querySelector('.main-content');
    const topbar = document.querySelector('.header');
    const scrollThreshold = 50; // Adjust this value as needed
    let isScrolledDown = false;

    mainContent.addEventListener('scroll', function() {
        const currentScrollTop = this.scrollTop;

        if (currentScrollTop > scrollThreshold && !isScrolledDown) {
            topbar.classList.add('scrolled-down');
            isScrolledDown = true;
        } else if (currentScrollTop <= scrollThreshold && isScrolledDown) {
            topbar.classList.remove('scrolled-down');
            isScrolledDown = false;
        }
    });
});