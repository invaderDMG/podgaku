/**
 * Podgaku - Vista Pública
 * Solo muestra episodios, sin funcionalidades de administración
 */
class PodcastViewer {
    constructor() {
        this.episodes = [];
        this.init();
    }

    async init() {
        await this.loadEpisodes();
        this.renderEpisodes();
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
                        <button class="btn btn-small btn-outline" onclick="podcastViewer.playEpisode('${episode.audio_url}')">
                            <i class="fas fa-play"></i> Reproducir
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
        // Crear elemento de audio temporal para reproducir
        const audio = new Audio(audioUrl);
        audio.play().catch(error => {
            this.showNotification('Error al reproducir el episodio', 'error');
            console.error('Error:', error);
        });
    }

    showNotification(message, type = 'info') {
        const notifications = document.getElementById('notifications');
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;
        
        notifications.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.podcastViewer = new PodcastViewer();
});