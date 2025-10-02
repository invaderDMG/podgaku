#!/usr/bin/env python3
"""
🚀 DESPLIEGUE COMPLETO DE PODGAKU
=================================
Script maestro que sube todo el contenido al servidor:
- RSS actualizado
- Episodios nuevos/modificados
- Frontend web completo

Autor: Sistema de Podcast Podgaku
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔄 {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=False, text=True)
        print(f"✅ {description} - COMPLETADO")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}")
        print(f"   Código de salida: {e.returncode}")
        return False

def check_prerequisites():
    """Verifica que todo esté listo para el despliegue"""
    print("🔍 VERIFICANDO PRERREQUISITOS")
    print("=" * 50)
    
    # Verificar archivo .env
    if not Path('.env').exists():
        print("❌ Archivo .env no encontrado")
        print("   Crea el archivo .env con las credenciales del servidor")
        return False
    
    # Cargar variables de entorno
    load_dotenv()
    required_vars = ['FTP_HOST', 'FTP_USERNAME', 'FTP_PASSWORD', 'FTP_EPISODES_DIR', 'FTP_RSS_PATH']
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
        return False
    
    # Verificar archivos necesarios
    required_files = ['episodes.json', 'podcast_config.py', 'web_static/index.html', 'web_static/admin.html']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    print("✅ Todos los prerrequisitos están listos")
    return True

def main():
    """Función principal del despliegue"""
    print("🚀 DESPLIEGUE COMPLETO DE PODGAKU")
    print("=" * 50)
    print("Este script realizará las siguientes acciones:")
    print("1. 📄 Regenerar RSS con configuración actualizada")
    print("2. 📡 Subir episodios nuevos/modificados + RSS")
    print("3. 🌐 Subir frontend web completo")
    print("4. ✅ Verificar que todo esté funcionando")
    print()
    
    # Verificar prerrequisitos
    if not check_prerequisites():
        print("\n❌ DESPLIEGUE CANCELADO - Corrige los errores y vuelve a intentar")
        sys.exit(1)
    
    # Verificar si se ejecuta en modo no interactivo
    auto_deploy = '--auto' in sys.argv or '--yes' in sys.argv
    
    if not auto_deploy:
        # Pedir confirmación solo en modo interactivo
        try:
            response = input("¿Continuar con el despliegue completo? (s/N): ").lower().strip()
            if response not in ['s', 'si', 'sí', 'y', 'yes']:
                print("🚫 Despliegue cancelado por el usuario")
                sys.exit(0)
        except (EOFError, KeyboardInterrupt):
            print("\n🚫 Despliegue cancelado")
            sys.exit(0)
    else:
        print("🤖 Modo automático activado - procediendo sin confirmación")
    
    print("\n🎬 INICIANDO DESPLIEGUE COMPLETO...")
    
    success_count = 0
    total_steps = 3
    
    # Paso 1: Regenerar RSS
    if run_command("python main.py update", "Regenerando RSS"):
        success_count += 1
    
    # Paso 2: Subir episodios y RSS
    if run_command("python update_podcast.py", "Subiendo episodios y RSS"):
        success_count += 1
    
    # Paso 3: Subir frontend web
    if run_command("python upload_web.py", "Subiendo frontend web"):
        success_count += 1
    
    # Resumen final
    print("\n" + "=" * 60)
    print("🎉 RESUMEN DEL DESPLIEGUE")
    print("=" * 60)
    
    if success_count == total_steps:
        print("✅ ¡DESPLIEGUE COMPLETADO CON ÉXITO!")
        print(f"   {success_count}/{total_steps} pasos completados")
        print("\n🌐 Tu podcast está disponible en:")
        
        # Obtener dominio de las variables de entorno
        load_dotenv()
        domain = os.getenv('PODCAST_DOMAIN', 'tu-dominio.com')
        
        print(f"   📱 Vista pública: https://{domain}/")
        print(f"   🔧 Administración: https://{domain}/admin.html")
        print(f"   📡 RSS Feed: https://{domain}/rss.xml")
        
        print("\n💡 Próximos pasos:")
        print("   • Verifica que el sitio web carga correctamente")
        print("   • Comprueba que las tracklists aparecen")
        print("   • Prueba el RSS en tu app de podcasts favorita")
        
    else:
        print(f"⚠️  DESPLIEGUE PARCIAL: {success_count}/{total_steps} pasos completados")
        print("   Revisa los errores anteriores y vuelve a ejecutar el script")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🚫 Despliegue interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
