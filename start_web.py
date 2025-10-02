#!/usr/bin/env python3
"""
Script para iniciar el servidor web del podcast
"""
import os
import sys
from web_server import app

def main():
    print("🎙️  Iniciando Podgaku Web Server...")
    print("📡 Servidor disponible en: http://localhost:8080")
    print("🔄 Presiona Ctrl+C para detener el servidor")
    print("-" * 50)
    
    # Verificar que las carpetas necesarias existen
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('episodes', exist_ok=True)
    
    # Iniciar el servidor
    app.run(debug=True, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
