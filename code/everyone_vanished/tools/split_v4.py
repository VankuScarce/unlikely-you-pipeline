import json, subprocess, numpy as np, re, difflib, sys, warnings, os
warnings.filterwarnings('ignore')
from faster_whisper import WhisperModel
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from shots import SHOTS
T={s:t for s,_,_,_,t in SHOTS}
SR=44100
m=WhisperModel('small.en',device='cpu',compute_type='int8')
G=json.load(open('vo_v4/groups.json'))
os.makedirs('vo_v4/lines',exist_ok=True)
NUM={'7:02':['7','02'],'3:17':['3','17'],'am':['am'],'forty-one':['41'],'2023':['2023'],'2025':['2025'],'2017':['2017'],'2021':['2021']}
def norm(w):
    w=w.lower().replace('’',"'")
    w=re.sub(r"[^a-z0-9':\-]",'',w)
    return w
def toks(text):
    out=[]
    for w in text.split():
        n=norm(w)
        if n in NUM: out+=NUM[n]; continue
        for p in re.split(r'[\-:]',n):
            p=p.strip("'")
            if p: out.append(p)
    return out
def load(f,sr):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-f','f32le','-ac','1','-ar',str(sr),'-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).copy()
report={}
for g,info in G.items():
    best=None
    for tk in 'ab':
        f=f'vo_v4/takes/{g}_{tk}.mp3'
        a16=load(f,16000)
        segs,_=m.transcribe(a16,language='en',word_timestamps=True,beam_size=5)
        words=[(w.word.strip(),w.start,w.end) for s in segs for w in s.words]
        # whisper tokens (split numbers like 7.02 / 3.17 / a.m.)
        wt=[]
        for w,s,e in words:
            n=w.lower().replace('a.m.','am').replace('p.m.','pm')
            parts=[p for p in re.split(r"[^a-z0-9']+",n) if p.strip("'")]
            for p in parts: wt.append((p.strip("'"),s,e))
        # script tokens with line index
        st=[]; 
        for li,sid in enumerate(info['ids']):
            for t in toks(T[sid]): st.append((t,li))
        sm=difflib.SequenceMatcher(None,[t for t,_ in st],[t for t,_,_ in wt],autojunk=False)
        errs=[]
        for op,i1,i2,j1,j2 in sm.get_opcodes():
            if op!='equal': errs.append((op,' '.join(t for t,_ in st[i1:i2]),' '.join(t for t,_,_ in wt[j1:j2]),info['ids'][st[min(i1,len(st)-1)][1]]))
        score=len(errs)
        if best is None or score<best[0]: best=(score,tk,wt,st,sm,errs)
    score,tk,wt,st,sm,errs=best
    report[g]={'take':tk,'errors':errs}
    # map script token -> whisper time
    tim=[None]*len(st)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): tim[blk.a+k]=(wt[blk.b+k][1],wt[blk.b+k][2])
    a=load(f'vo_v4/takes/{g}_{tk}.mp3',SR)
    nl=len(info['ids'])
    first=[None]*nl; last=[None]*nl
    for i,(t,li) in enumerate(st):
        if tim[i] is None: continue
        if first[li] is None: first[li]=tim[i][0]
        last[li]=tim[i][1]
    # cut points: min-energy within gap between last[li] and first[li+1]
    hop=int(0.01*SR); env=np.sqrt(np.convolve(a**2,np.ones(hop)/hop,'same'))
    cuts=[0]
    for li in range(nl-1):
        s0=int((last[li]-0.05)*SR); s1=int((first[li+1]+0.05)*SR)
        s0=max(s0,cuts[-1]+1); s1=max(s1,s0+hop)
        seg=env[s0:s1]; c=s0+int(np.argmin(seg))
        cuts.append(c)
    cuts.append(len(a))
    for li,sid in enumerate(info['ids']):
        x=a[cuts[li]:cuts[li+1]]
        # trim silence to 0.08 s pads
        e=np.sqrt(np.convolve(x**2,np.ones(hop)/hop,'same')); thr=max(e.max()*0.02,1e-4)
        idx=np.where(e>thr)[0]
        if len(idx): x=x[max(0,idx[0]-int(0.08*SR)):min(len(x),idx[-1]+int(0.12*SR))]
        fl=int(0.008*SR); x=x.copy(); x[:fl]*=np.linspace(0,1,fl); x[-fl:]*=np.linspace(1,0,fl)
        p=subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-c:a','pcm_s16le',f'vo_v4/lines/{sid}.wav'],input=x.astype(np.float32).tobytes())
    print(g,'take',tk,'errors',len(errs),[e for e in errs][:6],flush=True)
json.dump(report,open('vo_v4/report.json','w'),indent=1)
