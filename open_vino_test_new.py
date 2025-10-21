from datasets import load_dataset
from transformers import AutoProcessor
from optimum.intel.openvino import OVModelForSpeechSeq2Seq
import openvino_genai as ov_genai
import datasets

import huggingface_hub as hf_hub

model_id = "OpenVINO/whisper-tiny-int8-ov"
model_id_large = "OpenVINO/whisper-large-v3-int8-ov"
model_path = "whisper-tiny-int8-ov"

hf_hub.snapshot_download(model_id, local_dir=model_path)



device = "GPU"
pipe = ov_genai.WhisperPipeline(model_path, device)

dataset = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation", trust_remote_code=True)
sample = dataset[0]["audio"]["array"]
print(pipe.generate(sample))
