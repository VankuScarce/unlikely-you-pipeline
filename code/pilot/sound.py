"""Procedural music bed + SFX for the cold open (no licensed assets). Writes 48k stereo wav."""
import numpy as np, wave, sys
SR=48000; DUR=40.0; N=int(SR*DUR)
rng=np.random.default_rng(3)
mus=np.zeros(N); sfx=np.zeros(N)
T=np.arange(N)/SR
def add(buf,t0,sig):
    i=int(t0*SR); j=min(N,i+len(sig)); buf[i:j]+=sig[:j-i]
def env(n,a=0.005,d=0.3):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def tone(f,dur,a=0.005,d=0.3,kind='sine'):
    n=int(dur*SR); t=np.arange(n)/SR
    w=np.sin(2*np.pi*f*t) if kind=='sine' else np.sign(np.sin(2*np.pi*f*t))*0.5
    return w*env(n,a,d)
def lp(x,k=0.05):
    y=np.zeros_like(x); s=0
    for i in range(len(x)): s+=k*(x[i]-s); y[i]=s
    return y
def noise(dur): return rng.normal(0,1,int(dur*SR))
# --- music: D minor pad
def pad(f0,t0,t1,amp):
    n=int((t1-t0)*SR); t=np.arange(n)/SR
    sig=sum(np.sin(2*np.pi*f*t+ph)*(0.5 if f>f0 else 1) for f,ph in ((f0,0),(f0*1.5,1),(f0*2.0018,2),(f0*1.189,0.5)))
    e=np.minimum(1,t/1.5)*np.minimum(1,(n/SR-t)/0.8)
    add(mus,t0,sig*e*amp)
pad(73.42,0,8.6,0.05)          # D2 calm-ish
pad(73.42,8.6,19,0.07); pad(69.30,19,26,0.08); pad(65.41,26,33.2,0.09)
# pulse kick from 8.6
bpm=100; beat=60/bpm
def kick():
    n=int(0.35*SR); t=np.arange(n)/SR; f=50+90*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)
t=8.6
while t<33.2:
    add(mus,t,kick()*(0.22 if t<26 else 0.32)); 
    if t>=26:
        add(mus,t+beat/2, np.diff(noise(0.06),prepend=0)*env(int(0.06*SR),0.001,0.02)*0.06)
    t+=beat
# bass ostinato in chase
for k in range(int((33.2-26)/ (beat/2))):
    f=[73.42,73.42,87.31,65.41][k%4]
    add(mus,26+k*beat/2,tone(f,beat/2,0.003,0.12,'square')*0.10)
# sting at 36.4
for f in (146.8,174.6,220.0,293.7):
    add(mus,36.4,tone(f,3.5,0.01,1.2,'square')*0.06)
add(mus,36.4,kick()*0.6)
add(mus,36.4,lp(noise(2.5),0.02)*np.exp(-np.arange(int(2.5*SR))/SR*2)*0.3)
# --- sfx
add(sfx,0.3,tone(1318.5,1.2,0.002,0.4)*0.25); add(sfx,0.55,tone(1046.5,1.4,0.002,0.5)*0.25)  # door chime
for k in range(14):  # typing
    add(sfx,10.0+k*0.1+rng.uniform(0,0.04), np.diff(noise(0.03),prepend=0)*env(int(0.03*SR),0.0005,0.008)*0.18)
add(sfx,11.0,tone(880,0.18,0.001,0.1,'square')*0.12); add(sfx,11.2,tone(660,0.25,0.001,0.15,'square')*0.12)  # error beep
add(sfx,12.2,tone(440,0.5,0.001,0.3,'square')*0.10)
n=int(0.6*SR); tt=np.arange(n)/SR  # stamp thud
add(sfx,15.45,(np.sin(2*np.pi*(60+40*np.exp(-tt*20))*tt)*np.exp(-tt*8)*0.6 + lp(noise(0.6),0.2)*np.exp(-tt*25)*0.4))
st=lp(noise(3.2),0.3)-lp(noise(3.2),0.05)   # radio static
add(sfx,19.0,st*0.10*np.minimum(1,np.arange(len(st))/SR/0.3))
for k in range(5): add(sfx,19.3+k*0.55,tone(1800+300*k,0.08,0.001,0.04,'square')*0.06)
def siren(t0,dur):
    n=int(dur*SR); tt=np.arange(n)/SR; f=750+450*np.sin(2*np.pi*tt/dur*2-np.pi/2)
    s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.minimum(1,tt/0.1)*np.minimum(1,(dur-tt)/0.3)
    add(sfx,t0,s*0.10)
siren(25.15,1.6); siren(26.8,6.0)
for i,t0 in enumerate((28.5,29.4,30.3,31.2)): add(sfx,t0,tone(880*2**(i/6),0.4,0.002,0.15)*0.18)
for k in range(2): add(sfx,34.6+k,np.diff(noise(0.04),prepend=0)*env(int(0.04*SR),0.0005,0.01)*0.25)
for tr in (8.6,14.0,19.0,22.2,26.0,33.2,36.4):  # whoosh
    w=lp(noise(0.5),0.08); e=np.sin(np.linspace(0,np.pi,len(w)))**2; add(sfx,tr-0.3,w*e*0.35)
out=np.stack([mus+sfx, mus+sfx],1)
out=out/np.max(np.abs(out))*0.85
with wave.open(sys.argv[1],'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((out*32767).astype(np.int16).tobytes())
print('ok')
