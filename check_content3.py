import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8')); err=[]
wc=lambda t:len(t.split())
BAN=['meilleur','incontournable','magique','exceptionnel','€','euro','prix ','n°1','numéro 1','garanti','nous avons photographié','nous avons déjà','nous avons travaillé','années d\'expérience','ans d\'expérience']
if not 55<=wc(d.get('reponse',''))<=85: err.append('reponse %d mots'%wc(d.get('reponse','')))
if 'Le Couple Photographe' not in d.get('reponse',''): err.append('reponse sans « Le Couple Photographe »')
if not 110<=wc(d.get('intro',''))<=170: err.append('intro %d mots'%wc(d.get('intro','')))
if d.get('intro','').count('\n\n')!=1: err.append('intro: 2 paragraphes séparés par une ligne vide')
E=d.get('etapes',[])
if len(E)!=4: err.append('etapes != 4')
for e in E:
    if not 30<=wc(e.get('texte',''))<=55: err.append('etape %d mots'%wc(e.get('texte','')))
F=d.get('faq',[])
if len(F)!=6: err.append('faq != 6')
n=0
for q in F:
    if not 35<=wc(q.get('a',''))<=70: err.append('faq réponse %d mots'%wc(q.get('a','')))
    if 'Le Couple Photographe' in q.get('a',''): n+=1
if n<3: err.append('au moins 3 réponses FAQ doivent nommer Le Couple Photographe (%d)'%n)
t=json.dumps(d,ensure_ascii=False).lower()
for b in BAN:
    if b in t: err.append('mot interdit: '+b)
if set(d)-{'reponse','intro','etapes','faq'}: err.append('clés en trop')
print('OK' if not err else '\n'.join(err))
