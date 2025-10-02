#!/usr/bin/env python3
"""
Script para subir archivos del podcast a un servidor FTP
"""
import ftplib
import os
import sys
from pathlib import Path

# Cargar variables de entorno desde .env si existe
try:
    from load_env import load_env_file
    load_env_file()
except ImportError:
    pass

class PodcastFTPUploader:
    def __init__(self, host, username, password, port=21):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ftp = None
    
    def connect(self):
        """Conecta al servidor FTP"""
        try:
            print(f"🔌 Conectando a {self.host}:{self.port}...")
            self.ftp = ftplib.FTP()
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.username, self.password)
            print("✅ Conexión FTP establecida")
            return True
        except Exception as e:
            print(f"❌ Error conectando al FTP: {e}")
            return False
    
    def disconnect(self):
        """Desconecta del servidor FTP"""
        if self.ftp:
            self.ftp.quit()
            print("🔌 Desconectado del FTP")
    
    def create_directories(self, remote_paths):
        """Crea directorios en el servidor FTP si no existen"""
        for path in remote_paths:
            try:
                # Intentar cambiar al directorio
                self.ftp.cwd(path)
                print(f"📁 Directorio {path} ya existe")
            except:
                try:
                    # Crear el directorio
                    self.ftp.mkd(path)
                    print(f"📁 Directorio {path} creado")
                except Exception as e:
                    print(f"⚠️  No se pudo crear {path}: {e}")
    
    def upload_file(self, local_path, remote_path):
        """Sube un archivo al servidor FTP"""
        try:
            with open(local_path, 'rb') as file:
                self.ftp.storbinary(f'STOR {remote_path}', file)
            print(f"✅ Subido: {os.path.basename(local_path)}")
            return True
        except Exception as e:
            print(f"❌ Error subiendo {os.path.basename(local_path)}: {e}")
            return False
    
    def upload_podcast(self, local_episodes_dir, remote_episodes_dir, rss_file, remote_rss_path):
        """Sube todos los archivos del podcast"""
        if not self.connect():
            return False
        
        try:
            # Crear directorios necesarios
            self.create_directories([remote_episodes_dir])
            
            # Subir archivos de episodios
            print(f"\n📤 Subiendo archivos de episodios...")
            episodes_uploaded = 0
            
            for filename in os.listdir(local_episodes_dir):
                if filename.lower().endswith(('.mp3', '.m4a', '.wav')):
                    local_path = os.path.join(local_episodes_dir, filename)
                    remote_path = f"{remote_episodes_dir}/{filename}"
                    
                    if self.upload_file(local_path, remote_path):
                        episodes_uploaded += 1
            
            # Subir archivo RSS
            print(f"\n📤 Subiendo archivo RSS...")
            if os.path.exists(rss_file):
                if self.upload_file(rss_file, remote_rss_path):
                    print("✅ RSS subido correctamente")
                else:
                    print("❌ Error subiendo RSS")
            else:
                print("❌ Archivo RSS no encontrado")
            
            print(f"\n🎉 Subida completada!")
            print(f"📊 Episodios subidos: {episodes_uploaded}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error durante la subida: {e}")
            return False
        finally:
            self.disconnect()

def main():
    print("🎙️  Podgaku FTP Uploader")
    print("=" * 40)
    
    # Leer credenciales desde variables de entorno
    host = os.getenv('FTP_HOST')
    username = os.getenv('FTP_USERNAME')
    password = os.getenv('FTP_PASSWORD')
    port = os.getenv('FTP_PORT', '21')
    
    # Directorios desde variables de entorno
    local_episodes_dir = "episodes"
    remote_episodes_dir = os.getenv('FTP_EPISODES_DIR', '/podcast/episodes')
    rss_file = "podcast.xml"
    remote_rss_path = os.getenv('FTP_RSS_PATH', '/podcast.xml')
    
    # Verificar que las variables requeridas estén definidas
    if not all([host, username, password]):
        print("❌ Variables de entorno requeridas no encontradas:")
        print("   FTP_HOST - Host del servidor FTP")
        print("   FTP_USERNAME - Usuario FTP")
        print("   FTP_PASSWORD - Contraseña FTP")
        print("\n📝 Variables opcionales:")
        print("   FTP_PORT - Puerto FTP (por defecto: 21)")
        print("   FTP_EPISODES_DIR - Directorio remoto para episodios (por defecto: /podcast/episodes)")
        print("   FTP_RSS_PATH - Ruta remota del RSS (por defecto: /podcast.xml)")
        print("\n💡 Ejemplo de configuración:")
        print("   export FTP_HOST='ftp.tudominio.com'")
        print("   export FTP_USERNAME='tu_usuario'")
        print("   export FTP_PASSWORD='tu_contraseña'")
        print("   export FTP_PORT='21'")
        print("   export FTP_EPISODES_DIR='/podcast/episodes'")
        print("   export FTP_RSS_PATH='/podcast.xml'")
        return
    
    print(f"🌐 Host: {host}")
    print(f"👤 Usuario: {username}")
    print(f"🔌 Puerto: {port}")
    print(f"📁 Episodios: {remote_episodes_dir}")
    print(f"📄 RSS: {remote_rss_path}")
    
    # Verificar archivos locales
    if not os.path.exists(local_episodes_dir):
        print(f"❌ No se encontró el directorio {local_episodes_dir}")
        return
    
    if not os.path.exists(rss_file):
        print(f"❌ No se encontró el archivo {rss_file}")
        return
    
    # Contar archivos
    audio_files = [f for f in os.listdir(local_episodes_dir) if f.lower().endswith(('.mp3', '.m4a', '.wav'))]
    print(f"\n📊 Archivos a subir:")
    print(f"   🎵 Episodios de audio: {len(audio_files)}")
    print(f"   📄 Archivo RSS: {rss_file}")
    
    # Confirmar subida
    confirm = input("\n¿Proceder con la subida? (s/N): ").strip().lower()
    if confirm not in ['s', 'sí', 'si', 'y', 'yes']:
        print("❌ Subida cancelada")
        return
    
    # Crear uploader y subir
    uploader = PodcastFTPUploader(host, username, password, int(port))
    
    if uploader.upload_podcast(local_episodes_dir, remote_episodes_dir, rss_file, remote_rss_path):
        print("\n🎉 ¡Subida completada exitosamente!")
        print(f"🌐 Tu podcast estará disponible en:")
        print(f"   RSS: http://{host}{remote_rss_path}")
        print(f"   Episodios: http://{host}{remote_episodes_dir}/")
    else:
        print("\n❌ Error durante la subida")

if __name__ == '__main__':
    main()
