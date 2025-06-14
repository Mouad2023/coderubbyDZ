document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);

    themeToggle.addEventListener('click', () => {
        const newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // History Management (only for index.html)
    if (document.getElementById('history-content')) {
        const historyContent = document.getElementById('history-items');
        const clearHistoryBtn = document.getElementById('clear-history');
        const toggleHistoryBtn = document.getElementById('toggle-history');
        const historyGrid = document.querySelector('.history-grid');
        const modal = document.getElementById('history-modal');
        const modalClose = document.getElementById('modal-close');
        const modalPrompt = document.getElementById('modal-prompt');
        const modalResponse = document.getElementById('modal-response');

        // Toggle collapsible history
        toggleHistoryBtn.addEventListener('click', () => {
            historyGrid.classList.toggle('collapsed');
            toggleHistoryBtn.classList.toggle('collapsed');
        });

        function loadHistory() {
            const history = JSON.parse(localStorage.getItem('promptHistory') || '[]');
            historyContent.innerHTML = '';
            history.forEach((item, index) => {
                const historyItem = document.createElement('div');
                historyItem.className = 'history-item';
                historyItem.innerHTML = `
                    <h3>Prompt #${index + 1}</h3>
                    <p>${item.prompt.substring(0, 50)}${item.prompt.length > 50 ? '...' : ''}</p>
                `;
                historyItem.addEventListener('click', () => {
                    modalPrompt.textContent = item.prompt;
                    modalResponse.textContent = item.response;
                    modal.classList.add('active');
                });
                historyContent.appendChild(historyItem);
            });
        }

        function addToHistory(prompt, response) {
            const history = JSON.parse(localStorage.getItem('promptHistory') || '[]');
            history.push({ prompt, response, timestamp: new Date().toLocaleString() });
            localStorage.setItem('promptHistory', JSON.stringify(history));
            loadHistory();
        }

        clearHistoryBtn.addEventListener('click', () => {
            localStorage.removeItem('promptHistory');
            loadHistory();
        });

        modalClose.addEventListener('click', () => {
            modal.classList.remove('active');
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });

        // Load history on page load
        loadHistory();

        // Add new response to history if present
        const responseElement = document.querySelector('.response-card');
        if (responseElement) {
            const prompt = responseElement.querySelector('.prompt-text').textContent;
            const response = responseElement.querySelector('code').textContent;
            addToHistory(prompt, response);
        }
    }
});