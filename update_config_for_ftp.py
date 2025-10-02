#!/usr/bin/env python3
"""
Script para actualizar la configuración del podcast con las URLs del servidor FTP
"""
import os
import sys

# Cargar variables de entorno desde .env si existe
try:
    from load_env import load_env_file
    load_env_file()
except ImportError:
    pass

def update_podcast_config(domain, episodes_path="/podcast/episodes", rss_path="/podcast.xml"):
    """Actualiza la configuración del podcast con las URLs del servidor"""
    
    config_file = "podcast_config.py"
    
    if not os.path.exists(config_file):
        print(f"❌ No se encontró el archivo {config_file}")
        return False
    
    # Leer el archivo actual
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Crear la nueva configuración
    new_config = f'''# Configuración del servidor
SERVER_CONFIG = {{
    "base_url": "https://{domain}",  # Tu dominio real
    "rss_path": "{rss_path}",
    "episodes_path": "{episodes_path}/"
}}

# Configuración para desarrollo local (comentada)
# SERVER_CONFIG = {{
#     "base_url": "http://localhost:8080",  # Para desarrollo local
#     "rss_path": "/podcast.xml",
#     "episodes_path": "/episodes/"
# }}'''
    
    # Reemplazar la configuración del servidor
    import re
    pattern = r'# Configuración del servidor.*?(?=\n\n|\Z)'
    new_content = re.sub(pattern, new_config, content, flags=re.DOTALL)
    
    # Escribir el archivo actualizado
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Configuración actualizada:")
    print(f"   🌐 Dominio: https://{domain}")
    print(f"   📁 Episodios: {episodes_path}/")
    print(f"   📄 RSS: {rss_path}")
    
    return True

def main():
    print("🔧 Actualizador de Configuración para FTP")
    print("=" * 45)
    
    # Leer configuración desde variables de entorno
    domain = os.getenv('PODCAST_DOMAIN')
    episodes_path = os.getenv('PODCAST_EPISODES_PATH', '/podcast/episodes')
    rss_path = os.getenv('PODCAST_RSS_PATH', '/podcast.xml')
    
    if not domain:
        print("❌ Variable de entorno PODCAST_DOMAIN no encontrada")
        print("\n📝 Variables de entorno requeridas:")
        print("   PODCAST_DOMAIN - Dominio de tu servidor (ej: tudominio.com)")
        print("\n📝 Variables opcionales:")
        print("   PODCAST_EPISODES_PATH - Ruta de episodios (por defecto: /podcast/episodes)")
        print("   PODCAST_RSS_PATH - Ruta del RSS (por defecto: /podcast.xml)")
        print("\n💡 Ejemplo de configuración:")
        print("   export PODCAST_DOMAIN='tudominio.com'")
        print("   export PODCAST_EPISODES_PATH='/podcast/episodes'")
        print("   export PODCAST_RSS_PATH='/podcast.xml'")
        return
    
    # Actualizar configuración
    if update_podcast_config(domain, episodes_path, rss_path):
        print("\n🎉 Configuración actualizada exitosamente!")
        print("\n📝 Próximos pasos:")
        print("1. Ejecuta: python main.py update")
        print("2. Ejecuta: python ftp_uploader.py")
        print("3. Actualiza Anchor con la nueva URL del RSS")
    else:
        print("❌ Error actualizando la configuración")

if __name__ == '__main__':
    main()
