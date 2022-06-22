var background = [
  "#1b2469",
  "#5b6063",
  "#cdaeb4",
  "#bda299",
  "#3f464e",
  "#7b94cd",
]; //Add more backgrounds to the array

var backgroundReverse = [
  "#1b2469",
  "#7b94cd",
  "#3f464e",
  "#bda299",
  "#cdaeb4",
  "#5b6063",
];

var backgroundCount = 0;

$(function () {
  $("body").css("background", "(" + background[backgroundCount] + ")"); //allows a variable for changing background img based in an array, change number in [] to change background...
});

$(".slider-right").on("click", function () {
  backgroundCount++;
  if (backgroundCount > background.length - 1) backgroundCount = 0;
  $("body").css("background", background[backgroundCount]);
});

$(".slider-left").on("click", function () {
  backgroundCount++;
  if (backgroundCount > backgroundReverse.length - 1) backgroundCount = 0;
  $("body").css("background", backgroundReverse[backgroundCount]);
});

$(document).on("ready", function () {
  var slide = $(".slider-single");
  var slideTotal = slide.length - 1;
  var slideCurrent = -1;

  function slideInitial() {
    slide.addClass("proactivede");
    setTimeout(function () {
      slideRight();
    }, 500);
  }

  function slideRight() {
    if (slideCurrent < slideTotal) {
      slideCurrent++;
    } else {
      slideCurrent = 0;
    }

    if (slideCurrent > 0) {
      var preactiveSlide = slide.eq(slideCurrent - 1);
    } else {
      var preactiveSlide = slide.eq(slideTotal);
    }
    var activeSlide = slide.eq(slideCurrent);
    if (slideCurrent < slideTotal) {
      var proactiveSlide = slide.eq(slideCurrent + 1);
    } else {
      var proactiveSlide = slide.eq(0);
    }

    slide.each(function () {
      var thisSlide = $(this);
      if (thisSlide.hasClass("preactivede")) {
        thisSlide
          .removeClass("preactivede preactive active proactive")
          .addClass("proactivede");
      }
      if (thisSlide.hasClass("preactive")) {
        thisSlide
          .removeClass("preactive active proactive proactivede")
          .addClass("preactivede");
      }
    });
    preactiveSlide
      .removeClass("preactivede active proactive proactivede")
      .addClass("preactive");
    activeSlide
      .removeClass("preactivede preactive proactive proactivede")
      .addClass("active");
    proactiveSlide
      .removeClass("preactivede preactive active proactivede")
      .addClass("proactive");
  }

  function slideLeft() {
    if (slideCurrent > 0) {
      slideCurrent--;
    } else {
      slideCurrent = slideTotal;
    }

    if (slideCurrent < slideTotal) {
      var proactiveSlide = slide.eq(slideCurrent + 1);
    } else {
      var proactiveSlide = slide.eq(0);
    }
    var activeSlide = slide.eq(slideCurrent);
    if (slideCurrent > 0) {
      var preactiveSlide = slide.eq(slideCurrent - 1);
    } else {
      var preactiveSlide = slide.eq(slideTotal);
    }
    slide.each(function () {
      var thisSlide = $(this);
      if (thisSlide.hasClass("proactivede")) {
        thisSlide
          .removeClass("preactive active proactive proactivede")
          .addClass("preactivede");
      }
      if (thisSlide.hasClass("proactive")) {
        thisSlide
          .removeClass("preactivede preactive active proactive")
          .addClass("proactivede");
      }
    });
    preactiveSlide
      .removeClass("preactivede active proactive proactivede")
      .addClass("preactive");
    activeSlide
      .removeClass("preactivede preactive proactive proactivede")
      .addClass("active");
    proactiveSlide
      .removeClass("preactivede preactive active proactivede")
      .addClass("proactive");
  }
  var left = $(".slider-left");
  var right = $(".slider-right");
  left.on("click", function () {
    slideLeft();
  });
  right.on("click", function () {
    slideRight();
  });
  slideInitial();
});
