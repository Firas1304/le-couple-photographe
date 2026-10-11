# -*- coding: utf-8 -*-
"""Pages prestations, zones (Paris + Île-de-France) et combinaisons prestation x zone."""
import hashlib, json
import build as B
from data_services import SERVICES
from data_places import PLACES, PRIORITY, DEPS
esc=B.esc; href=B.href; img=B.img
import glob, os
CONTENT={}
for _f in glob.glob('content/*.json'):
    try: CONTENT[os.path.basename(_f)[:-5]]=json.load(open(_f,encoding='utf-8'))
    except Exception: pass
SV={s['slug']:s for s in SERVICES}; PL={p['slug']:p for p in PLACES}
CATN={'P':'nature et jardins','M':'monuments et architecture','W':'bords d\'eau','Q':'rues et quartiers','I':'lieux intérieurs'}
def h(s,m): return int(hashlib.md5(s.encode()).hexdigest(),16)%m
def low(s): return s[0].lower()+s[1:]
def pick_spots(pl,sv,n=3):
    order=sv['cats']; out=[]
    for c in order:
        for sp in pl['spots']:
            if sp[1]==c and sp not in out: out.append(sp)
    for sp in pl['spots']:
        if sp not in out: out.append(sp)
    return out[:n]
def dep_label(pl): return '%s (%s)'%(DEPS[pl['dep']],pl['dep'])
REAL={'grossesse':(2000,38),'famille':(2100,14),'solo':(2200,20)}
def seed(a):
    if a=='solo'+'paris-1er': return 2212   # colonne Vendôme (Paris 1er)
    if a=='solo'+'paris-8e': return 2200   # La Madeleine
    if a=='famille'+'paris-1er': return 2108   # Louvre
    if a=='famille'+'paris-7e': return 2106   # tour Eiffel
    if a=='grossessesceaux': return 2033   # parc de Sceaux
    if a=='grossesseparis-8e': return 2030   # pont Alexandre III, Paris 8e
    if a=='grossesseparis-1er': return 2014   # Palais-Royal : photos prises sur place
    for k,(base,n) in REAL.items():   # vraies photos par prestation
        if a.startswith(k): return base+h(a,n)
    return {'paris-1er':300}.get(a, 140+h(a,50))
def gstrip(s,k,alt):
    return B.strip(REAL[s][0]+h(k,max(1,REAL[s][1]-3)) if s in REAL else seed(k)+4,alt)

def place_list_links(depth,places,limit=None):
    return [(p['name'],'zones/%s/'%p['slug']) for p in (places[:limit] if limit else places)]

# ---------------- hub prestations ----------------
def hub_services():
    d=1;path='services/'
    tiles=''.join('<a class="tile rv" href="%s" data-cursor><div class="im">%s</div><h3>%s</h3><span>Photo &amp; vidéo</span></a>'%(href(d,'services/%s/'%s['slug']),img(seed(s['slug']),s['nom']),esc(s['name'])) for s in SERVICES)
    body=B.header(d)+B.hero(d,[('Accueil',''),('Prestations',None)],'Photographe et vidéaste <em>pour chaque moment</em>','Mariage, grossesse, couple, famille, naissance, événements professionnels : une prestation pour chaque étape de vie, en photo et en vidéo, à Paris et en Île-de-France.',150,'Photographe et vidéaste à Paris')+'<section class="sec" id="details"><div class="tiles">%s</div></section>'%tiles+B.cta(d)+B.footer(d)
    B.page(path,d,'Photographe et vidéaste Paris, tous types de shooting | Le Couple Photographe','Photographe et vidéaste à Paris et en Île-de-France : mariage, grossesse, couple, famille, naissance, corporate, événements. Découvrez nos 12 prestations.',[B.BIZ,B.breadcrumb_ld([('Accueil',''),('Prestations',path)])],body)
    return [path]

