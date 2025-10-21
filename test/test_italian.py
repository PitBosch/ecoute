#!/usr/bin/env python3
"""
Script di test per verificare il supporto per l'italiano
"""

import TranscriberModels
import sys

def test_italian_support():
    """Testa il supporto per l'italiano"""
    print("🧪 Test del supporto per l'italiano...")
    
    try:
        # Test del modello locale
        print("📝 Testando il modello Faster Whisper per l'italiano...")
        model = TranscriberModels.get_model(use_api=False, language="it", use_ollama=False, use_openvino=False)
        print("✅ Modello Faster Whisper per l'italiano caricato con successo")
        
        # Test del modello API
        print("🌐 Testando il modello API per l'italiano...")
        api_model = TranscriberModels.get_model(use_api=True, language="it", use_ollama=False, use_openvino=False)
        print("✅ Modello API per l'italiano configurato con successo")
        
        print("\n🎉 Tutti i test sono passati! Il supporto per l'italiano è attivo.")
        return True
        
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        return False

def test_multilingual_support():
    """Testa il supporto per multiple lingue"""
    print("\n🌍 Test del supporto multilingue...")
    
    languages = ["it", "en", "es", "fr", "de"]
    
    for lang in languages:
        try:
            print(f"📝 Testando lingua: {lang}")
            model = TranscriberModels.get_model(use_api=False, language=lang, use_ollama=False, use_openvino=False)
            print(f"✅ Lingua {lang} supportata")
        except Exception as e:
            print(f"❌ Errore con lingua {lang}: {e}")
            return False
    
    print("🎉 Supporto multilingue verificato!")
    return True

if __name__ == "__main__":
    print("🚀 Avvio test per il supporto italiano...\n")
    
    success = True
    success &= test_italian_support()
    success &= test_multilingual_support()
    
    if success:
        print("\n✅ Tutti i test sono passati! Il progetto è pronto per l'uso.")
        sys.exit(0)
    else:
        print("\n❌ Alcuni test sono falliti. Controlla le dipendenze.")
        sys.exit(1) 