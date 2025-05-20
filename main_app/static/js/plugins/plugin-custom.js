"use strict";
document.addEventListener("DOMContentLoaded", function () {

    $(function ($) {

        /* select two init */
        $(".select-two").select2({
          allowClear: true
        });
        $('.single-select').on('click', function () {
          const singleSelect = $('.select2-container--open');
          var selectType = $(this).attr('class').split(' ')[0];
          $(singleSelect[1]).addClass(selectType);
          const computedStyle = window.getComputedStyle(this);
          const width = computedStyle.width;
          $(singleSelect[1]).find('.select2-dropdown').css('right', '-'+(width));
        });

        /* datepicker init */
        $(".datepicker").datepicker();

        /* Splitting init */
        Splitting();

        // lenis matchMedia Init
        ScrollTrigger.matchMedia({
          "(min-width: 992px)": function() {

            // horizontal scroll 
            const horizontalSections = document.querySelectorAll(".horizontal");
            if(horizontalSections){
              horizontalSections.forEach(section => {
                let horizontalItems = gsap.utils.toArray(section.querySelectorAll(".horizontal-item"));
                gsap.to(horizontalItems, {
                  xPercent: -100 * (horizontalItems.length - 1),
                  ease: "sine.out",
                  scrollTrigger: {
                    trigger: section,
                    pin: true,
                    scrub: 9,
                    snap: 2 / (horizontalItems.length - 4),
                    end: "+=" + section.offsetWidth
                  }
                });
              });
            }

          },
          
          // responsive
          "(max-width: 991px)": function() {

            const horizontalSections = document.querySelectorAll(".horizontal");
            if(horizontalSections){
              horizontalSections.forEach(section => {
                let horizontalItems = gsap.utils.toArray(section.querySelectorAll(".horizontal-item"));
                gsap.to(horizontalItems, {
                  xPercent: -0 * (horizontalItems.length - 1),
                  scrollTrigger: {
                    pin: false,
                  }
                });
              });
            }

          },

        });
        
        // gSap animation start

        // Visible From Right Animation
        if(document.querySelector('.visible-from-right')){
          let visibleFromRight = document.querySelectorAll(".visible-from-right")
          visibleFromRight.forEach((visibleFromRight) => {
            let split_item = new SplitText(visibleFromRight, { type: "chars, words" })
            gsap.from(split_item.chars, { duration: 1, x: 95, autoAlpha: 0, stagger: 0.15 });
          })
        }

        // Visible From Right Slowly Animation
        let visibleSlowlyRight = document.querySelectorAll(".visible-slowly-right");
        if ($(visibleSlowlyRight).length > 0) {
          let char_come = gsap.utils.toArray(visibleSlowlyRight);
          char_come.forEach((char_come) => {
            let split_char = new SplitText(char_come, {
              type: "chars, words",
              lineThreshold: 0.5,
            });
            const tl2 = gsap.timeline({
              scrollTrigger: {
                trigger: char_come,
                start: "top 90%",
                end: "bottom 60%",
                scrub: false,
                markers: false,
                toggleActions: "play none none none",
              },
            });
            tl2.from(split_char.chars, {
              duration: 0.8,
              x: 70,
              autoAlpha: 0,
              stagger: 0.03,
            });
          });
        }

        // Visible From Bottom Animation
        let visibleFromBottom = gsap.utils.toArray(".visible-from-bottom");
        visibleFromBottom.forEach(splitArea => {
          const trigger = gsap.timeline({
            scrollTrigger: {
              trigger: splitArea,
              start: 'top 90%',
              end: 'bottom 60%',
              scrub: false,
              markers: false,
            }
          });
          const contentSplitted = new SplitText(splitArea, { type: "words, lines" });
          gsap.set(splitArea, { perspective: 400 });
          contentSplitted.split({ type: "lines" })
          trigger.from(contentSplitted.lines, { duration: 1, delay: 0.3, opacity: 0, rotationX: -75, force3D: true, transformOrigin: "top center -50", stagger: 0.1 });
        });
    
        // Visible Slowly From Bottom Animation 
        const visibleSlowlyBottom = document.querySelectorAll(".visible-slowly-bottom");
        function visibleSlowly() {
          visibleSlowlyBottom.forEach(splitArea => {
            if (splitArea.anim) {
              splitArea.anim.progress(1).kill();
              splitArea.split.revert();
            }
            splitArea.split = new SplitText(splitArea, {
              type: "lines,words,chars",
              linesClass: "split-line"
            });
            splitArea.anim = gsap.from(splitArea.split.chars, {
              scrollTrigger: {
                trigger: splitArea,
                toggleActions: "restart pause resume reverse",
                start: 'top 90%',
              },
              duration: 0.8,
              ease: "circ.out",
              y: 70,
              stagger: 0.02
            });
          });
        }
        ScrollTrigger.addEventListener("refresh", visibleSlowly);
        visibleSlowly();

        // image right to left 
        gsap.registerPlugin(ScrollTrigger);
            let revealContainers = document.querySelectorAll(".reveal-one");
            revealContainers.forEach((container) => {
            let image = container.querySelector(".reveal-image-one");
            let rts = gsap.timeline({
                scrollTrigger: {
                trigger: container,
                toggleActions: "restart none none reset",
                start: "top 90%",
                end: "top 0%",
                }
            });
            rts.set(container, {
                autoAlpha: 1
            });
            rts.from(container, 1.5, {
                xPercent: 100,
                ease: Power2.out
            });
            rts.from(image, 1.5, {
                xPercent: -100,
                scale: 1.3,
                delay: -1.5,
                ease: Power2.out
            });
        });

        // image left to right 
        let revealContainersSecond = document.querySelectorAll(".reveal-three");
        revealContainersSecond.forEach((container) => {
          let image = container.querySelector(".reveal-image-three");
          let rts = gsap.timeline({
            scrollTrigger: {
              trigger: container,
              toggleActions: "restart none none reset",
            }
          });
          rts.set(container, {
            autoAlpha: 1
          });
          rts.from(container, 1.5, {
            xPercent: -100,
            ease: Power2.out
          });
        });

        // reveal-third
        gsap.registerPlugin(ScrollTrigger);
        let revealContainersThird = document.querySelectorAll(".reveal-third");
        revealContainersThird.forEach((container) => {
          let image = container.querySelector(".reveal-image-third");
          let rts = gsap.timeline({
            scrollTrigger: {
              trigger: container,
              toggleActions: "restart none reset",
              start: "top 0%",
              end: "bottom 0%",
            }
          });

          rts.set(container, {
            autoAlpha: 1
          });
          rts.from(container, 1.5, {
            xPercent: 100,
            ease: Power2.out
          });
          rts.from(image, 1.5, {
            xPercent: -100,
            scale: 1.3,
            delay: -1.5,
            ease: Power2.out
          });
        });          

        // box-content
        const boxContent = document.querySelectorAll('.box-content')
        boxContent.forEach((el) => {
          const hoverContent = el.querySelector('.hover-content')
          el.addEventListener('mouseenter', (e) => {
            gsap.to(hoverContent, { autoAlpha: 1 })
          })
          el.addEventListener('mouseleave', (e) => {
            gsap.to(hoverContent, { autoAlpha: 0 })
          })
          el.addEventListener('mousemove', (e) => {
            gsap.set(hoverContent, {
              force3D: true,
              x: e.offsetX - 100, y: e.offsetY - 100 
            })
          })
        })

        // reveal-fourth
        let revealContainersFourth = document.querySelectorAll(".reveal-fourth");
        revealContainersFourth.forEach((container) => {
          let image = container.querySelector("img");
          let tl = gsap.timeline({
            scrollTrigger: {
              trigger: container,
              toggleActions: "restart none none reset"
            }
          });
          tl.set(container, { autoAlpha: 1 });
          tl.from(container, 1.5, {
            xPercent: 100,
            ease: Power2.out
          });
          tl.from(image, 1.5, {
            xPercent: -100,
            scale: 1.3,
            delay: -1.5,
            ease: Power2.out
          });
        });

      // sticky section
      if(document.querySelector(".sticky-area")){

        ScrollTrigger.matchMedia({
          "(min-width: 767px)": function() {
          
            let st = ScrollTrigger.create({
              trigger: ".sticky-wrapper",
              pin: ".sticky-area",
              start: "top center",
              end: "+=100",
            });

          },
        });

      }
      
      if(document.querySelector(".scroll-down-wrapper")){
        gsap.to(".scroll-down-circle", {
          y: -300,
          autoAlpha: 0,
          ease: "none",
          scrollTrigger: {
            trigger: ".scroll-down-circle-wrapper",
            start: "top 25%",
            end: "30% top",
            scrub: true,
            markers: false,
            duration: 15,
          },
        });
      }

      // vanilla tilt animation start
      // button Vivacity
      let btnVivacity = document.querySelectorAll(".btn-vivacity");
      if (btnVivacity) {
        VanillaTilt.init(btnVivacity, {
          max: 14,
          speed: 2800,
          perspective: 500,
        });
      }

      // img Vivacity
      let imgVivacity = document.querySelectorAll(".image-vivacity");
      if (imgVivacity) {
        VanillaTilt.init(imgVivacity, {
          max: 3,
          speed: 6800,
          perspective: 450,
        });
      }

      // content Vivacity
      let contentVivacity = document.querySelectorAll(".content-vivacity");
      if (contentVivacity) {
        VanillaTilt.init(contentVivacity, {
          max: 4,
          speed: 8000,
          perspective: 650,
        });
      }

      // content-sec Vivacity
      let contentSecVivacity = document.querySelectorAll(".content-sec-vivacity");
      if (contentSecVivacity) {
        VanillaTilt.init(contentSecVivacity, {
          max: 20,
          speed: 1000,
          perspective: 1000,
        });
      }


      // bannerCarousel
      let bannerCarousel = document.querySelector('.banner-carousel');
      if(bannerCarousel){
        const swiper = new Swiper(bannerCarousel, {
          loop: true,
          centeredSlides: true,
          paginationClickable: true,
          autoplay: {
            delay: 200000,
            disableOnInteraction: false,
          },
          spaceBetween: 0,
          slidesPerView: 1,
          paginationClickable: true,
          navigation: {
            nextEl: bannerCarousel.closest('section').querySelector('.ara-next'),
            prevEl: bannerCarousel.closest('section').querySelector('.ara-prev'),
          },
          pagination: {
            el: bannerCarousel.querySelector('.slider-pagination'),
            clickable: true,
          },
          breakpoints: {
            1700: {
                slidesPerView: 3,
            },
            1300: {
                slidesPerView: 2.1,
            },
            1200: {
                slidesPerView: 1.6,
            },
            1100: {
                slidesPerView: 2.1,
            },
            992: {
                slidesPerView: 1.9,
            },
            768: {
                slidesPerView: 1.8,
            },
            576: {
                slidesPerView: 1.6,
            },
            480: {
                slidesPerView: 1.4,
            },
          },
        });
      }

      // bannerSecondCarousel
      let bannerSecondCarousel = document.querySelector('.banner-second-carousel');
      if(bannerSecondCarousel){
        const swiper = new Swiper(bannerSecondCarousel, {
          loop: true,
          centeredSlides: true,
          paginationClickable: true,
          autoplay: {
            delay: 200000,
            disableOnInteraction: false,
          },
          spaceBetween: 24,
          slidesPerView: 1,
          paginationClickable: true,
          navigation: {
            nextEl: bannerSecondCarousel.closest('section').querySelector('.ara-next'),
            prevEl: bannerSecondCarousel.closest('section').querySelector('.ara-prev'),
          },
          pagination: {
            el: bannerSecondCarousel.querySelector('.slider-pagination'),
            clickable: true,
          },
        });
      }

      // popularCoupon
      let popularCouponCarousel = document.querySelector('.popular-coupon-carousel');
      if(popularCouponCarousel){
        const swiper = new Swiper(popularCouponCarousel, {
          loop: true,
          centeredSlides: true,
          paginationClickable: true,
          autoplay: {
            delay: 200000,
            disableOnInteraction: false,
          },
          spaceBetween: 24,
          slidesPerView: 1,
          paginationClickable: true,
          navigation: {
            nextEl: popularCouponCarousel.closest('section').querySelector('.ara-next'),
            prevEl: popularCouponCarousel.closest('section').querySelector('.ara-prev'),
          },
          breakpoints: {
            1400: {
                slidesPerView: 3,
            },
            1200: {
                slidesPerView: 2.8,
            },
            992: {
                slidesPerView: 2.4,
            },
            768: {
                slidesPerView: 1.8,
            },
            480: {
                slidesPerView: 1.4,
            },
          },
          pagination: {
            el: popularCouponCarousel.querySelector('.slider-pagination'),
            clickable: true,
          },
        });
      }

      // endingCoupon
      let endingCouponCarousel = document.querySelector('.ending-coupon-carousel');
      if(endingCouponCarousel){
        const swiper = new Swiper(endingCouponCarousel, {
          loop: true,
          centeredSlides: true,
          paginationClickable: true,
          autoplay: {
            delay: 200000,
            disableOnInteraction: false,
          },
          spaceBetween: 24,
          slidesPerView: 1,
          paginationClickable: true,
          navigation: {
            nextEl: endingCouponCarousel.closest('section').querySelector('.ara-next'),
            prevEl: endingCouponCarousel.closest('section').querySelector('.ara-prev'),
          },
          breakpoints: {
            1400: {
                slidesPerView: 3,
            },
            1200: {
                slidesPerView: 2.8,
            },
            992: {
                slidesPerView: 2.4,
            },
            768: {
                slidesPerView: 1.8,
            },
            480: {
                slidesPerView: 1.4,
            },
          },
          pagination: {
            el: endingCouponCarousel.querySelector('.slider-pagination'),
            clickable: true,
          },
        });
      }

      // customersFeedback
      let customersFeedbackCarousel = document.querySelector('.customers-feedback-carousel');
      if(customersFeedbackCarousel){
        const swiper = new Swiper(customersFeedbackCarousel, {
          loop: true,
          centeredSlides: true,
          paginationClickable: true,
          autoplay: {
            delay: 200000,
            disableOnInteraction: false,
          },
          spaceBetween: 0,
          slidesPerView: 1,
          paginationClickable: true,
          navigation: {
            nextEl: customersFeedbackCarousel.closest('section').querySelector('.ara-next'),
            prevEl: customersFeedbackCarousel.closest('section').querySelector('.ara-prev'),
          },
          breakpoints: {
            1400: {
                slidesPerView: 3,
            },
            1200: {
                slidesPerView: 2.5,
            },
            992: {
                slidesPerView: 2,
            },
            768: {
                slidesPerView: 1.6,
            },
            480: {
                slidesPerView: 1.4,
            },
          },
        });
      }

      // customersFeedback
      let customersFeedbackCarouselFourth = document.querySelector('.customers-feedback-carousel-fourth');
      const collapseSection = document.querySelector('.collapse-section');
      const sidebarToggle = document.querySelector('.sidebar-icon');
      if(customersFeedbackCarouselFourth && collapseSection){
        const normalBreakpoints = {
          1700: {
            slidesPerView: 3,
          },
          1500: {
            slidesPerView: 2.3,
          },
          1300: {
            slidesPerView: 2.0,
          },
          1200: {
            slidesPerView: 1.8,
          },
          992: {
            slidesPerView: 2,
          },
          768: {
            slidesPerView: 1.6,
          },
          480: {
            slidesPerView: 1.4,
          },
        };
        const collapsedBreakpoints = {
          1400: {
            slidesPerView: 3,
          },
          1200: {
            slidesPerView: 2.5,
          },
          992: {
            slidesPerView: 2,
          },
          768: {
            slidesPerView: 1.6,
          },
          480: {
            slidesPerView: 1.4,
          },
        };
        const swiper = new Swiper(customersFeedbackCarouselFourth, {
          loop: true,
          centeredSlides: true,
          paginationClickable: true,
          autoplay: {
            delay: 200000,
            disableOnInteraction: false,
          },
          spaceBetween: 24,
          slidesPerView: 1,
          paginationClickable: true,
          navigation: {
            nextEl: customersFeedbackCarouselFourth.closest('section').querySelector('.ara-next'),
            prevEl: customersFeedbackCarouselFourth.closest('section').querySelector('.ara-prev'),
          },
          breakpoints: normalBreakpoints,
        });
        let isCollapsed = false;
        if(sidebarToggle) {
          sidebarToggle.addEventListener('click', () => {
            isCollapsed = !isCollapsed;
            swiper.params.breakpoints = isCollapsed ? collapsedBreakpoints : normalBreakpoints;
            swiper.update();
            swiper.updateSize();
            swiper.updateSlides();
            swiper.updateProgress();
            swiper.updateSlidesClasses();
            swiper.slideTo(swiper.activeIndex, 0, false);
          });
        }
      }

      // customersFeedbackSecond
      let customersFeedbackSecondCarousel = document.querySelector('.customers-feedback-second-carousel');
      if(customersFeedbackSecondCarousel){
        const swiper = new Swiper(customersFeedbackSecondCarousel, {
          loop: true,
          centeredSlides: false,
          paginationClickable: true,
          autoplay: {
            delay: 200000,
            disableOnInteraction: false,
          },
          spaceBetween: 24,
          slidesPerView: 1,
          paginationClickable: true,
          navigation: {
            nextEl: customersFeedbackSecondCarousel.closest('section').querySelector('.ara-next'),
            prevEl: customersFeedbackSecondCarousel.closest('section').querySelector('.ara-prev'),
          },
          breakpoints: {
            1400: {
                slidesPerView: 2,
            },
            1200: {
                slidesPerView: 2.2,
                centeredSlides: true,
            },
            992: {
                slidesPerView: 1.8,
                centeredSlides: true,
            },
            768: {
                slidesPerView: 1.6,
                centeredSlides: true,
            },
            480: {
                slidesPerView: 1.3,
                centeredSlides: true,
            },
          },
        });
      }

      // customersFeedbackThird
      let customersFeedbackThirdCarousel = document.querySelector('.customers-feedback-third-carousel');
      if (customersFeedbackThirdCarousel) {
        const swiper = new Swiper(customersFeedbackThirdCarousel, {
          loop: true,
          centeredSlides: false,
          paginationClickable: true,
          autoplay: {
            delay: 200000,
            disableOnInteraction: false,
          },
          spaceBetween: 0,
          slidesPerView: 1,
          paginationClickable: true,
          navigation: {
            nextEl: null,
            prevEl: null,
          },
        });
        const nextButtons = customersFeedbackThirdCarousel.closest('section').querySelectorAll('.ara-next');
        nextButtons.forEach((nextButton) => {
          nextButton.addEventListener('click', () => {
            swiper.slideNext();
          });
        });
        const prevButtons = customersFeedbackThirdCarousel.closest('section').querySelectorAll('.ara-prev');
        prevButtons.forEach((prevButton) => {
          prevButton.addEventListener('click', () => {
            swiper.slidePrev();
          });
        });
      }      

      // cashbackIncreased
      let cashbackIncreasedCarousel = document.querySelector('.cashback-increased-carousel');
      if(cashbackIncreasedCarousel){
        const swiper = new Swiper(cashbackIncreasedCarousel, {
          loop: true,
          centeredSlides: true,
          paginationClickable: true,
          autoplay: {
            delay: 200000,
            disableOnInteraction: false,
          },
          spaceBetween: 24,
          slidesPerView: 1,
          paginationClickable: true,
          navigation: {
            nextEl: cashbackIncreasedCarousel.closest('section').querySelector('.ara-next'),
            prevEl: cashbackIncreasedCarousel.closest('section').querySelector('.ara-prev'),
          },
          breakpoints: {
            1400: {
                slidesPerView: 3,
            },
            1200: {
                slidesPerView: 3.2,
            },
            992: {
                slidesPerView: 2.8,
            },
            768: {
                slidesPerView: 2.2,
            },
            480: {
                slidesPerView: 1.6,
            },
          },
        });
      }

      // bestPartner
      let bestPartnerCarousel = document.querySelector('.best-partner-carousel');
      if(bestPartnerCarousel){
        const swiper = new Swiper(bestPartnerCarousel, {
          autoplay: true,
          slidesPerView: 'auto',
          spaceBetween: 20,
          loop: true,
          autoplay: {
            delay: 5,
            disableOnInteraction: false,
          },
          speed: 5000,
        });
      }

      /* Wow js */
      new WOW().init();

    });
});