# ---------------- page prestation ----------------
def service_page(i,s):
    d=2;path='services/%s/'%s['slug']
    others=[(o['name'],'services/%s/'%o['slug']) for o in SERVICES if o['slug']!=s['slug']]
    zones=[(p['name'],'services/%s/%s/'%(s['slug'],p['slug'])) if (p['slug'] in PRIORITY or p['slug'] in CONTENT) else (p['name'],'zones/%s/'%p['slug']) for p in PLACES if p['slug'] in PRIORITY+['paris-1er','paris-11e','paris-12e']][:14]
    G=B.load_page('service',s['slug'])
    faqs=[(q['q'],q['a']) for q in G['faq']] if G else s['faq']
    ld=[B.BIZ,B.breadcrumb_ld([('Accueil',''),('Prestations','services/'),(s['name'],path)]),B.faq_ld(faqs),{"@context":"https://schema.org","@type":"Service","serviceType":s['nom'],"name":s['nom']+' à Paris et en Île-de-France',"provider":{"@type":"Photographer","name":B.NAME},"areaServed":"Île-de-France"}]
    steps=''.join('<div class="rv"><h3>%s</h3><p>%s</p></div>'%(esc(e['titre']),esc(e['texte'])) for e in G['etapes']) if G else ''.join('<div class="rv"><h3>%s</h3><p>%s</p></div>'%(esc(a),esc(b)) for a,b in s['deroule'])
    pv='<section class="cols"><div><div class="eyebrow">Photo et vidéo</div><h2 style="margin-top:18px">Deux regards, <em>une seule équipe</em></h2></div><div class="prose"><h3>Côté photo</h3><p>%s</p><h3>Côté vidéo</h3><p>%s</p><h3>Durée</h3><p>%s</p></div></section>'%(esc(s['photo']),esc(s['video']),esc(s['duree']))
    dep='<section class="cols" id="details"><div><div class="eyebrow">Notre approche</div><h2 style="margin-top:18px">%s</h2></div><div class="prose">%s</div></section>'%(['Ce que nous <em>faisons</em>','Notre <em>manière</em> de travailler','Pourquoi <em>nous choisir</em>'][i%3],''.join('<p>%s</p>'%esc(p) for p in (G['intro'].split('\n\n') if G else s['intro'])))
    ste='<section class="cols"><div><div class="eyebrow">Déroulé</div><h2 style="margin-top:18px">Du premier échange <em>à la livraison</em></h2></div><div class="moments">%s</div></section>'%steps
    con='<section class="cols"><div><div class="eyebrow">Conseils</div><h2 style="margin-top:18px">Pour une <em>belle séance</em></h2></div><div class="prose">%s<h3>Quelle saison ?</h3><p>%s</p></div></section>'%(''.join('<p>%s</p>'%esc(c) for c in s['conseils']),esc(s['saison']))
    orders=[[dep,pv,ste,con],[dep,ste,con,pv],[pv,dep,con,ste]]
    body=B.header(d)+B.hero(d,[('Accueil',''),('Prestations','services/'),(s['name'],None)],s['h1']+' <em>à Paris</em>' if False else s['h1']+' à Paris',esc(s['lead']),seed(s['slug']),s['nom']+' à Paris',ans=(G['reponse'] if G else '%s à Paris et en Île-de-France. Prestation : %s. %s %s'%(B.BRAND_DEF,s['nom'].lower(),s['photo'],s['video'])))
    body+='<section class="facts"><div><small>Zone</small><b>Paris et Île-de-France</b></div><div><small>Photo</small><b>Galerie privée retouchée</b></div><div><small>Vidéo</small><b>Film monté sur mesure</b></div><div><small>Devis</small><b>Personnalisé</b></div></section>'
    body+=''.join(orders[i%3])+gstrip(s['slug'],s['slug'],s['nom'])+B.faq_html(faqs)
    body+=B.links_block(d,'%s près de chez vous'%s['name'],zones+[('Toutes les zones','zones/')])+B.cta(d)+B.links_block(d,'Autres prestations',others)+B.footer(d)
    B.page(path,d,'%s à Paris et Île-de-France | Le Couple Photographe'%s['nom'],'%s à Paris et en Île-de-France. %s Demandez votre devis.'%(s['nom'],s['lead'].split('.')[0]+'.'),ld,body)
    return [path]

# ---------------- hub zones ----------------
def hub_zones():
    d=1;path='zones/'
    blocks=''
    for dep,nm in DEPS.items():
        ps=[p for p in PLACES if p['dep']==dep]
        if not ps: continue
        blocks+='<div class="rv" style="margin-bottom:46px"><h3 style="font:italic 400 clamp(28px,3.6vw,48px)/1.1 var(--serif);margin-bottom:16px">%s <span style="color:var(--mute);font-size:.5em;letter-spacing:.14em">%s</span></h3><div class="links">%s</div></div>'%(nm,dep,''.join('<a href="%s">%s</a>'%(href(d,'zones/%s/'%p['slug']),esc(p['name'])) for p in ps))
    body=B.header(d)+B.hero(d,[('Accueil',''),('Zones',None)],'Photographe et vidéaste <em>dans toute l\'Île-de-France</em>','Paris, ses 20 arrondissements, et les communes des huit départements : trouvez votre page locale, avec les lieux que nous aimons photographier.',160,'Photographe à Paris et en Île-de-France')+'<section class="sec" id="details">%s</section>'%blocks+B.cta(d)+B.footer(d)
    B.page(path,d,'Photographe vidéaste Paris et Île-de-France, toutes les zones | Le Couple Photographe','Photographe et vidéaste dans les 20 arrondissements de Paris et dans les communes d\'Île-de-France : Versailles, Boulogne-Billancourt, Vincennes, Fontainebleau, Saint-Denis et plus.',[B.BIZ,B.breadcrumb_ld([('Accueil',''),('Zones',path)])],body)
    return [path]

