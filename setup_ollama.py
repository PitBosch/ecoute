#!/usr/bin/env python3
"""
Script per installare e configurare Ollama per Ecoute
"""

import subprocess
import sys
import os
import platform

def check_ollama_installed():
    """Verifica se Ollama è installato"""
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ollama():
    """Installa Ollama"""
    system = platform.system().lower()
    
    print("🔧 Installazione di Ollama...")
    
    if system == "windows":
        print("📥 Scaricando Ollama per Windows...")
        # Usa winget se disponibile
        try:
            subprocess.run(["winget", "install", "ollama.ollama"], check=True)
            print("✅ Ollama installato con winget")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ winget non disponibile. Installa manualmente da https://ollama.ai")
            return False
    
    elif system == "darwin":  # macOS
        print("📥 Scaricando Ollama per macOS...")
        try:
            subprocess.run(["brew", "install", "ollama"], check=True)
            print("✅ Ollama installato con Homebrew")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Homebrew non disponibile. Installa manualmente da https://ollama.ai")
            return False
    
    elif system == "linux":
        print("📥 Scaricando Ollama per Linux...")
        try:
            subprocess.run(["curl", "-fsSL", "https://ollama.ai/install.sh", "|", "sh"], shell=True, check=True)
            print("✅ Ollama installato")
        except subprocess.CalledProcessError:
            print("❌ Errore nell'installazione. Installa manualmente da https://ollama.ai")
            return False
    
    return True

def setup_whisper_model():
    """Configura il modello Whisper"""
    print("🤖 Configurando il modello Whisper...")
    
    try:
        # Scarica il modello Whisper
        subprocess.run(["ollama", "pull", "whisper"], check=True)
        print("✅ Modello Whisper scaricato")
        
        # Test del modello
        print("🧪 Testando il modello...")
        test_result = subprocess.run(["ollama", "run", "whisper", "--help"], capture_output=True, text=True)
        if test_result.returncode == 0:
            print("✅ Modello Whisper funzionante")
            return True
        else:
            print("❌ Errore nel test del modello")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore nella configurazione: {e}")
        return False

def main():
    print("🚀 Setup di Ollama per Ecoute\n")
    
    # Verifica se Ollama è già installato
    if check_ollama_installed():
        print("✅ Ollama già installato")
    else:
        print("📥 Ollama non trovato, installazione...")
        if not install_ollama():
            print("❌ Installazione fallita")
            sys.exit(1)
    
    # Configura il modello Whisper
    if not setup_whisper_model():
        print("❌ Configurazione del modello fallita")
        sys.exit(1)
    
    print("\n🎉 Setup completato!")
    print("Ora puoi usare Ecoute con Ollama:")
    print("python main.py --ollama")
    
    # Test finale
    print("\n🧪 Test finale...")
    try:
        result = subprocess.run(["ollama", "run", "whisper", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tutto funziona perfettamente!")
        else:
            print("⚠️  Modello installato ma potrebbe richiedere configurazione manuale")
    except Exception as e:
        print(f"⚠️  Test finale fallito: {e}")

if __name__ == "__main__":
    main() 