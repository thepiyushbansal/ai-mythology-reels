"""Optional step: listen back to the voiceover and save the time of every spoken word.

Runs faster-whisper on assets/voice_raw.wav and writes whisper_words.json.
build.py uses it, when present, to light up each caption word exactly when it's spoken.
"""
import json
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")
segments, _ = model.transcribe("assets/voice_raw.wav", language="hi", word_timestamps=True)
words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for seg in segments for w in seg.words]
json.dump(words, open("whisper_words.json", "w"), ensure_ascii=False, indent=1)
print(f"{len(words)} words saved to whisper_words.json")
