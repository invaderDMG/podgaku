"""
Gestor de episodios del podcast
"""
from datetime import datetime
from typing import List, Dict, Optional
import json
import os

class Episode:
    def __init__(self, title: str, description: str, audio_url: str, 
                 duration: str, pub_date: datetime, episode_number: int = None,
                 season: int = None, tracklist: List[str] = None):
        self.title = title
        self.description = description
        self.audio_url = audio_url
        self.duration = duration  # Formato HH:MM:SS
        self.pub_date = pub_date
        self.episode_number = episode_number
        self.season = season
        self.tracklist = tracklist or []
    
    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "description": self.description,
            "audio_url": self.audio_url,
            "duration": self.duration,
            "pub_date": self.pub_date.isoformat(),
            "episode_number": self.episode_number,
            "season": self.season,
            "tracklist": self.tracklist
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Episode':
        return cls(
            title=data["title"],
            description=data["description"],
            audio_url=data["audio_url"],
            duration=data["duration"],
            pub_date=datetime.fromisoformat(data["pub_date"]),
            episode_number=data.get("episode_number"),
            season=data.get("season"),
            tracklist=data.get("tracklist", [])
        )

class EpisodeManager:
    def __init__(self, episodes_file: str = "episodes.json"):
        self.episodes_file = episodes_file
        self.episodes: List[Episode] = []
        self.load_episodes()
    
    def load_episodes(self):
        """Carga episodios desde el archivo JSON"""
        if os.path.exists(self.episodes_file):
            try:
                with open(self.episodes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.episodes = [Episode.from_dict(ep) for ep in data]
            except Exception as e:
                print(f"Error cargando episodios: {e}")
                self.episodes = []
    
    def save_episodes(self):
        """Guarda episodios en el archivo JSON"""
        try:
            with open(self.episodes_file, 'w', encoding='utf-8') as f:
                json.dump([ep.to_dict() for ep in self.episodes], f, 
                         indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando episodios: {e}")
    
    def add_episode(self, episode: Episode):
        """Añade un nuevo episodio"""
        self.episodes.append(episode)
        self.episodes.sort(key=lambda x: x.pub_date, reverse=True)
        self.save_episodes()
    
    def get_episodes(self) -> List[Episode]:
        """Obtiene todos los episodios ordenados por fecha (más recientes primero)"""
        return sorted(self.episodes, key=lambda x: x.pub_date, reverse=True)
    
    def get_latest_episode(self) -> Optional[Episode]:
        """Obtiene el episodio más reciente"""
        episodes = self.get_episodes()
        return episodes[0] if episodes else None
    
    def update_episode(self, index: int, episode: Episode):
        """Actualiza un episodio existente"""
        if 0 <= index < len(self.episodes):
            self.episodes[index] = episode
            self.episodes.sort(key=lambda x: x.pub_date, reverse=True)
            self.save_episodes()
    
    def delete_episode(self, index: int):
        """Elimina un episodio"""
        if 0 <= index < len(self.episodes):
            del self.episodes[index]
            self.save_episodes()
