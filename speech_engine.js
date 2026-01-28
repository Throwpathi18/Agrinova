const SpeechEngine = {
    selectedLanguage: 'en-US',
    
    speak: function(text) {
        if (!'speechSynthesis' in window) {
            console.error("Speech Synthesis not supported");
            return;
        }

        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = this.selectedLanguage;
        utterance.rate = 0.9;
        utterance.pitch = 1;

        window.speechSynthesis.speak(utterance);
    },

    setLanguage: function(langCode) {
        this.selectedLanguage = langCode;
    }
};

// Available languages mapping
const languages = {
    'English': 'en-US',
    'Hindi': 'hi-IN',
    'Bengali': 'bn-IN',
    'Telugu': 'te-IN'
};
