document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll('#eventTabs .tab-button'); // CHANGED
    const cards = document.querySelectorAll('.event-card');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const category = tab.getAttribute('data-category');

            cards.forEach(card => {
                if (category === 'all' || card.getAttribute('data-type') === category) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
});