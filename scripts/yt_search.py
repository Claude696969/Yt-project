import json, re, sys, subprocess, urllib.parse
def fetch(q, sp):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(q) + ("&sp=" + sp if sp else "")
    html = subprocess.run(["curl","-sS","-H","Accept-Language: en-US","-A","Mozilla/5.0",url],capture_output=True,text=True).stdout
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html)
    return json.loads(m.group(1)) if m else {}
def walk(o, out):
    if isinstance(o, dict):
        if "videoRenderer" in o:
            v=o["videoRenderer"]
            out.append(dict(id=v.get("videoId"),title="".join(r.get("text","") for r in v.get("title",{}).get("runs",[])),
              channel="".join(r.get("text","") for r in v.get("ownerText",{}).get("runs",[])),
              views=v.get("viewCountText",{}).get("simpleText",""),published=v.get("publishedTimeText",{}).get("simpleText",""),
              length=v.get("lengthText",{}).get("simpleText","")))
        for x in o.values(): walk(x,out)
    elif isinstance(o,list):
        for x in o: walk(x,out)
res={}
for q in sys.argv[1:]:
    for sp in ["CAM%253D", ""]:
        out=[]; walk(fetch(q,sp),out)
        for v in out:
            if v["id"]: v["query"]=q; res.setdefault(v["id"],v)
def n(s):
    d=re.sub(r"[^\d]","",s); return int(d) if d else 0
rows=sorted(res.values(),key=lambda v:-n(v["views"]))
json.dump(rows,open("yt/search.json","w"),indent=1)
for v in rows: print(f'{n(v["views"]):>12,} | {v["title"][:70]} | {v["channel"]} | {v["published"]} | {v["length"]} | {v["id"]}')
