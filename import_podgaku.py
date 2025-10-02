#!/usr/bin/env python3
"""
Script para importar el RSS completo de Podgaku y los archivos de audio
"""
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import re
from podcast_manager import PodcastManager
from episode_manager import Episode

def parse_rss_file(rss_file):
    """Parsea el archivo RSS de Podgaku y extrae los episodios"""
    tree = ET.parse(rss_file)
    root = tree.getroot()
    
    episodes = []
    
    # Buscar todos los items (episodios)
    for item in root.findall('.//item'):
        try:
            # Extraer información básica
            title = item.find('title').text if item.find('title') is not None else "Sin título"
            description = item.find('description').text if item.find('description') is not None else ""
            link = item.find('link').text if item.find('link') is not None else ""
            guid = item.find('guid').text if item.find('guid') is not None else ""
            
            # Fecha de publicación
            pub_date_text = item.find('pubDate').text if item.find('pubDate') is not None else ""
            pub_date = parse_date(pub_date_text)
            
            # Duración
            duration = item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}duration')
            duration_text = duration.text if duration is not None else "00:00:00"
            
            # Número de episodio (extraer del título o GUID)
            episode_number = extract_episode_number(title, guid)
            
            # Extraer tracklist de la descripción
            tracklist = extract_tracklist(description)
            
            # Limpiar descripción (remover HTML y tracklist)
            clean_description = clean_html_description(description)
            
            # Buscar archivo de audio correspondiente
            audio_filename = find_audio_file(episode_number, title)
            
            episode_data = {
                'title': title,
                'description': clean_description,
                'audio_filename': audio_filename,
                'duration': duration_text,
                'pub_date': pub_date,
                'episode_number': episode_number,
                'season': 1,  # Asumir temporada 1 por ahora
                'tracklist': tracklist,
                'original_link': link,
                'original_guid': guid
            }
            
            episodes.append(episode_data)
            
        except Exception as e:
            print(f"Error procesando episodio: {e}")
            continue
    
    return episodes

def parse_date(date_string):
    """Convierte string de fecha a datetime"""
    try:
        # Formato: "Wed, 25 Dec 2024 08:40:50 GMT"
        return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S GMT")
    except:
        try:
            # Formato alternativo
            return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z")
        except:
            return datetime.now()

def extract_episode_number(title, guid):
    """Extrae el número de episodio del título o GUID"""
    # Buscar patrones como "Episode 1", "Episodio 1", etc.
    patterns = [
        r'Episode\s+(\d+)',
        r'Episodio\s+(\d+)',
        r'#(\d+)',
        r'(\d+)\s*[-–]',  # Número seguido de guión
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            return int(match.group(1))
    
    # Si no se encuentra, buscar en el GUID
    if guid:
        match = re.search(r'(\d+)', guid)
        if match:
            return int(match.group(1))
    
    return None

def extract_tracklist(description):
    """Extrae la tracklist de la descripción HTML"""
    tracklist = []
    
    # Buscar listas ordenadas o no ordenadas
    ol_pattern = r'<ol[^>]*>(.*?)</ol>'
    ul_pattern = r'<ul[^>]*>(.*?)</ul>'
    
    for pattern in [ol_pattern, ul_pattern]:
        matches = re.findall(pattern, description, re.DOTALL | re.IGNORECASE)
        for match in matches:
            # Extraer elementos de lista
            li_pattern = r'<li[^>]*>(.*?)</li>'
            items = re.findall(li_pattern, match, re.DOTALL | re.IGNORECASE)
            for item in items:
                # Limpiar HTML
                clean_item = re.sub(r'<[^>]+>', '', item).strip()
                if clean_item:
                    tracklist.append(clean_item)
    
    return tracklist

def clean_html_description(description):
    """Limpia la descripción HTML y la convierte a texto plano"""
    # Remover HTML tags
    clean = re.sub(r'<[^>]+>', '', description)
    # Remover CDATA
    clean = clean.replace('<![CDATA[', '').replace(']]>', '')
    # Limpiar espacios extra
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def find_audio_file(episode_number, title):
    """Busca el archivo de audio correspondiente en la carpeta episodes"""
    episodes_dir = 'episodes'
    
    if not os.path.exists(episodes_dir):
        return None
    
    # Lista de archivos disponibles
    audio_files = [f for f in os.listdir(episodes_dir) if f.lower().endswith(('.mp3', '.m4a', '.wav'))]
    
    # Buscar por número de episodio
    if episode_number:
        for file in audio_files:
            if file.startswith(f"{episode_number:02d}") or file.startswith(f"{episode_number:2d}"):
                return file
    
    # Buscar por palabras clave del título
    title_keywords = title.lower().split()
    for file in audio_files:
        file_lower = file.lower()
        # Buscar coincidencias de palabras clave
        matches = sum(1 for keyword in title_keywords if keyword in file_lower)
        if matches >= 2:  # Al menos 2 palabras coinciden
            return file
    
    # Si no se encuentra, devolver el primer archivo disponible
    return audio_files[0] if audio_files else None

def main():
    print("🔄 Importando podcast completo de Podgaku...")
    
    # Verificar que existe el archivo RSS
    rss_file = 'podgaku.rss'
    if not os.path.exists(rss_file):
        print(f"❌ No se encontró el archivo {rss_file}")
        return
    
    # Parsear el RSS
    print("📖 Leyendo archivo RSS...")
    episodes_data = parse_rss_file(rss_file)
    print(f"✅ Encontrados {len(episodes_data)} episodios en el RSS")
    
    # Inicializar el gestor del podcast
    manager = PodcastManager()
    
    # Limpiar episodios existentes
    print("🗑️  Limpiando episodios existentes...")
    manager.episode_manager.episodes = []
    manager.episode_manager.save_episodes()
    
    # Importar cada episodio
    print("📥 Importando episodios...")
    imported_count = 0
    
    for i, ep_data in enumerate(episodes_data):
        try:
            # Construir URL del audio
            if ep_data['audio_filename']:
                audio_url = f"http://localhost:8080/episodes/{ep_data['audio_filename']}"
            else:
                print(f"⚠️  No se encontró archivo de audio para: {ep_data['title']}")
                continue
            
            # Crear episodio
            episode = Episode(
                title=ep_data['title'],
                description=ep_data['description'],
                audio_url=audio_url,
                duration=ep_data['duration'],
                pub_date=ep_data['pub_date'],
                episode_number=ep_data['episode_number'],
                season=ep_data['season'],
                tracklist=ep_data['tracklist']
            )
            
            # Añadir episodio
            manager.episode_manager.add_episode(episode)
            imported_count += 1
            
            print(f"✅ Importado: {ep_data['title']}")
            
        except Exception as e:
            print(f"❌ Error importando episodio {i+1}: {e}")
            continue
    
    # Actualizar RSS
    print("📡 Generando RSS actualizado...")
    manager.update_rss()
    
    print(f"🎉 Importación completada! {imported_count} episodios importados")
    print(f"📁 Archivos de audio encontrados: {len(os.listdir('episodes'))}")

if __name__ == '__main__':
    main()
