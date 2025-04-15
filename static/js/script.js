const themeToggle = () => {
    // Add toggle button
    const navbar = document.querySelector('.navbar .container-fluid');
    const toggleButton = document.createElement('button');
    toggleButton.className = 'btn btn-outline-primary ms-2';
    toggleButton.id = 'theme-toggle';
    toggleButton.innerHTML = '🌓';
    navbar.insertBefore(toggleButton, navbar.firstChild.nextSibling);

    // Theme management
    const getTheme = () => localStorage.getItem('theme') || 'light';
    
    const setTheme = (theme) => {
        document.documentElement.setAttribute('data-bs-theme', theme);
        
        // Footer specific styling
        const footer = document.querySelector('[data-theme-footer]');
        if (theme === 'dark') {
            footer.classList.remove('bg-light');
            footer.classList.add('bg-dark', 'text-light');
            footer.style.backgroundColor = '#212529';
        } else {
            footer.classList.remove('bg-dark', 'text-light');
            footer.classList.add('bg-light');
            footer.style.backgroundColor = '#f8f9fa';
        }
        
        // Store theme preference
        localStorage.setItem('theme', theme);
    };

    // Initialize theme
    setTheme(getTheme());

    // Toggle event
    toggleButton.addEventListener('click', () => {
        const currentTheme = getTheme();
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', themeToggle);
