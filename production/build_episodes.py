"""Builds episodes/<id>-<slug>/ folders (episode.md, script.txt, clips/) from episodes.json. Re-run after editing the JSON."""
import json, pathlib
root = pathlib.Path(__file__).parent
data = json.loads((root / "episodes.json").read_text(encoding="utf-8"))
style, chars = data["style"], data["characters"]
for ep in data["episodes"]:
    d = root / "episodes" / f'{ep["id"]}-{ep["slug"]}'
    (d / "clips").mkdir(parents=True, exist_ok=True)
    (d / "script.txt").write_text(ep["script"] + "\n", encoding="utf-8")
    used = [c for c in chars if any(c in s[1] for s in ep["shots"])]
    words = len(ep["script"].split())
    md = [f'# {ep["id"]}: {ep["title"]}', "",
          f'**Premise type:** {ep["premise_type"]} · **Script length:** {words} words (about {round(words / 2.6)} s spoken)', "",
          "## Narration", "", ep["script"], "",
          "## OpenArt shots", "",
          "Settings: **9:16**, 5–6 s per clip. Paste **Style + Shot** for each clip, save as `clips/01.mp4`, `02.mp4`, and so on.", "",
          f"**Style (prefix every prompt):** {style}", ""]
    if used:
        md += ["**Characters in this episode** (create once in OpenArt as saved characters, reuse by tag):", ""]
        md += [f"- `{c}`: {chars[c]}" for c in used] + [""]
    md += ["| Clip | Time | Prompt |", "|---|---|---|"]
    md += [f"| {i:02d} | {t} | {p} |" for i, (t, p) in enumerate(ep["shots"], 1)]
    md += ["", "## Upload", "", f'**Title:** {ep["title"]}', "",
           "**Description:**", "", "```",
           ep["title"].split(" #")[0], "", "Would you survive in this town? Comment the rule YOUR town should have 👇",
           "", "#roblox #shorts #inthistown #robloxstory", "```", "",
           "**YouTube Studio:** Altered/synthetic content: *No* is fine for clearly animated/cartoon content (check current guidance). Audience: Not made for kids unless you mean it."]
    (d / "episode.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("wrote", d.relative_to(root))
