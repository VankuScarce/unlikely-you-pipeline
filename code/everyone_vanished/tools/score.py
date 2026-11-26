"""Lay the per-section ElevenLabs music cues on the episode timeline with crossfades.
Usage: python3 score.py SECTIONS.json CUE_DIR OUT.wav TOTAL_SECONDS"""
import sys, json, subprocess, numpy as np, wave, re
SR=48000
sec=json.load(open(sys.argv[1])); cdir=sys.argv[2]; out=sys.argv[3]; total=float(sys.argv[4])
# cue file, section key, start offset, gain dB (relative), fade-in, fade-out
PLAN=[('c01','cold',0.0,0,0.5,3.0),('c02','auto',-0.6,-1,1.2,2.5),('c03','grid',-0.6,1.5,1.5,2.5),('c04','door',-0.4,0,0.6,0.8),
      ('c05','reveal',-0.2,-2,0.4,2.5),('c06','week1',-0.6,-1,1.2,2.5),('c07','month1',-0.6,1,1.0,2.5),('c08','comforts',-0.6,0,1.5,2.5),
      ('c09','quiet',-0.8,2,2.0,3.0),('c10','year1',-0.8,0,2.0,2.5),('c11','mission',-0.6,0,1.5,2.5),('c12','end',-0.8,-1,2.0,4.0)]
def load(f):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).astype(float)
def lufs(f):
    o=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',f,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.search(r'I:\s+(-?[\d.]+)',o[o.rindex('Summary'):]).group(1))
n=int((total+2)*SR); buf=np.zeros(n)
for cue,key,off,g,fi,fo in PLAN:
    f=f'{cdir}/{cue}.mp3'; x=load(f); L=lufs(f)
    x=x*10**((-23-L+g)/20)               # every cue to -23 LUFS (+ per-cue offset)
    t0,t1=sec[key]; s=t0+off
    end=total if key=='end' else (sec['title'][1]+0.3 if key=='cold' else t1+1.5)   # let each cue ring into the next one
    d=min(len(x)/SR, end-s); x=x[:int(d*SR)].copy()
    a=int(fi*SR); b=int(min(fo,d/2)*SR)
    x[:a]*=np.linspace(0,1,a)**2; x[-b:]*=np.linspace(1,0,b)**1.5
    i0=int(s*SR); buf[i0:i0+len(x)]+=x[:n-i0]
    print(cue,key,'len',round(len(x)/SR,1),'section',round(t1-t0,1),'lufs',L)
pcm=(np.clip(buf[:int(total*SR)],-1,1)*32767).astype(np.int16)
with wave.open(out,'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
