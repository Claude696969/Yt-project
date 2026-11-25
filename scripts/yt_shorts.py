import json,re,sys,subprocess,urllib.parse,time
def fetch(q,sp):
    url="https://www.youtube.com/results?search_query="+urllib.parse.quote_plus(q)+("&sp="+sp if sp else "")
    h=subprocess.run(["curl","-sS","-H","Accept-Language: en-US","-A","Mozilla/5.0",url],capture_output=True,text=True).stdout
    m=re.search(r"var ytInitialData = (\{.*?\});</script>",h); return json.loads(m.group(1)) if m else None
def walk(o,out):
    if isinstance(o,dict):
        if "shortsLockupViewModel" in o:
            s=o["shortsLockupViewModel"]; js=json.dumps(s,ensure_ascii=False)
            vid=re.search(r'"videoId": "([^"]+)"',js); a=s.get("accessibilityText","")
            mm=re.match(r"(.*), ([\d.,]+ ?(?:thousand|million|billion)?) views? - play Short",a)
            out.append(dict(id=vid.group(1) if vid else None,title=mm.group(1) if mm else a,views=mm.group(2) if mm else "",short=True))
        if "reelItemRenderer" in o:
            r=o["reelItemRenderer"]; out.append(dict(id=r.get("videoId"),title=r.get("headline",{}).get("simpleText",""),views=r.get("viewCountText",{}).get("simpleText",""),short=True))
        for x in o.values(): walk(x,out)
    elif isinstance(o,list):
        for x in o: walk(x,out)
def n(s):
    m=re.match(r"([\d.]+)\s*(thousand|million|billion)?",s.replace(",",""))
    if not m: return 0
    return int(float(m.group(1))*{None:1,"thousand":1e3,"million":1e6,"billion":1e9}[m.group(2)])
res={}
for q in sys.argv[1:]:
    for sp in ["CAM%253D",""]:
        d=fetch(q,sp)
        if d is None: print("BLOCKED/noparse",q,file=sys.stderr); continue
        out=[]; walk(d,out)
        for v in out:
            if v["id"]: v["query"]=q; res.setdefault(v["id"],v)
        time.sleep(4)
rows=sorted(res.values(),key=lambda v:-n(v["views"]))
json.dump(rows,open("yt/shorts.json","w"),indent=1)
for v in rows: print(f'{v["views"]:>14} | {v["title"][:80]} | https://youtube.com/shorts/{v["id"]}')
