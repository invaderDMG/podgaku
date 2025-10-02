"""
Gestor principal del podcast - Interfaz fácil para actualizar el RSS
"""
from datetime import datetime
from episode_manager import EpisodeManager, Episode
from rss_generator import RSSGenerator
from podcast_config import SERVER_CONFIG

class PodcastManager:
    def __init__(self):
        self.episode_manager = EpisodeManager()
        self.rss_generator = RSSGenerator()
    
    def add_new_episode(self, title: str, description: str, audio_filename: str, 
                       duration: str, episode_number: int = None, 
                       season: int = None, tracklist: list = None):
        """
        Añade un nuevo episodio y actualiza el RSS automáticamente
        
        Args:
            title: Título del episodio
            description: Descripción del episodio
            audio_filename: Nombre del archivo de audio (se construirá la URL completa)
            duration: Duración en formato HH:MM:SS o MM:SS
            episode_number: Número del episodio (opcional)
            season: Número de temporada (opcional)
            tracklist: Lista de canciones (opcional)
        """
        # Construir URL completa del audio
        audio_url = f"{SERVER_CONFIG['base_url']}{SERVER_CONFIG['episodes_path']}{audio_filename}"
        
        # Crear episodio
        episode = Episode(
            title=title,
            description=description,
            audio_url=audio_url,
            duration=duration,
            pub_date=datetime.now(),
            episode_number=episode_number,
            season=season,
            tracklist=tracklist or []
        )
        
        # Añadir episodio
        self.episode_manager.add_episode(episode)
        
        # Actualizar RSS
        self.update_rss()
        
        print(f"✅ Episodio '{title}' añadido y RSS actualizado")
    
    def update_rss(self, output_file: str = "podcast.xml"):
        """Actualiza el archivo RSS con todos los episodios"""
        episodes = self.episode_manager.get_episodes()
        self.rss_generator.save_rss(episodes, output_file)
        print(f"📡 RSS actualizado con {len(episodes)} episodios")
    
    def list_episodes(self):
        """Lista todos los episodios"""
        episodes = self.episode_manager.get_episodes()
        if not episodes:
            print("📭 No hay episodios")
            return
        
        print(f"📻 Episodios de Podgaku ({len(episodes)} total):")
        print("-" * 50)
        for i, episode in enumerate(episodes):
            print(f"{i+1}. {episode.title}")
            print(f"   📅 {episode.pub_date.strftime('%Y-%m-%d %H:%M')}")
            print(f"   ⏱️  {episode.duration}")
            if episode.episode_number:
                print(f"   # Episodio {episode.episode_number}")
            print()
    
    def get_latest_episode(self):
        """Obtiene información del episodio más reciente"""
        episode = self.episode_manager.get_latest_episode()
        if episode:
            print(f"🎧 Último episodio: {episode.title}")
            print(f"📅 Publicado: {episode.pub_date.strftime('%Y-%m-%d %H:%M')}")
            print(f"⏱️  Duración: {episode.duration}")
            return episode
        else:
            print("📭 No hay episodios")
            return None
    
    def migrate_from_anchor(self):
        """Migra episodios existentes desde el RSS de Anchor"""
        print("🔄 Iniciando migración desde Anchor...")
        
        # Episodios extraídos del RSS de Anchor (todos los episodios disponibles)
        anchor_episodes = [
            {
                "title": "Anime openings from the 70s",
                "description": "Music and anime have been linked since the earliest days of animation, and openings have been usually the first attempt to get audience's attention, so usually they were really intense songs with catchy melodies and upbeats. In today's episode we'll cover my favourite openings from the 70s, and we'll hear the opening songs of these animes: 1. Kagaku Ninja Tai Gatchaman 2. Mazinger Z 3. Devilman 4. Cutie Honey 5. Uchū Senkan Yamato 6. Candy Candy 7. Lupin the III 8. Kidō Senshi GUNDAM 9. VERSAILLES No Bara",
                "duration": "00:30:48",
                "pub_date": datetime(2020, 9, 28, 9, 45, 54),
                "episode_number": 4,
                "season": 1,
                "tracklist": [
                    "Kagaku Ninja Tai Gatchaman",
                    "Mazinger Z", 
                    "Devilman",
                    "Cutie Honey",
                    "Uchū Senkan Yamato",
                    "Candy Candy",
                    "Lupin the III",
                    "Kidō Senshi GUNDAM",
                    "VERSAILLES No Bara"
                ]
            },
            {
                "title": "浜崎あゆみ (Ayumi Hamasaki)",
                "description": "Ayumi Hamasaki fue durante mucho tiempo la definición del JPop, reinando las listas de éxitos y dando a conocer el género de forma internacional. Los remixes de sus canciones han sonado en los clubs más importantes, y aunque ahora mismo su carrera está de capa caída por cuestiones de salud, nos ha dejado un legado impresionante tanto en cifras como en calidad musical",
                "duration": "00:34:35",
                "pub_date": datetime(2020, 9, 11, 7, 56, 51),
                "episode_number": 3,
                "season": 1,
                "tracklist": [
                    "Startin'",
                    "Talking 2 Myself",
                    "Evolution",
                    "Boys & Girls",
                    "Audience",
                    "Fly High",
                    "STEP YOU",
                    "Unite"
                ]
            },
            {
                "title": "The Yellow Monkey",
                "description": "The Yellow Monkey nos ofrece rock puro y duro, con temazos como Spark, Burn o el conocidísimo Tactics, que sirvió de opening para el anime Ruroni Kenshin. Este capítulo no habría sido posible sin Ryoga, que se encargó de la selección musical, guión y locución. ¡Un abrazo, Ryoga!",
                "duration": "00:31:21",
                "pub_date": datetime(2019, 8, 8, 8, 48, 31),
                "episode_number": 2,
                "season": 5,
                "tracklist": [
                    "Spark",
                    "Morality",
                    "Slave",
                    "Second Cry",
                    "Kanashiki ASIAN BOY (悲しきASIAN BOY)",
                    "Tactics",
                    "PUNCH DUNKARD (パンチドランカー)",
                    "Burn",
                    "So Young",
                    "Primal (プライマル。)"
                ]
            },
            {
                "title": "L'Arc~en~ciel",
                "description": "El pop-rock japonés ha llegado a niveles de éxito tan altos gracias a grupos como L'Arc~en~ciel y canciones como Blurry Eyes, Honey o Daybreak's Bell, que podréis escuchar en este programa. L'Arc~en~ciel son actualmente Hyde, Tetsuya, Ken y Yukihiro, y sus nombres han cruzado la frontera japonesa hasta hacerse muy conocidos y respetados en mercados tan importantes como Estados Unidos y Europa.",
                "duration": "00:27:23",
                "pub_date": datetime(2019, 8, 8, 7, 45, 30),
                "episode_number": 2,
                "season": 4,
                "tracklist": [
                    "Honey",
                    "Niji",
                    "Blurry Eyes",
                    "Dive to Blue",
                    "And She Said",
                    "Daybreak's Bell"
                ]
            },
            {
                "title": "Penicillin",
                "description": "Penicillin gozó de éxito de público y crítica en la escena Visual Kei de principios de los 90. Hakuei, Chisato y O-Jiro nos presentan temas tan geniales como Will o Love Dragoon. Este capítulo no podría haber sido posible sin la ayuda de Elisa Fortes, que se ha encargado tanto de la selección musical como del guión y la locución. ¡¡Un abrazo Elisa!!",
                "duration": "00:41:31",
                "pub_date": datetime(2019, 8, 8, 7, 40, 41),
                "episode_number": 2,
                "season": 3,
                "tracklist": [
                    "Will",
                    "Melody",
                    "Blue Moon",
                    "Grind",
                    "Candy Romance",
                    "99banme no Yoru",
                    "Love Dragoon",
                    "Inazuma Rainbow"
                ]
            },
            {
                "title": "X Japan",
                "description": "Poco se puede hablar de X Japan a estas alturas. Muchos dicen que es la primera banda Visual Kei de la escena musical japonesa, una adaptación tardía del Glam de Inglaterra y Estados Unidos, y otros coinciden en que es la banda de rock más relevante en la historia de la música japonesa. La voz de Toshi, las guitarras de hide y Pata, el bajo de Heath y Taiji según la época, y las composiciones, piano y batería de Yoshiki Hayashi, han llenado las listas de éxitos con canciones como Kurenai, Silent Jealousy o Sadistic Desire y que, por supuesto, escucharás en este capítulo.",
                "duration": "00:51:31",
                "pub_date": datetime(2019, 8, 8, 7, 8, 23),
                "episode_number": 2,
                "season": 1,
                "tracklist": [
                    "X",
                    "Sadistic Desire",
                    "Kurenai (紅)",
                    "Weekend",
                    "Silent Jealousy",
                    "Say Anything",
                    "Rusty Nail",
                    "Jade"
                ]
            },
            {
                "title": "演歌 (Especial Enka)",
                "description": "Un género muy tradicional en Japón es el Enka, que podríamos definir como canción melódica moderna. En este primer capítulo dedicado al Enka escucharemos grandes clásicos de este género como Kawa No Nagare no You ni, interpretada por la reina del género Hibari Misora, o Jinsei Iroiro de Chiyoko Shimakura.",
                "duration": "00:29:26",
                "pub_date": datetime(2019, 8, 8, 6, 48, 24),
                "episode_number": 1,
                "season": 6,
                "tracklist": [
                    "Gannosuke Ashiya (芦屋雁之助) - Musume Yo (娘よ)",
                    "Hiroshi Itsuki (五木ひろし) - Nagaragawa Enka (長良川艶歌)",
                    "Teresa Teng (テレサ・テン) - Tsugunai (つぐない)",
                    "Toba Ichirou (鳥羽一郎) - Kyoudai Sen (兄弟船)",
                    "Chiyoko Shimakura (島倉千代子) - Jinsei Iroiro (人生いろいろ)",
                    "Yoshi Ikuzo (吉幾三) - Yuki Kuni (雪國)",
                    "Hibari Misora (美空ひばり)- Kawa No Nagare no You ni (川の流れのように)"
                ]
            },
            {
                "title": "Chage & Aska",
                "description": "Chage & Aska es el nombre artístico del dúo de cantautores formado por Shuji Shibata y Ryo Asuka que debutaron a finales de los años 70 con un estilo de música muy ligero y elegante. Juntos compusieron e interpretaron canciones como Say Yes o Love Song y llegaron a lo más alto de la lista ORICON en múltiples ocasiones.",
                "duration": "00:35:55",
                "pub_date": datetime(2019, 8, 7, 11, 35, 6),
                "episode_number": 1,
                "season": 5,
                "tracklist": [
                    "Tasogare Wo Matazuni (黄昏を待たずに)",
                    "Hitorizaki (ひとり咲き)",
                    "Banri no Kawa (万里の河)",
                    "Yuuwaku no Bell ga Naru (誘惑のベルが鳴る)",
                    "SAY YES",
                    "Hanayaka ni Kizutsuite (華やかに傷ついて)",
                    "LOVE SONG",
                    "Naze ni Kimi Wa Kaeranai (なぜに君は帰らない)"
                ]
            },
            {
                "title": "The Alfee",
                "description": "Las armonías vocales de The Alfee y su solos de guitarra llevan acompañándonos más de 40 años. Sus miembros, Masaru Sakurai, Konosuke Sakazaki y Toshihiko Takamizawa, han creado éxitos como Hoshizora no DISTANCE o Brave Love.",
                "duration": "00:29:23",
                "pub_date": datetime(2019, 8, 7, 11, 25, 41),
                "episode_number": 1,
                "season": 4,
                "tracklist": [
                    "Hoshizora no Disutansu (星空のディスタンス)",
                    "STARSHIP – Hikari wo Motomete – (STARSHIP－光を求めて)",
                    "Mary-Anne (メリーアン)",
                    "Cinderella Wa Nemurenai (シンデレラは眠れない)",
                    "Brave Love: Galaxy Express 999",
                    "Flower Revolution"
                ]
            },
            {
                "title": "おニャン子クラブ (Onyanko Club)",
                "description": "El origen de las bandas masivas de chicas en Japón es Onyanko Club, con canciones pegadizas y letras que abogan por un estilo de vida limpio y divertido. En ese capítulo encontrarás los mejores éxitos de Onyako Club, como 'Sērāfuku O Nugasanai De' o 'Wedding Dress', así como sus anécdotas y polémicas.",
                "duration": "00:29:01",
                "pub_date": datetime(2019, 8, 2, 15, 57, 16),
                "episode_number": 1,
                "season": 2,
                "tracklist": [
                    "SERAFUKU o Nugasanaide (セーラー服を脱がさないで)",
                    "Oyoshininatte ne TEACHER (およしになってねTEACHER)",
                    "Jaa Ne (じゃあね)",
                    "Otto CHIKKAN! (おっとCHIKAN!)",
                    "Osaki Ni Shitsure (お先に失礼)",
                    "Koi Wa QUESTION (恋はくえすちょん)",
                    "Wedding Dress (ウェディングドレス)",
                    "Katatsumari SAMBA (かたつむりサンバ)"
                ]
            }
        ]
        
        for ep_data in anchor_episodes:
            # Construir URL del audio (asumiendo que tienes los archivos)
            audio_filename = f"episode_{ep_data['episode_number']}.mp3"
            audio_url = f"{SERVER_CONFIG['base_url']}{SERVER_CONFIG['episodes_path']}{audio_filename}"
            
            episode = Episode(
                title=ep_data["title"],
                description=ep_data["description"],
                audio_url=audio_url,
                duration=ep_data["duration"],
                pub_date=ep_data["pub_date"],
                episode_number=ep_data["episode_number"],
                season=ep_data["season"],
                tracklist=ep_data["tracklist"]
            )
            
            self.episode_manager.add_episode(episode)
            print(f"✅ Migrado: {ep_data['title']}")
        
        # Actualizar RSS
        self.update_rss()
        print(f"🎉 Migración completada! {len(anchor_episodes)} episodios migrados")
