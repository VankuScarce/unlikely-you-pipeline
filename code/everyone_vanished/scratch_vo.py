"""Free placeholder voice (Kokoro, am_michael) per shot, for timing. Real voice replaces vo/<id>.wav later."""
import sys, os, soundfile as sf
sys.path.insert(0, os.path.dirname(__file__))
from shots import SHOTS
from kokoro_onnx import Kokoro
k = Kokoro('/tmp/claude-0/kokoro/kokoro-v1.0.onnx', '/tmp/claude-0/kokoro/voices-v1.0.bin')
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
for sid, card, scene, p, txt in SHOTS:
    if not txt: continue
    s, sr = k.create(txt.replace('3:17 AM', 'three seventeen A M').replace('7:02', 'seven oh two'), voice='am_michael', speed=1.08, lang='en-us')
    sf.write(f'{out}/{sid}.wav', s, sr); print(sid, round(len(s)/sr, 2), flush=True)
