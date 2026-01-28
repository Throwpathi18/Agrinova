const OfflineStore = {
    save: function(key, data) {
        const payload = {
            timestamp: new Date().getTime(),
            content: data
        };
        localStorage.setItem(key, JSON.stringify(payload));
    },

    get: function(key) {
        const raw = localStorage.getItem(key);
        if (!raw) return null;
        
        const data = JSON.parse(raw);
        // Data is considered fresh for 1 hour
        const hour = 60 * 60 * 1000;
        if (new Date().getTime() - data.timestamp > hour) {
            console.log(`Cache for ${key} expired.`);
        }
        return data.content;
    }
};

window.addEventListener('online', () => {
    document.getElementById('offline-indicator').style.display = 'none';
});

window.addEventListener('offline', () => {
    document.getElementById('offline-indicator').style.display = 'block';
});
