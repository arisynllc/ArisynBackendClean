import random
from typing import Dict, List, Any

class FXChainGenerator:
    """Generates realistic FX chain recommendations based on vocal analysis and artist matches"""
    
    def __init__(self):
        self.fx_categories = {
            "pitch": {
                "autotune": {"intensity": (0.1, 1.0), "speed": (0.1, 100), "humanize": (0, 50)},
                "pitch_correction": {"strength": (0.1, 0.8), "preserve_vibrato": (0, 100)},
                "harmony": {"voices": (1, 4), "spread": (5, 20), "mix": (10, 60)},
                "octave": {"shift": (-12, 12), "mix": (10, 40)}
            },
            "eq": {
                "low_cut": {"frequency": (20, 120), "slope": (6, 48)},
                "presence_boost": {"frequency": (2000, 8000), "gain": (1, 6), "q": (0.5, 3.0)},
                "warmth": {"frequency": (200, 800), "gain": (-2, 4), "q": (0.8, 2.5)},
                "air": {"frequency": (8000, 16000), "gain": (0.5, 4), "q": (0.3, 1.5)},
                "de_ess": {"frequency": (4000, 9000), "threshold": (-20, -5), "ratio": (2, 8)}
            },
            "dynamics": {
                "compressor": {"threshold": (-25, -5), "ratio": (2, 8), "attack": (0.1, 10), "release": (50, 500)},
                "limiter": {"threshold": (-3, -0.1), "release": (5, 100)},
                "gate": {"threshold": (-60, -20), "attack": (0.1, 5), "release": (10, 200)},
                "de_esser": {"threshold": (-15, -5), "frequency": (4000, 8000)}
            },
            "space": {
                "reverb": {"type": ["hall", "room", "plate", "spring"], "size": (0.1, 1.0), "decay": (0.5, 8.0), "mix": (5, 40)},
                "delay": {"time": (50, 500), "feedback": (10, 70), "mix": (5, 30)},
                "chorus": {"rate": (0.1, 2.0), "depth": (10, 80), "mix": (5, 25)},
                "spatial_enhancer": {"width": (100, 200), "depth": (0, 100)}
            },
            "time": {
                "echo": {"time": (100, 1000), "feedback": (10, 60), "mix": (10, 35)},
                "modulation_delay": {"time": (200, 800), "mod_rate": (0.1, 1.0), "mod_depth": (5, 50)},
                "ping_pong_delay": {"left_time": (150, 400), "right_time": (200, 600), "feedback": (15, 55)},
                "tape_delay": {"time": (100, 600), "wow_flutter": (0, 30), "saturation": (0, 40)}
            }
        }
    
    def generate_chain(self, vocal_metrics: Dict[str, Any], artist_match: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive FX chain based on analysis"""
        
        primary_artist = artist_match["matches"][0]["artist"]
        recommended_effects = artist_match["matches"][0]["recommended_effects"]
        
        # Build FX chain for each category
        fx_chain = {}
        
        # Pitch processing
        fx_chain["pitch"] = self._generate_pitch_fx(vocal_metrics, primary_artist, recommended_effects)
        
        # EQ processing
        fx_chain["eq"] = self._generate_eq_fx(vocal_metrics, primary_artist)
        
        # Dynamics processing
        fx_chain["dynamics"] = self._generate_dynamics_fx(vocal_metrics, primary_artist)
        
        # Spatial processing
        fx_chain["space"] = self._generate_space_fx(vocal_metrics, primary_artist, recommended_effects)
        
        # Time-based processing
        fx_chain["time"] = self._generate_time_fx(vocal_metrics, primary_artist, recommended_effects)
        
        # Generate processing order and overall settings
        chain_metadata = self._generate_chain_metadata(fx_chain, primary_artist)
        
        return {
            "fx_chain": fx_chain,
            "metadata": chain_metadata,
            "artist_inspiration": primary_artist,
            "processing_confidence": round(random.uniform(82, 96), 1),
            "estimated_processing_time": round(random.uniform(15, 45), 1)  # seconds
        }
    
    def _generate_pitch_fx(self, vocal_metrics: Dict, artist: str, recommended_effects: List[str]) -> Dict[str, Any]:
        """Generate pitch processing effects"""
        pitch_fx = {"enabled": [], "disabled": []}
        
        # Autotune/Pitch Correction based on artist style
        autotune_artists = ["Future", "Travis Scott", "Juice WRLD", "Post Malone"]
        
        if artist in autotune_artists or "autotune" in recommended_effects:
            autotune_settings = {
                "name": "autotune",
                "enabled": True,
                "parameters": {
                    "intensity": round(random.uniform(0.3, 0.9), 2),
                    "speed": round(random.uniform(5, 40), 1),
                    "humanize": round(random.uniform(10, 40), 1),
                    "key": vocal_metrics.get("key", "C Major"),
                    "scale": "chromatic" if artist == "Travis Scott" else "major"
                }
            }
            pitch_fx["enabled"].append(autotune_settings)
        else:
            # Subtle pitch correction
            correction_settings = {
                "name": "pitch_correction",
                "enabled": True,
                "parameters": {
                    "strength": round(random.uniform(0.2, 0.6), 2),
                    "preserve_vibrato": round(random.uniform(60, 90), 1),
                    "cents_tolerance": round(random.uniform(15, 35), 1)
                }
            }
            pitch_fx["enabled"].append(correction_settings)
        
        # Harmony generation (sometimes)
        if random.random() > 0.6:  # 40% chance
            harmony_settings = {
                "name": "harmony",
                "enabled": True,
                "parameters": {
                    "voices": random.randint(1, 3),
                    "spread": round(random.uniform(5, 15), 1),
                    "mix": round(random.uniform(15, 35), 1),
                    "intervals": ["third", "fifth"] if random.random() > 0.5 else ["octave"]
                }
            }
            pitch_fx["enabled"].append(harmony_settings)
        
        return pitch_fx
    
    def _generate_eq_fx(self, vocal_metrics: Dict, artist: str) -> Dict[str, Any]:
        """Generate EQ processing chain"""
        eq_chain = []
        
        # High-pass filter (always included)
        high_pass = {
            "name": "high_pass",
            "enabled": True,
            "parameters": {
                "frequency": round(random.uniform(60, 100), 1),
                "slope": random.choice([12, 18, 24]),
                "resonance": round(random.uniform(0.5, 1.2), 1)
            }
        }
        eq_chain.append(high_pass)
        
        # Presence boost for clarity
        presence = {
            "name": "presence_boost",
            "enabled": True,
            "parameters": {
                "frequency": round(random.uniform(3000, 6000), 1),
                "gain": round(random.uniform(2, 5), 1),
                "q": round(random.uniform(1.0, 2.5), 1)
            }
        }
        eq_chain.append(presence)
        
        # Warmth adjustment based on vocal characteristics
        characteristics = vocal_metrics.get("characteristics", {})
        warmth_level = characteristics.get("warmth", 0.5)
        
        warmth = {
            "name": "warmth",
            "enabled": True,
            "parameters": {
                "frequency": round(random.uniform(400, 800), 1),
                "gain": round(random.uniform(-1, 3), 1) if warmth_level < 0.5 else round(random.uniform(1, 4), 1),
                "q": round(random.uniform(1.0, 2.0), 1)
            }
        }
        eq_chain.append(warmth)
        
        # Air/brightness boost
        if characteristics.get("brightness", 0.5) < 0.6:
            air = {
                "name": "air_boost",
                "enabled": True,
                "parameters": {
                    "frequency": round(random.uniform(10000, 15000), 1),
                    "gain": round(random.uniform(1, 3), 1),
                    "q": round(random.uniform(0.5, 1.5), 1)
                }
            }
            eq_chain.append(air)
        
        # De-esser if needed
        if characteristics.get("brightness", 0.5) > 0.7:
            de_ess = {
                "name": "de_esser",
                "enabled": True,
                "parameters": {
                    "frequency": round(random.uniform(5000, 8000), 1),
                    "threshold": round(random.uniform(-15, -8), 1),
                    "ratio": round(random.uniform(3, 6), 1)
                }
            }
            eq_chain.append(de_ess)
        
        return {"chain": eq_chain, "bypass_all": False}
    
    def _generate_dynamics_fx(self, vocal_metrics: Dict, artist: str) -> Dict[str, Any]:
        """Generate dynamics processing chain"""
        dynamics_chain = []
        
        # Compressor (essential for vocals)
        foundation = vocal_metrics.get("foundation", {})
        dynamic_range = foundation.get("dynamic_range", 75)
        
        compressor = {
            "name": "vocal_compressor",
            "enabled": True,
            "parameters": {
                "threshold": round(random.uniform(-18, -8), 1),
                "ratio": round(random.uniform(3, 6), 1),
                "attack": round(random.uniform(1, 5), 1),
                "release": round(random.uniform(100, 300), 1),
                "knee": round(random.uniform(1, 4), 1),
                "makeup_gain": round(random.uniform(2, 8), 1)
            }
        }
        dynamics_chain.append(compressor)
        
        # Limiter for peak control
        limiter = {
            "name": "peak_limiter",
            "enabled": True,
            "parameters": {
                "threshold": round(random.uniform(-2, -0.5), 1),
                "release": round(random.uniform(10, 50), 1),
                "lookahead": round(random.uniform(2, 8), 1)
            }
        }
        dynamics_chain.append(limiter)
        
        # Gate for noise control (if needed)
        if foundation.get("tone_consistency", 80) < 75:
            gate = {
                "name": "noise_gate",
                "enabled": True,
                "parameters": {
                    "threshold": round(random.uniform(-45, -25), 1),
                    "attack": round(random.uniform(0.5, 3), 1),
                    "release": round(random.uniform(50, 150), 1),
                    "hold": round(random.uniform(5, 20), 1)
                }
            }
            dynamics_chain.append(gate)
        
        return {"chain": dynamics_chain, "parallel_processing": random.random() > 0.7}
    
    def _generate_space_fx(self, vocal_metrics: Dict, artist: str, recommended_effects: List[str]) -> Dict[str, Any]:
        """Generate spatial processing effects"""
        space_fx = []
        
        # Reverb (almost always included)
        reverb_types = {
            "Future": "hall",
            "Travis Scott": "hall",
            "The Weeknd": "plate",
            "Drake": "room",
            "Post Malone": "room"
        }
        
        reverb = {
            "name": "reverb",
            "enabled": True,
            "parameters": {
                "type": reverb_types.get(artist, random.choice(["hall", "room", "plate"])),
                "size": round(random.uniform(0.3, 0.8), 2),
                "decay": round(random.uniform(1.2, 4.0), 1),
                "pre_delay": round(random.uniform(10, 40), 1),
                "mix": round(random.uniform(15, 35), 1),
                "damping": round(random.uniform(0.3, 0.7), 2)
            }
        }
        space_fx.append(reverb)
        
        # Chorus for width (sometimes)
        if "chorus" in recommended_effects or random.random() > 0.6:
            chorus = {
                "name": "chorus",
                "enabled": True,
                "parameters": {
                    "rate": round(random.uniform(0.3, 1.2), 2),
                    "depth": round(random.uniform(20, 60), 1),
                    "mix": round(random.uniform(10, 25), 1),
                    "voices": random.randint(2, 4)
                }
            }
            space_fx.append(chorus)
        
        # Stereo widening
        if artist in ["Travis Scott", "The Weeknd"]:
            widener = {
                "name": "stereo_widener",
                "enabled": True,
                "parameters": {
                    "width": round(random.uniform(120, 180), 1),
                    "bass_mono": True,
                    "frequency_split": round(random.uniform(200, 400), 1)
                }
            }
            space_fx.append(widener)
        
        return {"effects": space_fx, "send_levels": round(random.uniform(15, 35), 1)}
    
    def _generate_time_fx(self, vocal_metrics: Dict, artist: str, recommended_effects: List[str]) -> Dict[str, Any]:
        """Generate time-based processing effects"""
        time_fx = []
        
        # Delay based on artist style
        delay_artists = ["Travis Scott", "Future", "The Weeknd", "Kanye West"]
        
        if artist in delay_artists or "delay" in recommended_effects:
            delay_type = "ping_pong" if artist == "Travis Scott" else "stereo"
            
            delay = {
                "name": f"{delay_type}_delay",
                "enabled": True,
                "parameters": {
                    "time": round(random.uniform(150, 400), 1),
                    "feedback": round(random.uniform(20, 50), 1),
                    "mix": round(random.uniform(12, 28), 1),
                    "filter": {
                        "high_cut": round(random.uniform(6000, 12000), 1),
                        "low_cut": round(random.uniform(100, 300), 1)
                    }
                }
            }
            
            if delay_type == "ping_pong":
                delay["parameters"]["spread"] = round(random.uniform(50, 100), 1)
            
            time_fx.append(delay)
        
        # Modulation delay for texture
        if random.random() > 0.7:  # 30% chance
            mod_delay = {
                "name": "modulation_delay",
                "enabled": True,
                "parameters": {
                    "time": round(random.uniform(200, 600), 1),
                    "mod_rate": round(random.uniform(0.2, 0.8), 2),
                    "mod_depth": round(random.uniform(10, 40), 1),
                    "mix": round(random.uniform(8, 20), 1)
                }
            }
            time_fx.append(mod_delay)
        
        return {"effects": time_fx, "tempo_sync": vocal_metrics.get("bpm", 120)}
    
    def _generate_chain_metadata(self, fx_chain: Dict, artist: str) -> Dict[str, Any]:
        """Generate metadata about the FX chain"""
        
        # Count enabled effects
        total_effects = 0
        for category in fx_chain.values():
            if isinstance(category, dict):
                if "enabled" in category:
                    total_effects += len(category.get("enabled", []))
                elif "chain" in category:
                    total_effects += len(category.get("chain", []))
                elif "effects" in category:
                    total_effects += len(category.get("effects", []))
        
        # Processing order
        processing_order = [
            "pitch", "eq", "dynamics", "space", "time"
        ]
        
        # CPU usage estimation
        cpu_usage = round(random.uniform(15, 45), 1)
        
        # Latency estimation
        latency_ms = round(random.uniform(8, 25), 1)
        
        return {
            "total_effects": total_effects,
            "processing_order": processing_order,
            "cpu_usage_percent": cpu_usage,
            "latency_ms": latency_ms,
            "artist_style": artist,
            "chain_complexity": "High" if total_effects > 12 else "Medium" if total_effects > 8 else "Low",
            "recommended_for": ["recording", "live_performance"] if total_effects < 10 else ["recording"]
        }
