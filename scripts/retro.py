"""Original pixel-art assets and real GitHub score. Python standard library only."""
from pathlib import Path
from datetime import date, datetime, timedelta
import json, os, urllib.request, html

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'retro'
OUT.mkdir(exist_ok=True)
INK='#182a3a'; PAPER='#fff3d6'; TEAL='#82d5bc'; GOLD='#ffcd6b'; PINK='#ed99ae'
# Five-by-seven bitmap lettering, drawn as paths: no external fonts or requests.
FONT = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-./:+? ', [
'01110/10001/10001/11111/10001/10001/10001','11110/10001/10001/11110/10001/10001/11110','01111/10000/10000/10000/10000/10000/01111','11110/10001/10001/10001/10001/10001/11110','11111/10000/10000/11110/10000/10000/11111','11111/10000/10000/11110/10000/10000/10000','01111/10000/10000/10111/10001/10001/01111','10001/10001/10001/11111/10001/10001/10001','11111/00100/00100/00100/00100/00100/11111','00111/00010/00010/00010/10010/10010/01100','10001/10010/10100/11000/10100/10010/10001','10000/10000/10000/10000/10000/10000/11111','10001/11011/10101/10101/10001/10001/10001','10001/11001/10101/10011/10001/10001/10001','01110/10001/10001/10001/10001/10001/01110','11110/10001/10001/11110/10000/10000/10000','01110/10001/10001/10001/10101/10010/01101','11110/10001/10001/11110/10100/10010/10001','01111/10000/10000/01110/00001/00001/11110','11111/00100/00100/00100/00100/00100/00100','10001/10001/10001/10001/10001/10001/01110','10001/10001/10001/10001/10001/01010/00100','10001/10001/10001/10101/10101/10101/01010','10001/10001/01010/00100/01010/10001/10001','10001/10001/01010/00100/00100/00100/00100','11111/00001/00010/00100/01000/10000/11111',
'01110/10001/10011/10101/11001/10001/01110','00100/01100/00100/00100/00100/00100/01110','01110/10001/00001/00010/00100/01000/11111','11110/00001/00001/01110/00001/00001/11110','00010/00110/01010/10010/11111/00010/00010','11111/10000/10000/11110/00001/00001/11110','01110/10000/10000/11110/10001/10001/01110','11111/00001/00010/00100/01000/01000/01000','01110/10001/10001/01110/10001/10001/01110','01110/10001/10001/01111/00001/00001/01110',
'00000/00000/00000/11111/00000/00000/00000','00000/00000/00000/00000/00000/00110/00110','00001/00001/00010/00100/01000/10000/10000','00000/00100/00100/00000/00100/00100/00000','00000/00100/00100/11111/00100/00100/00000','01110/10001/00001/00010/00100/00000/00100','00000/00000/00000/00000/00000/00000/00000']))

FONT['>']='10000/01000/00100/00010/00100/01000/10000'
FONT['=']='00000/00000/11111/00000/11111/00000/00000'
FONT['_']='00000/00000/00000/00000/00000/00000/11111'

def rect(x,y,w,h,c): return f'<path fill="{c}" d="M{x} {y}h{w}v{h}h-{w}z"/>'
def text(s,x,y,size=2,c=PAPER):
    d=[]
    for i,ch in enumerate(s.upper()):
        for row,line in enumerate(FONT.get(ch,FONT['?']).split('/')):
            for col,p in enumerate(line):
                if p=='1': d.append(f'M{x+(i*6+col)*size} {y+row*size}h{size}v{size}h-{size}z')
    return f'<path fill="{c}" d="{"".join(d)}"/>'

