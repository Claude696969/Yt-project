"""Assemble a finished 1080x1920 Short from an episode folder.

    python make_short.py episodes/001-love-counter
    python make_short.py episodes/001-love-counter --voice en-US-GuyNeural --rate +10% --music music/calm.mp3

Expects:  <episode>/script.txt   narration text
          <episode>/clips/       OpenArt clips named 01.mp4, 02.mp4, ... (images .png/.jpg also work)
Produces: <episode>/voice.mp3, <episode>/captions.ass, <episode>/final.mp4

Voice comes from edge-tts (free Microsoft neural voices, needs internet). With --voice-file you can
use your own recording instead; captions are then skipped (use CapCut auto-captions).
Requires: Python 3.10+, ffmpeg on PATH, `pip install edge-tts`.
"""
import argparse, json, pathlib, subprocess, sys

W, H, FPS = 1080, 1920, 30
EXTS = {".mp4", ".mov", ".webm", ".png", ".jpg", ".jpeg", ".webp"}


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg failed:\n{' '.join(map(str, cmd))}\n{r.stderr[-2000:]}")
    return r.stdout


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).strip())


def tts(text, voice, rate, out):
    """Generate narration with edge-tts; returns list of (start_s, end_s, word)."""
    import edge_tts
    try:
        com = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    except TypeError:  # older edge-tts versions emit word boundaries by default
        com = edge_tts.Communicate(text, voice, rate=rate)
    words = []
    with open(out, "wb") as f:
        for chunk in com.stream_sync():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                s = chunk["offset"] / 1e7
                words.append((s, s + chunk["duration"] / 1e7, chunk["text"]))
    return words


def ass_time(t):
    h, t = divmod(t, 3600); m, s = divmod(t, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def write_captions(words, out, per_line=3):
    """Big, bold, centered 2-3 word captions (the style used by the top Shorts)."""
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Arial Black,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,7,3,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for i in range(0, len(words), per_line):
        grp = words[i:i + per_line]
        end = words[i + per_line][0] if i + per_line < len(words) else grp[-1][1] + 0.3
        text = " ".join(w for _, _, w in grp).upper().replace("{", "(").replace("}", ")")
        lines.append(f"Dialogue: 0,{ass_time(grp[0][0])},{ass_time(end)},Cap,,0,0,0,,{text}")
    pathlib.Path(out).write_text(head + "\n".join(lines) + "\n", encoding="utf-8")


def assemble(ep, voice_path, captions, music=None, music_vol=0.12):
    clips = sorted(p for p in (ep / "clips").iterdir() if p.suffix.lower() in EXTS)
    if not clips:
        sys.exit(f"No clips in {ep / 'clips'}. Save your OpenArt clips there as 01.mp4, 02.mp4, ...")
    total = duration(voice_path) + 0.6
    seg = total / len(clips)
    tmp = ep / "_tmp"; tmp.mkdir(exist_ok=True)
    fit = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1"
    parts = []
    for i, c in enumerate(clips):
        o = tmp / f"{i:02d}.mp4"
        if c.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:  # still image: slow zoom
            vf = f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},zoompan=z='min(zoom+0.0008,1.15)':d={int(seg*FPS)}:s={W}x{H}:fps={FPS},setsar=1"
            cmd = ["ffmpeg", "-y", "-loop", "1", "-i", str(c), "-t", f"{seg:.3f}", "-vf", vf]
        else:  # video: fit to 9:16, hold last frame if the clip is too short
            cmd = ["ffmpeg", "-y", "-i", str(c), "-t", f"{seg:.3f}", "-vf", f"{fit},tpad=stop_mode=clone:stop_duration={seg:.3f}"]
        run(cmd + ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", str(o)])
        parts.append(o)
    (tmp / "list.txt").write_text("".join(f"file '{p.name}'\n" for p in parts))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "video.mp4"], cwd=tmp)

    # Run from the episode folder with relative paths: avoids Windows "C:\" escaping in the subtitles filter.
    cmd = ["ffmpeg", "-y", "-i", "_tmp/video.mp4", "-i", voice_path.name]
    if music:
        cmd += ["-stream_loop", "-1", "-i", str(pathlib.Path(music).resolve())]
    vf = "subtitles=captions.ass" if captions else "null"
    if music:
        af = f"[2:a]volume={music_vol}[m];[1:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]"
        cmd += ["-filter_complex", f"[0:v]{vf}[v];{af}", "-map", "[v]", "-map", "[a]"]
    else:
        cmd += ["-vf", vf, "-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "final.mp4"]
    run(cmd, cwd=ep)
    for p in tmp.iterdir():
        p.unlink()
    tmp.rmdir()
    print(f"Done: {ep / 'final.mp4'} ({total:.1f}s, {len(clips)} clips, {seg:.1f}s each)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--voice", default="en-US-ChristopherNeural", help="edge-tts voice (list: edge-tts --list-voices)")
    ap.add_argument("--rate", default="+8%", help="speaking speed, e.g. +10%%")
    ap.add_argument("--voice-file", help="use your own narration audio instead of edge-tts (no captions)")
    ap.add_argument("--music", help="optional background music file")
    ap.add_argument("--music-volume", type=float, default=0.12)
    a = ap.parse_args()
    ep = pathlib.Path(a.episode).resolve()
    if a.voice_file:
        voice = ep / "voice.mp3"
        run(["ffmpeg", "-y", "-i", a.voice_file, str(voice)])
        captions = False
    else:
        voice = ep / "voice.mp3"
        words = tts((ep / "script.txt").read_text(encoding="utf-8").strip(), a.voice, a.rate, voice)
        (ep / "words.json").write_text(json.dumps(words), encoding="utf-8")
        write_captions(words, ep / "captions.ass")
        captions = True
    assemble(ep, voice, captions, a.music, a.music_volume)


if __name__ == "__main__":
    main()
