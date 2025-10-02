# 🎙️ Podgaku Podcast RSS Generator

Sistema completo para generar y gestionar el feed RSS de tu podcast, con migración desde Anchor y despliegue automático a tu propio servidor.

## 🚀 Características

- ✅ **Frontend web moderno** con drag & drop para subir episodios
- ✅ **Extracción automática** de metadatos MP3 (ID3 tags)
- ✅ **Generación automática** de RSS XML válido y bien formateado
- ✅ **Gestión visual** de episodios con tracklists
- ✅ **Migración completa** desde Anchor RSS
- ✅ **Despliegue automático** vía SFTP
- ✅ **Frontend web público** desplegable en servidor
- ✅ **Panel de administración** web con estadísticas
- ✅ **Soporte completo** para metadatos (tracklist, temporadas, etc.)
- ✅ **Responsive design** para móviles y tablets
- ✅ **Variables de entorno** para configuración segura

## 📁 Estructura del proyecto

```
podcastXMLgen/
├── main.py                 # Script principal (línea de comandos)
├── web_server.py           # Servidor web Flask local
├── start_web.py            # Script para iniciar el servidor web
├── podcast_manager.py      # Gestor principal del podcast
├── episode_manager.py      # Gestión de episodios
├── rss_generator.py        # Generador de RSS XML
├── podcast_config.py       # Configuración del podcast
├── load_env.py             # Cargador de variables de entorno
├── sftp_uploader.py        # Subida de archivos vía SFTP
├── upload_web.py           # Despliegue del frontend web
├── deploy_to_ftp.py        # Despliegue completo automatizado
├── fix_episode_mapping.py  # Corrección de mapeo de episodios
├── .env                    # Variables de entorno (crear desde .env.example)
├── env.example             # Ejemplo de variables de entorno
├── templates/              # Plantillas HTML (sistema local)
│   ├── index.html          # Vista pública local
│   └── admin.html          # Panel de administración local
├── static/                 # Archivos estáticos (sistema local)
│   ├── css/style.css       # Estilos CSS
│   ├── js/app.js           # JavaScript vista pública
│   ├── js/admin.js         # JavaScript administración
│   └── img/                # Imágenes (banner, logo)
├── web_static/             # Frontend web para servidor
│   ├── index.html          # Vista pública web
│   ├── admin.html          # Panel administración web
│   ├── app.js              # JavaScript público
│   ├── admin.js            # JavaScript admin
│   ├── style.css           # Estilos CSS
│   └── img/                # Imágenes
├── uploads/                # Archivos temporales (se crea automáticamente)
├── episodes/               # Archivos de audio finales (se crea automáticamente)
├── episodes.json           # Base de datos de episodios (se crea automáticamente)
├── podcast.xml             # Feed RSS generado
└── README.md              # Este archivo
```

## ⚙️ Configuración inicial

### 1. Instalar dependencias

```bash
pip install flask mutagen python-dotenv paramiko
```

### 2. Configurar variables de entorno

Copia el archivo de ejemplo y edítalo con tus datos:

```bash
cp env.example .env
```

Edita `.env` con tus credenciales:

```bash
# Configuración del Podcast
PODCAST_DOMAIN=tudominio.com
PODCAST_EPISODES_PATH=/episodes
PODCAST_RSS_PATH=/rss.xml

# Credenciales SFTP
FTP_HOST=tudominio.com
FTP_USERNAME=tu_usuario
FTP_PASSWORD=tu_contraseña
FTP_PORT=22
FTP_EPISODES_DIR=/www/episodes
FTP_RSS_PATH=/www/rss.xml
```

### 3. Configurar información del podcast

Edita `podcast_config.py` con los datos de tu podcast:

```python
PODCAST_CONFIG = {
    "title": "Tu Podcast",
    "description": "Descripción de tu podcast",
    "author": "Tu Nombre",
    "email": "tu@email.com",
    "website": "https://tudominio.com",
    "image_url": "https://tudominio.com/cover.jpg",
    "category": "Music",
    "explicit": False,
    "type": "episodic"
}
```

### 4. Migrar episodios existentes (opcional)

Si vienes desde Anchor u otro servicio:

```bash
python main.py migrate
```

## 🎯 Uso del sistema

### 🌐 Frontend Web Local (Recomendado para gestión)

1. **Iniciar el servidor web**:
   ```bash
   python start_web.py
   ```

2. **Abrir en el navegador**:
   ```
   http://localhost:8080
   ```

3. **Gestionar episodios**:
   - **Vista pública**: `http://localhost:8080/`
   - **Administración**: `http://localhost:8080/admin`

4. **Subir nuevo episodio**:
   - Ve al panel de administración
   - Arrastra un archivo MP3/M4A al área de subida
   - Los metadatos se extraen automáticamente
   - Completa la información faltante
   - Añade el tracklist (una canción por línea)
   - ¡Guarda y el RSS se actualiza automáticamente!

### 📡 Despliegue al servidor

Una vez que tengas episodios listos:

1. **Despliegue completo** (recomendado para primera vez):
   ```bash
   python deploy_to_ftp.py
   ```
   Esto hace:
   - Actualiza configuración para producción
   - Regenera RSS con URLs correctas
   - Sube todos los archivos de audio
   - Sube el RSS actualizado

2. **Solo subir archivos nuevos**:
   ```bash
   python sftp_uploader.py
   ```

3. **Desplegar frontend web**:
   ```bash
   python upload_web.py
   ```

### 💻 Línea de Comandos

**Comandos disponibles**:
```bash
# Añadir un nuevo episodio interactivamente
python main.py add

# Listar todos los episodios
python main.py list

# Ver el episodio más reciente
python main.py latest

# Actualizar el RSS manualmente
python main.py update

# Migrar desde Anchor
python main.py migrate

# Ver ayuda
python main.py help
```

