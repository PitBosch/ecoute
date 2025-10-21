#!/usr/bin/env python3
"""
Script di setup automatico per Voxtral-Mini-3B-2507
Installa e configura tutte le dipendenze necessarie per utilizzare Voxtral in ecoute.
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

def check_python_version():
    """Verifica la versione di Python"""
    version = sys.version_info
    print(f"🐍 Python versione: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ richiesto per Voxtral")
        return False
    
    print("✅ Versione Python compatibile")
    return True

def check_cuda():
    """Verifica se CUDA è disponibile"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA disponibile - Device: {torch.cuda.get_device_name(0)}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB")
            return True
        else:
            print("⚠️  CUDA non disponibile - Voxtral userà CPU (molto lento)")
            return False
    except ImportError:
        print("⚠️  PyTorch non installato - sarà installato durante il setup")
        return False

def install_base_dependencies():
    """Installa le dipendenze base"""
    print("\n📦 Installazione dipendenze base...")
    
    base_packages = [
        "torch>=2.0.1",
        "torchaudio>=2.0.2",
        "transformers>=4.30.0",
        "accelerate>=0.20.0",
        "numpy>=1.24.0"
    ]
    
    for package in base_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], f"Installazione {package}"):
            return False
    
    return True

def install_voxtral_dependencies():
    """Installa le dipendenze specifiche per Voxtral"""
    print("\n🎯 Installazione dipendenze Voxtral...")
    
    voxtral_packages = [
        "mistral_common[audio]>=1.8.1",
        "soundfile>=0.12.0",
        "pydub>=0.25.0"
    ]
    
    for package in voxtral_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], f"Installazione {package}"):
            return False
    
    return True

def install_system_dependencies():
    """Installa dipendenze di sistema se necessario"""
    print("\n🔧 Verifica dipendenze di sistema...")
    
    system = platform.system().lower()
    
    if system == "linux":
        print("💡 Su Linux, potresti aver bisogno di:")
        print("   sudo apt-get install ffmpeg libsndfile1")
    elif system == "darwin":  # macOS
        print("💡 Su macOS, potresti aver bisogno di:")
        print("   brew install ffmpeg")
    elif system == "windows":
        print("💡 Su Windows, assicurati di avere:")
        print("   - Visual C++ Redistributable")
        print("   - FFmpeg (scaricabile da https://ffmpeg.org/)")
    
    return True

def test_voxtral_installation():
    """Testa l'installazione di Voxtral"""
    print("\n🧪 Test installazione Voxtral...")
    
    try:
        # Test import delle librerie principali
        print("   Testing imports...")
        from transformers import VoxtralForConditionalGeneration, AutoProcessor
        import mistral_common
        print("   ✅ Import Voxtral riuscito")
        
        # Test versioni
        import transformers
        print(f"   📋 Transformers: {transformers.__version__}")
        print(f"   📋 Mistral Common: {mistral_common.__version__}")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Errore import: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Errore generico: {e}")
        return False

def download_voxtral_model():
    """Pre-scarica il modello Voxtral per velocizzare il primo avvio"""
    print("\n⬇️  Download modello Voxtral-Mini-3B-2507...")
    
    try:
        from transformers import VoxtralForConditionalGeneration, AutoProcessor
        from huggingface_hub import snapshot_download
        
        model_id = "mistralai/Voxtral-Mini-3B-2507"
        
        print(f"   Downloading {model_id}...")
        snapshot_download(repo_id=model_id, cache_dir=None)
        print("   ✅ Modello scaricato con successo")
        
        return True
        
    except Exception as e:
        print(f"   ⚠️  Download fallito: {e}")
        print("   💡 Il modello sarà scaricato al primo utilizzo")
        return False

