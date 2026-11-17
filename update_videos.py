#!/usr/bin/env python3
"""Refresh public YouTube channel feeds without an API key. Standard library only."""
import json, re, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'videos.json'
HANDLES=['raisingfloofz','Vicky_and_her_Essas','FLUFF_ESSAS','StarLight-2025-f5v','Wobbles_Essa','JAUGWIREESSA','CollieMENACE','OliPaws_ESSA','Candy_dragonz','that_one_cute_pup','CuddlyHowlers','Bellasworkingpups']
HEADERS={'User-Agent':'Mozilla/5.0 (compatible; ESSAzTube/1.0; public feed reader)','Accept-Language':'en-US,en;q=0.9'}

def fetch(url):
    req=urllib.request.Request(url,headers=HEADERS)
    with urllib.request.urlopen(req,timeout=22) as r:return r.read().decode('utf-8','replace')

def existing():
    if OUT.exists():
        try:return json.loads(OUT.read_text())
        except Exception:pass
    return {'channels':[],'videos':[]}

def main():
    old=existing(); oldch={c['handle'].lower():c for c in old.get('channels',[])}
    channels=[]; allvideos={v['id']:v for v in old.get('videos',[]) if 'id' in v}
    for handle in HANDLES:
        prior=oldch.get(handle.lower(),{})
        channel={'handle':handle,'id':prior.get('id',''),'name':prior.get('name',handle),'avatar':prior.get('avatar',''),'featured':True}
        try:
            html=fetch('https://www.youtube.com/@'+urllib.parse.quote(handle,safe='_-'))
            match=re.search(r'"(?:channelId|externalId)":"(UC[a-zA-Z0-9_-]{22})"',html)
            if not match:match=re.search(r'https://www.youtube.com/channel/(UC[a-zA-Z0-9_-]{22})',html)
            if match:channel['id']=match.group(1)
            title=re.search(r'<meta\s+property="og:title"\s+content="([^"]+)',html)
            if title:
                import html as htmlmod
                channel['name']=htmlmod.unescape(title.group(1))
            avatar=re.search(r'<meta\s+property="og:image"\s+content="([^"]+)',html)
            if avatar:channel['avatar']=avatar.group(1).replace('&amp;','&')
        except Exception as e:print('Channel lookup issue',handle,str(e))
        channels.append(channel)
        if not channel['id']:
            print('UNRESOLVED channel:',handle);continue
        try:
            rss=fetch('https://www.youtube.com/feeds/videos.xml?channel_id='+channel['id'])
            root=ET.fromstring(rss)
            ns={'a':'http://www.w3.org/2005/Atom','yt':'http://www.youtube.com/xml/schemas/2015','media':'http://search.yahoo.com/mrss/'}
            for entry in root.findall('a:entry',ns):
                vid=entry.findtext('yt:videoId',default='',namespaces=ns)
                if not re.fullmatch(r'[a-zA-Z0-9_-]{11}',vid):continue
                title=entry.findtext('a:title',default='Video',namespaces=ns)
                published=entry.findtext('a:published',default='',namespaces=ns)
                description=entry.findtext('media:group/media:description',default='',namespaces=ns)
                # Preserve old videos, refresh metadata when a video appears in RSS.
                allvideos[vid]={'id':vid,'channelId':channel['id'],'handle':handle,'title':title,'published':published,'description':description[:500], 'thumbnail':'https://i.ytimg.com/vi/'+vid+'/hqdefault.jpg'}
            print('Updated',handle)
        except Exception as e:print('Feed issue',handle,str(e))
        time.sleep(.35)
    valid={h.lower() for h in HANDLES}
    videos=[v for v in allvideos.values() if v.get('handle','').lower() in valid]
    videos.sort(key=lambda v:v.get('published',''),reverse=True)
    # Retain history from prior runs; cap storage to keep GitHub Pages fast.
    payload={'updatedAt':datetime.now(timezone.utc).isoformat(),'channels':channels,'videos':videos[:500]}
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print('Saved',len(payload['videos']),'videos;',sum(bool(c['id']) for c in channels),'resolved channels')

if __name__=='__main__':main()
