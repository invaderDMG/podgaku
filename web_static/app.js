/**
 * Podgaku - Frontend Web Estático
 * Lee episodios directamente del RSS XML
 */
class PodcastViewer {
    constructor() {
        this.episodes = [];
        this.init();
    }

    async init() {
        await this.loadEpisodesFromRSS();
        this.renderEpisodes();
    }

    async loadEpisodesFromRSS() {
        try {
            // Cargar el RSS XML
            const response = await fetch('rss.xml');
            if (!response.ok) {
                throw new Error('Error al cargar el RSS');
            }
            
            const xmlText = await response.text();
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
            
            // Extraer episodios del RSS
            const items = xmlDoc.querySelectorAll('item');
            this.episodes = [];
            
            items.forEach((item, index) => {
                const title = item.querySelector('title')?.textContent || 'Sin título';
                const description = item.querySelector('description')?.textContent || '';
                const audioUrl = item.querySelector('enclosure')?.getAttribute('url') || '';
                const pubDate = item.querySelector('pubDate')?.textContent || '';
                const duration = item.querySelector('itunes\\:duration, duration')?.textContent || '';
                const episodeNumber = item.querySelector('itunes\\:episode, episode')?.textContent || '';
                const season = item.querySelector('itunes\\:season, season')?.textContent || '';
                
                // Extraer tracklist del contenido CDATA
                let tracklist = [];
                const contentEncoded = item.querySelector('content\\:encoded');
                if (contentEncoded) {
                    const content = contentEncoded.textContent;
                    // Buscar listas <ul><li>
                    const ulMatch = content.match(/<ul>(.*?)<\/ul>/s);
                    if (ulMatch) {
                        const liMatches = ulMatch[1].match(/<li>(.*?)<\/li>/g);
                        if (liMatches) {
                            tracklist = liMatches.map(li => li.replace(/<\/?li>/g, ''));
                        }
                    }
                }
                
                // Formatear fecha
                let formattedDate = '';
                if (pubDate) {
                    try {
                        formattedDate = new Date(pubDate).toLocaleDateString('es-ES');
                    } catch (e) {
                        formattedDate = pubDate;
                    }
                }
                
                this.episodes.push({
                    title,
                    description,
                    audio_url: audioUrl,
                    pub_date: pubDate,
                    formatted_date: formattedDate,
                    duration,
                    episode_number: episodeNumber,
                    season,
                    tracklist
                });
            });
            
            console.log(`✅ Cargados ${this.episodes.length} episodios del RSS`);
            
        } catch (error) {
            console.error('Error cargando RSS:', error);
            this.showNotification('Error al cargar los episodios del RSS', 'error');
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
                            <span><i class="fas fa-calendar"></i> ${episode.formatted_date}</span>
                            <span><i class="fas fa-clock"></i> ${episode.duration}</span>
                            ${episode.episode_number ? `<span><i class="fas fa-hashtag"></i> Episodio ${episode.episode_number}</span>` : ''}
                            ${episode.season ? `<span><i class="fas fa-tv"></i> Temporada ${episode.season}</span>` : ''}
                        </div>
                    </div>
                    <div class="episode-actions">
                        <button class="btn btn-small btn-outline" onclick="podcastViewer.playEpisode('${episode.audio_url}')">
                            <i class="fas fa-play"></i> Reproducir
                        </button>
                        <a href="${episode.audio_url}" download class="btn btn-small btn-secondary">
                            <i class="fas fa-download"></i> Descargar
                        </a>
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
        // Crear contenedor de notificaciones si no existe
        let notifications = document.getElementById('notifications');
        if (!notifications) {
            notifications = document.createElement('div');
            notifications.id = 'notifications';
            notifications.className = 'notifications';
            document.body.appendChild(notifications);
        }
        
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
