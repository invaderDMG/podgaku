/**
 * Podgaku - Frontend Web Estático
 * Lee episodios directamente del RSS XML
 */
class PodcastViewer {
    constructor() {
        this.episodes = [];
        this.filteredEpisodes = [];
        this.currentFilter = 'all';
        this.initializeNavigation();
        this.init();
    }

    initializeNavigation() {
        // Añadir event listeners a los botones de navegación
        const navButtons = document.querySelectorAll('.nav-btn');
        navButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const filter = e.currentTarget.dataset.filter;
                this.filterEpisodes(filter);
                this.updateActiveNavButton(e.currentTarget);
            });
        });
    }

    updateActiveNavButton(activeButton) {
        // Remover clase active de todos los botones
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        // Añadir clase active al botón clickeado
        activeButton.classList.add('active');
    }

    filterEpisodes(filter) {
        this.currentFilter = filter;
        
        if (filter === 'all') {
            this.filteredEpisodes = [...this.episodes];
        } else {
            const seasonNumber = parseInt(filter);
            this.filteredEpisodes = this.episodes.filter(episode => 
                episode.season === seasonNumber
            );
        }
        
        this.renderEpisodes();
        this.updateSectionTitle(filter);
        this.updateEpisodeCount();
    }

    updateSectionTitle(filter) {
        const sectionTitle = document.getElementById('sectionTitle');
        if (filter === 'all') {
            sectionTitle.innerHTML = '<i class="fas fa-headphones"></i> Todos los episodios';
        } else {
            sectionTitle.innerHTML = `<i class="fas fa-play"></i> Temporada ${filter}`;
        }
    }

    updateEpisodeCount() {
        const countElement = document.getElementById('episodeCount');
        const count = this.filteredEpisodes.length;
        countElement.textContent = `${count} episodio${count !== 1 ? 's' : ''}`;
    }

    async init() {
        await this.loadEpisodesFromRSS();
        // Inicializar con todos los episodios
        this.filteredEpisodes = [...this.episodes];
        this.renderEpisodes();
        this.updateEpisodeCount();
    }

    async loadEpisodesFromRSS() {
        try {
            // Cargar el RSS XML
            const response = await fetch('rss.xml');
            if (!response.ok) {
                throw new Error(`Error al cargar el RSS: ${response.status} ${response.statusText}`);
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
                const durationRaw = item.querySelector('itunes\\:duration, duration')?.textContent || '';
                const duration = this.formatDuration(durationRaw);
                const episodeNumber = parseInt(item.querySelector('itunes\\:episode, episode')?.textContent) || null;
                const season = parseInt(item.querySelector('itunes\\:season, season')?.textContent) || null;
                
                
                // Extraer tracklist del contenido CDATA
                let tracklist = [];
                
                // Probar diferentes selectores para content:encoded
                let contentEncoded = item.querySelector('content\\:encoded');
                if (!contentEncoded) {
                    contentEncoded = item.getElementsByTagName('content:encoded')[0];
                }
                if (!contentEncoded) {
                    contentEncoded = item.querySelector('[*|encoded]');
                }
                if (!contentEncoded) {
                    // Buscar por nombre de tag directamente
                    const allElements = item.getElementsByTagName('*');
                    for (let el of allElements) {
                        if (el.tagName === 'content:encoded' || el.localName === 'encoded') {
                            contentEncoded = el;
                            break;
                        }
                    }
                }
                
                if (contentEncoded) {
                    let content = contentEncoded.textContent;
                    // Decodificar entidades HTML
                    content = content.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
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
            
            
        } catch (error) {
            console.error('Error cargando RSS:', error);
            this.showNotification('Error al cargar los episodios del RSS', 'error');
        }
    }

    renderEpisodes() {
        const episodesList = document.getElementById('episodesList');
        
        if (this.filteredEpisodes.length === 0) {
            episodesList.innerHTML = '<div class="loading">No hay episodios disponibles</div>';
            return;
        }

        episodesList.innerHTML = this.filteredEpisodes.map((episode, index) => `
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

    formatDuration(duration) {
        if (!duration) return '';
        
        // Si ya está en formato mm:ss o hh:mm:ss, devolverlo tal como está
        if (duration.includes(':')) {
            return duration;
        }
        
        // Si está en segundos, convertir a mm:ss
        const totalSeconds = parseInt(duration);
        if (isNaN(totalSeconds)) return duration;
        
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
        
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.podcastViewer = new PodcastViewer();
});

// Backup: inicializar inmediatamente si el DOM ya está listo
if (document.readyState !== 'loading') {
    window.podcastViewer = new PodcastViewer();
}
