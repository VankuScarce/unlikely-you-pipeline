import sys, json, subprocess, numpy as np, re, os
from faster_whisper import WhisperModel
vo, ids, out = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
m = WhisperModel('small.en', device='cpu', compute_type='int8')
res = json.load(open(out)) if os.path.exists(out) else {}
for i in ids:
    if i in res: continue
    raw = subprocess.run(['ffmpeg','-v','error','-i',f'{vo}/{i}.wav','-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout
    a = np.frombuffer(raw, np.float32)
    segs, _ = m.transcribe(a, language='en', word_timestamps=True, beam_size=5)
    res[i] = [(w.word.strip(), round(w.start,3), round(w.end,3)) for s in segs for w in s.words]
    print(i, len(res[i]), ' '.join(w for w,_,_ in res[i])[:90], flush=True)
json.dump(res, open(out,'w'))
