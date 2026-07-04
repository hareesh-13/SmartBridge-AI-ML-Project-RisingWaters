document.addEventListener('DOMContentLoaded', () => {
    // Scroll Progress Indicator
    const progressBar = document.getElementById('scrollProgress');
    
    window.addEventListener('scroll', () => {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        if (progressBar) {
            progressBar.style.width = scrolled + '%';
        }

        // Back-to-Top visibility
        const backToTop = document.getElementById('backToTop');
        if (backToTop) {
            if (winScroll > 300) {
                backToTop.style.display = 'flex';
            } else {
                backToTop.style.display = 'none';
            }
        }
    });

    // Smooth scroll for Back-to-Top
    const backToTopBtn = document.getElementById('backToTop');
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Number counter animation for statistics cards
    const counters = document.querySelectorAll('.stat-number');
    const speed = 100; // Lower is faster

    const startCounters = () => {
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const isPercent = counter.getAttribute('data-percent') === 'true';
            
            const updateCount = () => {
                const count = +counter.innerText.replace('%', '');
                const inc = target / speed;

                if (count < target) {
                    const nextVal = Math.min(target, count + inc);
                    if (isPercent) {
                        counter.innerText = nextVal.toFixed(2) + '%';
                    } else {
                        counter.innerText = Math.ceil(nextVal);
                    }
                    setTimeout(updateCount, 15);
                } else {
                    if (isPercent) {
                        counter.innerText = target.toFixed(2) + '%';
                    } else {
                        counter.innerText = target;
                    }
                }
            };
            updateCount();
        });
    };

    // Trigger counters only when visible on viewport
    if (counters.length > 0) {
        const observerOptions = {
            threshold: 0.5
        };
        const statsObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    startCounters();
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        const statsSection = document.querySelector('.stats-section');
        if (statsSection) {
            statsObserver.observe(statsSection);
        }
    }

    // Prediction Form validation & loading indicator
    const predictForm = document.getElementById('predictForm');
    const loadingOverlay = document.getElementById('loadingOverlay');

    if (predictForm) {
        predictForm.addEventListener('submit', (e) => {
            // Form is valid, show loader
            if (predictForm.checkValidity()) {
                if (loadingOverlay) {
                    loadingOverlay.style.display = 'flex';
                }
            }
        });
    }

    // Dynamic scroll spy for highlighting navigation links
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= (sectionTop - 150)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href && (href === `#${current}` || href.endsWith(`#${current}`))) {
                link.classList.add('active');
            }
        });
    });
});
