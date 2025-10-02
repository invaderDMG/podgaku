"""
Generador de RSS para podcast
"""
from datetime import datetime
from typing import List
import xml.etree.ElementTree as ET
from xml.dom import minidom
from episode_manager import Episode
from podcast_config import PODCAST_CONFIG, SERVER_CONFIG

class RSSGenerator:
    def __init__(self):
        self.config = PODCAST_CONFIG
        self.server_config = SERVER_CONFIG
    
    def format_duration(self, duration: str) -> str:
        """Convierte duración de HH:MM:SS a segundos"""
        try:
            parts = duration.split(':')
            if len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
                return str(hours * 3600 + minutes * 60 + seconds)
            elif len(parts) == 2:
                minutes, seconds = map(int, parts)
                return str(minutes * 60 + seconds)
            else:
                return duration
        except:
            return duration
    
    def format_date_rfc2822(self, date: datetime) -> str:
        """Formatea fecha en formato RFC 2822 para RSS"""
        return date.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    def create_rss(self, episodes: List[Episode]) -> str:
        """Genera el XML RSS completo"""
        # Crear elemento raíz
        rss = ET.Element("rss")
        rss.set("version", "2.0")
        rss.set("xmlns:itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
        rss.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
        rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")
        
        # Canal
        channel = ET.SubElement(rss, "channel")
        
        # Título
        title = ET.SubElement(channel, "title")
        title.text = self.config["title"]
        
        # Descripción
        description = ET.SubElement(channel, "description")
        description.text = self.config["description"]
        
        # Idioma
        language = ET.SubElement(channel, "language")
        language.text = self.config["language"]
        
        # Autor
        author = ET.SubElement(channel, "itunes:author")
        author.text = self.config["author"]
        
        # Email (iTunes)
        email = ET.SubElement(channel, "itunes:email")
        email.text = self.config["email"]
        
        # Owner (iTunes - requerido por Anchor)
        owner = ET.SubElement(channel, "itunes:owner")
        owner_email = ET.SubElement(owner, "itunes:email")
        owner_email.text = self.config["email"]
        
        # Managing Editor (RSS estándar - requerido por muchas plataformas)
        managing_editor = ET.SubElement(channel, "managingEditor")
        managing_editor.text = f"{self.config['email']} ({self.config['author']})"
        
        # WebMaster (RSS estándar - contacto técnico)
        webmaster = ET.SubElement(channel, "webMaster")
        webmaster.text = f"{self.config['email']} ({self.config['author']})"
        
        # Categoría
        category = ET.SubElement(channel, "itunes:category")
        category.set("text", self.config["category"])
        
        # Imagen
        image = ET.SubElement(channel, "itunes:image")
        image.set("href", self.config["image_url"])
        
        # Explicit
        explicit = ET.SubElement(channel, "itunes:explicit")
        explicit.text = "false" if not self.config["explicit"] else "true"
        
        # Tipo
        podcast_type = ET.SubElement(channel, "itunes:type")
        podcast_type.text = self.config["type"]
        
        # Link al sitio web
        link = ET.SubElement(channel, "link")
        link.text = self.config["website"]
        
        # Atom link para auto-discovery
        atom_link = ET.SubElement(channel, "atom:link")
        atom_link.set("href", f"{self.server_config['base_url']}{self.server_config['rss_path']}")
        atom_link.set("rel", "self")
        atom_link.set("type", "application/rss+xml")
        
        # Última fecha de construcción
        last_build_date = ET.SubElement(channel, "lastBuildDate")
        last_build_date.text = self.format_date_rfc2822(datetime.now())
        
        # Generador
        generator = ET.SubElement(channel, "generator")
        generator.text = "Podgaku RSS Generator"
        
        # Añadir episodios
        for episode in episodes:
            self._add_episode_to_channel(channel, episode)
        
        # Convertir a string XML formateado
        rough_string = ET.tostring(rss, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        
        # Formatear el XML con indentación
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # Limpiar líneas vacías extra que genera toprettyxml
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    def _add_episode_to_channel(self, channel, episode: Episode):
        """Añade un episodio al canal RSS"""
        item = ET.SubElement(channel, "item")
        
        # Título del episodio
        title = ET.SubElement(item, "title")
        title.text = episode.title
        
        # Descripción
        description = ET.SubElement(item, "description")
        description.text = episode.description
        
        # Link al episodio
        link = ET.SubElement(item, "link")
        link.text = episode.audio_url
        
        # GUID
        guid = ET.SubElement(item, "guid")
        guid.text = episode.audio_url
        guid.set("isPermaLink", "true")
        
        # Fecha de publicación
        pub_date = ET.SubElement(item, "pubDate")
        pub_date.text = self.format_date_rfc2822(episode.pub_date)
        
        # Duración
        duration = ET.SubElement(item, "itunes:duration")
        duration.text = self.format_duration(episode.duration)
        
        # Número de episodio
        if episode.episode_number:
            episode_num = ET.SubElement(item, "itunes:episode")
            episode_num.text = str(episode.episode_number)
        
        # Temporada
        if episode.season:
            season = ET.SubElement(item, "itunes:season")
            season.text = str(episode.season)
        
        # Explicit
        explicit = ET.SubElement(item, "itunes:explicit")
        explicit.text = "false"
        
        # Tipo de episodio
        episode_type = ET.SubElement(item, "itunes:episodeType")
        episode_type.text = "full"
        
        # Enclosure (archivo de audio)
        enclosure = ET.SubElement(item, "enclosure")
        enclosure.set("url", episode.audio_url)
        enclosure.set("type", "audio/mpeg")
        enclosure.set("length", "0")  # Se puede calcular el tamaño real del archivo
        
        # Tracklist si existe
        if episode.tracklist:
            content = ET.SubElement(item, "content:encoded")
            tracklist_html = "<p>TRACKLIST:</p><ul>"
            for track in episode.tracklist:
                tracklist_html += f"<li>{track}</li>"
            tracklist_html += "</ul>"
            content.text = f"<![CDATA[{tracklist_html}]]>"
    
    def save_rss(self, episodes: List[Episode], output_file: str = "podcast.xml"):
        """Genera y guarda el RSS en un archivo"""
        rss_content = self.create_rss(episodes)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rss_content)
        print(f"RSS generado y guardado en: {output_file}")
