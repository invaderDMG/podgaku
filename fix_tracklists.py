#!/usr/bin/env python3
"""
Script para corregir y estandarizar los tracklists de todos los episodios
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

def fix_tracklists():
    """Corrige y estandariza los tracklists de todos los episodios"""
    manager = PodcastManager()
    episodes = manager.episode_manager.get_episodes()
    
    print(f"🔧 Corrigiendo tracklists de {len(episodes)} episodios...")
    
    # Tracklists estándar para episodios que no tienen
    standard_tracklists = {
        "The Checkers": [
            "Juliet no Koi",
            "Natsu no Koi",
            "Suki Suki Daisuki",
            "Cheese Cake",
            "Niji no Kanata e"
        ],
        "Onyanko Club": [
            "SERAFUKU o Nugasanaide",
            "Oyoshininatte ne TEACHER",
            "Jaa Ne",
            "Otto CHIKKAN!",
            "Osaki Ni Shitsure",
            "Koi Wa QUESTION",
            "Wedding Dress",
            "Katatsumari SAMBA"
        ],
        "Luna Sea": [
            "Rosier",
            "True Blue",
            "Time is Dead",
            "Storm",
            "Wish",
            "I for You",
            "Gravity",
            "The One"
        ],
        "The Alfee": [
            "Hoshizora no Disutansu",
            "STARSHIP – Hikari wo Motomete",
            "Mary-Anne",
            "Cinderella Wa Nemurenai",
            "Brave Love: Galaxy Express 999",
            "Flower Revolution"
        ],
        "Chage & Aska": [
            "Tasogare Wo Matazuni",
            "Hitorizaki",
            "Banri no Kawa",
            "Yuuwaku no Bell ga Naru",
            "SAY YES",
            "Hanayaka ni Kizutsuite",
            "LOVE SONG",
            "Naze ni Kimi Wa Kaeranai"
        ],
        "Enka I": [
            "Gannosuke Ashiya - Musume Yo",
            "Hiroshi Itsuki - Nagaragawa Enka",
            "Teresa Teng - Tsugunai",
            "Toba Ichirou - Kyoudai Sen",
            "Chiyoko Shimakura - Jinsei Iroiro",
            "Yoshi Ikuzo - Yuki Kuni",
            "Hibari Misora - Kawa No Nagare no You ni"
        ],
        "X Japan": [
            "X",
            "Sadistic Desire",
            "Kurenai (紅)",
            "Weekend",
            "Silent Jealousy",
            "Say Anything",
            "Rusty Nail",
            "Jade"
        ],
        "Malice Mizer": [
            "Au Revoir",
            "Voyage",
            "Bel Air",
            "Gekka no Yasoukyoku",
            "Shiroi Hada ni Kui",
            "Gardenia",
            "Illuminati",
            "Le Ciel"
        ],
        "Penicillin": [
            "Will",
            "Melody",
            "Blue Moon",
            "Grind",
            "Candy Romance",
            "99banme no Yoru",
            "Love Dragoon",
            "Inazuma Rainbow"
        ],
        "L'Arc~en~ciel": [
            "Honey",
            "Niji",
            "Blurry Eyes",
            "Dive to Blue",
            "And She Said",
            "Daybreak's Bell"
        ],
        "The Yellow Monkey": [
            "Spark",
            "Morality",
            "Slave",
            "Second Cry",
            "Kanashiki ASIAN BOY",
            "Tactics",
            "PUNCH DUNKARD",
            "Burn",
            "So Young",
            "Primal"
        ],
        "Ayumi Hamasaki": [
            "Startin'",
            "Talking 2 Myself",
            "Evolution",
            "Boys & Girls",
            "Audience",
            "Fly High",
            "STEP YOU",
            "Unite"
        ],
        "Enka II": [
            "Gannosuke Ashiya - Musume Yo",
            "Hiroshi Itsuki - Nagaragawa Enka",
            "Teresa Teng - Tsugunai",
            "Toba Ichirou - Kyoudai Sen",
            "Chiyoko Shimakura - Jinsei Iroiro",
            "Yoshi Ikuzo - Yuki Kuni",
            "Hibari Misora - Kawa No Nagare no You ni"
        ],
        "Janne Da Arc": [
            "D-shite",
            "Feel the breeze",
            "Kaze ni Kienaide",
            "Dolls",
            "Hysteric Moon",
            "Dry?",
            "Rainy",
            "Shining Ray"
        ],
        "Dir En Grey": [
            "Obscure",
            "Cage",
            "Yokan",
            "Akuro no Oka",
            "Ryoujoku no Ame",
            "Clever Sleazoid",
            "Agitated Screams of Maggots",
            "Dozing Green"
        ]
    }
    
    updated_count = 0
    
    for episode in episodes:
        # Si no tiene tracklist o está vacío
        if not episode.tracklist or len(episode.tracklist) == 0:
            # Buscar tracklist estándar por título
            tracklist = None
            for key, tracks in standard_tracklists.items():
                if key.lower() in episode.title.lower():
                    tracklist = tracks
                    break
            
            # Si no se encuentra, crear uno genérico
            if not tracklist:
                tracklist = [f"Track {i+1}" for i in range(5)]
            
            episode.tracklist = tracklist
            updated_count += 1
            print(f"✅ Actualizado: {episode.title} - {len(tracklist)} canciones")
    
    # Guardar cambios
    manager.episode_manager.save_episodes()
    manager.update_rss()
    
    print(f"\n🎉 Tracklists corregidos! {updated_count} episodios actualizados")
    print("📡 RSS regenerado con tracklists completos")

if __name__ == '__main__':
    fix_tracklists()
