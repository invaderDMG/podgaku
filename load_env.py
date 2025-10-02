#!/usr/bin/env python3
"""
Utilidad para cargar variables de entorno desde archivo .env
"""
import os
from pathlib import Path

def load_env_file(env_file='.env'):
    """Carga variables de entorno desde un archivo .env"""
    env_path = Path(env_file)
    
    if not env_path.exists():
        print(f"⚠️  Archivo {env_file} no encontrado")
        print(f"💡 Copia env.example a {env_file} y configura tus valores")
        return False
    
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Ignorar comentarios y líneas vacías
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    # Remover comillas si las hay
                    value = value.strip('\'"')
                    os.environ[key.strip()] = value
    
    print(f"✅ Variables de entorno cargadas desde {env_file}")
    return True

if __name__ == '__main__':
    load_env_file()
