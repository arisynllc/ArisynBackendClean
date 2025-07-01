import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import uuid

# Import our analysis modules
from vocal_analyzer import VocalAnalyzer
from artist_matcher import ArtistMatcher
from fx_chain_generator import FXChainGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configure CORS
CORS(app, origins=["*"], methods=["GET", "POST", "OPTIONS"], 
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"])

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'flac', 'aac'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize analysis modules
vocal_analyzer = VocalAnalyzer()
artist_matcher = ArtistMatcher()
fx_chain_generator = FXChainGenerator()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "Vocal Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze - POST - Upload audio file for analysis",
            "health": "/ - GET - Health check"
        }
    })

@app.route('/analyze', methods=['POST'])
def analyze_vocal():
    """Main endpoint for vocal analysis"""
    file_path = None
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                "error": "Invalid file type. Supported formats: mp3, wav, m4a, flac, aac"
            }), 400
        
        # Generate secure filename
        if not file.filename:
            return jsonify({"error": "File must have a name"}), 400
        
        filename = secure_filename(str(file.filename))
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save uploaded file
        file.save(file_path)
        
        app.logger.info(f"Processing file: {unique_filename}")
        
        # Step 1: Vocal Analysis
        app.logger.debug("Starting vocal analysis...")
        vocal_metrics = vocal_analyzer.analyze(file_path)
        
        # Step 2: Artist Matching
        app.logger.debug("Starting artist matching...")
        artist_match = artist_matcher.find_matches(vocal_metrics)
        
        # Step 3: FX Chain Generation
        app.logger.debug("Generating FX chain...")
        fx_chain = fx_chain_generator.generate_chain(vocal_metrics, artist_match)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        # Prepare response
        response_data = {
            "success": True,
            "analysis": {
                "vocal_metrics": vocal_metrics,
                "artist_match": artist_match,
                "fx_chain": fx_chain
            },
            "message": "Vocal analysis completed successfully"
        }
        
        app.logger.info(f"Analysis completed for {unique_filename}")
        return jsonify(response_data)
        
    except RequestEntityTooLarge:
        return jsonify({"error": "File too large. Maximum size is 50MB"}), 413
    
    except Exception as e:
        app.logger.error(f"Error during analysis: {str(e)}")
        
        # Clean up file if it exists
        if file_path:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass  # Ignore cleanup errors
            
        return jsonify({
            "error": "Internal server error during analysis",
            "message": str(e)
        }), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({"error": "File too large. Maximum size is 50MB"}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)