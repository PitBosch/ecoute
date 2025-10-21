from transformers import VoxtralForConditionalGeneration, AutoProcessor

from transformers import VoxtralForConditionalGeneration, AutoProcessor
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
repo_id = "mistralai/Voxtral-Mini-3B-2507"

processor = AutoProcessor.from_pretrained(repo_id)
model = VoxtralForConditionalGeneration.from_pretrained(repo_id, torch_dtype=torch.bfloat16, device_map=device)