# ---------------- page zone ----------------
def zone_page(p):
    d=2;path='zones/%s/'%p['slug']
    sp=p['spots']
    spots=''.join('<div class="rv"><h3>%s</h3><p>%s.</p></div>'%(esc(n),esc(c[0].upper()+c[1:])) for n,_,c in sp)
    svc=''.join('<a class="tile rv" href="%s" data-cursor><div class="im">%s</div><h3>%s</h3><span>%s</span></a>'%(href(d,'services/%s/%s/'%(s['slug'],p['slug']) if (p['slug'] in PRIORITY or p['slug'] in CONTENT) else 'services/%s/'%s['slug']),img(seed(s['slug']+p['slug']),s['name']+' à '+p['name']),esc(s['name']),'à '+esc(p['name'])) for s in SERVICES)
    same=[q for q in PLACES if q['dep']==p['dep'] and q['slug']!=p['slug']][:8]
    faqs=[("Êtes-vous photographe et vidéaste à %s ?"%p['name'],"Oui. Nous intervenons à %s (%s) pour les mariages, les séances de couple, de famille, de grossesse, les naissances et les événements professionnels."%(p['name'],dep_label(p))),
          ("Quels sont les lieux que vous aimez photographier à %s ?"%p['name'],"Parmi nos lieux favoris : %s."%'; '.join('%s (%s)'%(n,c) for n,_,c in sp)),
          ("Comment se déplacer à %s pour une séance ?"%p['name'],p['acc']+" Nous nous déplaçons avec notre matériel et nous préparons l'itinéraire avec vous.")]
    ld=[B.BIZ,B.breadcrumb_ld([('Accueil',''),('Zones','zones/'),(p['name'],path)]),B.faq_ld(faqs),{"@context":"https://schema.org","@type":"Photographer","name":B.NAME+' à '+p['name'],"url":B.DOMAIN+'/'+path,"areaServed":{"@type":"AdministrativeArea" if p['dep']!='75' else "City","name":p['name']},"parentOrganization":{"@type":"Organization","name":B.NAME}}]
    body=B.header(d)+B.hero(d,[('Accueil',''),('Zones','zones/'),(p['name'],None)],'Photographe et vidéaste à <em>%s</em>'%esc(p['name']),esc(p['intro']),seed(p['slug']),'Photographe à '+p['name'],ans='%s qui intervient à %s (%s). Prestations : mariage, séance couple, famille, grossesse, naissance, nouveau-né, gender reveal, anniversaire, diplôme, portraits et événements professionnels. Lieux de prise de vue : %s.'%(B.BRAND_DEF,p['name'],dep_label(p),', '.join(n for n,_,_ in p['spots'])))
    body+='<section class="facts" id="details"><div><small>Lieu</small><b>%s</b></div><div><small>Département</small><b>%s</b></div><div><small>Accès</small><b>%s</b></div><div><small>Ambiance</small><b>%s</b></div></section>'%(esc(p['name']),esc(dep_label(p)),esc(p['acc'].split('.')[0]),esc(p['vibe'].split(',')[0].split('.')[0]))
    body+='<section class="cols"><div><div class="eyebrow">Les lieux</div><h2 style="margin-top:18px">Où photographier <em>à %s</em></h2></div><div class="moments">%s</div></section>'%(esc(p['name']),spots)
    body+='<section class="cols"><div><div class="eyebrow">Lumière et ambiance</div><h2 style="margin-top:18px">Le bon <em>moment</em></h2></div><div class="prose"><p>%s</p><p>%s</p></div></section>'%(esc(p['vibe']),esc(p['light']))
    body+='<section class="sec" aria-label="Prestations"><div class="sec-h"><div class="eyebrow">Prestations</div><h2>À %s, <em>nous photographions</em></h2></div><div class="tiles">%s</div></section>'%(esc(p['name']),svc)
    body+=B.faq_html(faqs)+B.cta(d)+B.links_block(d,'Autour de %s'%p['name'],[(q['name'],'zones/%s/'%q['slug']) for q in same]+[('Toutes les zones','zones/')])+B.footer(d)
    B.page(path,d,'Photographe et vidéaste %s | Le Couple Photographe'%p['name'],'Photographe et vidéaste à %s (%s) : mariage, couple, famille, grossesse, naissance, événements. %s'%(p['name'],dep_label(p),p['intro'].split('.')[0]+'.'),ld,body)
    return [path]

