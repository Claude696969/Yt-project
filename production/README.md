# Production kit: OpenArt + Claude Code

**Who does what**

| Step | Who | Where |
|---|---|---|
| 1. Premise, script, shot prompts, title, description | Claude Code | `episodes.json` → `python build_episodes.py` |
| 2. Visuals (8 clips per episode) | **You** | OpenArt |
| 3. Voice, captions, music, final 9:16 video | Claude Code | `python make_short.py episodes/<folder>` |
| 4. Upload, schedule, track results | You upload; Claude Code updates `tracker.csv` | YouTube Studio |

## One-time setup (Windows)
- [ ] Python 3.10+ and FFmpeg (`winget install Gyan.FFmpeg`), then `pip install edge-tts`
- [ ] In OpenArt, create the **saved characters** from `episodes.json` → `characters` (`@Pip` is your channel's main character). Use the **same style text** every time.
- [ ] Optional: one or two background music tracks from the YouTube Audio Library in a `music/` folder

## Per-episode loop (~45–60 min once you're practised)
1. Open `episodes/<id>-<slug>/episode.md`
2. In OpenArt (9:16, 5–6 s clips), generate each shot: **style line + shot prompt**, using your saved characters. Download them as `clips/01.mp4` … `clips/08.mp4`.
   - If a clip comes out bad, regenerate it, or use a still image (`.png`). The script slowly zooms still images.
   - OpenArt is weak at **numbers and text** (like the "0" above the head). Put those in afterwards as a CapCut text overlay if they come out garbled.
3. Run `python make_short.py episodes/<id>-<slug>`, optionally with `--music music/track.mp3`. Watch `final.mp4`.
4. Upload using the title and description in `episode.md`. Log it in `tracker.csv`.
5. After 48 h and 7 d, paste views and "% viewed vs swiped" into the tracker. Ask Claude Code to write the next batch, leaning towards the premise types that win.

## Asking Claude Code for more
> Read production/README.md, episodes.json and tracker.csv. Write 5 new episodes in the same format, weighted towards the best-performing premise types, then run build_episodes.py.

## Rules to stay monetizable
- **Original stories only.** Don't copy other channels' scripts or characters.
- YouTube can demonetize **mass-produced, repetitive** AI content ("inauthentic content" policy). Vary premises, keep a recurring character and real storytelling, and don't post near-identical videos.
- AI images of a *Roblox-like* blocky style are fine to make, but don't use Roblox logos or claim the video is official Roblox content.
- Check OpenArt's plan terms allow **commercial use** of what you generate.

Media files (`clips/`, `voice.mp3`, `final.mp4`) are git-ignored because they're too big for the repo. Back them up separately.
