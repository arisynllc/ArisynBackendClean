import os
import logging
import time
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import mimetypes

from vocal_analyzer import VocalAnalyzer
from artist_matcher import ArtistMatcher
from fx_chain_generator import FXChainGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "arisyn-dev-key-2025")

# Configure CORS for v0.dev integration
CORS(app, origins=["*"], methods=["GET", "POST", "OPTIONS"], 
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"])

# File upload configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'flac', 'aac'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize analysis components
vocal_analyzer = VocalAnalyzer()
artist_matcher = ArtistMatcher()
fx_chain_generator = FXChainGenerator()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_audio_file(file):
    """Validate uploaded audio file"""
    if not file:
        return False, "No file provided"
    
    if file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, f"Unsupported file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS).upper()}"
    
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type and not mime_type.startswith('audio/'):
        return False, "File is not a valid audio format"
    
    return True, "Valid file"

@app.route('/', methods=['GET'])
def root_check():
    """Root endpoint health check"""
    return jsonify({
        "status": "online",
        "service": "Arisyn AI Vocal Analysis Backend",
        "version": "1.0.0",
        "endpoints": {
            "health": "/",
            "analyze": "/analyze"
        },
        "supported_formats": list(ALLOWED_EXTENSIONS),
        "max_file_size": "50MB"
    }), 200

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_vocal():
    """Main vocal analysis endpoint"""
    try:
        # Handle CORS preflight
        if request.method == 'OPTIONS':
            return '', 204
        
        # Check if file is in request
        if 'audio' not in request.files:
            return jsonify({
                "error": "No audio file provided",
                "message": "Please upload an audio file using the 'audio' field"
            }), 400
        
        file = request.files['audio']
        
        # Validate file
        is_valid, validation_message = validate_audio_file(file)
        if not is_valid:
            return jsonify({
                "error": "Invalid file",
                "message": validation_message
            }), 400
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        timestamp = str(int(time.time()))
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        app.logger.info(f"File uploaded successfully: {unique_filename}")
        
        # Simulate AI processing delay (1-3 seconds)
        processing_delay = random.uniform(1.2, 2.8)
        time.sleep(processing_delay)
        
        # Perform vocal analysis
        vocal_metrics = vocal_analyzer.analyze(file_path)
        
        # Get artist DNA match
        artist_match = artist_matcher.find_matches(vocal_metrics)
        
        # Generate FX chain recommendations
        fx_chain = fx_chain_generator.generate_chain(vocal_metrics, artist_match)
        
        # Generate mock before/after URLs (in production, these would be processed audio files)
        base_url = request.host_url.rstrip('/')
        before_url = f"{base_url}/audio/before/{unique_filename}"
        after_url = f"{base_url}/audio/after/{unique_filename}"
        
        # Construct comprehensive analysis response
        analysis_response = {
            "status": "success",
            "processing_time": round(processing_delay, 2),
            "file_info": {
                "original_name": filename,
                "size_mb": round(os.path.getsize(file_path) / (1024 * 1024), 2),
                "format": filename.rsplit('.', 1)[1].lower() if '.' in filename else "unknown"
            },
            "vocal_analysis": vocal_metrics,
            "artist_dna": artist_match,
            "fx_chain": fx_chain,
            "audio_urls": {
                "before": before_url,
                "after": after_url
            },
            "soundcard_data": {
                "title": f"Vocal Analysis - {filename}",
                "artist_match_primary": artist_match["matches"][0]["artist"],
                "match_percentage": artist_match["matches"][0]["confidence"],
                "key_signature": vocal_metrics["key"],
                "bpm": vocal_metrics["bpm"],
                "vocal_range": vocal_metrics["range"],
                "foundation_score": vocal_metrics["foundation"]["overall_score"]
            },
            "timestamp": timestamp
        }
        
        app.logger.info(f"Analysis completed for {filename}")
        
        # Clean up uploaded file (optional - keep for demo purposes)
        # os.remove(file_path)
        
        return jsonify(analysis_response), 200
        
    except RequestEntityTooLarge:
        return jsonify({
            "error": "File too large",
            "message": "Maximum file size is 50MB"
        }), 413
        
    except Exception as e:
        app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({
            "error": "Analysis failed",
            "message": f"An error occurred during vocal analysis: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist",
        "available_endpoints": ["/", "/analyze"]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred on the server"
    }), 500
