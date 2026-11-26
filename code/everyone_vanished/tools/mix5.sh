#!/bin/bash
# usage: mix5.sh MUSIC_GAIN_DB OUTDIR   (stems from out5)
set -e
G=${1:-2}; D=${2:-/tmp/claude-0/ep2/mix5}; S=/tmp/claude-0/ep2/out5
mkdir -p $D
DUCK="sidechaincompress=threshold=0.16:ratio=2:attack=60:release=650:knee=6"
# ducked music stem alone (for measuring)
ffmpeg -y -v error -i $S/vo.wav -i $S/score.wav -filter_complex \
 "[0:a]volume=8.1dB[v];[1:a]volume=${G}dB[m];[m][v]$DUCK[md]" -map "[md]" -c:a pcm_s16le $D/music_ducked.wav
ffmpeg -y -v error -i $S/vo.wav -i $S/sfx.wav -i $S/score.wav -filter_complex \
 "[0:a]volume=8.1dB,asplit=3[v1][v2][v3];[1:a]volume=12.4dB[s0];[2:a]volume=${G}dB[m0];[s0][v1]sidechaincompress=threshold=0.105:ratio=2.5:attack=15:release=300[sd];[m0][v2]$DUCK[md];[v3][sd][md]amix=inputs=3:normalize=0,alimiter=limit=0.95:attack=2:release=50:level=false,aresample=48000,pan=stereo|c0=0.7071*c0|c1=0.7071*c0" \
 -c:a pcm_s16le $D/mix_st.wav
ffmpeg -nostats -i $D/mix_st.wav -af ebur128=peak=true -f null - 2>&1 | grep -A14 Summary | grep -E "I:|Peak|LRA:"
