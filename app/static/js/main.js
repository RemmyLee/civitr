// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", function () {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Handle image modal for gallery
  var modelImages = document.querySelectorAll(
    ".model-gallery img, .card-img-top"
  );
  if (modelImages.length > 0) {
    modelImages.forEach(function (img) {
      img.addEventListener("click", function () {
        var modalId = "imageModal";

        // Check if modal exists, create if not
        if (!document.getElementById(modalId)) {
          var modal = document.createElement("div");
          modal.className = "modal fade";
          modal.id = modalId;
          modal.tabIndex = "-1";
          modal.setAttribute("aria-hidden", "true");

          modal.innerHTML = `
              <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title">Image Preview</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body text-center">
                    <img id="modalImage" src="" class="img-fluid" alt="Preview">
                  </div>
                </div>
              </div>
            `;

          document.body.appendChild(modal);
        }

        // Display modal with clicked image
        document.getElementById("modalImage").src = this.src;
        var modalInstance = new bootstrap.Modal(
          document.getElementById(modalId)
        );
        modalInstance.show();
      });
    });
  }

  // Back to top button functionality
  var backToTopBtn = document.getElementById("back-to-top");
  if (backToTopBtn) {
    // Initially hide the button
    backToTopBtn.style.display = "none";

    // Show/hide the button based on scroll position
    window.addEventListener("scroll", function () {
      if (window.pageYOffset > 300) {
        backToTopBtn.style.display = "block";
      } else {
        backToTopBtn.style.display = "none";
      }
    });

    // Smooth scroll to top when clicked
    backToTopBtn.addEventListener("click", function () {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });
  }

  // Add animation to model cards
  var modelCards = document.querySelectorAll(".model-card");
  if (modelCards.length > 0) {
    // Initialize animation delay counter
    var delay = 0;

    // Apply staggered animation to each card
    modelCards.forEach(function (card, index) {
      // Calculate delay (100ms between each card, row reset every 4 cards)
      delay = (index % 4) * 100;

      // Apply delay
      card.style.animationDelay = delay + "ms";
    });
  }

  // Initialize dropdowns with hover functionality for desktop
  var dropdowns = document.querySelectorAll(".navbar .dropdown");
  if (dropdowns.length > 0 && window.innerWidth >= 992) {
    dropdowns.forEach(function (dropdown) {
      dropdown.addEventListener("mouseenter", function () {
        this.querySelector(".dropdown-toggle").click();
      });

      dropdown.addEventListener("mouseleave", function () {
        this.querySelector(".dropdown-toggle").click();
      });
    });
  }

  // Filter form submitting for model page
  var filterSelects = document.querySelectorAll(".filter-select");
  if (filterSelects.length > 0) {
    filterSelects.forEach(function (select) {
      select.addEventListener("change", function () {
        this.closest("form").submit();
      });
    });
  }

  // Handle dark mode toggle (if implemented)
  var darkModeToggle = document.getElementById("darkModeToggle");
  if (darkModeToggle) {
    darkModeToggle.addEventListener("click", function () {
      document.documentElement.classList.toggle("dark-mode");
      localStorage.setItem(
        "darkMode",
        document.documentElement.classList.contains("dark-mode")
      );
    });

    // Check for saved dark mode preference
    if (localStorage.getItem("darkMode") === "true") {
      document.documentElement.classList.add("dark-mode");
    }
  }

  // Enhanced image hover effect
  var cardImgWrappers = document.querySelectorAll(".card-img-wrapper");
  if (cardImgWrappers.length > 0) {
    cardImgWrappers.forEach(function (wrapper) {
      wrapper.addEventListener("mouseenter", function () {
        this.querySelector("img")?.classList.add("zoomed");
      });

      wrapper.addEventListener("mouseleave", function () {
        this.querySelector("img")?.classList.remove("zoomed");
      });
    });
  }

  // Add lazy loading to images
  var images = document.querySelectorAll("img:not([loading])");
  if (images.length > 0) {
    images.forEach(function (img) {
      if (!img.hasAttribute("loading")) {
        img.setAttribute("loading", "lazy");
      }
    });
  }

  // NSFW toggle persistence
  var nsfwCheckboxes = document.querySelectorAll('input[name="nsfw"]');
  if (nsfwCheckboxes.length > 0) {
    // Get current URL parameters to check current NSFW state
    const urlParams = new URLSearchParams(window.location.search);
    const currentNsfwParam = urlParams.get("nsfw");

    // Determine the correct state based on URL parameter or localStorage
    let nsfwEnabled = false;

    // URL parameter takes precedence if present
    if (currentNsfwParam !== null) {
      nsfwEnabled = currentNsfwParam === "true";
      // Update localStorage to match URL
      localStorage.setItem("nsfw", nsfwEnabled);
    } else {
      // Fall back to localStorage if URL param not present
      nsfwEnabled = localStorage.getItem("nsfw") === "true";
    }

    // Set all checkboxes to match the determined state
    nsfwCheckboxes.forEach(function (checkbox) {
      checkbox.checked = nsfwEnabled;

      // Add event listener to update preference when changed
      checkbox.addEventListener("change", function () {
        const newState = this.checked;
        localStorage.setItem("nsfw", newState);

        // Update all other checkboxes to match
        nsfwCheckboxes.forEach(function (otherCheckbox) {
          if (otherCheckbox !== checkbox) {
            otherCheckbox.checked = newState;
          }
        });

        // Handle form submission correctly to ensure parameter is always included
        // Get the current form
        const form = this.closest("form");

        // If checkbox is unchecked, we need to add a hidden field to ensure
        // the nsfw=false parameter is sent (checkboxes only send values when checked)
        if (
          !newState &&
          !form.querySelector('input[type="hidden"][name="nsfw"]')
        ) {
          const hiddenField = document.createElement("input");
          hiddenField.type = "hidden";
          hiddenField.name = "nsfw";
          hiddenField.value = "false";
          form.appendChild(hiddenField);
        }

        // Submit the form
        form.submit();
      });
    });
  }

  // Initialize popovers for file details
  var fileInfoBtns = document.querySelectorAll(".file-info-btn");
  if (fileInfoBtns.length > 0) {
    fileInfoBtns.forEach(function (btn) {
      new bootstrap.Popover(btn, {
        html: true,
        trigger: "focus",
      });
    });
  }
});
