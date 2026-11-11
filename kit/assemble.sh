#!/usr/bin/env bash
# Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT)
# assemble.sh — encode a folder of JPG frames (q00000.jpg, q00001.jpg, ...) into an MP4 in 4-second chunks,
# then concatenate them losslessly and mux the audio. Keeps 4K60 encoding under ~1 GB of RAM.
# usage: assemble.sh <frames_dir> <audio.wav> <out.mp4> [fps=60] [crf=16]
set -euo pipefail
Q="$1"; AUD="$2"; OUT="$3"; FPS="${4:-60}"; CRF="${5:-16}"
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
N=$(ls "$Q"/q*.jpg | wc -l); CHUNK=240
TMP="$Q/_chunks"; rm -rf "$TMP"; mkdir -p "$TMP"; : > "$TMP/list.txt"
for ((s=0; s<N; s+=CHUNK)); do
  k=$((s/CHUNK)); n=$(( N-s < CHUNK ? N-s : CHUNK ))
  "$FF" -y -loglevel error -threads 1 -framerate "$FPS" -start_number "$s" -i "$Q/q%05d.jpg" -frames:v "$n" \
    -c:v libx264 -preset veryfast -crf "$CRF" -pix_fmt yuv420p -profile:v high -level:v 5.2 \
    -x264-params "threads=2:sliced-threads=1:rc-lookahead=8:ref=2:bframes=2:colorprim=bt709:transfer=bt709:colormatrix=bt709" \
    -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -r "$FPS" "$TMP/p$k.mp4"
  echo "file 'p$k.mp4'" >> "$TMP/list.txt"; echo "  chunk $k done ($n frames)"
done
"$FF" -y -loglevel error -f concat -safe 0 -i "$TMP/list.txt" -i "$AUD" -map 0:v -map 1:a -c:v copy \
  -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart "$OUT"
rm -rf "$TMP"; echo "done: $OUT"
