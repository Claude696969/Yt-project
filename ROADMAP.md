# Roadmap: making "In This Town" Roblox Shorts (Windows + Claude Code)

The format is a vertical Short of about 30–60 seconds. It opens with **"In This Town/World, [one strange rule]…"**, a narrator (usually a TTS voice) tells a short story over Roblox avatar footage, and it ends on a twist. See [REPORT.md](REPORT.md) for the videos this plan is based on.

> Make **your own** stories and footage. The genre is free to use, but re-uploading or copying other creators' videos will get your channel struck.

---

## Phase 0: Set up your laptop (1 evening)

- [ ] Install **Git for Windows**: https://git-scm.com/download/win
- [ ] Install **Claude Code** by running this in PowerShell: `irm https://claude.ai/install.ps1 | iex`, then run `claude` and log in. Docs: https://code.claude.com/docs
- [ ] Install **Python 3.12+**: https://www.python.org/downloads/ (tick "Add to PATH")
- [ ] Install **FFmpeg** by running this in PowerShell: `winget install Gyan.FFmpeg`
- [ ] Clone this repo:
  ```
  git clone https://github.com/Claude696969/Yt-project.git
  cd Yt-project
  git checkout claude/eager-gauss-95lyjn
  claude
  ```
- [ ] Install **Roblox** and **Roblox Studio**: https://create.roblox.com
- [ ] Install **OBS Studio** for screen recording: https://obsproject.com
- [ ] Install **CapCut Desktop** for editing, auto-captions and built-in TTS: https://www.capcut.com
  - DaVinci Resolve is a free alternative: https://www.blackmagicdesign.com/products/davinciresolve
- [ ] Create a **YouTube channel** (a separate brand account is a good idea) and a **TikTok** account for cross-posting

## Phase 1: Learn the format (1–2 days)

- [ ] Watch the top 10 Shorts in REPORT.md. For each one, note:
  - the hook rule
  - how many seconds pass before the twist
  - the voice style
  - the caption style
  - the background music
- [ ] Use this story template:
  1. **Rule:** "In this town, you can't speak."
  2. **How everyone lives with it:** one or two lines
  3. **"Except me" or the problem:** the narrator is the exception
  4. **Escalation:** one or two lines
  5. **Twist or punchline:** the last line
- [ ] Target length: **80–130 words**, which is about 30–50 seconds of narration
- [ ] Aim for the premises that performed best: **danger, death or survival** (walking alone is deadly; tag is deadly), **visible stats** (IQ shows; steal buttons), and **emotional rules** (mirrors show happiest moment)

## Phase 2: Build your production pipeline (2–4 days)

Ask Claude Code at home to help build each of these.

- [ ] **Story writer:** use Claude to brainstorm 50 premises, then write scripts with the template above. Save them in `stories/001.md`, `stories/002.md`, and so on.
- [ ] **Voiceover:** choose one of these:
  - Free: CapCut's built-in TTS voices, or **edge-tts** (Python, free Microsoft neural voices: `pip install edge-tts`). Claude Code can script batch generation.
  - Paid, best quality: **ElevenLabs** (https://elevenlabs.io)
- [ ] **Footage:** choose one of these:
  - Easy: pose and act scenes in a game such as **Brookhaven** with friends or alts, and record with OBS
  - Better: build small sets in **Roblox Studio** and animate with the built-in **Animation Editor**, or with **Moon Animator 2** (a paid Studio plugin and the standard for Roblox animators)
  - Free assets: the Roblox Studio Toolbox and Creator Store for maps and props
- [ ] **Edit:** set CapCut to **1080×1920 (9:16)**, add the voice, footage, **big centered auto-captions**, quiet background music and sound effects
  - Music and SFX: YouTube Audio Library (in YouTube Studio), https://pixabay.com/music
- [ ] **Optional automation:** have Claude Code write a Python + FFmpeg script that turns a story, a voice file and clips into a captioned vertical MP4. Use Whisper for captions (`pip install openai-whisper`).

## Phase 3: Make your first batch (week 1)

- [ ] Make **10 Shorts** before posting any, so you have a buffer
- [ ] **Title format:** `In This Town, [Rule]… 😱 #roblox #shorts`, short with only 2–3 hashtags (the top videos all do this)
- [ ] Make the first spoken line the same as the title. You have about 1 second to hook the viewer.
- [ ] Check each video before export:
  - [ ] vertical
  - [ ] under 60 seconds
  - [ ] captions readable
  - [ ] twist lands in the last 3 seconds
  - [ ] no copyrighted music

## Phase 4: Post and grow (weeks 2–6)

- [ ] Post **1–2 Shorts per day** at consistent times
- [ ] Cross-post the same video to **TikTok** and **Instagram Reels**
- [ ] Each week, open **YouTube Studio → Analytics** and check:
  - views
  - "viewed vs swiped away" percentage
  - average % viewed
- [ ] Make **more of whatever premise type wins**, and drop what flops
- [ ] Once you have 20+ Shorts, upload a **long-form compilation** (15–40 min, numbered: "In This Town Roblox Stories Compilation #1"). Compilations reached 0.5–2.5M views within weeks.
- [ ] Watch for trending sounds and memes (like the "HUSS HUSS HUSS" meme) and do a quick version within days of it starting
- [ ] Re-run `scripts/yt_shorts.py` monthly to see which premises are rising

## Phase 5: Monetize (when eligible)

- [ ] Apply for the **YouTube Partner Program**. Shorts route: 1,000 subscribers + 10M Shorts views in 90 days. Check current rules in YouTube Studio → Earn.
- [ ] Use long-form compilations, which earn more per view than Shorts

---

## Resources summary

| Need | Free option | Paid upgrade |
|---|---|---|
| Story writing | Claude Code | — |
| Voice | CapCut TTS, edge-tts | ElevenLabs |
| Footage | Roblox + OBS, Roblox Studio Animation Editor | Moon Animator 2 |
| Editing and captions | CapCut Desktop, DaVinci Resolve | CapCut Pro |
| Music and SFX | YouTube Audio Library, Pixabay | Epidemic Sound |
| Automation | Python + FFmpeg + Whisper (built with Claude Code) | — |
| Research | `scripts/` in this repo | vidIQ / TubeBuddy |

**Hardware:** any laptop that runs Roblox smoothly is enough. 16GB RAM helps with editing, and a headset mic is useful if you ever do your own voice.

## First prompt to give Claude Code at home

> Read REPORT.md and ROADMAP.md. Help me with Phase 2: write 20 original "In This Town" story scripts using the template, then build a Python script that generates voiceovers with edge-tts into a `voice/` folder.
