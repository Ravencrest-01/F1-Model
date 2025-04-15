// Utility Functions
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    document.body.appendChild(spinner);
}

function hideLoading() {
    const spinner = document.querySelector('.spinner');
    if (spinner) {
        spinner.remove();
    }
}

// API Calls
async function fetchRaceData(year, round) {
    try {
        const response = await fetch(`/api/races/${year}/${round}`);
        if (!response.ok) throw new Error('Race data not found');
        return await response.json();
    } catch (error) {
        console.error('Error fetching race data:', error);
        throw error;
    }
}

async function fetchDriverData(driverId) {
    try {
        const response = await fetch(`/api/drivers/${driverId}`);
        if (!response.ok) throw new Error('Driver data not found');
        return await response.json();
    } catch (error) {
        console.error('Error fetching driver data:', error);
        throw error;
    }
}

async function fetchUpcomingRace() {
    try {
        const response = await fetch('/api/upcoming');
        if (!response.ok) throw new Error('Upcoming race data not found');
        return await response.json();
    } catch (error) {
        console.error('Error fetching upcoming race data:', error);
        throw error;
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Add event listeners for navigation
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const href = link.getAttribute('href');
            window.location.href = href;
        });
    });

    // Add event listeners for race cards
    const raceCards = document.querySelectorAll('.race-card');
    raceCards.forEach(card => {
        card.addEventListener('click', () => {
            const year = card.dataset.year;
            const round = card.dataset.round;
            window.location.href = `/races/${year}/${round}`;
        });
    });

    // Add event listeners for driver cards
    const driverCards = document.querySelectorAll('.driver-card');
    driverCards.forEach(card => {
        card.addEventListener('click', () => {
            const driverId = card.dataset.driverId;
            window.location.href = `/drivers/${driverId}`;
        });
    });
});

// Error Handling
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    // You could show a user-friendly error message here
});

// Utility for handling API errors
function handleApiError(error) {
    console.error('API Error:', error);
    // You could show a user-friendly error message here
} 