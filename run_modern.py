#!/usr/bin/env python3
"""
Ecoute Modern - Avvio dell'applicazione moderna
"""

import sys
import subprocess
import os

def check_dependencies():
    """Verifica che tutte le dipendenze siano installate"""
    try:
        import PyQt6
        import sqlalchemy
        print("✅ Dipendenze PyQt6 e SQLAlchemy trovate")
    except ImportError as e:
        print(f"❌ Dipendenze mancanti: {e}")
        print("Installazione dipendenze...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6", "sqlalchemy"])
        return False
    return True

def check_ffmpeg():
    """Verifica che ffmpeg sia installato"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ FFmpeg trovato")
        return True
    except FileNotFoundError:
        print("❌ FFmpeg non trovato. Installa FFmpeg per continuare.")
        return False

def main():
    print("🎙️  Avvio Ecoute Modern...")
    
    # Verifica dipendenze
    if not check_dependencies():
        print("Riavvia l'applicazione dopo l'installazione delle dipendenze.")
        return
    
    if not check_ffmpeg():
        print("Installa FFmpeg e riprova.")
        return
    
    # Mostra info sui modelli disponibili
    print("\n📋 Modelli disponibili:")
    print("   • FasterWhisper (default): python run_modern.py")
    print("   • OpenVINO GenAI:         python run_modern.py --openvino-genai")
    print("   • Voxtral-Mini-3B:        python run_modern.py --voxtral")
    print("   • OpenVINO Whisper:       python run_modern.py --openvino")
    print("   • Ollama Whisper:         python run_modern.py --ollama")
    print("   • OpenAI API:             python run_modern.py --api")
    print("")
    
    # Avvia l'applicazione
    try:
        from modern_ui import main as run_modern_app
        print("🚀 Avvio interfaccia moderna...")
        run_modern_app()
    except Exception as e:
        print(f"❌ Errore nell'avvio: {e}")
        print("Fallback alla versione classica...")
        try:
            from main import main as run_classic_app
            run_classic_app()
        except Exception as e2:
            print(f"❌ Errore anche nella versione classica: {e2}")

if __name__ == "__main__":
    main() 