def update_requirements_file():
    """Aggiorna il file requirements.txt se necessario"""
    print("\n📝 Aggiornamento requirements.txt...")
    
    requirements_file = "requirements.txt"
    voxtral_deps = [
        "mistral_common[audio]>=1.8.1",
        "accelerate>=0.20.0", 
        "pydub>=0.25.0"
    ]
    
    try:
        # Leggi requirements esistenti
        with open(requirements_file, 'r') as f:
            content = f.read()
        
        # Aggiungi dipendenze Voxtral se non presenti
        lines_to_add = []
        for dep in voxtral_deps:
            if dep.split('>=')[0].split('[')[0] not in content:
                lines_to_add.append(dep)
        
        if lines_to_add:
            with open(requirements_file, 'a') as f:
                f.write("\n# Voxtral dependencies (auto-added)\n")
                for line in lines_to_add:
                    f.write(f"{line}\n")
            print(f"   ✅ Aggiunte {len(lines_to_add)} dipendenze a requirements.txt")
        else:
            print("   ✅ Requirements.txt già aggiornato")
        
        return True
        
    except Exception as e:
        print(f"   ⚠️  Errore aggiornamento requirements.txt: {e}")
        return False

def create_example_script():
    """Crea uno script di esempio per testare Voxtral"""
    print("\n📄 Creazione script di esempio...")
    
    example_script = """#!/usr/bin/env python3
# Quick test script for Voxtral
import sys
sys.path.append('.')
import TranscriberModels

print("🎙️  Testing Voxtral integration...")

try:
    model = TranscriberModels.get_model(
        use_api=False, 
        language="it", 
        use_voxtral=True
    )
    print("✅ Voxtral loaded successfully!")
    print("🚀 Ready to use Voxtral in ecoute!")
    print("   Run: python run_modern.py --voxtral")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Try running: python setup_voxtral.py")
"""
    
    try:
        with open("quick_test_voxtral.py", "w") as f:
            f.write(example_script)
        print("   ✅ Script di esempio creato: quick_test_voxtral.py")
        return True
    except Exception as e:
        print(f"   ⚠️  Errore creazione script: {e}")
        return False

def main():
    """Funzione principale del setup"""
    print("🎙️  SETUP VOXTRAL-MINI-3B-2507 PER ECOUTE")
    print("=" * 50)
    
    # Verifica Python
    if not check_python_version():
        print("\n❌ Setup interrotto - aggiorna Python")
        return False
    
    # Verifica CUDA
    check_cuda()
    
    # Installa dipendenze
    print("\n📦 INSTALLAZIONE DIPENDENZE")
    print("-" * 30)
    
    if not install_base_dependencies():
        print("\n❌ Errore installazione dipendenze base")
        return False
    
    if not install_voxtral_dependencies():
        print("\n❌ Errore installazione dipendenze Voxtral")
        return False
    
    # Installa dipendenze di sistema
    install_system_dependencies()
    
    # Testa installazione
    print("\n🧪 TEST INSTALLAZIONE")
    print("-" * 20)
    
    if not test_voxtral_installation():
        print("\n❌ Test installazione fallito")
        print("💡 Prova a eseguire: pip install --upgrade transformers mistral_common[audio]")
        return False
    
    # Aggiorna requirements
    update_requirements_file()
    
    # Crea script di esempio
    create_example_script()
    
    # Opzionale: scarica modello
    print("\n🤔 Vuoi scaricare il modello ora? (richiede ~10GB)")
    choice = input("   [y/N]: ").lower().strip()
    if choice in ['y', 'yes', 's', 'si']:
        download_voxtral_model()
    
    # Riepilogo finale
    print("\n" + "=" * 50)
    print("🎉 SETUP COMPLETATO!")
    print("=" * 50)
    print("\n✅ Voxtral-Mini-3B-2507 installato con successo!")
    print("\n🚀 Come utilizzare:")
    print("   • Interfaccia moderna: python run_modern.py --voxtral")
    print("   • Interfaccia classica: python main.py --voxtral")
    print("   • Test rapido:        python quick_test_voxtral.py")
    print("   • Test completo:      python test_voxtral.py")
    
    print("\n📋 Lingue supportate:")
    languages = ["italiano", "inglese", "spagnolo", "francese", "tedesco", "portoghese", "hindi", "olandese"]
    for lang in languages:
        print(f"   • {lang}")
    
    print(f"\n💡 Per maggiori informazioni: README_VOXTRAL.md")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrotto dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore imprevisto: {e}")
        sys.exit(1) 