# ---------------- page prestation x zone ----------------
H1={'mariage':'Photographe et vidéaste de mariage à <em>%s</em>','grossesse':'Séance photo grossesse à <em>%s</em>','couple':'Photographe de couple à <em>%s</em>','famille':'Séance photo famille à <em>%s</em>','gender-reveal':'Gender reveal à <em>%s</em>, photo et vidéo','professionnels':'Photographe corporate à <em>%s</em>','evenements-professionnels':'Photographe d\'événement d\'entreprise à <em>%s</em>','solo':'Portrait solo à <em>%s</em>','anniversaire':'Photographe d\'anniversaire à <em>%s</em>','diplome':'Photographe de remise de diplôme à <em>%s</em>','naissance':'Photographe de naissance à <em>%s</em>','nouveau-ne':'Photographe nouveau-né à <em>%s</em>'}
POUR={'mariage':'un mariage','grossesse':'une séance grossesse','couple':'une séance couple','famille':'une séance famille','gender-reveal':'un gender reveal','professionnels':'des portraits professionnels','evenements-professionnels':'un événement d\'entreprise','solo':'un portrait solo','anniversaire':'un anniversaire','diplome':'une remise de diplôme','naissance':'une naissance','nouveau-ne':'une séance nouveau-né'}
def combo_page(s,p):
    d=3;path='services/%s/%s/'%(s['slug'],p['slug'])
    k=h(s['slug']+p['slug'],3)
    top=pick_spots(p,s,4)
    seen=set(); parts=[]
    for n,cat,c in top:
        extra='' if cat in seen else ' '+s['sent'].get(cat,'')
        seen.add(cat)
        parts.append('<div class="rv"><h3>%s</h3><p>%s.%s</p></div>'%(esc(n),esc(c[0].upper()+c[1:]),esc(extra)))
    cards=''.join(parts)
    cons=s['conseils'][h(p['slug']+s['slug'],len(s['conseils']))]
    s1=top[0][0]; s2=top[1][0] if len(top)>1 else top[0][0]
    lead_opts=["%s Pour %s, nous aimons le cadre de %s et celui de %s."%(p['intro'],POUR[s['slug']],s1,s2),
               "%s %s Nous vous proposons de commencer à %s, puis de poursuivre à %s."%(p['vibe'],s['lead'],s1,s2),
               "%s Une séance à %s, c'est aussi la possibilité de varier les ambiances entre %s et %s."%(s['lead'],p['name'],s1,s2)]
    lead=lead_opts[k]
    C=CONTENT.get(p['slug'],{}).get(s['slug'])
    faqs=[("Où faire un shooting %s à %s ?"%(low(s['name']),p['name']),"Nos lieux préférés pour ce type de séance : %s. Nous choisissons avec vous selon votre style et la météo."%'; '.join('%s (%s)'%(n,c) for n,_,c in top)),
          ("Quelle est la meilleure lumière à %s pour une séance %s ?"%(p['name'],low(s['name'])),p['light']+" "+s['saison']),
          ("Comment venir à %s ?"%p['name'],p['acc']+" Nous nous déplaçons avec notre matériel photo et vidéo."),
          s['faq'][h(p['slug'],len(s['faq']))]]
    if C: faqs=[(q['q'],q['a']) for q in C['faq']]+faqs[2:3]+[faqs[3]]
    ld=[B.BIZ,B.breadcrumb_ld([('Accueil',''),('Prestations','services/'),(s['name'],'services/%s/'%s['slug']),(p['name'],path)]),B.faq_ld(faqs),{"@context":"https://schema.org","@type":"Service","serviceType":s['nom'],"name":"%s à %s"%(s['nom'],p['name']),"provider":{"@type":"Photographer","name":B.NAME},"areaServed":{"@type":"Place","name":p['name']}}]
    sec_spots='<section class="cols" id="details"><div><div class="eyebrow">Lieux à %s</div><h2 style="margin-top:18px">Nos lieux <em>pour cette séance</em></h2></div><div class="moments">%s</div></section>'%(esc(p['name']),cards)
    if C: cons=C['conseil']
    sec_scene=('<section class="cols" id="details"><div><div class="eyebrow">Prises de vue à %s</div><h2 style="margin-top:18px">Où faire <em>votre shooting</em></h2></div><div class="prose"><p>%s</p></div></section>'%(esc(p['name']),esc(C['scene']))) if C else ''
    sec_conseil='<section class="cols"><div><div class="eyebrow">Notre conseil</div><h2 style="margin-top:18px">%s</h2></div><div class="prose"><p>%s</p><p>%s</p><p>%s</p><p>%s</p></div></section>'%(['Bien <em>choisir</em> son moment','Sur <em>place</em>','Pour que tout <em>se passe bien</em>'][k],esc(p['vibe']+' '+p['light']),esc(s['intro'][k%2]),esc(cons),esc('À %s, vous êtes à %s : %s'%(p['name'],low(p['acc'].split('.')[0]) if False else p['acc'].split('.')[0],'nous préparons l\'itinéraire entre les lieux avec vous.')))
    sec_deroule='<section class="cols"><div><div class="eyebrow">Déroulé</div><h2 style="margin-top:18px">%s</h2></div><div class="moments">%s</div></section>'%('De l\'échange <em>à la livraison</em>',''.join('<div class="rv"><h3>%s</h3><p>%s</p></div>'%(esc(a),esc(b)) for a,b in s['deroule'][:3]))
    sec_spots=sec_spots.replace(' id="details"','') if C else sec_spots
    orders=[[sec_scene,sec_spots,sec_conseil],[sec_scene,sec_conseil,sec_spots],[sec_scene,sec_spots,sec_conseil]] if C else [[sec_spots,sec_conseil],[sec_conseil,sec_spots],[sec_spots,sec_conseil]]
    zones_near=[(q['name'],'services/%s/%s/'%(s['slug'],q['slug'])) for q in PLACES if q['slug'] in PRIORITY and q['slug']!=p['slug']][:6]
    body=B.header(d)+B.hero(d,[('Accueil',''),(s['name'],'services/%s/'%s['slug']),(p['name'],None)],H1[s['slug']]%esc(p['name']),esc(lead),seed(s['slug']+p['slug']),s['nom']+' à '+p['name'],ans='%s qui propose la prestation « %s » à %s (%s). Lieux de prise de vue possibles : %s. Devis personnalisé sur la page Devis.'%(B.BRAND_DEF,s['nom'].lower(),p['name'],dep_label(p),', '.join(n for n,_,_ in top[:3])))
    body+='<section class="facts"><div><small>Prestation</small><b>%s</b></div><div><small>Lieu</small><b>%s</b></div><div><small>Durée</small><b>%s</b></div><div><small>Livraison</small><b>Photo et vidéo</b></div></section>'%(esc(s['name']),esc(p['name']),esc(s['duree'].split(',')[0].rstrip('.')))
    body+=''.join(orders[k])+(gstrip(s['slug'],p['slug'],'%s à %s'%(s['nom'],p['name'])) if s['slug'] in REAL else B.strip(seed(p['slug'])+s['cats'].__len__(),'%s à %s'%(s['nom'],p['name'])))+B.faq_html(faqs)+B.cta(d)
    body+=B.links_block(d,'%s ailleurs en Île-de-France'%s['name'],zones_near+[(s['name']+' en Île-de-France','services/%s/'%s['slug']),('Zone : '+p['name'],'zones/%s/'%p['slug'])])+B.footer(d)
    B.page(path,d,'%s à %s | Le Couple Photographe'%(s['nom'],p['name']),'%s à %s (%s). %s Devis personnalisé.'%(s['nom'],p['name'],dep_label(p),p['intro'].split('.')[0]+'.'),ld,body)
    return [path]

def run():
    urls=[]
    urls+=hub_services()
    for i,s in enumerate(SERVICES): urls+=service_page(i,s)
    urls+=hub_zones()
    for p in PLACES: urls+=zone_page(p)
    combos=[pid for pid in [p['slug'] for p in PLACES] if pid in CONTENT or pid in PRIORITY]
    for s in SERVICES:
        for pid in combos: urls+=combo_page(s,PL[pid])
    return urls