## 🌐 Tu sitio web desplegado

Una vez desplegado, tendrás:

- **🏠 Página principal**: `https://tudominio.com/`
  - Lista todos los episodios
  - Botones de reproducción y descarga
  - Tracklists organizadas
  - Diseño responsive

- **🔧 Panel de administración**: `https://tudominio.com/admin.html`
  - Estadísticas del podcast
  - Información detallada de episodios
  - Vista de gestión

- **📡 RSS Feed**: `https://tudominio.com/rss.xml`
  - Listo para Apple Podcasts, Spotify, etc.

## 📊 Flujo de trabajo completo

### Para añadir un nuevo episodio:

1. **🎵 Preparar audio**: Archivo MP3/M4A con metadatos ID3
2. **💻 Sistema local**: 
   ```bash
   python start_web.py
   ```
3. **📝 Administración**: `http://localhost:8080/admin`
4. **📤 Subir**: Drag & drop del archivo
5. **✏️ Editar**: Completar metadatos y tracklist
6. **💾 Guardar**: El sistema actualiza automáticamente
7. **🚀 Desplegar**:
   ```bash
   python sftp_uploader.py
   ```
8. **✅ ¡Listo!**: Episodio disponible en tu web y RSS

### Para gestión diaria:

- **Local**: Desarrollo y pruebas en `localhost:8080`
- **Web**: Vista pública en tu dominio
- **RSS**: Actualización automática
- **Backup**: Todos los datos en `episodes.json`

## 🔧 Archivos importantes

### Variables de entorno (`.env`)
```bash
# Nunca subir este archivo a git
# Contiene credenciales sensibles
PODCAST_DOMAIN=tudominio.com
FTP_USERNAME=usuario
FTP_PASSWORD=contraseña
# ... más configuraciones
```

### Base de datos (`episodes.json`)
```json
{
  "title": "Título del episodio",
  "description": "Descripción con\n\nsaltos de línea",
  "audio_url": "https://tudominio.com/episodes/archivo.mp3",
  "duration": "45:30",
  "pub_date": "2024-01-15T10:00:00",
  "episode_number": 1,
  "season": 1,
  "tracklist": [
    "Canción 1 - Artista 1",
    "Canción 2 - Artista 2"
  ]
}
```

### RSS generado (`podcast.xml`)
- Formato estándar RSS 2.0
- Compatible con iTunes/Apple Podcasts
- Metadatos completos
- Tracklists en HTML
- URLs absolutas para producción

## 🛠️ Personalización avanzada

### Cambiar diseño web
Edita los archivos en `web_static/`:
- `style.css`: Colores, fuentes, layout
- `index.html`: Estructura de la página pública
- `admin.html`: Panel de administración

### Añadir metadatos al RSS
Modifica `rss_generator.py`:
```python
# Añadir campo personalizado
custom_field = ET.SubElement(item, "itunes:customField")
custom_field.text = "valor personalizado"
```

### Configurar servidor web
Edita `web_server.py` para:
- Cambiar puerto
- Añadir rutas
- Modificar configuración Flask

## 🆘 Solución de problemas

### Error de conexión SFTP
```bash
❌ Error: Operation timed out
```
**Solución**:
- Verifica credenciales en `.env`
- Confirma que el puerto sea 22 (SFTP)
- Prueba conexión manual: `sftp usuario@servidor`

### RSS no se actualiza
```bash
❌ URLs incorrectas en el RSS
```
**Solución**:
```bash
python main.py update
```

### Archivos no se suben
```bash
❌ Permission denied
```
**Solución**:
- Verifica permisos del directorio remoto
- Confirma rutas en `.env`
- Usa rutas absolutas: `/www/episodes`

### Frontend web no carga
```bash
❌ Error 404 en imágenes
```
**Solución**:
```bash
python upload_web.py
```

### Tracklists no aparecen
```bash
⚠️ Episodios sin tracklist
```
**Solución**:
```bash
python fix_tracklists.py
```

## 📋 Checklist de despliegue

### Primera vez:
- [ ] Configurar `.env` con credenciales
- [ ] Editar `podcast_config.py`
- [ ] Migrar episodios existentes
- [ ] Probar sistema local
- [ ] Desplegar con `deploy_to_ftp.py`
- [ ] Subir frontend con `upload_web.py`
- [ ] Verificar RSS en navegador
- [ ] Probar reproducción de episodios

### Episodio nuevo:
- [ ] Subir via frontend local
- [ ] Verificar metadatos y tracklist
- [ ] Probar reproducción local
- [ ] Desplegar con `sftp_uploader.py`
- [ ] Verificar en web pública

## 🔒 Seguridad

- ✅ **Variables de entorno**: Credenciales nunca en código
- ✅ **SFTP**: Conexión cifrada
- ✅ **Frontend estático**: Sin vulnerabilidades de servidor
- ✅ **Validación**: Archivos de audio verificados

## 📈 Estadísticas disponibles

El panel de administración web muestra:
- Total de episodios
- Duración total del podcast
- Duración promedio por episodio
- Total de canciones en tracklists
- Episodios con tracklist completa
- Último episodio publicado

## 🎧 Compatibilidad

### Plataformas soportadas:
- ✅ Apple Podcasts
- ✅ Spotify
- ✅ Google Podcasts
- ✅ Overcast
- ✅ Pocket Casts
- ✅ Cualquier app que soporte RSS

### Formatos de audio:
- ✅ MP3 (recomendado)
- ✅ M4A
- ✅ Otros formatos soportados por navegadores

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente para tu podcast.

---

**¡Disfruta creando contenido para tu podcast! 🎧**

*Sistema desarrollado para Podgaku - Explorando los sonidos de la música japonesa*