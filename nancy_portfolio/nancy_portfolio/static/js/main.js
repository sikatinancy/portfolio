document.addEventListener("DOMContentLoaded", () => {

    /* ========================================================
       MOBILE MENU
       ======================================================== */

    const menuButton =
        document.getElementById("mobile-menu-button");

    const mobileMenu =
        document.getElementById("mobile-menu");

    if (menuButton && mobileMenu) {

        menuButton.addEventListener("click", () => {

            mobileMenu.classList.toggle("hidden");

        });

    }


    /* ========================================================
       SCROLL REVEAL
       ======================================================== */

    const revealElements =
        document.querySelectorAll(".reveal");

    const revealObserver =
        new IntersectionObserver(
            (entries) => {

                entries.forEach((entry) => {

                    if (entry.isIntersecting) {

                        entry.target.classList.add("visible");

                        revealObserver.unobserve(
                            entry.target
                        );

                    }

                });

            },
            {
                threshold: 0.15,
            }
        );

    revealElements.forEach((element) => {

        revealObserver.observe(element);

    });


    /* ========================================================
       NAVBAR SCROLL
       ======================================================== */

    const header =
        document.getElementById("site-header");

    if (header) {

        window.addEventListener("scroll", () => {

            if (window.scrollY > 50) {

                header.classList.add(
                    "shadow-2xl"
                );

            } else {

                header.classList.remove(
                    "shadow-2xl"
                );

            }

        });

    }

});