#!/usr/bin/env python3
"""
Script para subir archivos del podcast usando SFTP
"""
import os
import sys
import paramiko
from pathlib import Path
from load_env import load_env_file

def upload_to_sftp():
    """Sube archivos al servidor usando SFTP"""
    
    # Cargar variables de entorno
    load_env_file()
    
    # Configuración SFTP
    host = os.getenv('FTP_HOST', 'podgaku.jdlcgarcia.es')
    port = int(os.getenv('FTP_PORT', '22'))
    username = os.getenv('FTP_USERNAME')
    password = os.getenv('FTP_PASSWORD')
    
    episodes_dir = os.getenv('FTP_EPISODES_DIR', '/var/www/podgaku/episodes')
    rss_path = os.getenv('FTP_RSS_PATH', '/var/www/podgaku/rss.xml')
    
    print("🚀 Subida SFTP de Podgaku")
    print("=" * 30)
    print(f"🔍 Configuración de conexión:")
    print(f"   Host: {host}")
    print(f"   Puerto: {port}")
    print(f"   Usuario: {username}")
    print(f"   Protocolo: SFTP")
    print(f"   Directorio episodios: {episodes_dir}")
    print(f"   Archivo RSS: {rss_path}")
    
    if not all([host, username, password]):
        print("❌ Error: Faltan credenciales SFTP en el archivo .env")
        return False
    
    try:
        # Crear cliente SSH/SFTP
        print(f"\n🔌 Conectando a {host}:{port}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Conectar
        ssh.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=30
        )
        
        # Crear cliente SFTP
        sftp = ssh.open_sftp()
        print("✅ Conexión SFTP establecida")
        
        # Verificar que el directorio de episodios existe
        try:
            sftp.stat(episodes_dir)
            print(f"📁 Directorio {episodes_dir} encontrado ✅")
        except FileNotFoundError:
            print(f"❌ Error: Directorio {episodes_dir} no existe en el servidor")
            print("💡 Verifica la ruta en tu archivo .env")
            return False
        
        # Subir archivos de episodios
        episodes_folder = Path('episodes')
        if episodes_folder.exists():
            audio_files = list(episodes_folder.glob('*.mp3')) + list(episodes_folder.glob('*.m4a'))
            print(f"\n📁 Subiendo {len(audio_files)} archivos de audio...")
            
            for i, audio_file in enumerate(audio_files, 1):
                remote_path = f"{episodes_dir}/{audio_file.name}"
                print(f"   [{i}/{len(audio_files)}] {audio_file.name}...")
                
                try:
                    sftp.put(str(audio_file), remote_path)
                    print(f"   ✅ Subido: {audio_file.name}")
                except Exception as e:
                    print(f"   ❌ Error subiendo {audio_file.name}: {e}")
        else:
            print("⚠️  Carpeta 'episodes' no encontrada")
        
        # Subir archivo RSS
        rss_file = Path('podcast.xml')
        if rss_file.exists():
            print(f"\n📄 Subiendo RSS a {rss_path}...")
            try:
                sftp.put(str(rss_file), rss_path)
                print("✅ RSS subido correctamente")
            except Exception as e:
                print(f"❌ Error subiendo RSS: {e}")
                print(f"💡 Verifica que el directorio padre de {rss_path} existe")
        else:
            print("⚠️  Archivo podcast.xml no encontrado")
        
        # Cerrar conexiones
        sftp.close()
        ssh.close()
        print("\n🎉 Subida completada!")
        return True
        
    except paramiko.AuthenticationException:
        print("❌ Error de autenticación: Verifica usuario y contraseña")
        return False
    except paramiko.SSHException as e:
        print(f"❌ Error SSH: {e}")
        return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal"""
    success = upload_to_sftp()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
