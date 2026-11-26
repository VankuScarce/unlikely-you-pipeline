"""Builds the pilot's main body (after the cold open): timeline JSON, VO track, music bed, sound cues."""
import json, subprocess, numpy as np, wave, sys
VO = '/mnt/project-files/pilot/vo_full/s%d.mp3'
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
STING = 3.0; TAIL = 0.8
EXT = '/mnt/project-files/pilot/vo_full/n%d.mp3'
sections = [
 dict(stars=1, value="00:01:30", heading="ONE STAR: SOMEBODY NOTICED", clips=[
  (VO%1,[('camera_map',.35,{'cameras':45,'caption':'100,000+ plate cameras mapped across the US (Pew, 2026)'}),
   ('camera_map',.30,{'cameras':45,'route':True,'caption':'Every camera: seen here, at this second'}),
   ('ozzie_explains',.35,{'lines':["Stars don't go up","because you did","something dramatic.","A system noticed you."]})]),
  (EXT%1,[('location_gas_station',.55,{}),
   ('stat_card',.45,{'value':12,'suffix':'x','caption':'Times you were recorded before starting the engine','estimate':True})])]),
 dict(stars=2, value="00:11:40", heading="TWO STARS: THE CHASE", clips=[
  (VO%2,[('dispatch_grid',.55,{'caption':"They drive to where you're going"}),
   ('ozzie_explains',.45,{'lines':["Chases get called off.","Good news?","No. Something better","is already watching."]})]),
  (EXT%2,[('stat_card',.25,{'value':120,'suffix':' MPH','caption':'Your car, flat out','bg':'orange'}),
   ('stat_card',.35,{'value':670616629,'suffix':' MPH','caption':'A radio call (the speed of light)'}),
   ('dispatch_grid',.40,{'caption':"You're racing the radio"})])]),
 dict(stars=3, value="00:38:10", heading="THREE STARS: EYE IN THE SKY", clips=[
  (VO%3,[('thermal',.30,{'callout':'TARGET NORTHBOUND'}),
   ('stat_card',.15,{'value':130,'suffix':'+ MPH','caption':'Patrol helicopter, in a straight line'}),
   ('thermal',.30,{'callout':'TARGET ENTERING PARKING GARAGE'}),
   ('ozzie_explains',.25,{'lines':["Its job isn't","to catch you.","It's to narrate you."]})])]),
 dict(stars=4, value="09:20:00", heading="FOUR STARS: THE CITY CLOSES", clips=[
  (VO%4,[('ozzie_explains',.40,{'lines':["Your phone.","Your bank card.","Your face.","The roads."]}),
   ('exits_closing',.35,{'caption':'A peninsula has only so many ways out'}),
   ('stat_card',.25,{'value':11,'fmt':'${:,.0f}','caption':'Cash left. No phone, no card, no home, no sleep.','bg':'red'})]),
  (EXT%3,[('ozzie_explains',.35,{'lines':["Night one.","Hotel? Needs ID.","Friend's couch?","First place they check."]}),
   ('stat_card',.35,{'value':0.10,'fmt':'{:.2f}','suffix':' BAC','caption':'Impairment after 24 hours awake (NIOSH)','bg':'slate'}),
   ('ozzie_explains',.30,{'lines':["Tired people","use the card.","Tired people","call their mom."]})])]),
 dict(stars=5, value="72:00:00", heading="FIVE STARS: THEY NEVER STOP", clips=[
  (VO%5,[('case_file',.28,{}),
   ('ozzie_explains',.30,{'lines':["They don't drive fast.","They're patient.","They wait for you","to call someone."]}),
   ('stat_card',.20,{'value':500,'suffix':'+','caption':'Names on the Ten Most Wanted list since 1950. Most were caught.'}),
   ('stat_card',.22,{'value':7,'suffix':' DAYS','caption':"Ozzie's best case for an ordinary person",'bg':'orange','estimate':True})]),
  (EXT%4,[('stat_card',.30,{'value':16,'suffix':' YEARS','caption':'One famous fugitive\'s run. Caught in 2011.','bg':'slate'}),
   ('ozzie_explains',.40,{'lines':["Not a car chase.","Not a helicopter.","One neighbor","who watched TV."]}),
   ('stat_card',.30,{'value':11,'fmt':'${:,.0f}','caption':'You, on the other hand.','bg':'red'})])]),
 dict(stars=5, value="168:00:00", heading="THE FINAL ODDS", clips=[
  (EXT%5,[('ozzie_explains',1.0,{'lines':["90 sec: on camera","11 min: helicopter","1 hour: on foot","1 week, at best."]})])]),
 dict(stars=1, value="00:00:00", heading="THE TWIST", clips=[
  (VO%6,[('record_screen',.25,{}),
   ('ozzie_explains',.45,{'lines':["Stop.","Hands visible.","\"I'd like to speak","to a lawyer.\""]}),
   ('location_gas_station',.30,{})])]),
 dict(stars=0, value="LIFETIME", heading="SURVIVAL TIME: YOUR WHOLE LIFE", clips=[
  (VO%7,[('ozzie_explains',1.0,{'lines':["NEXT WEEK:","Everyone on Earth","calls in sick.","Same day."]})])]),
]
scenes=[]; vo=[]; stings=[]; t=0.0
for i,sec in enumerate(sections):
    scenes.append({'type':'odds_board','dur':STING,'p':{'stars':sec['stars'],'value':sec['value'],'heading':sec['heading']}})
    stings.append(t); t += STING
    for f,body in sec['clips']:
        vo.append((f,t)); L = dur(f)+TAIL; tot=0
        for typ,frac,p in body:
            d=round(L*frac,3); scenes.append({'type':typ,'dur':d,'p':p}); tot+=d
        t += tot
