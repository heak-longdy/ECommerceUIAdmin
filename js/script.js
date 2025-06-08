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
    if (sidebar.classList.contains("collapsed")) {
      // In collapsed mode, sections become icon-only buttons
      sectionTitles.forEach(function (title) {
        const section = title.id.replace("title-", "");
        const iconElement = title.querySelector(".material-symbols-outlined");
        if (iconElement) {
          title.innerHTML =
            '<div class="section-title-content"><span class="material-symbols-outlined">' +
            iconElement.textContent +
            "</span></div>";
        }
        title.onclick = null; // Remove dropdown functionality when collapsed
      });
    } else {
      // In expanded mode, restore full functionality
      sectionTitles.forEach(function (title) {
        const section = title.id.replace("title-", "");
        const sectionData = {
          "title-build": { icon: "build", text: "Build" },
          "title-run": { icon: "play_arrow", text: "Run" },
          "title-analytics": { icon: "analytics", text: "Analytics" },
          "title-ai": { icon: "smart_toy", text: "AI" },
        };

        if (sectionData[title.id]) {
          title.innerHTML = `
                                <div class="section-title-content">
                                    <span class="material-symbols-outlined">${
                                      sectionData[title.id].icon
                                    }</span>
                                    <span class="section-text">${
                                      sectionData[title.id].text
                                    }</span>
                                </div>
                                <span class="material-symbols-outlined arrow" id="arrow-${section}">keyboard_arrow_down</span>
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
(function () {
  let lastScrollTop = 0;
  const mainContent = document.querySelector(".main-content");
  const topbar = document.querySelector(".topbar");
  
  if (mainContent && topbar) {
    mainContent.addEventListener("scroll", function () {
      const st = mainContent.scrollTop;
      
      if (st > 0 && !topbar.classList.contains("scrolled-down")) {
        // Any scroll down from the top - change to red
        topbar.classList.add("scrolled-down");
      } else if (st === 0 && topbar.classList.contains("scrolled-down")) {
        // At the very top - change back to original
        topbar.classList.remove("scrolled-down");
      }
      lastScrollTop = st <= 0 ? 0 : st;
    });
  }
})();
