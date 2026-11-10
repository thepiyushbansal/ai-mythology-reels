"""Step 2: voiceover + timings.
Speaks each line with Kokoro's Hindi male voice, trims silence, joins with short pauses,
and writes assets/voiceover.wav + timings.json (start/end per line, start per caption word).
"""
import json, os, sys
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from script import LINES

VOICE = sys.argv[1] if len(sys.argv) > 1 else "hm_omega"
SPEED = float(sys.argv[2]) if len(sys.argv) > 2 else 1.05
GAP, LEAD = 0.35, 0.4                  # pause between lines, silence before the first line

k = Kokoro(os.path.expanduser("~/tts/kokoro-v1.0.int8.onnx"), os.path.expanduser("~/tts/voices-v1.0.bin"))

def trim(a, sr, thr=0.01):
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx) == 0:
        return a
    s, e = max(idx[0] - int(.03 * sr), 0), min(idx[-1] + int(.06 * sr), len(a))
    return a[s:e]

out, t, timings, sr = [], LEAD, [], 24000
out.append(np.zeros(int(LEAD * sr), dtype=np.float32))
for i, L in enumerate(LINES):
    a, sr = k.create(L["hi"], voice=VOICE, speed=SPEED, lang="hi")
    a = trim(a.astype(np.float32), sr)
    dur = len(a) / sr
    # spread caption words over the line by spoken length (Devanagari chars per word, + pause weight on punctuation)
    hi_w, en_w = L["hi"].split(), L["en"].split()
    assert len(hi_w) == len(en_w), (i, len(hi_w), len(en_w))
    weights = [len(w.strip("।,.!?:")) + (3 if w[-1] in "।,.!?:" or w.endswith("...") else 0) + 2 for w in hi_w]
    tot, acc, words = sum(weights), 0, []
    for w_en, wt in zip(en_w, weights):
        words.append(dict(w=w_en, t=round(t + dur * acc / tot, 3)))
        acc += wt
    timings.append(dict(i=i, start=round(t, 3), end=round(t + dur, 3), words=words, key=L["key"], title=L["title"]))
    out.append(a)
    out.append(np.zeros(int(GAP * sr), dtype=np.float32))
    t += dur + GAP

os.makedirs("assets", exist_ok=True)
audio = np.concatenate(out)
audio = audio / max(1e-6, np.abs(audio).max()) * 0.89
sf.write("assets/voice_raw.wav", audio, sr)
json.dump(timings, open("timings.json", "w"), indent=1, ensure_ascii=False)
print(f"voice={VOICE} speed={SPEED} total={len(audio)/sr:.2f}s")
for T in timings:
    print(f"  {T['i']+1}. {T['start']:6.2f}-{T['end']:6.2f}  {T['title']}")
