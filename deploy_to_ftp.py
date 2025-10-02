#!/usr/bin/env python3
"""
Script maestro para desplegar el podcast completo al servidor FTP
"""
import os
import sys
from pathlib import Path

# Cargar variables de entorno
try:
    from load_env import load_env_file
    load_env_file()
except ImportError:
    pass

def check_required_vars():
    """Verifica que todas las variables de entorno requeridas estén definidas"""
    required_vars = {
        'PODCAST_DOMAIN': 'Dominio del servidor',
        'FTP_HOST': 'Host FTP',
        'FTP_USERNAME': 'Usuario FTP',
        'FTP_PASSWORD': 'Contraseña FTP'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"  {var} - {description}")
    
    if missing_vars:
        print("❌ Variables de entorno requeridas no encontradas:")
        for var in missing_vars:
            print(var)
        print("\n💡 Configura las variables en un archivo .env o exportalas:")
        print("   cp env.example .env")
        print("   # Edita .env con tus credenciales")
        return False
    
    return True

def main():
    print("🚀 Despliegue Completo de Podgaku a FTP")
    print("=" * 45)
    
    # Verificar variables de entorno
    if not check_required_vars():
        return
    
    # Mostrar configuración
    print("\n📋 Configuración detectada:")
    print(f"   🌐 Dominio: {os.getenv('PODCAST_DOMAIN')}")
    print(f"   📡 FTP: {os.getenv('FTP_HOST')}:{os.getenv('FTP_PORT', '21')}")
    print(f"   👤 Usuario: {os.getenv('FTP_USERNAME')}")
    print(f"   📁 Episodios: {os.getenv('FTP_EPISODES_DIR', '/podcast/episodes')}")
    print(f"   📄 RSS: {os.getenv('FTP_RSS_PATH', '/podcast.xml')}")
    
    # Confirmar despliegue
    confirm = input("\n¿Proceder con el despliegue? (s/N): ").strip().lower()
    if confirm not in ['s', 'sí', 'si', 'y', 'yes']:
        print("❌ Despliegue cancelado")
        return
    
    print("\n🔄 Iniciando despliegue...")
    
    # Paso 1: Actualizar configuración
    print("\n1️⃣  Actualizando configuración del podcast...")
    try:
        from update_config_for_ftp import update_podcast_config
        domain = os.getenv('PODCAST_DOMAIN')
        episodes_path = os.getenv('PODCAST_EPISODES_PATH', '/podcast/episodes')
        rss_path = os.getenv('PODCAST_RSS_PATH', '/podcast.xml')
        
        if update_podcast_config(domain, episodes_path, rss_path):
            print("✅ Configuración actualizada")
        else:
            print("❌ Error actualizando configuración")
            return
    except Exception as e:
        print(f"❌ Error en paso 1: {e}")
        return
    
    # Paso 2: Regenerar RSS
    print("\n2️⃣  Regenerando RSS con nuevas URLs...")
    try:
        from podcast_manager import PodcastManager
        manager = PodcastManager()
        manager.update_rss()
        print("✅ RSS regenerado")
    except Exception as e:
        print(f"❌ Error en paso 2: {e}")
        return
    
    # Paso 3: Subir archivos al FTP
    print("\n3️⃣  Subiendo archivos al servidor FTP...")
    try:
        from ftp_uploader import PodcastFTPUploader
        
        uploader = PodcastFTPUploader(
            host=os.getenv('FTP_HOST'),
            username=os.getenv('FTP_USERNAME'),
            password=os.getenv('FTP_PASSWORD'),
            port=int(os.getenv('FTP_PORT', '21'))
        )
        
        if uploader.upload_podcast(
            local_episodes_dir="episodes",
            remote_episodes_dir=os.getenv('FTP_EPISODES_DIR', '/podcast/episodes'),
            rss_file="podcast.xml",
            remote_rss_path=os.getenv('FTP_RSS_PATH', '/podcast.xml')
        ):
            print("✅ Archivos subidos correctamente")
        else:
            print("❌ Error subiendo archivos")
            return
    except Exception as e:
        print(f"❌ Error en paso 3: {e}")
        return
    
    # Éxito
    print("\n🎉 ¡Despliegue completado exitosamente!")
    print(f"\n📡 Tu podcast está disponible en:")
    print(f"   RSS: https://{os.getenv('PODCAST_DOMAIN')}{os.getenv('PODCAST_RSS_PATH', '/podcast.xml')}")
    print(f"   Episodios: https://{os.getenv('PODCAST_DOMAIN')}{os.getenv('PODCAST_EPISODES_PATH', '/podcast/episodes')}/")
    
    print(f"\n📝 Próximos pasos:")
    print(f"1. Verifica que el RSS es accesible en tu navegador")
    print(f"2. Actualiza Anchor con la nueva URL del RSS")
    print(f"3. Prueba la reproducción de algunos episodios")

if __name__ == '__main__':
    main()
