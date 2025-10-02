"""
Configuración del podcast Podgaku
"""
from datetime import datetime

# Metadatos del podcast (actualizados desde podgaku.rss)
PODCAST_CONFIG = {
    "title": "Podgaku: Exploring the Sounds of Japanese Music - Descubre la música japonesa en Podgaku",
    "description": "Welcome to Podgaku, the podcast where we explore Japanese music in a unique and personal way. We'll take you on a musical journey from traditional sounds to modern pop and rock. Discover the history, culture, and evolution of music in Japan, and new and old artists and their different genres. ¡Bienvenidos a Podgaku, el podcast donde exploramos la música japonesa de una forma única y personal! Te llevaremos a un viaje musical desde los sonidos tradicionales hasta el pop y rock moderno. Descubre la historia, cultura y evolución de la música en Japón, nuevos y antiguos artistas y sus géneros.",
    "language": "en-US",
    "author": "Juan García",
    "email": "podgaku@gmail.com",
        "website": "https://podgaku.jdlcgarcia.es",
    "image_url": "https://d3t3ozftmdmh3i.cloudfront.net/production/podcast_uploaded_nologo/2100407/2100407-1679474811468-a41f8d5345f0e.jpg",
    "category": "Music",
    "explicit": False,
    "type": "episodic"
}

# Configuración del servidor
SERVER_CONFIG = {
    "base_url": "https://podgaku.jdlcgarcia.es",  # Tu dominio real
    "rss_path": "/podcast.xml",
    "episodes_path": "/episodes/"
}

# Configuración para desarrollo local (comentada)
# SERVER_CONFIG = {
#     "base_url": "http://localhost:8080",  # Para desarrollo local
#     "rss_path": "/podcast.xml",
#     "episodes_path": "/episodes/"
# }

# Configuración para desarrollo local (comentada)
# SERVER_CONFIG = {
#     "base_url": "http://localhost:8080",  # Para desarrollo local
#     "rss_path": "/podcast.xml",
#     "episodes_path": "/episodes/"
# }

# Configuración para desarrollo local (comentada)
# SERVER_CONFIG = {
#     "base_url": "http://localhost:8080",  # Para desarrollo local
#     "rss_path": "/podcast.xml",
#     "episodes_path": "/episodes/"
# }

# Configuración para desarrollo local (comentada)
# SERVER_CONFIG = {
#     "base_url": "http://localhost:8080",  # Para desarrollo local
#     "rss_path": "/podcast.xml",
#     "episodes_path": "/episodes/"
# }

# Configuración para desarrollo local (comentada)
# SERVER_CONFIG = {
#     "base_url": "http://localhost:8080",  # Para desarrollo local
#     "rss_path": "/podcast.xml",
#     "episodes_path": "/episodes/"
# }

# Configuración para desarrollo local (comentada)
# SERVER_CONFIG = {
#     "base_url": "http://localhost:8080",  # Para desarrollo local
#     "rss_path": "/podcast.xml",
#     "episodes_path": "/episodes/"
# }

# Configuración para desarrollo local (comentada)
# SERVER_CONFIG = {
#     "base_url": "http://localhost:8080",  # Para desarrollo local
#     "rss_path": "/podcast.xml",
#     "episodes_path": "/episodes/"
# }

# Configuración para producción (descomenta y modifica cuando despliegues)
# SERVER_CONFIG = {
#     "base_url": "https://tudominio.com",  # Tu dominio real
#     "rss_path": "/podcast.xml",
#     "episodes_path": "/episodes/"
# }
