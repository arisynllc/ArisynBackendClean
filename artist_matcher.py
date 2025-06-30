import random
from typing import Dict, List, Any

class ArtistMatcher:
    """Simulates AI artist DNA matching with realistic confidence scores"""
    
    def __init__(self):
        self.artist_database = {
            "Future": {
                "vocal_characteristics": ["autotune_heavy", "melodic_rap", "mumbly", "atlanta_sound"],
                "typical_bpm": (120, 150),
                "vocal_effects": ["pitch_correction", "reverb", "delay", "distortion"],
                "genre": "Hip-Hop/Trap"
            },
            "Travis Scott": {
                "vocal_characteristics": ["psychedelic", "autotune_artistic", "energetic", "layered"],
                "typical_bpm": (130, 160),
                "vocal_effects": ["heavy_autotune", "reverb", "phaser", "compression"],
                "genre": "Hip-Hop/Psychedelic Trap"
            },
            "The Weeknd": {
                "vocal_characteristics": ["falsetto", "dark", "smooth", "r&b_influenced"],
                "typical_bpm": (90, 130),
                "vocal_effects": ["reverb", "chorus", "compression", "eq_boost"],
                "genre": "R&B/Pop"
            },
            "Drake": {
                "vocal_characteristics": ["melodic", "conversational", "canadian", "versatile"],
                "typical_bpm": (100, 140),
                "vocal_effects": ["subtle_autotune", "compression", "eq", "reverb"],
                "genre": "Hip-Hop/Pop"
            },
            "Post Malone": {
                "vocal_characteristics": ["raspy", "melodic", "country_influenced", "versatile"],
                "typical_bpm": (100, 140),
                "vocal_effects": ["autotune", "reverb", "compression", "distortion"],
                "genre": "Pop/Hip-Hop"
            },
            "Lil Uzi Vert": {
                "vocal_characteristics": ["high_pitched", "energetic", "punk_influenced", "experimental"],
                "typical_bpm": (140, 180),
                "vocal_effects": ["pitch_shift", "reverb", "delay", "distortion"],
                "genre": "Hip-Hop/Punk Rap"
            },
            "Juice WRLD": {
                "vocal_characteristics": ["melodic", "emotional", "freestyle", "versatile"],
                "typical_bpm": (120, 150),
                "vocal_effects": ["autotune", "reverb", "compression", "eq"],
                "genre": "Hip-Hop/Emo Rap"
            },
            "Kanye West": {
                "vocal_characteristics": ["soulful", "experimental", "pitched_vocals", "innovative"],
                "typical_bpm": (90, 140),
                "vocal_effects": ["pitch_shift", "vocoder", "reverb", "compression"],
                "genre": "Hip-Hop/Experimental"
            }
        }
    
    def find_matches(self, vocal_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Find artist DNA matches based on vocal analysis"""
        
        matches = []
        
        # Generate matches based on vocal characteristics
        artists = list(self.artist_database.keys())
        random.shuffle(artists)
        
        # Select 3-5 matches with varying confidence levels
        num_matches = random.randint(3, 5)
        selected_artists = artists[:num_matches]
        
        for i, artist in enumerate(selected_artists):
            artist_data = self.artist_database[artist]
            
            # Calculate confidence based on various factors
            base_confidence = random.uniform(60, 95)
            
            # Adjust confidence based on BPM similarity
            artist_bpm_range = artist_data["typical_bpm"]
            vocal_bpm = vocal_metrics.get("bpm", 120)
            
            if artist_bpm_range[0] <= vocal_bpm <= artist_bpm_range[1]:
                base_confidence += random.uniform(5, 15)
            else:
                base_confidence -= random.uniform(5, 10)
            
            # Adjust confidence based on vocal foundation
            foundation_score = vocal_metrics.get("foundation", {}).get("overall_score", 80)
            if foundation_score > 85:
                base_confidence += random.uniform(3, 8)
            
            # Ensure confidence is within realistic bounds
            confidence = max(45, min(97, base_confidence))
            
            # Generate specific matching attributes
            matching_attributes = self._generate_matching_attributes(artist_data, vocal_metrics)
            
            match_data = {
                "artist": artist,
                "confidence": round(confidence, 1),
                "genre": artist_data["genre"],
                "matching_attributes": matching_attributes,
                "recommended_effects": artist_data["vocal_effects"][:3],  # Top 3 effects
                "similarity_factors": {
                    "vocal_style": round(random.uniform(0.6, 0.95), 2),
                    "bpm_compatibility": round(random.uniform(0.5, 0.9), 2),
                    "tonal_characteristics": round(random.uniform(0.5, 0.92), 2),
                    "production_style": round(random.uniform(0.4, 0.88), 2)
                }
            }
            
            matches.append(match_data)
        
        # Sort matches by confidence (highest first)
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Generate overall DNA analysis
        primary_match = matches[0]
        dna_analysis = {
            "dominant_influence": primary_match["artist"],
            "confidence_level": "High" if primary_match["confidence"] > 80 else "Medium" if primary_match["confidence"] > 65 else "Low",
            "genre_classification": primary_match["genre"],
            "style_evolution_potential": round(random.uniform(70, 95), 1),
            "unique_characteristics": self._identify_unique_traits(vocal_metrics)
        }
        
        return {
            "matches": matches,
            "dna_analysis": dna_analysis,
            "total_artists_analyzed": len(self.artist_database),
            "analysis_confidence": round(sum(m["confidence"] for m in matches) / len(matches), 1)
        }
    
    def _generate_matching_attributes(self, artist_data: Dict, vocal_metrics: Dict) -> List[str]:
        """Generate specific attributes that match between vocal and artist"""
        possible_attributes = [
            "melodic phrasing", "vocal rhythm", "tonal quality", "breath control",
            "pitch variation", "emotional delivery", "vocal texture", "dynamic range",
            "harmonic choices", "vocal timing", "articulation style", "vocal runs"
        ]
        
        num_attributes = random.randint(2, 4)
        return random.sample(possible_attributes, num_attributes)
    
    def _identify_unique_traits(self, vocal_metrics: Dict) -> List[str]:
        """Identify unique vocal traits that set this voice apart"""
        unique_traits = []
        
        characteristics = vocal_metrics.get("characteristics", {})
        
        if characteristics.get("brightness", 0) > 0.7:
            unique_traits.append("bright vocal tone")
        if characteristics.get("warmth", 0) > 0.6:
            unique_traits.append("warm vocal texture")
        if characteristics.get("raspiness", 0) > 0.4:
            unique_traits.append("distinctive rasp")
        
        foundation = vocal_metrics.get("foundation", {})
        if foundation.get("vibrato_control", 0) > 85:
            unique_traits.append("exceptional vibrato control")
        if foundation.get("dynamic_range", 0) > 88:
            unique_traits.append("impressive dynamic range")
        
        # Add some general unique traits if we don't have enough
        general_traits = [
            "natural pitch accuracy", "distinctive vocal timbre", "unique vocal placement",
            "exceptional breath support", "natural melodic instinct", "distinctive vocal character"
        ]
        
        while len(unique_traits) < 3:
            trait = random.choice([t for t in general_traits if t not in unique_traits])
            unique_traits.append(trait)
        
        return unique_traits[:4]  # Return max 4 traits
