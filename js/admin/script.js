function toggleDropdown(section) {
  const sidebar = document.getElementById("sidebar");
  if (sidebar.classList.contains("collapsed")) return; // Prevent toggle when collapsed
  const menu = document.getElementById("dropdown-" + section);
  const title = document.getElementById("title-" + section);
  const arrow = document.getElementById("arrow-" + section);
  const isOpen = menu.classList.contains("open");
  if (isOpen) {
    menu.classList.remove("open");
    title.classList.remove("open");
    if (arrow) arrow.style.transform = "rotate(0deg)";
  } else {
    menu.classList.add("open");
    title.classList.add("open");
    if (arrow) arrow.style.transform = "rotate(180deg)";
  }
}
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  const mainContent = document.querySelector(".main-content");
  const topbar = document.querySelector(".topbar");

  sidebar.classList.toggle("collapsed");

  // Adjust main-content and topbar left margin with smooth transition
  if (sidebar.classList.contains("collapsed")) {
    mainContent.style.marginLeft = "56px";
    topbar.style.left = "56px";
  } else {
    mainContent.style.marginLeft = "260px";
    topbar.style.left = "260px";
  }

  // Update tooltips and section titles after animation completes
  setTimeout(function () {
    updateSectionTitles();
    updateTooltips();
  }, 350); // Wait for transition to complete
}

let tooltipHandlers = [];

