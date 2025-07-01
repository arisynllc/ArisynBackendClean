from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid, os, datetime
import logging
from werkzeug.utils import secure_filename

# Import our analysis modules
from vocal_analyzer import VocalAnalyzer
from artist_matcher import ArtistMatcher
from fx_chain_generator import FXChainGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Enable CORS for all routes
CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"], 
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"])

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'aac', 'flac'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Create upload directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize analysis components
vocal_analyzer = VocalAnalyzer()
artist_matcher = ArtistMatcher()
fx_generator = FXChainGenerator()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def health():
    """Health check endpoint"""
    return jsonify({
        "service": "Arisyn AI Vocal Analysis Backend",
        "status": "online",
        "version": "1.0.0",
        "max_file_size": "50MB",
        "supported_formats": list(ALLOWED_EXTENSIONS),
        "endpoints": {
            "analyze": "/analyze",
            "health": "/"
        }
    })

@app.route("/analyze", methods=["POST"])
def analyze():
    """Main vocal analysis endpoint"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"error": "No file part in request"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file or not allowed_file(file.filename):
            return jsonify({
                "error": "File type not allowed", 
                "supported_formats": list(ALLOWED_EXTENSIONS)
            }), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        if not filename:
            filename = f"audio_{uuid.uuid4().hex[:8]}.wav"
        
        # Save file temporarily
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        app.logger.info(f"Processing file: {filename}")
        
        # Perform vocal analysis
        vocal_metrics = vocal_analyzer.analyze(file_path)
        app.logger.debug(f"Vocal analysis complete: {vocal_metrics}")
        
        # Find artist matches
        artist_matches = artist_matcher.find_matches(vocal_metrics)
        app.logger.debug(f"Artist matching complete: {artist_matches}")
        
        # Generate FX chain recommendations
        fx_chain = fx_generator.generate_chain(vocal_metrics, artist_matches)
        app.logger.debug(f"FX chain generation complete")
        
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Return comprehensive analysis results
        return jsonify({
            "message": "Vocal analysis completed successfully",
            "filename": filename,
            "vocal_analysis": vocal_metrics,
            "artist_matches": artist_matches,
            "fx_chain": fx_chain,
            "analysis_id": str(uuid.uuid4())
        })
        
    except Exception as e:
        app.logger.error(f"Analysis error: {str(e)}")
        # Clean up file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        return jsonify({
            "error": "Internal server error during analysis",
            "details": str(e)
        }), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        "error": "File too large",
        "max_size": "50MB"
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": {
            "health": "/",
            "analyze": "/analyze"
        }
    }), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)