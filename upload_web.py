#!/usr/bin/env python3
"""
Script para subir el frontend web estático al servidor
"""
import os
import paramiko
from pathlib import Path
from load_env import load_env_file

def upload_web_frontend():
    """Sube el frontend web estático al servidor"""
    
    load_env_file()
    
    host = os.getenv('FTP_HOST')
    port = int(os.getenv('FTP_PORT', '22'))
    username = os.getenv('FTP_USERNAME')
    password = os.getenv('FTP_PASSWORD')
    
    print("🌐 Subiendo Frontend Web de Podgaku")
    print("=" * 35)
    print(f"🔍 Servidor: {host}:{port}")
    print(f"👤 Usuario: {username}")
    
    if not all([host, username, password]):
        print("❌ Error: Faltan credenciales en el archivo .env")
        return False
    
    try:
        # Conectar
        print(f"\n🔌 Conectando...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, port=port, username=username, password=password)
        
        sftp = ssh.open_sftp()
        print("✅ Conexión SFTP establecida")
        
        # Archivos a subir
        web_files = [
            ('web_static/index.html', '/www/index.html'),
            ('web_static/admin.html', '/www/admin.html'),
            ('web_static/app.js', '/www/app.js'),
            ('web_static/admin.js', '/www/admin.js'),
            ('web_static/style.css', '/www/style.css'),
            ('web_static/img/banner.png', '/www/img/banner.png'),
            ('web_static/img/logo.jpg', '/www/img/logo.jpg'),
            ('web_static/img/logo3000.png', '/www/img/logo3000.png')
        ]
        
        # Crear directorio img si no existe
        try:
            sftp.stat('/www/img')
            print("📁 Directorio /www/img existe")
        except FileNotFoundError:
            print("📁 Creando directorio /www/img...")
            sftp.mkdir('/www/img')
        
        # Subir archivos
        print(f"\n📁 Subiendo {len(web_files)} archivos web...")
        
        for i, (local_path, remote_path) in enumerate(web_files, 1):
            local_file = Path(local_path)
            if local_file.exists():
                print(f"   [{i}/{len(web_files)}] {local_file.name}...")
                try:
                    sftp.put(str(local_file), remote_path)
                    print(f"   ✅ Subido: {local_file.name}")
                except Exception as e:
                    print(f"   ❌ Error subiendo {local_file.name}: {e}")
            else:
                print(f"   ⚠️  Archivo no encontrado: {local_path}")
        
        sftp.close()
        ssh.close()
        
        print("\n🎉 Frontend web subido correctamente!")
        print("\n🌐 Tu sitio web está disponible en:")
        print(f"   📱 Vista pública: https://podgaku.jdlcgarcia.es/")
        print(f"   🔧 Administración: https://podgaku.jdlcgarcia.es/admin.html")
        print(f"   📡 RSS Feed: https://podgaku.jdlcgarcia.es/rss.xml")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    success = upload_web_frontend()
    if success:
        print("\n💡 Notas importantes:")
        print("• El frontend es completamente estático y lee directamente del RSS")
        print("• Para añadir episodios, usa el sistema local y luego sube con sftp_uploader.py")
        print("• El panel de administración web es solo informativo")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())
