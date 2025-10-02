# 🚀 Guía de Despliegue a FTP

## 📋 Configuración con Variables de Entorno

### 1. **Crear archivo de configuración**

```bash
# Copiar el archivo de ejemplo
cp env.example .env

# Editar con tus credenciales
nano .env
```

### 2. **Configurar variables de entorno**

Edita el archivo `.env` con tus datos:

```bash
# Configuración del Podcast
PODCAST_DOMAIN=tudominio.com
PODCAST_EPISODES_PATH=/podcast/episodes
PODCAST_RSS_PATH=/podcast.xml

# Credenciales FTP
FTP_HOST=ftp.tudominio.com
FTP_USERNAME=tu_usuario_ftp
FTP_PASSWORD=tu_contraseña_ftp
FTP_PORT=21
FTP_EPISODES_DIR=/podcast/episodes
FTP_RSS_PATH=/podcast.xml
```

### 3. **Desplegar automáticamente**

```bash
# Despliegue completo en un solo comando
python deploy_to_ftp.py
```

## 🔧 Scripts Individuales

### **Actualizar configuración**
```bash
python update_config_for_ftp.py
```

### **Regenerar RSS**
```bash
python main.py update
```

### **Subir archivos al FTP**
```bash
python ftp_uploader.py
```

## 📁 Estructura en el Servidor

```
/
├── podcast.xml                    # Feed RSS principal
└── podcast/
    └── episodes/
        ├── 01 - The Checkers.m4a
        ├── 02 - Onyanko Club.m4a
        ├── ...
        └── 21 - Anime Ops 10s Parte 1.mp3
```

## 🌐 URLs Resultantes

- **RSS**: `https://tudominio.com/podcast.xml`
- **Episodios**: `https://tudominio.com/podcast/episodes/`

## ⚠️ Consideraciones de Seguridad

1. **Nunca subas el archivo `.env`** a repositorios públicos
2. **Usa contraseñas seguras** para el FTP
3. **Considera usar SFTP** en lugar de FTP si es posible
4. **Verifica permisos** de escritura en el servidor

## 🔍 Verificación Post-Despliegue

1. **Verificar RSS**: Abre `https://tudominio.com/podcast.xml` en el navegador
2. **Verificar episodios**: Prueba algunos enlaces de audio
3. **Actualizar Anchor**: Cambia la URL del RSS en Anchor
4. **Probar reproducción**: Verifica que los episodios se reproducen correctamente

## 🆘 Solución de Problemas

### **Error de conexión FTP**
- Verifica que `FTP_HOST` y `FTP_PORT` sean correctos
- Confirma que las credenciales sean válidas
- Verifica que el servidor FTP esté funcionando

### **Error de permisos**
- Asegúrate de que el usuario FTP tenga permisos de escritura
- Verifica que las rutas de directorios existan

### **RSS no accesible**
- Verifica que el archivo se subió correctamente
- Confirma que la URL sea accesible desde el navegador
- Revisa la configuración de `PODCAST_DOMAIN`

## 📞 Soporte

Si tienes problemas, verifica:
1. Variables de entorno configuradas correctamente
2. Credenciales FTP válidas
3. Permisos de escritura en el servidor
4. URLs accesibles desde el navegador
