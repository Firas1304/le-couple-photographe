import json,sys,re
f=sys.argv[1]; d=json.load(open(f,encoding='utf-8')); err=[]
wc=lambda t:len(t.split())
BAN=['meilleur','incontournable','magique','exceptionnel','€','euro','prix ','n°1','numéro 1','garanti','nous avons photographié','nous avons déjà','nous avons travaillé','🙂']
if not 90<=wc(d.get('intro',''))<=150: err.append('intro %d mots'%wc(d.get('intro','')))
if d.get('intro','').count('\n\n')!=1: err.append('intro doit avoir exactement 2 paragraphes séparés par une ligne vide')
L=d.get('lieux',[])
if not 4<=len(L)<=5: err.append('lieux: %d'%len(L))
for l in L:
    if not 30<=wc(l.get('texte',''))<=55: err.append('lieu %s: %d mots'%(l.get('nom'),wc(l.get('texte',''))))
if not 40<=wc(d.get('conseil',''))<=70: err.append('conseil %d mots'%wc(d.get('conseil','')))
if not 30<=wc(d.get('saison',''))<=60: err.append('saison %d mots'%wc(d.get('saison','')))
F=d.get('faq',[])
if len(F)!=4: err.append('faq != 4')
for q in F:
    if not 30<=wc(q.get('a',''))<=60: err.append('faq réponse %d mots'%wc(q.get('a','')))
txt=json.dumps(d,ensure_ascii=False).lower()
for b in BAN:
    if b in txt: err.append('mot interdit: '+b)
extra=set(d)-{'intro','lieux','conseil','saison','faq'}
if extra: err.append('clés en trop %s'%extra)
print('OK' if not err else '\n'.join(err))
