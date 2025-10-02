/**
 * Podgaku - Panel de Administración Web Estático
 */
class AdminViewer {
    constructor() {
        this.episodes = [];
        this.podcastInfo = {};
        this.init();
    }

    async init() {
        await this.loadPodcastData();
        this.renderPodcastInfo();
        this.renderStats();
        this.renderEpisodes();
    }

    async loadPodcastData() {
        try {
            const response = await fetch('rss.xml');
            if (!response.ok) {
                throw new Error('Error al cargar el RSS');
            }
            
            const xmlText = await response.text();
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
            
            // Extraer información del podcast
            const channel = xmlDoc.querySelector('channel');
            this.podcastInfo = {
                title: channel.querySelector('title')?.textContent || '',
                description: channel.querySelector('description')?.textContent || '',
                language: channel.querySelector('language')?.textContent || '',
                author: channel.querySelector('itunes\\:author, author')?.textContent || '',
                email: channel.querySelector('itunes\\:email, email')?.textContent || '',
                website: channel.querySelector('link')?.textContent || '',
                image: channel.querySelector('itunes\\:image, image')?.getAttribute('href') || '',
                lastBuildDate: channel.querySelector('lastBuildDate')?.textContent || '',
                generator: channel.querySelector('generator')?.textContent || ''
            };
            
            // Extraer episodios
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
                
                // Extraer tracklist
                let tracklist = [];
                const contentEncoded = item.querySelector('content\\:encoded');
                if (contentEncoded) {
                    const content = contentEncoded.textContent;
                    const ulMatch = content.match(/<ul>(.*?)<\/ul>/s);
                    if (ulMatch) {
                        const liMatches = ulMatch[1].match(/<li>(.*?)<\/li>/g);
                        if (liMatches) {
                            tracklist = liMatches.map(li => li.replace(/<\/?li>/g, ''));
                        }
                    }
                }
                
                this.episodes.push({
                    title,
                    description,
                    audio_url: audioUrl,
                    pub_date: pubDate,
                    duration,
                    episode_number: episodeNumber,
                    season,
                    tracklist
                });
            });
            
        } catch (error) {
            console.error('Error cargando datos:', error);
        }
    }

    renderPodcastInfo() {
        const infoContainer = document.getElementById('podcastInfo');
        
        infoContainer.innerHTML = `
            <div class="info-grid">
                <div class="info-card">
                    <h4><i class="fas fa-podcast"></i> Información General</h4>
                    <div class="info-item">
                        <strong>Título:</strong> ${this.podcastInfo.title}
                    </div>
                    <div class="info-item">
                        <strong>Autor:</strong> ${this.podcastInfo.author}
                    </div>
                    <div class="info-item">
                        <strong>Email:</strong> ${this.podcastInfo.email}
                    </div>
                    <div class="info-item">
                        <strong>Idioma:</strong> ${this.podcastInfo.language}
                    </div>
                    <div class="info-item">
                        <strong>Sitio web:</strong> <a href="${this.podcastInfo.website}" target="_blank">${this.podcastInfo.website}</a>
                    </div>
                </div>
                
                <div class="info-card">
                    <h4><i class="fas fa-rss"></i> RSS Feed</h4>
                    <div class="info-item">
                        <strong>URL del RSS:</strong> 
                        <a href="rss.xml" target="_blank">https://podgaku.jdlcgarcia.es/rss.xml</a>
                    </div>
                    <div class="info-item">
                        <strong>Última actualización:</strong> ${new Date(this.podcastInfo.lastBuildDate).toLocaleString('es-ES')}
                    </div>
                    <div class="info-item">
                        <strong>Generador:</strong> ${this.podcastInfo.generator}
                    </div>
                </div>
            </div>
            
            <div class="info-card description-card">
                <h4><i class="fas fa-align-left"></i> Descripción</h4>
                <p>${this.podcastInfo.description}</p>
            </div>
        `;
    }

    renderStats() {
        const statsContainer = document.getElementById('podcastStats');
        
        // Calcular estadísticas
        const totalEpisodes = this.episodes.length;
        const totalDuration = this.calculateTotalDuration();
        const averageDuration = this.calculateAverageDuration();
        const episodesWithTracklist = this.episodes.filter(ep => ep.tracklist && ep.tracklist.length > 0).length;
        const totalTracks = this.episodes.reduce((total, ep) => total + (ep.tracklist ? ep.tracklist.length : 0), 0);
        
        // Episodio más reciente
        const latestEpisode = this.episodes.length > 0 ? this.episodes[0] : null;
        
        statsContainer.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">${totalEpisodes}</div>
                    <div class="stat-label"><i class="fas fa-headphones"></i> Total Episodios</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-number">${totalDuration}</div>
                    <div class="stat-label"><i class="fas fa-clock"></i> Duración Total</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-number">${averageDuration}</div>
                    <div class="stat-label"><i class="fas fa-chart-line"></i> Duración Promedio</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-number">${totalTracks}</div>
                    <div class="stat-label"><i class="fas fa-music"></i> Total Canciones</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-number">${episodesWithTracklist}</div>
                    <div class="stat-label"><i class="fas fa-list-music"></i> Con Tracklist</div>
                </div>
                
                ${latestEpisode ? `
                <div class="stat-card latest-episode">
                    <div class="stat-label"><i class="fas fa-star"></i> Último Episodio</div>
                    <div class="stat-text">${latestEpisode.title}</div>
                    <div class="stat-date">${new Date(latestEpisode.pub_date).toLocaleDateString('es-ES')}</div>
                </div>
                ` : ''}
            </div>
        `;
    }

    renderEpisodes() {
        const episodesList = document.getElementById('episodesList');
        
        if (this.episodes.length === 0) {
            episodesList.innerHTML = '<div class="loading">No hay episodios disponibles</div>';
            return;
        }

        episodesList.innerHTML = this.episodes.map((episode, index) => `
            <div class="episode-card admin-episode">
                <div class="episode-header">
                    <div>
                        <div class="episode-title">${episode.title}</div>
                        <div class="episode-meta">
                            <span><i class="fas fa-calendar"></i> ${new Date(episode.pub_date).toLocaleDateString('es-ES')}</span>
                            <span><i class="fas fa-clock"></i> ${episode.duration}</span>
                            ${episode.episode_number ? `<span><i class="fas fa-hashtag"></i> Episodio ${episode.episode_number}</span>` : ''}
                            ${episode.season ? `<span><i class="fas fa-tv"></i> Temporada ${episode.season}</span>` : ''}
                        </div>
                    </div>
                    <div class="episode-actions">
                        <a href="${episode.audio_url}" target="_blank" class="btn btn-small btn-outline">
                            <i class="fas fa-external-link-alt"></i> Ver Archivo
                        </a>
                    </div>
                </div>
                <div class="episode-content">
                    <div class="episode-description">${episode.description.replace(/\n/g, '<br>')}</div>
                    ${episode.tracklist && episode.tracklist.length > 0 ? `
                        <div class="tracklist">
                            <h4><i class="fas fa-music"></i> Tracklist (${episode.tracklist.length} canciones)</h4>
                            <ul>
                                ${episode.tracklist.map(track => `<li>${track}</li>`).join('')}
                            </ul>
                        </div>
                    ` : '<div class="no-tracklist"><i class="fas fa-exclamation-triangle"></i> Sin tracklist</div>'}
                </div>
            </div>
        `).join('');
    }

    calculateTotalDuration() {
        let totalMinutes = 0;
        
        this.episodes.forEach(episode => {
            if (episode.duration) {
                const parts = episode.duration.split(':');
                if (parts.length === 2) {
                    totalMinutes += parseInt(parts[0]) + (parseInt(parts[1]) / 60);
                } else if (parts.length === 3) {
                    totalMinutes += parseInt(parts[0]) * 60 + parseInt(parts[1]) + (parseInt(parts[2]) / 60);
                }
            }
        });
        
        const hours = Math.floor(totalMinutes / 60);
        const minutes = Math.floor(totalMinutes % 60);
        
        return `${hours}h ${minutes}m`;
    }

    calculateAverageDuration() {
        if (this.episodes.length === 0) return '0m';
        
        let totalMinutes = 0;
        let validEpisodes = 0;
        
        this.episodes.forEach(episode => {
            if (episode.duration) {
                const parts = episode.duration.split(':');
                if (parts.length === 2) {
                    totalMinutes += parseInt(parts[0]) + (parseInt(parts[1]) / 60);
                    validEpisodes++;
                } else if (parts.length === 3) {
                    totalMinutes += parseInt(parts[0]) * 60 + parseInt(parts[1]) + (parseInt(parts[2]) / 60);
                    validEpisodes++;
                }
            }
        });
        
        if (validEpisodes === 0) return '0m';
        
        const avgMinutes = Math.floor(totalMinutes / validEpisodes);
        return `${avgMinutes}m`;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.adminViewer = new AdminViewer();
});
