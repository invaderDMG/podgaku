#!/usr/bin/env python3
"""
Script inteligente para actualizar el podcast en el servidor SFTP
- Solo sube episodios nuevos (que no existen en el servidor)
- Siempre actualiza el RSS
- Mantiene un registro de archivos subidos
"""
import os
import json
import paramiko
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

def load_env_file():
    """Cargar variables de entorno desde .env"""
    if os.path.exists('.env'):
        load_dotenv()
        print("✅ Variables de entorno cargadas desde .env")
    else:
        print("⚠️ Archivo .env no encontrado")

def load_uploaded_files():
    """Cargar registro de archivos ya subidos"""
    uploaded_file = Path('uploaded_episodes.json')
    if uploaded_file.exists():
        try:
            with open(uploaded_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_uploaded_files(uploaded_files):
    """Guardar registro de archivos subidos"""
    with open('uploaded_episodes.json', 'w', encoding='utf-8') as f:
        json.dump(uploaded_files, f, indent=2, ensure_ascii=False)

def get_file_hash(file_path):
    """Obtener hash simple del archivo (tamaño + fecha modificación)"""
    try:
        stat = os.stat(file_path)
        return f"{stat.st_size}_{int(stat.st_mtime)}"
    except:
        return None

def check_remote_file_exists(sftp, remote_path):
    """Verificar si un archivo existe en el servidor remoto"""
    try:
        sftp.stat(remote_path)
        return True
    except FileNotFoundError:
        return False
    except:
        return False

def update_podcast():
    """Función principal para actualizar el podcast"""
    load_env_file()
    
    print("🎙️ ACTUALIZADOR INTELIGENTE DE PODCAST")
    print("=" * 45)
    
    # Cargar variables de entorno
    ftp_host = os.getenv('FTP_HOST')
    ftp_username = os.getenv('FTP_USERNAME') 
    ftp_password = os.getenv('FTP_PASSWORD')
    ftp_port = int(os.getenv('FTP_PORT', 22))
    episodes_dir = os.getenv('FTP_EPISODES_DIR')
    rss_path = os.getenv('FTP_RSS_PATH')
    
    # Verificar variables requeridas
    required_vars = {
        'FTP_HOST': ftp_host,
        'FTP_USERNAME': ftp_username,
        'FTP_PASSWORD': ftp_password,
        'FTP_EPISODES_DIR': episodes_dir,
        'FTP_RSS_PATH': rss_path
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        print(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("💡 Verifica tu archivo .env")
        return False
    
    print(f"🌐 Conectando a {ftp_host}:{ftp_port}")
    print(f"📁 Directorio episodios: {episodes_dir}")
    print(f"📄 Archivo RSS: {rss_path}")
    print()
    
    # Cargar registro de archivos subidos
    uploaded_files = load_uploaded_files()
    
    try:
        # Conexión SSH/SFTP
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ftp_host, port=ftp_port, username=ftp_username, password=ftp_password)
        print("✅ Conexión SFTP establecida")
        
        sftp = ssh.open_sftp()
        
        # Verificar que el directorio de episodios existe
        try:
            sftp.stat(episodes_dir)
            print(f"📁 Directorio {episodes_dir} encontrado ✅")
        except FileNotFoundError:
            print(f"❌ Error: Directorio {episodes_dir} no existe en el servidor")
            return False
        
        # 1. VERIFICAR Y SUBIR EPISODIOS NUEVOS
        episodes_folder = Path('episodes')
        new_episodes = []
        updated_episodes = []
        skipped_episodes = []
        
        if episodes_folder.exists():
            audio_files = list(episodes_folder.glob('*.mp3')) + list(episodes_folder.glob('*.m4a'))
            print(f"\n📁 Analizando {len(audio_files)} archivos de audio...")
            
            for audio_file in audio_files:
                file_name = audio_file.name
                remote_path = f"{episodes_dir}/{file_name}"
                current_hash = get_file_hash(audio_file)
                
                # Verificar si el archivo ya fue subido y no ha cambiado
                if file_name in uploaded_files:
                    stored_hash = uploaded_files[file_name].get('hash')
                    if stored_hash == current_hash:
                        # Verificar que realmente existe en el servidor
                        if check_remote_file_exists(sftp, remote_path):
                            skipped_episodes.append(file_name)
                            continue
                
                # El archivo es nuevo o ha cambiado, subirlo
                print(f"📤 Subiendo: {file_name}...")
                try:
                    sftp.put(str(audio_file), remote_path)
                    
                    # Actualizar registro
                    uploaded_files[file_name] = {
                        'hash': current_hash,
                        'uploaded_at': datetime.now().isoformat(),
                        'size': os.path.getsize(audio_file)
                    }
                    
                    if file_name in uploaded_files and 'uploaded_at' in uploaded_files[file_name]:
                        updated_episodes.append(file_name)
                    else:
                        new_episodes.append(file_name)
                    
                    print(f"   ✅ Subido: {file_name}")
                    
                except Exception as e:
                    print(f"   ❌ Error subiendo {file_name}: {e}")
        else:
            print("⚠️ Carpeta 'episodes' no encontrada")
        
        # 2. SIEMPRE ACTUALIZAR EL RSS
        rss_file = Path('podcast.xml')
        if rss_file.exists():
            print(f"\n📄 Actualizando RSS en {rss_path}...")
            try:
                sftp.put(str(rss_file), rss_path)
                print("✅ RSS actualizado correctamente")
            except Exception as e:
                print(f"❌ Error actualizando RSS: {e}")
                print(f"💡 Verifica que el directorio padre de {rss_path} existe")
        else:
            print("⚠️ Archivo podcast.xml no encontrado")
            print("💡 Ejecuta 'python main.py update' para generar el RSS")
        
        # Guardar registro actualizado
        save_uploaded_files(uploaded_files)
        
        sftp.close()
        ssh.close()
        
        # 3. RESUMEN DE LA OPERACIÓN
        print(f"\n🎉 ACTUALIZACIÓN COMPLETADA!")
        print("=" * 30)
        
        if new_episodes:
            print(f"📤 Episodios nuevos subidos ({len(new_episodes)}):")
            for episode in new_episodes:
                print(f"   + {episode}")
        
        if updated_episodes:
            print(f"🔄 Episodios actualizados ({len(updated_episodes)}):")
            for episode in updated_episodes:
                print(f"   ~ {episode}")
        
        if skipped_episodes:
            print(f"⏭️ Episodios omitidos (ya actualizados) ({len(skipped_episodes)}):")
            for episode in skipped_episodes[:5]:  # Mostrar solo los primeros 5
                print(f"   - {episode}")
            if len(skipped_episodes) > 5:
                print(f"   ... y {len(skipped_episodes) - 5} más")
        
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"   Total archivos locales: {len(audio_files) if 'audio_files' in locals() else 0}")
        print(f"   Nuevos: {len(new_episodes)}")
        print(f"   Actualizados: {len(updated_episodes)}")
        print(f"   Omitidos: {len(skipped_episodes)}")
        print(f"   RSS: ✅ Actualizado")
        
        return True
        
    except paramiko.AuthenticationException:
        print("❌ Error de autenticación. Verifica tu usuario y contraseña.")
        return False
    except paramiko.SSHException as e:
        print(f"❌ Error SSH: {e}")
        return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def reset_uploaded_registry():
    """Resetear el registro de archivos subidos (forzar re-subida)"""
    uploaded_file = Path('uploaded_episodes.json')
    if uploaded_file.exists():
        uploaded_file.unlink()
        print("🗑️ Registro de archivos subidos eliminado")
        print("💡 La próxima ejecución subirá todos los archivos")
    else:
        print("ℹ️ No hay registro de archivos subidos")

def show_uploaded_status():
    """Mostrar estado de archivos subidos"""
    uploaded_files = load_uploaded_files()
    episodes_folder = Path('episodes')
    
    print("📊 ESTADO DE EPISODIOS")
    print("=" * 25)
    
    if not episodes_folder.exists():
        print("⚠️ Carpeta 'episodes' no encontrada")
        return
    
    audio_files = list(episodes_folder.glob('*.mp3')) + list(episodes_folder.glob('*.m4a'))
    
    print(f"📁 Archivos locales: {len(audio_files)}")
    print(f"📤 Archivos en registro: {len(uploaded_files)}")
    print()
    
    for audio_file in audio_files:
        file_name = audio_file.name
        current_hash = get_file_hash(audio_file)
        
        if file_name in uploaded_files:
            stored_hash = uploaded_files[file_name].get('hash')
            uploaded_at = uploaded_files[file_name].get('uploaded_at', 'Desconocido')
            
            if stored_hash == current_hash:
                status = "✅ Actualizado"
            else:
                status = "🔄 Modificado (necesita subida)"
            
            print(f"  {file_name}: {status}")
            print(f"    Subido: {uploaded_at}")
        else:
            print(f"  {file_name}: 📤 Nuevo (necesita subida)")
        print()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'reset':
            reset_uploaded_registry()
        elif command == 'status':
            show_uploaded_status()
        elif command == 'help':
            print("🎙️ ACTUALIZADOR INTELIGENTE DE PODCAST")
            print("=" * 40)
            print("Uso:")
            print("  python update_podcast.py        - Actualizar podcast")
            print("  python update_podcast.py status - Ver estado de archivos")
            print("  python update_podcast.py reset  - Resetear registro (forzar re-subida)")
            print("  python update_podcast.py help   - Mostrar esta ayuda")
        else:
            print(f"❌ Comando desconocido: {command}")
            print("💡 Usa 'python update_podcast.py help' para ver comandos disponibles")
    else:
        update_podcast()
