#!/usr/bin/env python3
"""
Test molto semplice per OpenVINO GenAI
"""

try:
    print("1. Test import openvino_genai...")
    import openvino_genai as ov_genai
    print("✅ Import openvino_genai OK")
    
    print("\n2. Test caricamento modello...")
    model_path = "whisper-large-v3-turbo-int8"
    
    # Prova CPU
    print("   Tentativo con PU...")
    try:
        pipe = ov_genai.WhisperPipeline(model_path, "GPU")
        print("   ✅ Modello caricato su CPU!")
        
        # Test molto semplice
        import numpy as np
        test_audio = np.random.random(16000).astype(np.float32)
        result = pipe.generate(test_audio)
        print(f"   ✅ Test trascrizione: '{result}'")
        
    except Exception as e:
        print(f"   ❌ Errore CPU: {e}")
        
except Exception as e:
    print(f"❌ Errore generale: {e}")
    import traceback
    traceback.print_exc()