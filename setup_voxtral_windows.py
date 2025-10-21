#!/usr/bin/env python3
"""
Script di setup semplificato per Voxtral su Windows
Evita i problemi di compilazione con mistral_common[audio]
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Esegue un comando e gestisce gli errori"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} completato")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore durante {description}")
        print(f"Comando: {' '.join(command)}")
        print(f"Errore: {e.stderr}")
        return False

def check_system():
    """Verifica il sistema operativo"""
    system = platform.system()
    if system != "Windows":
        print(f"⚠️  Questo script è ottimizzato per Windows. Sistema rilevato: {system}")
        print("💡 Per altri sistemi usa: python setup_voxtral.py")
    
    version = sys.version_info
    print(f"🐍 Python versione: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ richiesto per Voxtral")
        return False
    
    print("✅ Sistema compatibile")
    return True

def install_basic_dependencies():
    """Installa le dipendenze base per Windows"""
    print("\n📦 Installazione dipendenze base per Windows...")
    
    # Dipendenze che funzionano bene su Windows con wheel precompilati
    packages = [
        "torch>=2.0.1",
        "transformers>=4.30.0", 
        "accelerate>=0.20.0",
        "numpy>=1.24.0",
        "soundfile>=0.12.0",
        "pydub>=0.25.0"
    ]
    
    for package in packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], f"Installazione {package}"):
            return False
    
    return True

def install_mistral_common():
    """Installa mistral_common senza le dipendenze audio problematiche"""
    print("\n🎯 Installazione mistral_common (versione Windows)...")
    
    # Installa mistral_common base senza le dipendenze audio
    if not run_command([sys.executable, "-m", "pip", "install", "mistral_common", "--no-deps"], 
                      "Installazione mistral_common base"):
        return False
    
    # Installa le dipendenze necessarie manualmente
    deps = ["click", "pydantic", "requests"]
    for dep in deps:
        if not run_command([sys.executable, "-m", "pip", "install", dep], f"Installazione {dep}"):
            continue  # Non critico se fallisce
    
    return True

def test_installation():
    """Testa l'installazione"""
    print("\n🧪 Test installazione...")
    
    try:
        # Test import
        print("   Testing imports...")
        from transformers import VoxtralForConditionalGeneration, AutoProcessor
        import mistral_common
        print("   ✅ Import riusciti")
        
        # Test versioni
        import transformers
        print(f"   📋 Transformers: {transformers.__version__}")
        print(f"   📋 Mistral Common: {mistral_common.__version__}")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Errore import: {e}")
        return False

def create_windows_test_script():
    """Crea uno script di test ottimizzato per Windows"""
    print("\n📄 Creazione script di test Windows...")
    
    script_content = '''#!/usr/bin/env python3
"""
Test script Voxtral per Windows
Versione semplificata senza dipendenze audio avanzate
"""

import sys
import os

# Aggiungi il percorso corrente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import TranscriberModels
    
    print("🎙️  Test Voxtral per Windows...")
    print("=" * 50)
    
    # Test caricamento modello
    print("\\n[INFO] Caricamento modello Voxtral...")
    model = TranscriberModels.get_model(
        use_api=False, 
        language="it", 
        use_voxtral=True
    )
    print("✅ Modello Voxtral caricato con successo!")
    
    print("\\n🚀 INSTALLAZIONE COMPLETATA!")
    print("=" * 50)
    print("Per usare Voxtral:")
    print("   • python run_modern.py --voxtral")
    print("   • python main.py --voxtral")
    
except Exception as e:
    print(f"❌ Errore: {e}")
    print("\\n💡 Soluzioni:")
    print("   1. Riavvia il terminale")
    print("   2. Esegui: python setup_voxtral_windows.py")
    print("   3. Controlla le dipendenze con: pip list")
'''
    
    try:
        with open("test_voxtral_windows.py", "w", encoding="utf-8") as f:
            f.write(script_content)
        print("   ✅ Script creato: test_voxtral_windows.py")
        return True
    except Exception as e:
        print(f"   ⚠️  Errore: {e}")
        return False

def show_windows_instructions():
    """Mostra istruzioni specifiche per Windows"""
    print("\n" + "=" * 60)
    print("🎉 SETUP WINDOWS COMPLETATO!")
    print("=" * 60)
    
    print(f"\n✅ Voxtral installato con successo su Windows!")
    
    print(f"\n🚀 Come utilizzare:")
    print("   • Interfaccia moderna: python run_modern.py --voxtral")
    print("   • Interfaccia classica: python main.py --voxtral") 
    print("   • Test Windows:        python test_voxtral_windows.py")
    
    print(f"\n⚠️  Note importanti per Windows:")
    print("   • Il primo avvio scaricherà il modello (~10GB)")
    print("   • Senza GPU, Voxtral sarà molto lento")
    print("   • Chiudi altre applicazioni per liberare RAM")
    
    print(f"\n🔧 In caso di problemi:")
    print("   • Riavvia PowerShell come amministratore")
    print("   • Verifica: pip list | findstr transformers")
    print("   • Reinstalla: python setup_voxtral_windows.py")
    
    return True

def main():
    """Funzione principale"""
    print("🏠 SETUP VOXTRAL PER WINDOWS")
    print("=" * 40)
    print("Versione ottimizzata per sistemi Windows")
    
    # Verifica sistema
    if not check_system():
        return False
    
    # Installa dipendenze
    if not install_basic_dependencies():
        print("\n❌ Errore installazione dipendenze base")
        return False
    
    # Installa mistral_common
    if not install_mistral_common():
        print("\n❌ Errore installazione mistral_common")
        return False
    
    # Test installazione
    if not test_installation():
        print("\n❌ Test fallito")
        print("💡 Prova a riavviare PowerShell e ripeti il setup")
        return False
    
    # Crea script di test
    create_windows_test_script()
    
    # Mostra istruzioni
    show_windows_instructions()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n💡 Documentazione completa: README_VOXTRAL.md")
            input("\nPremi Invio per chiudere...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrotto")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        sys.exit(1) 