def svg(body,w,h,title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title,quote=True)}" shape-rendering="crispEdges"><title>{html.escape(title)}</title><style>
    .float{{animation:float 2.4s steps(3,end) infinite}}.coin{{animation:coin 1.3s steps(2,end) infinite;transform-box:fill-box;transform-origin:center}}.blink{{animation:blink 1.5s steps(1,end) infinite}}.walk{{animation:walk .6s steps(2,end) infinite}}
    @keyframes float{{50%{{transform:translateY(-6px)}}}}@keyframes coin{{50%{{transform:scaleX(.3)}}}}@keyframes blink{{50%{{opacity:.25}}}}@keyframes walk{{50%{{transform:translateY(-2px)}}}}
    @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>{body}</svg>'''

def sprite(rows,x,y,scale,palette):
    return ''.join(rect(x+col*scale,y+row*scale,scale,scale,palette[p]) for row,line in enumerate(rows) for col,p in enumerate(line) if p in palette)

def coin(x,y):
    return '<g class="coin">'+sprite(['.aaa.','abcca','abcca','abcca','abcca','.aaa.'],x,y,3,{'a':'#bc783c','b':GOLD,'c':'#ffecad'})+'</g>'

def cloud(x,y,k=1):
    return f'<g transform="translate({x} {y}) scale({k})">'+rect(8,0,32,8,'#d9e8d5')+rect(0,8,64,8,'#d9e8d5')+rect(8,16,48,6,'#aacdc2')+'</g>'

def ground(y,w=960):
    b=rect(0,y,w,12,TEAL)+rect(0,y+12,w,5,'#448b86')+rect(0,y+17,w,90,'#5b5765')
    for x in range(0,w,32):
        b+=rect(x+2,y+22,26,18,'#71616d')+rect(x+17,y+48,26,18,'#71616d')+rect(x+3,y+24,5,3,'#958085')
    return b

def hero():
    b=rect(0,0,960,510,INK)+rect(8,8,944,494,'#243d4a')
    b+=text('PLAYER 01',32,28,2,TEAL)+text('GABRIELMELLO1407',342,28,2)+text('WORLD 01-01',790,28,2,GOLD)
    b+=rect(24,60,912,2,'#4f6d70')
    b+=text('GABRIEL',36,90,8,'#0f2331')+text('GABRIEL',32,86,8,PAPER)
    b+=text('MELLO',36,162,8,'#0f2331')+text('MELLO',32,158,8,TEAL)
    b+=text('SOFTWARE DEVELOPER',34,242,2)+text('FULL STACK / APPLIED AI',34,266,2,'#a9c4bf')
    b+=cloud(630,104)+cloud(798,75,.7)+cloud(866,180,.85)
    # A tiny original developer: dark hair, glasses, teal jacket, laptop backpack.
    player=['....hhhhh.....','...hhhhhhh....','...hssssss....','...sggsggs....','...sggsggs....','....sssss.....','.....sss......','...ttttttbb...','..tttttttbb...','..tstttttbb...','...sttttt.....','....ppppp.....','....pp.pp.....','....pp.pp.....','...ddd.ddd....']
    b+='<g class="walk">'+sprite(player,624,254,7,{'h':'#17232c','s':'#e4ab85','g':'#233c4a','t':TEAL,'b':'#c7a1c8','p':'#536b8b','d':'#132b39'})+'</g>'
    b+=rect(733,288,100,8,'#43666d')+rect(749,296,8,63,'#43666d')+rect(814,296,8,63,'#43666d')
    b+=rect(749,248,64,40,'#132b39')+rect(754,253,54,28,'#82d5bc')+text('>_',765,261,1,INK)+rect(744,288,74,5,PAPER)
    for x in [526,566,606]: b+=coin(x,329)
    for x in [450,482,514]: b+=rect(x,382,30,28,'#b38479')+rect(x+3,385,24,4,'#e1b18b')+rect(x+3,394,4,12,'#765965')
    b+='<g class="float">'+rect(864,262,40,40,'#bc783c')+rect(868,266,32,32,GOLD)+text('?',878,271,3,INK)+'</g>'
    b+=rect(604,359,326,10,TEAL)+rect(604,369,326,10,'#448b86')
    b+=ground(410)
    b+=text('BUILD. SHIP. PLAY AGAIN.',32,363,3,GOLD)
    b+=rect(24,455,912,34,INK)+text('PRESS START',40,465,2,TEAL)+text('PORTFOLIO / PROJECTS / CONTACT',382,466,1,PAPER)
    b+='<g class="blink">'+rect(221,465,10,14,GOLD)+'</g>'
    (OUT/'world.svg').write_text(svg(b,960,510,'Gabriel Mello. Original animated 2D pixel world: developer, coins, laptop and platforms.'))

def quests():
    b=rect(0,0,960,254,INK)+text('SELECT YOUR QUEST',28,24,3,TEAL)+text('FOUR BUILDS. REAL WORLDS.',28,58,1,'#a9c4bf')
    titles=['FLUNEXAPP','ROTAMER','COMPRAS','AITEC']
    desc=['WHATSAPP + AI','MOLECULAR LAB','PUBLIC SECTOR','INNOVATION']
    colors=[TEAL,PINK,GOLD,'#a9a9ed']
    for i in range(4):
        x=28+i*234
        b+=rect(x,94,204,132,'#35515b')+rect(x+4,98,196,124,'#243d4a')
        b+=text('0'+str(i+1),x+12,109,2,colors[i])+text(titles[i],x+12,153,2,PAPER)+text(desc[i],x+12,182,1.5,'#b3c9c3')
        b+=text('ENTER >',x+12,204,1,colors[i])
        b+='<g class="float" style="animation-delay:'+str(i*.3)+'s">'+coin(x+164,111)+'</g>'
    (OUT/'quests.svg').write_text(svg(b,960,254,'Quest select: FlunexApp, Rotamer, Compras Publicas, AITEC. Links below the image.'))

def streaks(days,today):
    counts={d['date']:d['contributionCount'] for d in days}
    longest=run=0
    previous=None
    for ds in sorted(counts):
        current=date.fromisoformat(ds)
        run=(run+1 if previous and current-previous==timedelta(days=1) else 1) if counts[ds]>0 else 0
        longest=max(longest,run); previous=current
    cursor=today if counts.get(today.isoformat(),0)>0 else today-timedelta(days=1)
    active=0
    while counts.get(cursor.isoformat(),0)>0:
        active+=1;cursor-=timedelta(days=1)
    return active,longest

def fetch():
    query='''query($login:String!){user(login:$login){repositories(ownerAffiliations:OWNER,privacy:PUBLIC){totalCount} contributionsCollection{totalCommitContributions contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}'''
    req=urllib.request.Request('https://api.github.com/graphql',data=json.dumps({'query':query,'variables':{'login':'GabrielMello1407'}}).encode(),headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Content-Type':'application/json','User-Agent':'Gabriel-Retro-Profile'})
    with urllib.request.urlopen(req,timeout=40) as response: payload=json.load(response)
    if payload.get('errors'): raise RuntimeError(payload['errors'])
    u=payload['data']['user'];c=u['contributionsCollection'];cal=c['contributionCalendar']
    days=[d for w in cal['weeks'] for d in w['contributionDays']]
    # GitHub's last calendar day is its authoritative reporting day.
    today=date.fromisoformat(days[-1]['date'])
    current,longest=streaks(days,today)
    return {'updated':datetime.now().isoformat(timespec='seconds')+'Z','current':current,'longest':longest,'commits':c['totalCommitContributions'],'contributions':cal['totalContributions'],'repos':u['repositories']['totalCount'],'days':days}

def score(data):
    b=rect(0,0,960,330,INK)+text('SAVE FILE / GITHUB',28,24,3,TEAL)
    b+=text('LAST 12 MONTHS',740,30,2,'#a9c4bf')
    metrics=[('CURRENT STREAK','current','DAYS'),('BEST STREAK','longest','DAYS'),('COMMITS','commits','12 MONTHS'),('CONTRIBUTIONS','contributions','12 MONTHS')]
    for i,(label,key,unit) in enumerate(metrics):
        x=28+234*i;c=[TEAL,GOLD,PINK,'#b9b3ef'][i]
        b+=rect(x,68,204,105,'#304954')+text(label,x+12,81,2,c)
        b+=text(str(data[key]) if data else '--',x+12,105,4,PAPER)+text(unit,x+12,147,1.5,'#a9c4bf')
    days=data.get('days',[])[-182:] if data else []
    for i,d in enumerate(days):
        n=d['contributionCount'];col=['#304954','#416b67','#509b83',TEAL,GOLD][0 if n==0 else min(4,1+(n>3)+(n>8)+(n>15))]
        x=28+(i//7)*22;y=201+(i%7)*12
        b+=f'<g><title>{d["date"]}: {n} contributions</title>'+rect(x,y,16,8,col)+'</g>'
    b+=text('ACTIVITY MAP',640,205,2,TEAL)+text('26 WEEKS / PUBLIC DATA',640,232,1,'#a9c4bf')
    b+=text('STREAK = DAYS WITH CONTRIBUTIONS',640,257,1,'#a9c4bf')
    b+=text('SYNCED '+data['updated'][:10] if data else 'SYNC PENDING / NEVER INVENTED',28,306,1,'#a9c4bf')
    (OUT/'score.svg').write_text(svg(b,960,330,'Real GitHub score: '+json.dumps({k:v for k,v in (data or {}).items() if k!='days'})+'. Streaks use contribution days in the last 12 months.'))

if __name__=='__main__':
    hero();quests()
    path=OUT/'stats.json'
    if os.environ.get('GH_TOKEN'):
        data=fetch();path.write_text(json.dumps(data,indent=2)+'\n')
    else:
        data=json.loads(path.read_text()) if path.exists() else None
    score(data)
