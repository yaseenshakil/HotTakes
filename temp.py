from transformers import pipeline
import torch

# print("CUDA available:", torch.cuda.is_available())
# print("Number of GPUs:", torch.cuda.device_count())
# if torch.cuda.is_available():
#     print("Current GPU:", torch.cuda.current_device())
#     print("GPU name:", torch.cuda.get_device_name(0))
#     print("PyTorch CUDA version:", torch.version.cuda)

device = 0 if torch.cuda.is_available() else -1

# classifier = pipeline("text-classification", model="Falconsai/offensive_speech_detection")
classifier = pipeline("text-classification", model="AbhishekkV19/bert-base-uncased-10k-vulgarity", device=device)

# text = "you stupid cunt"
# text = "kim kardashian is a cunt!!"
# text = "taylor swift is lame"
# text = "not black"
text = "a"

result = classifier(text)
result = result[0]
result["text"] = text

print(result)
# print(classifier(["hello"]*128))