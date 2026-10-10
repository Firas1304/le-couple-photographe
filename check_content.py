import json,sys,re,collections
f,slug=sys.argv[1],sys.argv[2]
sys.path.insert(0,'.')
from data_places import PLACES
from data_services import SERVICES
pl=[p for p in PLACES if p['slug']==slug][0]; spots=[s[0] for s in pl['spots']]
d=json.load(open(f,encoding='utf-8')); err=[]
wc=lambda t:len(t.split())
starts=collections.Counter()
seen=collections.Counter()
BAN=['meilleur','incontournable','magique','€','euro','prix ','n°1','numéro 1','garanti','nous avons photographié','nous avons déjà']
for s in SERVICES:
    e=d.get(s['slug'])
    if not e: err.append('manque '+s['slug']); continue
    sc,co,fq=e.get('scene',''),e.get('conseil',''),e.get('faq',[])
    if not 55<=wc(sc)<=100: err.append('%s scene %d mots'%(s['slug'],wc(sc)))
    if not 25<=wc(co)<=60: err.append('%s conseil %d mots'%(s['slug'],wc(co)))
    if len(fq)!=2: err.append(s['slug']+' faq != 2')
    for q in fq:
        if not 25<=wc(q.get('a',''))<=60: err.append('%s faq réponse %d mots'%(s['slug'],wc(q.get('a',''))))
    n=sum(1 for sp in spots if sp in sc)
    if n<2: err.append('%s scene cite %d spot(s) exact(s)'%(s['slug'],n))
    starts[' '.join(sc.split()[:3]).lower()]+=1
    txt=' '.join([sc,co]+[q['q']+' '+q['a'] for q in fq]).lower()
    for b in BAN:
        if b in txt: err.append('%s mot interdit: %s'%(s['slug'],b))
    for sent in re.split(r'(?<=[.!?])\s+',sc+' '+co):
        if len(sent.split())>5: seen[sent.strip().lower()]+=1
for k,v in starts.items():
    if v>1: err.append('début répété: '+k)
for k,v in seen.items():
    if v>1: err.append('phrase répétée: '+k[:50])
extra=set(d)-{s['slug'] for s in SERVICES}
if extra: err.append('clés en trop: %s'%extra)
print('OK' if not err else '\n'.join(err))
