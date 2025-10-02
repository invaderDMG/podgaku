#!/usr/bin/env python3
"""
Script principal para gestionar el podcast Podgaku
"""
import sys
from datetime import datetime
from podcast_manager import PodcastManager

def main():
    manager = PodcastManager()
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "add":
        add_episode_interactive(manager)
    elif command == "migrate":
        manager.migrate_from_anchor()
    elif command == "list":
        manager.list_episodes()
    elif command == "latest":
        manager.get_latest_episode()
    elif command == "update":
        manager.update_rss()
    elif command == "help":
        print_help()
    else:
        print(f"❌ Comando desconocido: {command}")
        print_help()

def add_episode_interactive(manager):
    """Interfaz interactiva para añadir un episodio"""
    print("🎙️  Añadir nuevo episodio a Podgaku")
    print("-" * 40)
    
    title = input("📝 Título del episodio: ").strip()
    if not title:
        print("❌ El título es obligatorio")
        return
    
    print("\n📄 Descripción del episodio (presiona Enter dos veces para terminar):")
    description_lines = []
    while True:
        line = input()
        if line == "" and description_lines and description_lines[-1] == "":
            break
        description_lines.append(line)
    
    description = "\n".join(description_lines).strip()
    if not description:
        print("❌ La descripción es obligatoria")
        return
    
    audio_filename = input("🎵 Nombre del archivo de audio (ej: episode_5.mp3): ").strip()
    if not audio_filename:
        print("❌ El nombre del archivo es obligatorio")
        return
    
    duration = input("⏱️  Duración (HH:MM:SS o MM:SS): ").strip()
    if not duration:
        print("❌ La duración es obligatoria")
        return
    
    episode_number = input("🔢 Número de episodio (opcional): ").strip()
    episode_number = int(episode_number) if episode_number.isdigit() else None
    
    season = input("📺 Temporada (opcional): ").strip()
    season = int(season) if season.isdigit() else None
    
    print("\n🎵 Tracklist (una canción por línea, línea vacía para terminar):")
    tracklist = []
    while True:
        track = input().strip()
        if not track:
            break
        tracklist.append(track)
    
    # Confirmar
    print(f"\n📋 Resumen del episodio:")
    print(f"   Título: {title}")
    print(f"   Archivo: {audio_filename}")
    print(f"   Duración: {duration}")
    if episode_number:
        print(f"   Episodio: {episode_number}")
    if season:
        print(f"   Temporada: {season}")
    if tracklist:
        print(f"   Canciones: {len(tracklist)}")
    
    confirm = input("\n¿Añadir este episodio? (s/N): ").strip().lower()
    if confirm in ['s', 'sí', 'si', 'y', 'yes']:
        manager.add_new_episode(
            title=title,
            description=description,
            audio_filename=audio_filename,
            duration=duration,
            episode_number=episode_number,
            season=season,
            tracklist=tracklist
        )
    else:
        print("❌ Episodio cancelado")

def print_help():
    """Muestra la ayuda del script"""
    print("""
🎙️  Podgaku Podcast Manager
============================

Comandos disponibles:

  add      - Añadir un nuevo episodio (modo interactivo)
  migrate  - Migrar episodios existentes desde Anchor
  list     - Listar todos los episodios
  latest   - Mostrar el episodio más reciente
  update   - Actualizar el archivo RSS
  help     - Mostrar esta ayuda

Ejemplos de uso:

  python main.py add
  python main.py migrate
  python main.py list
  python main.py update

Para añadir un episodio rápidamente desde línea de comandos:
  python main.py add "Título" "Descripción" "audio.mp3" "30:45" 5 1
""")

if __name__ == "__main__":
    main()
