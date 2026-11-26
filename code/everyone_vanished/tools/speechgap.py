import sys,subprocess,numpy as np,json
def load(f,g=0):
    r=subprocess.run(['ffmpeg','-v','error','-i',f,'-af',f'volume={g}dB,highpass=f=100','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(r,np.float32)
v=load(sys.argv[1],8.1); m=load(sys.argv[2]); sec=json.load(open(sys.argv[3]))
W=6400 # 0.4 s
n=min(len(v),len(m))//W
rv=20*np.log10(np.sqrt((v[:n*W].reshape(n,W)**2).mean(1))+1e-9)
rm=20*np.log10(np.sqrt((m[:n*W].reshape(n,W)**2).mean(1))+1e-9)
t=np.arange(n)*0.4
sp=rv>rv.max()-20
for k,(a,b) in sec.items():
    s=(t>=a)&(t<b)
    if (s&sp).sum()<5: continue
    g=rv[s&sp]-rm[s&sp]; q=rm[s&~sp]
    print(f'{k:9s} speech gap median {np.median(g):5.1f}  min(10pct) {np.percentile(g,10):5.1f}   music in pauses {np.median(q) if len(q) else float("nan"):6.1f} vs during speech {np.median(rm[s&sp]):6.1f}')
