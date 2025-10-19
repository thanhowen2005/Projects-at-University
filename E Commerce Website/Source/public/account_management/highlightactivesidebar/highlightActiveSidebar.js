document.addEventListener("DOMContentLoaded", function () {
  const currentPath = window.location.pathname.toLowerCase(); // vd: "/admin_product/admin_product_management_profile.html"

  const sidebarLinks = document.querySelectorAll(".sidebar-link");

  sidebarLinks.forEach(link => {
    const section = link.getAttribute("data-section");
    if (!section) return;

    if (currentPath.includes(section.toLowerCase())) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }
  });
});