function updateTooltips() {
  const sidebar = document.getElementById("sidebar");
  const menuItems = document.querySelectorAll(".sidebar-menu li");
  const sectionTitles = document.querySelectorAll(".sidebar-section-title");
  const sectionTitles22 = document.querySelectorAll(".sidebar-section");
  // Remove existing tooltips and event listeners
  document.querySelectorAll(".tooltip").forEach((tooltip) => tooltip.remove());

  // Clean up previous event listeners
  tooltipHandlers.forEach((handler) => {
    handler.element.removeEventListener("mouseenter", handler.enter);
    handler.element.removeEventListener("mouseleave", handler.leave);
  });
  tooltipHandlers = [];

  if (sidebar.classList.contains("collapsed")) {
    // Create tooltip element
    const tooltip = document.createElement("div");
    tooltip.className = "tooltip";
    document.body.appendChild(tooltip);

    // Add hover events for menu items
    menuItems.forEach(function (item) {
      const label = item.querySelector(".menu-label");
      if (label) {
        const enterHandler = function (e) {
          const rect = item.getBoundingClientRect();
          tooltip.textContent = label.textContent;
          tooltip.style.top = rect.top + rect.height / 2 + "px";
          tooltip.classList.add("show");
        };

        const leaveHandler = function () {
          tooltip.classList.remove("show");
        };

        item.addEventListener("mouseenter", enterHandler);
        item.addEventListener("mouseleave", leaveHandler);

        tooltipHandlers.push({
          element: item,
          enter: enterHandler,
          leave: leaveHandler,
        });
      }
    });

    // Add hover events for menu items
    sectionTitles22.forEach(function (item) {
      const label = item.querySelector(".menu-label");
      if (label) {
        const enterHandler = function (e) {
          const rect = item.getBoundingClientRect();
          tooltip.textContent = label.textContent;
          tooltip.style.top = rect.top + rect.height / 2 + "px";
          tooltip.classList.add("show");
        };

        const leaveHandler = function () {
          tooltip.classList.remove("show");
        };

        item.addEventListener("mouseenter", enterHandler);
        item.addEventListener("mouseleave", leaveHandler);

        tooltipHandlers.push({
          element: item,
          enter: enterHandler,
          leave: leaveHandler,
        });
      }
    });

    // Add hover events for dropdown sections
    // sectionTitles.forEach(function(title) {
    //     const titleText = title.getAttribute('data-title');
    //     if (titleText) {
    //         const enterHandler = function(e) {
    //             const rect = title.getBoundingClientRect();
    //             tooltip.textContent = titleText;
    //             tooltip.style.top = rect.top + rect.height / 2 + 'px';
    //             tooltip.classList.add('show');
    //         };

    //         const leaveHandler = function() {
    //             tooltip.classList.remove('show');
    //         };

    //         title.addEventListener('mouseenter', enterHandler);
    //         title.addEventListener('mouseleave', leaveHandler);

    //         tooltipHandlers.push({
    //             element: title,
    //             enter: enterHandler,
    //             leave: leaveHandler
    //         });
    //     }
    // });
  }
}
document.addEventListener("DOMContentLoaded", function () {
  // By default, dropdowns should be collapsed (not open)
  ["build", "run", "analytics", "ai"].forEach(function (section) {
    document.getElementById("dropdown-" + section).classList.remove("open");
    document.getElementById("title-" + section).classList.remove("open");
  });
  // Dropdown item select effect
  document
    .querySelectorAll(".sidebar-section-menu li")
    .forEach(function (item) {
      item.addEventListener("click", function (e) {
        const sidebar = document.getElementById("sidebar");
        if (sidebar.classList.contains("collapsed")) {
          // Prevent selection if sidebar is collapsed
          e.stopPropagation();
          return;
        }
        // Only one active per dropdown
        const parent = item.parentElement;
        parent.querySelectorAll("li.active").forEach(function (active) {
          active.classList.remove("active");
        });
        item.classList.add("active");
        e.stopPropagation();
      });
    });
  // Sidebar section icon-only mode when collapsed
  const sectionTitles = document.querySelectorAll(".sidebar-section-title");

  function updateSectionTitles() {
    const sidebar = document.getElementById("sidebar");
    const sectionTitles = document.querySelectorAll(".sidebar-section-title");
    if (sidebar.classList.contains("collapsed")) {
      // In collapsed mode, sections become icon-only buttons
      sectionTitles.forEach(function (title) {
        const section = title.id.replace("title-", "");
        const iconElement = title.querySelector(".bx");
        if (iconElement) {
          title.innerHTML =
            '<div class="section-title-content"><i class="bx ' +
            Array.from(iconElement.classList).filter(c => c.startsWith('bx-')).join(' ') +
            '"></i></div>';
        }
        title.onclick = null; // Remove dropdown functionality when collapsed
      });
    } else {
      // In expanded mode, restore full functionality
      sectionTitles.forEach(function (title) {
        const section = title.id.replace("title-", "");
        const sectionData = {
          "title-build": { icon: "bx-wrench", text: "Build" },
          "title-run": { icon: "bx-play", text: "Run" },
          "title-analytics": { icon: "bx-bar-chart-alt-2", text: "Analytics" },
          "title-ai": { icon: "bx-bot", text: "AI" },
        };

        if (sectionData[title.id]) {
          title.innerHTML = `
                                <div class="section-title-content">
                                    <i class="bx ${sectionData[title.id].icon}"></i>
                                    <span class="section-text">${sectionData[title.id].text}</span>
                                </div>
                                <i class="bx bx-chevron-down arrow" id="arrow-${section}"></i>
                            `;
          title.onclick = function () {
            toggleDropdown(section);
          };

          // Set arrow direction based on open state
          const menu = document.getElementById("dropdown-" + section);
          const arrow = document.getElementById("arrow-" + section);
          if (arrow && menu) {
            if (menu.classList.contains("open")) {
              arrow.style.transform = "rotate(180deg)";
            } else {
              arrow.style.transform = "rotate(0deg)";
            }
          }
        }
      });
    }
  }
  // Initialize the sidebar sections
  updateSectionTitles();

  // Add click handler for sidebar toggle button
  document
    .getElementById("sidebar-toggle-btn")
    .addEventListener("click", function () {
      // Add visual feedback
      this.style.transform = "scale(0.95)";
      setTimeout(() => {
        this.style.transform = "";
      }, 100);

      setTimeout(function () {
        updateSectionTitles();
        updateTooltips();
      }, 350); // Wait for transition to complete
    });

  // Initialize tooltips
  updateTooltips();
});
// Add scroll event to change topbar background on scroll down in main-content
// (function () {
//   let lastScrollTop = 0;
//   const mainContent = document.querySelector(".main-content");
//   const topbar = document.querySelector(".topbar");
  
//   if (mainContent && topbar) {
//     mainContent.addEventListener("scroll", function () {
//       const st = mainContent.scrollTop;
      
//       if (st > 0 && !topbar.classList.contains("scrolled-down")) {
//         // Any scroll down from the top - change to red
//         topbar.classList.add("scrolled-down");
//       } else if (st === 0 && topbar.classList.contains("scrolled-down")) {
//         // At the very top - change back to original
//         topbar.classList.remove("scrolled-down");
//       }
//       lastScrollTop = st <= 0 ? 0 : st;
//     });
//   }
// })();

// Topbar scroll effect
// Listen for scroll events on the main-content div (correct approach for your layout)
document.addEventListener('DOMContentLoaded', function() {
    const mainContent = document.querySelector('.main-content');
    const topbar = document.querySelector('.topbar');
    const scrollThreshold = 50; // Adjust this value as needed
    let isScrolledDown = false;
    
    mainContent.addEventListener('scroll', function() {
        const currentScrollTop = this.scrollTop;
        console.log('Scroll position:', currentScrollTop); // Debug line - you can remove this
        
        if (currentScrollTop > scrollThreshold && !isScrolledDown) {
            topbar.classList.add('scrolled-down');
            isScrolledDown = true;
            console.log('Added scrolled-down class'); // Debug line - you can remove this
            
        } else if (currentScrollTop <= scrollThreshold && isScrolledDown) {
            topbar.classList.remove('scrolled-down');
            isScrolledDown = false;
            console.log('Removed scrolled-down class'); // Debug line - you can remove this
        }
    });
});


