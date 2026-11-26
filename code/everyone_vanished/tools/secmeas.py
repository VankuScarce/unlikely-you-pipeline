import sys,json,subprocess,re
sec=json.load(open(sys.argv[1])); vo=sys.argv[2]; mu=sys.argv[3]; vg=float(sys.argv[4]) if len(sys.argv)>4 else 8.1
def I(f,a,b,g=0):
    o=subprocess.run(['ffmpeg','-hide_banner','-nostats','-ss',str(a),'-t',str(b-a),'-i',f,'-af',f'volume={g}dB,ebur128','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.search(r'I:\s+(-?[\d.]+)',o[o.rindex('Summary'):]).group(1))
for k,(a,b) in sec.items():
    if b-a<5: continue
    v=I(vo,a,b,vg); m=I(mu,a,b)
    print(f'{k:9s} voice {v:6.1f}  music {m:6.1f}  gap {v-m:5.1f} dB')
