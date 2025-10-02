/**
 * Podgaku - Panel de Administración
 * Funcionalidades completas de gestión de episodios
 */
class AdminManager {
    constructor() {
        this.episodes = [];
        this.currentFile = null;
        this.currentEpisodeIndex = null;
        this.init();
    }

    async init() {
        await this.loadEpisodes();
        this.renderEpisodes();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Upload area
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');

        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
        uploadArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
        uploadArea.addEventListener('drop', this.handleDrop.bind(this));

        fileInput.addEventListener('change', this.handleFileSelect.bind(this));

        // Form submission
        document.getElementById('episodeForm').addEventListener('submit', this.handleFormSubmit.bind(this));
    }

    async loadEpisodes() {
        try {
            const response = await fetch('/api/episodes');
            if (!response.ok) {
                throw new Error('Error al cargar episodios');
            }
            this.episodes = await response.json();
        } catch (error) {
            console.error('Error:', error);
            this.showNotification('Error al cargar los episodios', 'error');
        }
    }

    handleDragOver(e) {
        e.preventDefault();
        e.currentTarget.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.handleFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            this.handleFile(files[0]);
        }
    }

    handleFile(file) {
        if (!file.type.startsWith('audio/')) {
            this.showNotification('Por favor selecciona un archivo de audio', 'error');
            return;
        }

        this.currentFile = file;
        this.extractMetadata(file);
    }

    async extractMetadata(file) {
        try {
            // Simular extracción de metadatos (en un caso real usarías una librería como music-metadata)
            const duration = await this.getAudioDuration(file);
            
            // Pre-llenar formulario con datos del archivo
            document.getElementById('title').value = file.name.replace(/\.[^/.]+$/, "");
            document.getElementById('duration').value = this.formatDuration(duration);
            
            this.showMetadataSection();
            this.showNotification('Archivo cargado correctamente', 'success');
        } catch (error) {
            console.error('Error al extraer metadatos:', error);
            this.showNotification('Error al procesar el archivo', 'error');
        }
    }

    getAudioDuration(file) {
        return new Promise((resolve) => {
            const audio = new Audio();
            audio.addEventListener('loadedmetadata', () => {
                resolve(audio.duration);
            });
            audio.src = URL.createObjectURL(file);
        });
    }

    formatDuration(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }

    showMetadataSection() {
        document.getElementById('metadataSection').style.display = 'block';
        document.getElementById('metadataSection').scrollIntoView({ behavior: 'smooth' });
    }

    hideMetadataSection() {
        document.getElementById('metadataSection').style.display = 'none';
    }

    async handleFormSubmit(e) {
        e.preventDefault();

        const formData = new FormData(e.target);
        const tracklist = document.getElementById('tracklist').value
            .split('\n')
            .filter(track => track.trim() !== '');

        const episodeData = {
            title: formData.get('title'),
            description: formData.get('description'),
            duration: formData.get('duration'),
            episode_number: parseInt(formData.get('episodeNumber')) || null,
            season: parseInt(formData.get('season')) || null,
            tracklist: tracklist,
            audio_file: this.currentFile
        };

        try {
            await this.uploadEpisode(episodeData);
            this.showNotification('Episodio guardado correctamente', 'success');
            this.resetForm();
            await this.loadEpisodes();
            this.renderEpisodes();
        } catch (error) {
            console.error('Error al guardar episodio:', error);
            this.showNotification('Error al guardar el episodio', 'error');
        }
    }

    async uploadEpisode(episodeData) {
        const formData = new FormData();
        formData.append('title', episodeData.title);
        formData.append('description', episodeData.description);
        formData.append('duration', episodeData.duration);
        formData.append('episode_number', episodeData.episode_number || '');
        formData.append('season', episodeData.season || '');
        formData.append('tracklist', JSON.stringify(episodeData.tracklist));
        formData.append('audio_file', episodeData.audio_file);

        const response = await fetch('/api/episodes', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error al subir el episodio');
        }
    }

    resetForm() {
        document.getElementById('episodeForm').reset();
        document.getElementById('fileInput').value = '';
        this.currentFile = null;
        this.hideMetadataSection();
    }

    cancelUpload() {
        this.resetForm();
    }

    renderEpisodes() {
        const episodesList = document.getElementById('episodesList');
        
        if (this.episodes.length === 0) {
            episodesList.innerHTML = '<div class="loading">No hay episodios disponibles</div>';
            return;
        }

        episodesList.innerHTML = this.episodes.map((episode, index) => `
            <div class="episode-card">
                <div class="episode-header">
                    <div>
                        <div class="episode-title">${episode.title}</div>
                        <div class="episode-meta">
                            <span><i class="fas fa-calendar"></i> ${new Date(episode.pub_date).toLocaleDateString()}</span>
                            <span><i class="fas fa-clock"></i> ${episode.duration}</span>
                            ${episode.episode_number ? `<span><i class="fas fa-hashtag"></i> Episodio ${episode.episode_number}</span>` : ''}
                            ${episode.season ? `<span><i class="fas fa-tv"></i> Temporada ${episode.season}</span>` : ''}
                        </div>
                    </div>
                    <div class="episode-actions">
                        <button class="btn btn-small btn-outline" onclick="adminManager.playEpisode('${episode.audio_url}')">
                            <i class="fas fa-play"></i> Reproducir
                        </button>
                        <button class="btn btn-small btn-danger" onclick="adminManager.confirmDelete(${index})">
                            <i class="fas fa-trash"></i> Eliminar
                        </button>
                    </div>
                </div>
                <div class="episode-content">
                    <div class="episode-description">${episode.description.replace(/\n/g, '<br>')}</div>
                    ${episode.tracklist && episode.tracklist.length > 0 ? `
                        <div class="tracklist">
                            <h4><i class="fas fa-music"></i> Tracklist</h4>
                            <ul>
                                ${episode.tracklist.map(track => `<li>${track}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            </div>
        `).join('');
    }

    playEpisode(audioUrl) {
        const audio = new Audio(audioUrl);
        audio.play().catch(error => {
            this.showNotification('Error al reproducir el episodio', 'error');
            console.error('Error:', error);
        });
    }

    confirmDelete(index) {
        this.currentEpisodeIndex = index;
        document.getElementById('confirmModal').style.display = 'block';
    }

    async deleteEpisode() {
        if (this.currentEpisodeIndex === null) return;

        try {
            const episode = this.episodes[this.currentEpisodeIndex];
            const response = await fetch(`/api/episodes/${episode.id}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Error al eliminar el episodio');
            }

            this.showNotification('Episodio eliminado correctamente', 'success');
            this.closeModal();
            await this.loadEpisodes();
            this.renderEpisodes();
        } catch (error) {
            console.error('Error al eliminar episodio:', error);
            this.showNotification('Error al eliminar el episodio', 'error');
        }
    }

    closeModal() {
        document.getElementById('confirmModal').style.display = 'none';
        this.currentEpisodeIndex = null;
    }

    showNotification(message, type = 'info') {
        const notifications = document.getElementById('notifications');
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;
        
        notifications.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.adminManager = new AdminManager();
});
