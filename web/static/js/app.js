// Voice Assistant Web App
class VoiceAssistant {
    constructor() {
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.lastUserMessage = null;
        // Backend API URL - defaults to port 8000, can be overridden
        this.apiBaseUrl = window.API_BASE_URL || 'http://localhost:8000';
        
        this.initializeElements();
        this.setupEventListeners();
        this.checkMicrophonePermission();
        this.checkBackendConnection().catch(err => {
            console.warn('Initial backend check failed:', err);
        });
    }

    initializeElements() {
        this.recordBtn = document.getElementById('recordBtn');
        this.textInput = document.getElementById('textInput');
        this.sendTextBtn = document.getElementById('sendTextBtn');
        this.conversation = document.getElementById('conversation');
        this.recordingIndicator = document.getElementById('recordingIndicator');
        this.audioPlayer = document.getElementById('audioPlayer');
        this.connectionStatusSidebar = document.getElementById('connectionStatusSidebar');
        this.statusIndicator = document.getElementById('statusIndicator');
        this.connectionText = document.getElementById('connectionText');
    }

    setupEventListeners() {
        this.recordBtn.addEventListener('click', () => this.toggleRecording());
        this.sendTextBtn.addEventListener('click', () => this.sendTextMessage());
        this.textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendTextMessage();
            }
        });
    }

    async checkMicrophonePermission() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            stream.getTracks().forEach(track => track.stop());
            console.log('Microphone permission granted');
        } catch (error) {
            console.error('Microphone permission error:', error);
        }
    }

    async toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            await this.startRecording();
        }
    }

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    sampleRate: 16000,
                    channelCount: 1,
                    echoCancellation: true,
                    noiseSuppression: true
                }
            });

            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus'
            });

            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };

            this.mediaRecorder.onstop = () => {
                this.processRecording();
                stream.getTracks().forEach(track => track.stop());
            };

            this.mediaRecorder.start();
            this.isRecording = true;
            this.updateRecordingUI(true);

        } catch (error) {
            console.error('Error starting recording:', error);
            alert('Please allow microphone access to use voice recording.');
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            this.updateRecordingUI(false);
        }
    }

    async processRecording() {
        try {
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm;codecs=opus' });
            
            // Check if we have audio data
            if (audioBlob.size === 0) {
                throw new Error('No audio data recorded');
            }
            
            // Convert WebM to WAV format for backend compatibility
            const wavBlob = await this.convertToWav(audioBlob);
            
            // Check backend connection before sending
            await this.checkBackendConnection();
            
            // Show loading indicator
            const loadingId = this.showLoadingMessage();
            
            try {
                await this.sendVoiceMessage(wavBlob);
            } finally {
                // Remove loading indicator
                this.removeLoadingMessage(loadingId);
            }
        } catch (error) {
            console.error('Error processing recording:', error);
            const errorMsg = error.message || 'Unknown error occurred';
            this.removeLoadingMessage(); // Remove any loading messages
            this.addMessage('assistant', `Sorry, I encountered an error processing your voice: ${errorMsg}. Please try again.`);
        }
    }

    async convertToWav(audioBlob) {
        // For simplicity, we'll send WebM format
        // The backend Whisper model can handle various formats
        // If backend requires WAV, we'd need to use AudioContext to convert
        return audioBlob;
    }

    async sendVoiceMessage(audioBlob) {
        try {
            const formData = new FormData();
            formData.append('audio_file', audioBlob, 'recording.webm');

            const response = await fetch(`${this.apiBaseUrl}/api/voice/transcribe`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorText = await response.text();
                let errorMessage = `HTTP error! status: ${response.status}`;
                try {
                    const errorJson = JSON.parse(errorText);
                    errorMessage = errorJson.detail || errorMessage;
                } catch (e) {
                    errorMessage = errorText || errorMessage;
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();
            this.handleResponse(data);

        } catch (error) {
            console.error('Error sending voice message:', error);
            const errorMsg = error.message || 'Unknown error occurred';
            this.addMessage('assistant', `Sorry, I encountered an error: ${errorMsg}. Please check the console for details.`);
        }
    }

    async sendTextMessage() {
        const text = this.textInput.value.trim();
        if (!text) return;

        // Add user message to conversation
        this.addMessage('user', text);
        this.lastUserMessage = text;
        this.textInput.value = '';

        // Show loading indicator
        const loadingId = this.showLoadingMessage();

        try {
            // First check if backend is reachable
            await this.checkBackendConnection();

            const response = await fetch(`${this.apiBaseUrl}/api/text/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) {
                const errorText = await response.text();
                let errorMessage = `HTTP error! status: ${response.status}`;
                try {
                    const errorJson = JSON.parse(errorText);
                    errorMessage = errorJson.detail || errorMessage;
                } catch (e) {
                    errorMessage = errorText || errorMessage;
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();
            this.handleResponse(data);

        } catch (error) {
            console.error('Error sending text message:', error);
            const errorMsg = error.message || 'Unknown error occurred';
            
            // Check for common errors
            if (errorMsg.includes('Failed to fetch') || errorMsg.includes('NetworkError')) {
                this.addMessage('assistant', `Cannot connect to backend at ${this.apiBaseUrl}. Please make sure the backend server is running on port 8000.`);
            } else {
                this.addMessage('assistant', `Sorry, I encountered an error: ${errorMsg}. Please check the console for details.`);
            }
        } finally {
            // Remove loading indicator
            this.removeLoadingMessage(loadingId);
        }
    }

    async checkBackendConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            if (!response.ok) {
                throw new Error(`Backend health check failed: ${response.status}`);
            }
            const data = await response.json();
            console.log('Backend connection OK:', data);
            this.updateConnectionStatus('connected', 'Connected');
            return true;
        } catch (error) {
            console.error('Backend connection check failed:', error);
            this.updateConnectionStatus('disconnected', 'Disconnected');
            throw new Error(`Cannot reach backend at ${this.apiBaseUrl}. Is the server running?`);
        }
    }

    updateConnectionStatus(status, message) {
        if (!this.statusIndicator || !this.connectionText) return;
        
        this.statusIndicator.classList.remove('connected', 'disconnected');
        
        if (status === 'connected') {
            this.statusIndicator.classList.add('connected');
            this.connectionText.textContent = 'Connected';
        } else if (status === 'disconnected') {
            this.statusIndicator.classList.add('disconnected');
            this.connectionText.textContent = 'Disconnected';
        } else {
            this.connectionText.textContent = 'Connecting...';
        }
    }

    handleResponse(data) {
        // For voice messages, add the transcribed text as user message
        // For text messages, user message is already added
        if (data.text && !this.lastUserMessage) {
            this.addMessage('user', data.text);
        }

        // Add assistant response
        this.addMessage('assistant', data.response, data.intent, data.audio_url);
        
        this.updateConnectionStatus('connected', 'Connected');
        this.lastUserMessage = null; // Reset
    }

    addMessage(type, text, intent = null, audioUrl = null) {
        // Remove welcome message if it exists
        const welcomeMsg = this.conversation.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;

        // Avatar
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.textContent = type === 'user' ? 'U' : 'AI';
        messageDiv.appendChild(avatarDiv);

        // Content
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        // Header with author and timestamp
        const headerDiv = document.createElement('div');
        headerDiv.className = 'message-header';
        
        const authorSpan = document.createElement('span');
        authorSpan.className = 'message-author';
        authorSpan.textContent = type === 'user' ? 'You' : 'Assistant';
        headerDiv.appendChild(authorSpan);

        const timestampSpan = document.createElement('span');
        timestampSpan.className = 'message-timestamp';
        timestampSpan.textContent = this.getCurrentTime();
        headerDiv.appendChild(timestampSpan);

        if (intent && type === 'assistant') {
            const badge = document.createElement('span');
            badge.className = 'intent-badge';
            badge.textContent = intent;
            headerDiv.appendChild(badge);
        }

        contentDiv.appendChild(headerDiv);

        // Message text
        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.textContent = text;
        contentDiv.appendChild(textDiv);

        // Audio action button
        if (audioUrl && type === 'assistant') {
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'message-actions';
            
            const playBtn = document.createElement('button');
            playBtn.className = 'action-btn';
            playBtn.innerHTML = '🔊 Play Audio';
            playBtn.onclick = () => this.playAudio(audioUrl);
            
            actionsDiv.appendChild(playBtn);
            contentDiv.appendChild(actionsDiv);
        }

        messageDiv.appendChild(contentDiv);
        this.conversation.appendChild(messageDiv);
        
        // Scroll to bottom
        this.conversation.scrollTop = this.conversation.scrollHeight;
    }

    getCurrentTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        return `Today at ${hours}:${minutes}`;
    }

    showLoadingMessage() {
        // Remove welcome message if it exists
        const welcomeMsg = this.conversation.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }

        const loadingId = 'loading-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.id = loadingId;
        messageDiv.className = 'message assistant loading-message';

        // Avatar
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.textContent = 'AI';
        messageDiv.appendChild(avatarDiv);

        // Content
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        // Header
        const headerDiv = document.createElement('div');
        headerDiv.className = 'message-header';
        
        const authorSpan = document.createElement('span');
        authorSpan.className = 'message-author';
        authorSpan.textContent = 'Assistant';
        headerDiv.appendChild(authorSpan);

        const timestampSpan = document.createElement('span');
        timestampSpan.className = 'message-timestamp';
        timestampSpan.textContent = this.getCurrentTime();
        headerDiv.appendChild(timestampSpan);

        contentDiv.appendChild(headerDiv);

        // Loading text with animation
        const textDiv = document.createElement('div');
        textDiv.className = 'message-text loading-text';
        textDiv.innerHTML = '<span class="loading-dots"><span>.</span><span>.</span><span>.</span></span>';
        contentDiv.appendChild(textDiv);

        messageDiv.appendChild(contentDiv);
        this.conversation.appendChild(messageDiv);
        
        // Scroll to bottom
        this.conversation.scrollTop = this.conversation.scrollHeight;

        return loadingId;
    }

    removeLoadingMessage(loadingId = null) {
        if (loadingId) {
            const loadingMsg = document.getElementById(loadingId);
            if (loadingMsg) {
                loadingMsg.remove();
            }
        } else {
            // Remove any loading message
            const loadingMsgs = this.conversation.querySelectorAll('.loading-message');
            loadingMsgs.forEach(msg => msg.remove());
        }
    }

    playAudio(audioUrl) {
        const fullUrl = `${this.apiBaseUrl}${audioUrl}`;
        this.audioPlayer.src = fullUrl;
        this.audioPlayer.play().catch(error => {
            console.error('Error playing audio:', error);
        });
    }

    updateRecordingUI(isRecording) {
        if (isRecording) {
            this.recordBtn.classList.add('recording');
            this.recordingIndicator.classList.remove('hidden');
        } else {
            this.recordBtn.classList.remove('recording');
            this.recordingIndicator.classList.add('hidden');
        }
    }

    updateStatus(type, message) {
        // Status updates are now handled through connection status in sidebar
        // and inline status messages if needed
        console.log(`Status: ${type} - ${message}`);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VoiceAssistant();
});

