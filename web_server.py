"""
Servidor web Flask para el frontend del podcast
"""
import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from mutagen import File as MutagenFile
from mutagen.id3 import ID3NoHeaderError
from podcast_manager import PodcastManager

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EPISODES_FOLDER'] = 'episodes'

# Crear carpetas si no existen
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EPISODES_FOLDER'], exist_ok=True)

# Inicializar el gestor del podcast
podcast_manager = PodcastManager()

def extract_mp3_metadata(file_path):
    """Extrae metadatos de un archivo MP3"""
    try:
        audio_file = MutagenFile(file_path)
        if audio_file is None:
            return {}
        
        metadata = {}
        
        # Información básica
        if hasattr(audio_file, 'info'):
            metadata['duration'] = str(int(audio_file.info.length // 60)) + ':' + str(int(audio_file.info.length % 60)).zfill(2)
        
        # Tags ID3
        if hasattr(audio_file, 'tags') and audio_file.tags:
            tags = audio_file.tags
            
            # Mapeo de tags comunes
            tag_mapping = {
                'TIT2': 'title',           # Título
                'TPE1': 'artist',          # Artista
                'TALB': 'album',           # Álbum
                'TDRC': 'date',            # Fecha
                'TCON': 'genre',           # Género
                'COMM': 'comment',         # Comentario
                'TXXX': 'custom',          # Tags personalizados
            }
            
            for tag, field in tag_mapping.items():
                if tag in tags:
                    if tag == 'TXXX':
                        # Para tags personalizados, usar el texto como clave
                        for key, value in tags[tag].items():
                            metadata[f'custom_{key}'] = str(value)
                    else:
                        metadata[field] = str(tags[tag][0]) if tags[tag] else ''
        
        # Información del archivo
        file_stats = os.stat(file_path)
        metadata['file_size'] = file_stats.st_size
        metadata['file_name'] = os.path.basename(file_path)
        
        return metadata
        
    except Exception as e:
        print(f"Error extrayendo metadatos: {e}")
        return {}

@app.route('/')
def index():
    """Página principal - Vista pública"""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Panel de administración"""
    return render_template('admin.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """API para subir archivos y extraer metadatos"""
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó archivo'}), 400
    
    if file and file.filename.lower().endswith('.mp3'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extraer metadatos
        metadata = extract_mp3_metadata(file_path)
        
        # Obtener episodios existentes para sugerir número
        episodes = podcast_manager.episode_manager.get_episodes()
        next_episode = len(episodes) + 1 if episodes else 1
        
        return jsonify({
            'success': True,
            'filename': filename,
            'metadata': metadata,
            'suggested_episode': next_episode,
            'file_path': file_path
        })
    
    return jsonify({'error': 'Formato de archivo no válido. Solo se permiten archivos MP3'}), 400

@app.route('/api/episodes', methods=['GET'])
def get_episodes():
    """Obtener lista de episodios"""
    episodes = podcast_manager.episode_manager.get_episodes()
    return jsonify([ep.to_dict() for ep in episodes])

@app.route('/api/episodes', methods=['POST'])
def add_episode():
    """Añadir nuevo episodio"""
    try:
        data = request.json
        
        # Mover archivo de uploads a episodes
        source_path = data['file_path']
        filename = os.path.basename(source_path)
        dest_path = os.path.join(app.config['EPISODES_FOLDER'], filename)
        
        if os.path.exists(source_path):
            os.rename(source_path, dest_path)
        
        # Añadir episodio
        podcast_manager.add_new_episode(
            title=data['title'],
            description=data['description'],
            audio_filename=filename,
            duration=data['duration'],
            episode_number=data.get('episode_number'),
            season=data.get('season'),
            tracklist=data.get('tracklist', [])
        )
        
        return jsonify({'success': True, 'message': 'Episodio añadido exitosamente'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/episodes/<int:episode_id>', methods=['DELETE'])
def delete_episode(episode_id):
    """Eliminar episodio"""
    try:
        episodes = podcast_manager.episode_manager.get_episodes()
        if 0 <= episode_id < len(episodes):
            podcast_manager.episode_manager.delete_episode(episode_id)
            podcast_manager.update_rss()
            return jsonify({'success': True, 'message': 'Episodio eliminado'})
        else:
            return jsonify({'error': 'Episodio no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rss/update', methods=['POST'])
def update_rss():
    """Actualizar RSS manualmente"""
    try:
        podcast_manager.update_rss()
        return jsonify({'success': True, 'message': 'RSS actualizado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/episodes/<filename>')
def serve_episode(filename):
    """Servir archivos de episodios"""
    return send_from_directory(app.config['EPISODES_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