scenes.append({'type':'title_card','dur':5.0}); total = t+5.0
json.dump({'fps':24,'scenes':scenes}, open('/tmp/claude-0/ep/episode_body.json','w'), indent=1)
# VO track
inputs=[]; filt=[]
for i,(f,a) in enumerate(vo):
    inputs += ['-i', f]; filt.append(f"[{i}:a]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay={int(a*1000)}|{int(a*1000)}[v{i}]")
filt.append(''.join(f'[v{i}]' for i in range(len(vo))) + f"amix=inputs={len(vo)}:normalize=0,apad=whole_dur={total}[out]")
subprocess.check_call(['ffmpeg','-loglevel','error','-y',*inputs,'-filter_complex',';'.join(filt),'-map','[out]','-t',str(total),'/tmp/claude-0/ep/vo.wav'])
# music bed + stings
SR=48000; N=int(SR*total); rng=np.random.default_rng(1); mus=np.zeros(N)
def add(t0,sig):
    i=int(t0*SR); j=min(N,i+len(sig)); mus[i:j]+=sig[:j-i]
def tone(f,d,a=0.005,dec=0.3,sq=False):
    n=int(d*SR); tt=np.arange(n)/SR; w=np.sin(2*np.pi*f*tt); w=np.sign(w)*0.5 if sq else w
    return w*np.minimum(1,tt/a)*np.exp(-tt/dec)
roots=[73.42,73.42,69.30,65.41,61.74,61.74,87.31,73.42]
bounds=stings+[total]
for i in range(len(sections)):
    a,b=bounds[i],bounds[i+1]; n=int((b-a)*SR); tt=np.arange(n)/SR; f0=roots[i]
    pad=sum(np.sin(2*np.pi*f*tt+ph)*w for f,ph,w in ((f0,0,1),(f0*1.5,1,.5),(f0*2.003,2,.4),(f0*1.189 if i!=5 else f0*1.26,.5,.4)))
    e=np.minimum(1,tt/2)*np.minimum(1,(n/SR-tt)/1.0); add(a,pad*e*0.06)
    if i in (1,2):   # pulse in chase/helicopter
        k=a+STING
        while k<b-0.5:
            nn=int(0.3*SR); q=np.arange(nn)/SR; add(k,np.sin(2*np.pi*np.cumsum(50+90*np.exp(-q*30))/SR)*np.exp(-q*9)*0.22); k+=0.6
    if i in (4,5):          # tense high drone
        add(a+STING, np.sin(2*np.pi*f0*8*tt[:int((b-a-STING)*SR)])*0.012)
    # sting: chord stab + split-flap clicks
    for f in (f0*2,f0*2.4,f0*3,f0*4): add(bounds[i],tone(f,2.0,0.005,0.6,True)*0.05)
    for c in range(10): add(bounds[i]+0.3+c*0.06, np.diff(rng.normal(0,1,int(0.03*SR)),prepend=0)*np.exp(-np.arange(int(0.03*SR))/SR*120)*0.2)
for f in (146.8,174.6,220.0,293.7): add(total-5.0,tone(f,4,0.01,1.4,True)*0.06)
out=np.stack([mus,mus],1); out=out/np.max(np.abs(out))*0.8
with wave.open('/tmp/claude-0/ep/bed.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
print('total',round(total,2),'scenes',len(scenes))
