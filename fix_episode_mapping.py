#!/usr/bin/env python3
"""
Script para corregir el mapeo entre episodios y archivos de audio
"""
import os
import re
from podcast_manager import PodcastManager

# Cargar variables de entorno desde .env si existe
try:
    from load_env import load_env_file
    load_env_file()
except ImportError:
    pass

def fix_episode_mapping():
    """Corrige el mapeo entre episodios y archivos de audio"""
    manager = PodcastManager()
    episodes = manager.episode_manager.get_episodes()
    
    # Obtener lista de archivos de audio
    episodes_dir = 'episodes'
    audio_files = sorted([f for f in os.listdir(episodes_dir) if f.lower().endswith(('.mp3', '.m4a', '.wav'))])
    
    print(f"📁 Archivos de audio encontrados: {len(audio_files)}")
    for i, file in enumerate(audio_files, 1):
        print(f"  {i:2d}. {file}")
    
    print(f"\n📻 Episodios en la base de datos: {len(episodes)}")
    
    # Mapeo manual basado en el orden y contenido
    mapping = {
        # Anime openings (más recientes primero)
        "Anime openings from the 10s - First Half": "21 - Anime Ops 10s Parte 1.mp3",
        "Anime openings from the 00s - Second Half": "20 - Anime Ops 00s Parte 2.mp3", 
        "Anime openings from the 00s - First Half": "19 - Anime Ops 00s Parte 1.mp3",
        "Anime openings from the 90s": "18 - Anime Ops 90s.mp3",
        "Anime openings from the 80s": "17 - Anime Ops 80s.mp3",
        "Anime openings from the 70s": "16 - Anime Ops 70s.mp3",
        
        # Artistas individuales
        "Dir En Grey": "15 - Dir En Grey.m4a",
        "Janne Da Arc": "14 - Janne Da Arc.m4a",
        "演歌二 (Especial Enka II)": "13 - Enka II.m4a",
        "浜崎あゆみ (Ayumi Hamasaki)": "12 - Ayumi Hamasaki.m4a",
        "The Yellow Monkey": "11 - The Yellow Monkey.m4a",
        "L'Arc~en~ciel": "10 - Larc En Ciel.m4a",
        "Penicillin": "09 - Penicillin.m4a",
        "Malice Mizer": "08 - Malice Mizer.m4a",
        "X Japan": "07 - X Japan.m4a",
        "演歌 (Especial Enka)": "06 - Enka I.m4a",
        "Chage & Aska": "05 - Chage & Aska.m4a",
        "The Alfee": "04 - The Alfee.m4a",
        "Luna Sea": "03 - Luna Sea.m4a",
        "おニャン子クラブ (Onyanko Club)": "02 - Onyanko Club.m4a",
        "チェッカーズ (The Checkers)": "01 - The Checkers.m4a"
    }
    
    print("\n🔧 Aplicando mapeo corregido...")
    
    # Actualizar cada episodio
    for episode in episodes:
        if episode.title in mapping:
            new_filename = mapping[episode.title]
            old_url = episode.audio_url
            # Usar la configuración actual del servidor
            from podcast_config import SERVER_CONFIG
            new_url = f"{SERVER_CONFIG['base_url']}{SERVER_CONFIG['episodes_path']}{new_filename}"
            
            # Actualizar URL del audio
            episode.audio_url = new_url
            
            # Actualizar número de episodio basado en el nombre del archivo
            match = re.search(r'^(\d+)', new_filename)
            if match:
                episode.episode_number = int(match.group(1))
            
            print(f"✅ {episode.title} -> {new_filename}")
        else:
            print(f"⚠️  No se encontró mapeo para: {episode.title}")
    
    # Guardar cambios
    manager.episode_manager.save_episodes()
    manager.update_rss()
    
    print(f"\n🎉 Mapeo corregido! RSS actualizado.")

if __name__ == '__main__':
    fix_episode_mapping()
