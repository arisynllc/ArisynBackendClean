# Vocal Analysis API - Replit.md

## Overview

This is a Flask-based vocal analysis API that simulates AI-powered vocal analysis, artist matching, and FX chain generation for audio files. The application accepts audio uploads, analyzes vocal characteristics, matches them against a database of artists, and generates recommended audio processing chains.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **CORS Support**: Enabled for cross-origin requests (configured for v0.dev integration)
- **File Upload**: Werkzeug-based file handling with 50MB limit
- **Logging**: Python's built-in logging module configured for DEBUG level

### Core Components
The application follows a modular architecture with separate classes handling different aspects of vocal analysis:

1. **Flask Application** (`app.py`) - Main web server and routing
2. **Vocal Analyzer** (`vocal_analyzer.py`) - Simulates vocal characteristic analysis
3. **Artist Matcher** (`artist_matcher.py`) - Matches vocals against artist database
4. **FX Chain Generator** (`fx_chain_generator.py`) - Generates audio processing recommendations

## Key Components

### 1. Flask Application (app.py)
- **Purpose**: Main web server handling HTTP requests and file uploads
- **Key Features**:
  - File upload validation for audio formats (mp3, wav, m4a, flac, aac)
  - CORS configuration for frontend integration
  - Error handling for file size limits (50MB max)
  - Session management with configurable secret key

### 2. Vocal Analyzer (vocal_analyzer.py)
- **Purpose**: Simulates comprehensive vocal analysis
- **Analysis Metrics**:
  - Musical key and mode detection
  - BPM estimation
  - Vocal range classification (Soprano, Alto, Tenor, etc.)
  - Foundation metrics (pitch accuracy, breath control, tone consistency)
  - Advanced characteristics (brightness, warmth, raspiness)

### 3. Artist Matcher (artist_matcher.py)
- **Purpose**: Matches analyzed vocals against known artist profiles
- **Artist Database**: Includes popular artists like Future, Travis Scott, The Weeknd, Drake
- **Matching Criteria**:
  - Vocal characteristics
  - BPM ranges
  - Typical vocal effects used
  - Genre classification

### 4. FX Chain Generator (fx_chain_generator.py)
- **Purpose**: Generates audio processing recommendations
- **FX Categories**:
  - Pitch processing (autotune, pitch correction, harmony)
  - EQ (frequency shaping, presence, warmth)
  - Dynamics (compression, limiting, gating)
  - Spatial effects (reverb, delay, chorus)
  - Time-based effects (echo, modulation delay)

## Data Flow

1. **Upload**: Client uploads audio file via HTTP POST
2. **Validation**: File format and size validation
3. **Analysis**: VocalAnalyzer processes the audio file (simulated)
4. **Matching**: ArtistMatcher compares characteristics against database
5. **FX Generation**: FXChainGenerator creates processing recommendations
6. **Response**: JSON response with analysis results and recommendations

## External Dependencies

### Python Packages
- **Flask**: Web framework for API endpoints
- **Flask-CORS**: Cross-origin resource sharing support
- **Werkzeug**: File upload utilities and security

### File System Dependencies
- **Upload Directory**: `uploads/` folder for temporary file storage
- **Supported Formats**: MP3, WAV, M4A, FLAC, AAC audio files

## Deployment Strategy

### Environment Configuration
- **Session Secret**: Configurable via `SESSION_SECRET` environment variable
- **Default Port**: 5000 (configurable)
- **Debug Mode**: Enabled for development

### File Storage
- **Upload Folder**: Local filesystem storage in `uploads/` directory
- **File Validation**: Secure filename handling and extension checking
- **Size Limits**: 50MB maximum file size enforced

### CORS Configuration
- **Origins**: Wildcard allowed (configured for development)
- **Methods**: GET, POST, OPTIONS
- **Headers**: Content-Type, Authorization, X-Requested-With

## User Preferences

Preferred communication style: Simple, everyday language.

## Changelog

Changelog:
- June 30, 2025. Initial setup