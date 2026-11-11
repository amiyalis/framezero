# Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT)
"""
render.py — turn a deterministic HTML scene into an MP4 (or into still frames for review).

A scene is a 1080x1920 HTML page that defines:
    const DURATION = <seconds>;          // (DURACAO is also accepted)
    function seek(t) { ... }             // draws EXACTLY the instant t — no timers, no CSS animations
and contains the markers <!--BASE--> (font + motion helpers) and optionally <!--ICONS--> (SVG sprite).

Usage
    python3 kit/render.py scene.html out.mp4                          # 1080p30 preview, silent track
    python3 kit/render.py scene.html shots/s --stills 0,1.5,3         # PNG stills for QA (fast)
    python3 kit/render.py scene.html out-4K.mp4 --scale 2 --fps 60 --crf 16 \
            --audio soundtrack.wav --frames-dir /tmp/frames           # 4K60, low-RAM two-step mode
"""
import argparse, os, pathlib, shutil, subprocess, sys, time

import imageio_ffmpeg

# Optional: extra shared libraries for Chromium on minimal Linux boxes (folder with libnss3.so etc.)
_extra = os.environ.get('FRAMEZERO_CHROME_LIBS', '/home/user/.local/xlib/usr/lib/x86_64-linux-gnu')
if os.path.isdir(_extra):
    os.environ['LD_LIBRARY_PATH'] = _extra + ':' + os.environ.get('LD_LIBRARY_PATH', '')

from playwright.sync_api import sync_playwright  # noqa: E402

ap = argparse.ArgumentParser(description='Render a framezero HTML scene to MP4 or stills.')
ap.add_argument('html', help='scene file (1080x1920, defines DURATION and seek(t))')
ap.add_argument('out', help='output .mp4 — or a filename prefix when using --stills')
ap.add_argument('--fps', type=int, default=30)
ap.add_argument('--scale', type=int, default=1, help='device pixel ratio: 1 = 1080x1920, 2 = 4K 2160x3840')
ap.add_argument('--crf', default='17', help='x264 quality (lower = better/bigger). 16-18 is visually lossless')
ap.add_argument('--audio', default='', help='WAV/MP3 to mux in (default: silent stereo track)')
ap.add_argument('--stills', default='', help='comma-separated times in seconds: only save PNGs at these instants')
ap.add_argument('--frames-dir', default='', help='two-step mode: save JPG frames here, then encode in 4-second chunks (needs --audio)')
a = ap.parse_args()

KIT = pathlib.Path(__file__).resolve().parent
src_path = pathlib.Path(a.html).resolve()
src = src_path.read_text(encoding='utf8')
inject = '<style>' + (KIT / 'base.css').read_text() + '</style><script>' + (KIT / 'motion.js').read_text() + '</script>'
src = src.replace('<!--BASE-->', inject)
icons = (KIT / 'icons.svg').read_text()
src = src.replace('<!--ICONS-->', icons).replace('<!--ICONES-->', icons)

# The built page is written NEXT TO the scene, so relative paths (screens/x.png, logo.png) keep working.
tmp = src_path.with_name('.framezero-' + src_path.stem + '.html')
tmp.write_text(src, encoding='utf8')

FF = imageio_ffmpeg.get_ffmpeg_exe()
t0 = time.time()
try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=a.scale)
        page.on('pageerror', lambda e: print('PAGE ERROR:', e, file=sys.stderr))
        page.goto(tmp.as_uri())
        page.evaluate('document.fonts.ready')
        page.wait_for_timeout(300)  # let <img> decode
        dur = page.evaluate('typeof DURATION !== "undefined" ? DURATION : DURACAO')

        if a.stills:
            pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            for t in a.stills.split(','):
                page.evaluate(f'seek({float(t)})')
                out = f'{a.out}-{t}s.png'
                page.screenshot(path=out)
                print('still', out)
            browser.close()
            sys.exit(0)

        n = round(dur * a.fps)
        pathlib.Path(a.out).resolve().parent.mkdir(parents=True, exist_ok=True)
        audio_in = ['-i', a.audio] if a.audio else ['-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000']
        encode = ['-map', '0:v', '-map', '1:a', '-shortest',
                  '-c:v', 'libx264', '-preset', 'medium' if a.scale == 1 else 'faster', '-threads', '2', '-crf', a.crf,
                  '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level:v', '5.2' if a.scale > 1 else '4.2',
                  '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
                  '-x264-params', 'colorprim=bt709:transfer=bt709:colormatrix=bt709:rc-lookahead=12',
                  '-r', str(a.fps), '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-movflags', '+faststart', a.out]

        if a.frames_dir:
            if not a.audio:
                raise SystemExit('--frames-dir needs --audio')
            d = pathlib.Path(a.frames_dir)
            shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
            for i in range(n):
                page.evaluate(f'seek({i / a.fps})')
                page.screenshot(path=str(d / f'q{i:05d}.jpg'), type='jpeg', quality=96)
                if i % 120 == 0:
                    print(f'  frame {i}/{n}  {time.time() - t0:.0f}s', flush=True)
            browser.close()
            print('  encoding in chunks...', flush=True)
            # One 4K x264 process can exceed 1 GB of RAM; assemble.sh encodes 4 s chunks and concatenates losslessly.
            subprocess.run(['bash', str(KIT / 'assemble.sh'), str(d), a.audio, a.out, str(a.fps), a.crf], check=True)
            shutil.rmtree(d, ignore_errors=True)
        else:
            ff = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(a.fps), '-i', '-',
                                   *audio_in, *encode], stdin=subprocess.PIPE)
            for i in range(n):
                page.evaluate(f'seek({i / a.fps})')
                ff.stdin.write(page.screenshot(type='png'))
                if i % 120 == 0:
                    print(f'  frame {i}/{n}  {time.time() - t0:.0f}s', flush=True)
            ff.stdin.close(); ff.wait(); browser.close()
        print('video', a.out, f'{dur}s', n, 'frames', f'{time.time() - t0:.0f}s')
finally:
    tmp.unlink(missing_ok=True)