// Profile
var profile = document.querySelector(".profile");
var imgProfile = profile.querySelector("img");
var dropdownProfile = profile.querySelector(".profile-link");
imgProfile.addEventListener("click", function (e) {
  e.preventDefault();
  dropdownProfile.classList.toggle("show");
});
window.addEventListener("click", function (e) {
  if (e.target !== imgProfile) {
    if (e.target !== dropdownProfile) {
      if (dropdownProfile.classList.contains("show")) {
        dropdownProfile.classList.remove("show");
      }
    }
  }
}); 


// Dropdown functionality - completely
document.addEventListener('DOMContentLoaded', function() {
    console.log('Custom dropdown initialized');
    
    // Handle dropdown button clicks
    document.addEventListener('click', function(e) {
        const button = e.target.closest('.action-btn');
        
        if (button) {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('Dropdown button clicked');
            
            const dropdown = button.closest('.dropdown');
            const menu = dropdown.querySelector('.tb-dropdown-menu');
            
            // Close all other dropdowns
            document.querySelectorAll('.tb-dropdown-menu').forEach(otherMenu => {
                if (otherMenu !== menu) {
                    otherMenu.classList.remove('show');
                }
            });
            
            // Toggle current dropdown
            menu.classList.toggle('show');
            console.log('Menu toggled, has show class:', menu.classList.contains('show'));
        }
        
        // Handle dropdown item clicks
        const dropdownItem = e.target.closest('.dropdown-item');
        if (dropdownItem) {
            e.preventDefault();
            e.stopPropagation();
            
            const action = dropdownItem.getAttribute('data-action');
            console.log('Dropdown item clicked:', action);
            
            if (action === 'delete') {
                if (confirm('Are you sure you want to delete this row?')) {
                    const row = dropdownItem.closest('.column');
                    if (row) {
                        row.remove();
                        console.log('Row deleted');
                    }
                }
            } else if (action === 'edit') {
                alert('Edit functionality - implement as needed');
                console.log('Edit clicked');
            }
            
            // Close dropdown after action
            const menu = dropdownItem.closest('.tb-dropdown-menu');
            menu.classList.remove('show');
        }
        
        // Close dropdowns when clicking outside
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.tb-dropdown-menu').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
  
});


// window.Alpine = Alpine
// Alpine.start()

// Flash Messages Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        // Add close button functionality
        const closeBtn = alert.querySelector('.btn-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                dismissAlert(alert);
            });
        }
        
        // Auto-dismiss after 5 seconds for success messages
        if (alert.classList.contains('alert-success')) {
            setTimeout(function() {
                if (document.body.contains(alert)) {
                    dismissAlert(alert);
                }
            }, 5000);
        }
        
        // Auto-dismiss after 8 seconds for error messages
        if (alert.classList.contains('alert-error') || alert.classList.contains('alert-danger')) {
            setTimeout(function() {
                if (document.body.contains(alert)) {
                    dismissAlert(alert);
                }
            }, 8000);
        }
    });
});

function dismissAlert(alert) {
    alert.classList.add('fade-out');
    setTimeout(function() {
        if (alert.parentNode) {
            alert.parentNode.removeChild(alert);
        }
    }, 300); // Wait for fade-out animation
}

// Function to show flash message programmatically (for AJAX calls)
function showFlashMessage(message, category = 'info') {
    const flashContainer = document.querySelector('.flash-messages');
    if (!flashContainer) return;
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${category === 'error' ? 'danger' : category} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    
    let iconClass = 'bx-info-circle';
    if (category === 'success') iconClass = 'bx-check-circle';
    else if (category === 'error') iconClass = 'bx-error';
    else if (category === 'warning') iconClass = 'bx-error-circle';
    
    alertDiv.innerHTML = `
        <i class="bx ${iconClass} alert-icon"></i>
        ${message}
        <button type="button" class="btn-close" aria-label="Close">
            <i class="bx bx-x"></i>
        </button>
    `;
    
    flashContainer.appendChild(alertDiv);
    
    // Add close functionality
    const closeBtn = alertDiv.querySelector('.btn-close');
    closeBtn.addEventListener('click', function() {
        dismissAlert(alertDiv);
    });
    
    // Auto-dismiss
    const dismissTime = category === 'success' ? 5000 : 8000;
    setTimeout(function() {
        if (document.body.contains(alertDiv)) {
            dismissAlert(alertDiv);
        }
    }, dismissTime);
}