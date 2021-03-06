if (sessionStorage.getItem("theme") === null) {
  sessionStorage.setItem("theme", "light");
  document.getElementById("theme-toggle").checked = false;
} else {
  if (sessionStorage.getItem("theme") === "dark") {
    document.getElementById("theme-toggle").checked = true;
    document.getElementById("theme-icon").innerHTML = '<i class="fa fa-moon-o fa-2x"></i>';
  } else {
    document.getElementById("theme-toggle").checked = false;
  }
}
document.body.setAttribute("theme", sessionStorage.getItem("theme"));

document.getElementById("theme-toggle").addEventListener("click", (e) => {
  if (e.target.checked) {
    sessionStorage.setItem("theme", "dark");
    document.body.setAttribute("theme", "dark");
    document.getElementById("theme-icon").innerHTML = '<i class="fa fa-moon-o fa-2x"></i>';
  } else {
    sessionStorage.setItem("theme", "light");
    document.body.setAttribute("theme", "light");
    document.getElementById("theme-icon").innerHTML = '<i class="fa fa-sun-o fa-2x" style="color:gold; font-weight:bold"></i>';
  }
});

(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 70)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Scroll to top button appear
  $(document).scroll(function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 80
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Floating label headings for the contact form
  $(function() {
    $("body").on("input propertychange", ".floating-label-form-group", function(e) {
      $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
    }).on("focus", ".floating-label-form-group", function() {
      $(this).addClass("floating-label-form-group-with-focus");
    }).on("blur", ".floating-label-form-group", function() {
      $(this).removeClass("floating-label-form-group-with-focus");
    });
  });

})(jQuery); // End of use strict
