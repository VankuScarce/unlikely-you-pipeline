import subprocess, re, glob, os, sys
src, dst = sys.argv[1], sys.argv[2]
def meas(f):
    o = subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',f,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    s = o[o.rindex('Summary'):]
    return float(re.search(r'I:\s+(-?[\d.]+)',s).group(1)), float(re.search(r'Peak:\s+(-?[\d.]+)',s).group(1))
for f in sorted(glob.glob(src+'/*.wav')):
    n=os.path.basename(f); I,P=meas(f)
    tmp=dst+'/_'+n
    subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-af',f'highpass=f=70,volume={-22-I:.2f}dB,acompressor=threshold=0.07:ratio=3:attack=6:release=110:knee=4,alimiter=limit=0.5:attack=2:release=40:level=false','-c:a','pcm_s16le',tmp],check=True)
    I2,P2=meas(tmp)
    subprocess.run(['ffmpeg','-v','error','-y','-i',tmp,'-af',f'volume={-22-I2:.2f}dB','-c:a','pcm_s16le',dst+'/'+n],check=True)
    os.remove(tmp)
    I3,P3=meas(dst+'/'+n)
    print(n, I, P, '->', I3, P3)
