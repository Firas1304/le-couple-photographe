#!/usr/bin/env python3
"""Générateur du site Le Couple Photographe.
Usage : python3 build.py            -> site de production (liens propres) dans la racine du dépôt
        python3 build.py --artifact DIR -> variante de prévisualisation (liens index.html) dans DIR"""
import sys, os, json, html, shutil, re
ART = '--artifact' in sys.argv
OUT = sys.argv[sys.argv.index('--artifact')+1] if ART else '.'
DOMAIN = 'https://www.lecouplephotographe.fr'   # à remplacer par votre vrai domaine
IG = 'https://www.instagram.com/le_couple_photographe/'
NAME = 'Le Couple Photographe'
esc = html.escape

PALACES = [
 dict(slug='ritz-paris', name='Ritz Paris', addr='15 place Vendôme, 75001 Paris', area='Place Vendôme (1er)',
  hook="La place Vendôme et son écrin de pierre blanche composent un décor de mariage unique.",
  lieu="Le Ritz Paris donne sur la place Vendôme, l'une des plus belles places de la capitale. Le palace dispose aussi d'un jardin intérieur, précieux pour des portraits au calme loin de la foule.",
  lumiere="Les façades claires de la place Vendôme renvoient une lumière douce en fin de matinée. Nous prévoyons un créneau de portraits à ce moment, puis un second dans les salons.",
  orga="Prises de vue dans l'hôtel et sur la place : nous préparons le planning avec votre wedding planner et l'établissement pour que chaque lieu soit disponible à l'heure prévue."),
 dict(slug='le-bristol-paris', name='Le Bristol Paris', addr='112 rue du Faubourg Saint-Honoré, 75008 Paris', area='Faubourg Saint-Honoré (8e)',
  hook="Un palace au jardin intérieur, à deux pas de l'Élysée, pour un mariage élégant.",
  lieu="Le Bristol est installé rue du Faubourg Saint-Honoré, dans le triangle d'or parisien. Son jardin intérieur offre un cadre verdoyant rare en plein 8e arrondissement.",
  lumiere="Le jardin reçoit une lumière filtrée très flatteuse pour les portraits de couple et de famille. Nous l'utilisons de préférence avant le cocktail.",
  orga="Nous coordonnons les photos de groupe et les portraits pour qu'ils tiennent en quelques minutes, sans vous couper de vos invités."),
 dict(slug='plaza-athenee', name='Hôtel Plaza Athénée', addr='25 avenue Montaigne, 75008 Paris', area='Avenue Montaigne (8e)',
  hook="Les auvents rouges de l'avenue Montaigne, un décor devenu un symbole de Paris.",
  lieu="Le Plaza Athénée, avenue Montaigne, est reconnaissable à ses auvents rouges et à ses fleurs en façade. La cour intérieure et les salons offrent des arrière-plans très photogéniques.",
  lumiere="La façade et la cour sont à leur avantage par temps clair comme par temps couvert, car la couleur ressort davantage sous un ciel gris.",
  orga="Nous repérons les angles de la façade et de la cour avec vous en amont, pour gagner du temps le jour J."),
 dict(slug='le-meurice', name='Le Meurice', addr='228 rue de Rivoli, 75001 Paris', area='Rue de Rivoli (1er)',
  hook="Face au jardin des Tuileries, un palace pour un mariage à la française.",
  lieu="Le Meurice fait face au jardin des Tuileries, sur la rue de Rivoli. Les salons ornés de l'hôtel et le jardin tout proche permettent de varier les ambiances en quelques pas.",
  lumiere="Les Tuileries offrent de longues perspectives et une belle lumière en fin de journée, idéale pour une séance de couple après la cérémonie.",
  orga="Nous prévoyons un trajet court entre l'hôtel et le jardin, avec une marge pour la circulation et les invités."),
 dict(slug='four-seasons-george-v', name='Four Seasons Hotel George V', addr='31 avenue George V, 75008 Paris', area='Avenue George V (8e)',
  hook="Un palace réputé pour ses compositions florales, à quelques pas des Champs-Élysées.",
  lieu="Le George V se trouve avenue George V, près des Champs-Élysées. L'hôtel est connu pour ses grands arrangements floraux et sa cour intérieure.",
  lumiere="Les fleurs et les dorures demandent un traitement soigné des couleurs. Nous veillons à garder des teintes naturelles sur vos portraits.",
  orga="Nous échangeons avec votre fleuriste et votre décorateur pour photographier les compositions avant l'arrivée des invités."),
 dict(slug='hotel-de-crillon', name='Hôtel de Crillon', addr='10 place de la Concorde, 75008 Paris', area='Place de la Concorde (8e)',
  hook="Une façade du XVIIIe siècle sur la place de la Concorde, pour des images intemporelles.",
  lieu="L'Hôtel de Crillon occupe l'un des deux palais qui bordent la place de la Concorde, construits au XVIIIe siècle. La place et les perspectives vers les Tuileries donnent un cadre monumental.",
  lumiere="Tôt le matin ou au coucher du soleil, la place est dégagée et la lumière rasante met la pierre en valeur.",
  orga="Nous choisissons avec vous l'horaire des portraits extérieurs, pour éviter les heures de grande affluence."),
 dict(slug='shangri-la-paris', name='Shangri-La Paris', addr='10 avenue d\'Iéna, 75116 Paris', area='Avenue d\'Iéna (16e)',
  hook="Une ancienne demeure du prince Roland Bonaparte, avec la tour Eiffel en toile de fond.",
  lieu="Le Shangri-La Paris occupe l'ancien hôtel particulier du prince Roland Bonaparte, avenue d'Iéna. Plusieurs espaces de l'hôtel ont une vue sur la tour Eiffel.",
  lumiere="Les vues sur la tour Eiffel sont très sensibles à l'heure : nous repérons avec vous le meilleur moment pour les portraits sur terrasse ou en fenêtre.",
  orga="Nous préparons des repères visuels (étage, terrasse, salon) à l'avance pour que les portraits se fassent sans perte de temps."),
 dict(slug='mandarin-oriental-paris', name='Mandarin Oriental Paris', addr='251 rue Saint-Honoré, 75001 Paris', area='Rue Saint-Honoré (1er)',
  hook="Un palace contemporain avec jardin intérieur, au cœur du quartier Saint-Honoré.",
  lieu="Le Mandarin Oriental est situé rue Saint-Honoré, entre la place Vendôme et les Tuileries. Son jardin intérieur offre un décor calme et lumineux au centre de Paris.",
  lumiere="Le jardin est un bon choix pour des portraits naturels, sans fond urbain. Nous l'associons à une séance rapide aux Tuileries si la météo le permet.",
  orga="Nous adaptons le planning selon les espaces réservés pour votre événement, en lien avec l'hôtel."),
 dict(slug='the-peninsula-paris', name='The Peninsula Paris', addr='19 avenue Kléber, 75116 Paris', area='Avenue Kléber (16e)',
  hook="Un palace installé dans un bâtiment de 1908, près de l'Arc de Triomphe.",
  lieu="The Peninsula Paris occupe un bâtiment de 1908, avenue Kléber, à proximité de l'Arc de Triomphe. Les terrasses et les espaces de réception offrent des perspectives variées sur la ville.",
  lumiere="Les terrasses en hauteur apportent une belle lumière de fin de journée. Nous les prévoyons pour la séance de couple pendant le cocktail.",
  orga="Nous synchronisons les portraits avec le service de l'hôtel pour ne pas retarder le dîner."),
 dict(slug='royal-monceau', name='Le Royal Monceau', addr='37 avenue Hoche, 75008 Paris', area='Avenue Hoche (8e)',
  hook="Un palace du 8e arrondissement, près de l'Arc de Triomphe et du parc Monceau.",
  lieu="Le Royal Monceau est situé avenue Hoche, entre l'Arc de Triomphe et le parc Monceau. Le quartier permet des portraits dans un cadre haussmannien très parisien.",
  lumiere="Les larges avenues haussmanniennes offrent une lumière uniforme en journée. Le parc Monceau, tout proche, apporte de la verdure pour une séance de couple.",
  orga="Nous préparons un petit itinéraire à pied pour que la séance extérieure reste courte et confortable."),
]
CITIES = [
 dict(slug='paris', name='Paris', reg='Île-de-France', hook="Mairies, quais de Seine, palaces et toits de zinc.", lieux=["hôtels de ville et mairies d'arrondissement","quais de Seine et ponts","palaces et hôtels particuliers"], lum="Les quais et les rues haussmanniennes sont superbes tôt le matin, quand la ville est encore calme.", plan="Prévoyez du temps pour les déplacements entre la mairie, le lieu de réception et les spots photo."),
 dict(slug='versailles', name='Versailles', reg='Yvelines', hook="Le château, ses jardins et les rues du vieux Versailles.", lieux=["abords du château et jardins","domaines des Yvelines","rues du quartier Saint-Louis"], lum="Les jardins offrent de longues perspectives. Nous visons le début ou la fin de journée pour une lumière douce.", plan="Renseignez-vous sur les autorisations de prise de vue dans les lieux historiques bien en amont."),
 dict(slug='fontainebleau', name='Fontainebleau', reg='Seine-et-Marne', hook="Forêt, château et domaines de campagne à une heure de Paris.", lieux=["abords du château","forêt de Fontainebleau","domaines et manoirs alentour"], lum="La forêt filtre la lumière et crée une ambiance douce, même en plein été.", plan="Si vous passez par la forêt, prévoyez des chaussures confortables pour la séance de couple."),
 dict(slug='lyon', name='Lyon', reg='Auvergne-Rhône-Alpes', hook="Vieux-Lyon, Fourvière, quais du Rhône et de la Saône.", lieux=["Vieux-Lyon et ses traboules","colline de Fourvière","domaines du Beaujolais"], lum="Les ruelles du Vieux-Lyon sont plus intimes tôt le matin. Les quais sont idéaux au coucher du soleil.", plan="Les traboules sont étroites : nous prévoyons des portraits à deux ou en petit groupe."),
 dict(slug='bordeaux', name='Bordeaux', reg='Nouvelle-Aquitaine', hook="Place de la Bourse, miroir d'eau et châteaux viticoles.", lieux=["place de la Bourse et quais","châteaux de Saint-Émilion et du Médoc","bassin d'Arcachon"], lum="Les vignes à la fin de l'été donnent une lumière dorée très cinématographique.", plan="Pour un mariage dans un domaine viticole, prévoyez un temps d'installation plus long."),
 dict(slug='marseille', name='Marseille', reg='Provence-Alpes-Côte d\'Azur', hook="Vieux-Port, Notre-Dame de la Garde et calanques.", lieux=["Vieux-Port","Corniche et plages","calanques"], lum="La lumière méditerranéenne est forte à midi : nous plaçons les portraits tôt ou tard dans la journée.", plan="Le vent peut se lever sur la côte : prévoyez des tenues et des coiffures adaptées."),
 dict(slug='aix-en-provence', name='Aix-en-Provence', reg='Provence-Alpes-Côte d\'Azur', hook="Bastides, champs de lavande et rues du centre ancien.", lieux=["bastides et domaines","centre historique","campagne provençale"], lum="La lumière provençale est chaude et contrastée. Nous privilégions le début de soirée.", plan="En été, prévoyez de l'ombre et de l'eau pour vos invités pendant les photos de groupe."),
 dict(slug='nice', name='Nice', reg='Provence-Alpes-Côte d\'Azur', hook="Promenade des Anglais, vieille ville et arrière-pays.", lieux=["Promenade des Anglais","vieille ville de Nice","villas de la Côte d'Azur"], lum="Le lever du soleil sur la baie offre des portraits très doux avant la chaleur.", plan="La Promenade est très fréquentée : nous choisissons des horaires et des spots plus calmes."),
 dict(slug='cannes', name='Cannes', reg='Provence-Alpes-Côte d\'Azur', hook="La Croisette, le Suquet et les îles de Lérins.", lieux=["La Croisette","le Suquet","villas et hôtels de la Côte d'Azur"], lum="La baie et le port donnent de belles réflexions en fin de journée.", plan="Pendant les grands événements de la ville, circulation et hébergements sont plus tendus : anticipez."),
 dict(slug='lille', name='Lille', reg='Hauts-de-France', hook="Vieux-Lille, Grand-Place et briques flamandes.", lieux=["Vieux-Lille","Grand-Place","châteaux et fermes des Hauts-de-France"], lum="Les façades de brique et de pierre ressortent bien sous un ciel couvert, fréquent dans le Nord.", plan="Prévoyez un plan B pluie, par exemple une salle ou une galerie couverte pour les portraits."),
 dict(slug='toulouse', name='Toulouse', reg='Occitanie', hook="La ville rose, le Capitole et les bords de Garonne.", lieux=["place du Capitole","bords de la Garonne","domaines du Tarn et du Gers"], lum="La brique rose prend des teintes chaudes au coucher du soleil.", plan="Les mariages civils au Capitole sont très demandés : réservez la date tôt."),
 dict(slug='strasbourg', name='Strasbourg', reg='Grand Est', hook="La Petite France, la cathédrale et les maisons à colombages.", lieux=["Petite France","parvis de la cathédrale","domaines d'Alsace"], lum="Les canaux de la Petite France sont très photogéniques tôt le matin, sans foule.", plan="En hiver, les marchés de Noël animent la ville mais compliquent la circulation."),
 dict(slug='nantes', name='Nantes', reg='Pays de la Loire', hook="Château des ducs de Bretagne, Loire et île de Nantes.", lieux=["château des ducs de Bretagne","bords de Loire","manoirs et domaines des Pays de la Loire"], lum="Les bords de Loire offrent une belle lumière douce en fin de journée.", plan="Pour un mariage en domaine, comptez un temps de trajet entre la mairie et le lieu de réception."),
 dict(slug='biarritz', name='Biarritz', reg='Nouvelle-Aquitaine', hook="Côte basque, rocher de la Vierge et plages.", lieux=["rocher de la Vierge","Grande Plage","villas et domaines du Pays basque"], lum="Le coucher de soleil sur l'océan est le moment fort de la journée pour les portraits.", plan="Le vent et la marée changent le décor : nous vérifions les horaires de marée avec vous."),
 dict(slug='annecy', name='Annecy', reg='Auvergne-Rhône-Alpes', hook="Lac d'Annecy, vieille ville et montagnes.", lieux=["vieille ville et canaux","bords du lac","domaines de Haute-Savoie"], lum="Le lac et les montagnes offrent un décor spectaculaire à l'aube comme au crépuscule.", plan="Pour les lieux en hauteur, prévoyez le temps de trajet et la météo de montagne."),
 dict(slug='deauville', name='Deauville', reg='Normandie', hook="Planches, plages et manoirs normands.", lieux=["les Planches et la plage","manoirs et haras de Normandie","Honfleur et la côte"], lum="Les plages normandes sont lumineuses même par temps couvert, avec de belles nuances de gris et de bleu.", plan="Prévoyez des tenues adaptées au vent pour les photos de bord de mer."),
]
CULTURES = [
 dict(slug='mariage-marocain', name='Mariage marocain', adj='marocain',
  lead="Un mariage marocain se vit sur plusieurs temps et plusieurs tenues. Nous sommes là du henné à l'entrée des mariés, pour tout garder.",
  moments=[("La soirée du henné","Dessins de henné sur les mains, chants, famille réunie : des images pleines de couleurs et de tendresse."),("Les tenues et les caftans","La mariée change plusieurs fois de tenue. Nous photographions chaque look en détail et en portrait."),("La négafa et les préparatifs","Maquillage, bijoux, ceintures : nous suivons la préparation de la mariée avec discrétion."),("L'entrée des mariés","Youyous, musique, invités debout : nous restons au plus près de l'émotion."),("La soirée","Danses, plats traditionnels, gâteaux : la fête continue, nous aussi.")],
  tips=["Prévoyez un planning précis des changements de tenue pour que nous soyons prêts à chaque fois.","Indiquez-nous les personnes importantes à photographier (grands-parents, oncles, tantes).","Une journée marocaine est longue : une couverture étendue évite de rater des moments."]),
 dict(slug='mariage-tunisien', name='Mariage tunisien', adj='tunisien',
  lead="Henné, zaffa, tenues traditionnelles et soirée dansante : un mariage tunisien est une fête généreuse que nous racontons de bout en bout.",
  moments=[("La soirée du henné","Les mains décorées, les chants et les danses entre proches : une ambiance chaleureuse que nous photographions avec respect."),("La tenue traditionnelle","Jebba, kswa ou robe moderne : nous mettons en valeur chaque détail des tissus et des bijoux."),("La zaffa","La procession musicale d'entrée des mariés, pleine de rythme, de youyous et de joie."),("Les photos de famille","Un temps court et organisé pour les portraits des deux familles réunies."),("La soirée","Musique, danse, gâteaux : nous restons pour les moments forts jusqu'à tard.")],
  tips=["Précisez-nous l'ordre des temps forts (henné, zaffa, entrée) pour que nous soyons bien placés.","Si plusieurs lieux sont prévus, prévoyez les temps de trajet dans le planning.","Dites-nous les traditions de votre famille que vous tenez à voir sur vos photos."]),
 dict(slug='mariage-algerien', name='Mariage algérien', adj='algérien',
  lead="De la soirée du henné à la walima, les mariages algériens sont riches en traditions régionales. Nous les photographions avec soin et respect.",
  moments=[("La soirée du henné","Moment intime et festif qui réunit les femmes de la famille autour de la mariée."),("Les tenues traditionnelles","Chedda tlemcenienne, karakou, gandoura constantinoise ou robe de mariée : nous photographions chaque tenue en détail."),("L'entrée des mariés","Zorna, youyous et applaudissements : un moment à ne pas manquer."),("Les photos de famille","Un temps court pour réunir les deux familles et les amis proches."),("La walima et la soirée","Repas, danses et surprises : nous suivons la fête jusqu'à l'heure convenue.")],
  tips=["Précisez la région de votre famille pour que nous repérions les tenues et les traditions à photographier.","Prévoyez un temps dédié pour les portraits de la mariée avec ses bijoux.","Une couverture longue est recommandée pour suivre les différents temps de la journée."]),
]
HERO_SLUGS = ['paris','versailles','fontainebleau']

def href(depth, path):
    """path: '' | 'palaces/' | 'palaces/ritz-paris/' ; renvoie un lien relatif."""
    p = '../'*depth + path
    if ART and (path=='' or path.endswith('/')): p += 'index.html'
    if p=='' : p = './'
    return p

def asset(depth, f): return '../'*depth + f

def head(title, desc, path, depth, ld=None, home_fragment=False):
    canon = DOMAIN + '/' + path
    h = '<title>%s</title>\n<meta name="description" content="%s">\n<meta name="robots" content="index,follow,max-image-preview:large">\n<meta name="theme-color" content="#0d0c0b">\n<link rel="canonical" href="%s">\n' % (esc(title), esc(desc,True), canon)
    h += '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:url" content="%s">\n' % (esc(title,True), esc(desc,True), canon)
    h += '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Hanken+Grotesk:wght@300;400;500;700&display=swap">\n'
    h += '<link rel="stylesheet" href="%s">\n' % asset(depth,'style.css')
    for o in (ld or []): h += '<script type="application/ld+json">%s</script>\n' % json.dumps(o, ensure_ascii=False)
    return h

def breadcrumb_ld(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":DOMAIN+'/'+p} for i,(n,p) in enumerate(items)]}
def faq_ld(faqs):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
BIZ = {"@context":"https://schema.org","@type":["Photographer","LocalBusiness"],"name":NAME,"url":DOMAIN+"/","sameAs":[IG],"description":"Photographes de mariage à Paris, en Île-de-France et partout en France.","areaServed":[{"@type":"Country","name":"France"},{"@type":"AdministrativeArea","name":"Île-de-France"}]}

def header(depth):
    L = lambda a,t,c='': '<a href="%s"%s>%s</a>' % (a, (' class="%s"'%c if c else ''), t)
    nav = ''.join([L(href(depth,'services/'),'Prestations'),L(href(depth,'zones/'),'Zones'),L(href(depth,'palaces/'),'Palaces'),L(href(depth,'cultures/'),'Cultures'),L(href(depth,'contact/'),'Devis','cta')])
    menu = ''.join([L(href(depth,'services/'),'Prestations'),L(href(depth,'zones/'),'Zones'),L(href(depth,'palaces/'),'Palaces'),L(href(depth,'villes/'),'Villes'),L(href(depth,'cultures/'),'Cultures'),L(href(depth,'contact/'),'Devis')])
    return ('<div class="cur" id="cur"></div>\n<header class="nav"><a href="%s" class="logo" data-cursor>Le Couple Photographe</a><nav aria-label="Navigation principale">%s</nav><button class="burger" id="burger" aria-expanded="false">Menu</button></header>\n<div class="menu" id="menu">%s</div>\n') % (href(depth,''), nav, menu)

def footer(depth):
    def ul(items): return '<ul>'+''.join('<li><a href="%s">%s</a></li>'%(href(depth,p),n) for n,p in items)+'</ul>'
    from data_services import SERVICES as _S
    from data_places import PLACES as _P
    pal = ul([(x['name'],'services/%s/'%x['slug']) for x in _S]+[('Toutes les prestations','services/')])
    vil = ul([(x['name'],'zones/%s/'%x['slug']) for x in _P if x['slug'] in ('paris-4e','paris-7e','paris-8e','paris-16e','paris-18e','versailles','boulogne-billancourt','neuilly-sur-seine','vincennes','saint-germain-en-laye','fontainebleau')]+[('Toutes les zones','zones/')])
    cul = ul([(x['name'],'palaces/%s/'%x['slug']) for x in PALACES[:4]]+[('Palaces parisiens','palaces/'),('Villes de France','villes/')]+[(c['name'],'cultures/%s/'%c['slug']) for c in CULTURES]+[('Devis gratuit','contact/')])
    return ('<footer class="ft"><div><a href="%s" class="logo">Le Couple Photographe</a><p>Photographes de mariage à Paris, en Île-de-France et partout en France.</p><p style="margin-top:14px"><a href="%s" target="_blank" rel="noopener">Instagram @le_couple_photographe</a></p></div><div><h4>Prestations</h4>%s</div><div><h4>Paris &amp; Île-de-France</h4>%s</div><div><h4>Lieux &amp; cultures</h4>%s</div></footer>\n<div class="big" aria-hidden="true">Le Couple</div>\n<p style="padding:0 var(--g) 30px;color:var(--mute);font-size:13px">© <span id="yr"></span> Le Couple Photographe · Photographe de mariage Paris &amp; Île-de-France</p>\n<a class="stick" href="%s" data-cursor>Demander un devis</a>\n<script src="%s"></script>\n<script src="%s"></script>') % (href(depth,''), IG, pal, vil, cul, href(depth,'contact/'), asset(depth,'photos.js'), asset(depth,'app.js'))

def img(i, alt, cls=''):
    return '<img data-ph="%d" alt="%s" loading="lazy"%s>' % (i, esc(alt,True), (' class="%s"'%cls if cls else ''))

def faq_html(faqs):
    return '<section class="sec faq" aria-labelledby="faqt"><div class="sec-h"><div class="eyebrow">Questions fréquentes</div><h2 id="faqt">Avant de <em>nous écrire</em></h2></div>' + ''.join('<details><summary>%s</summary><p>%s</p></details>'%(esc(q),esc(a)) for q,a in faqs) + '</section>'

def cta(depth, title='Parlons de <em>votre mariage</em>'):
    return '<section class="cta-band"><div class="eyebrow" style="color:#6b645b;margin-bottom:20px">Devis personnalisé</div><h2>%s</h2><a class="btn" href="%s" data-cursor>Demander un devis</a></section>' % (title, href(depth,'contact/'))

def links_block(depth, title, items):
    return '<section class="rel"><div class="sec-h"><div class="eyebrow">À découvrir aussi</div><h2 style="font:400 clamp(30px,4vw,56px)/1 var(--serif)">%s</h2></div><div class="links">%s</div></section>' % (title, ''.join('<a href="%s">%s</a>'%(href(depth,p),n) for n,p in items))

def strip(seed, alt):
    return '<div class="strip">' + ''.join('<div class="im">%s</div>'%img(seed+i, alt) for i in range(4)) + '</div>'

def page(path, depth, title, desc, ld, body, home=False):
    out = os.path.join(OUT, path, 'index.html') if path else os.path.join(OUT,'index.html')
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    h = head(title, desc, path, depth, ld)
    if ART and not path:   # le fichier d'entrée d'un artifact est enveloppé par la plateforme : fragment sans <html>
        doc = h + body
    else:
        doc = '<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n' + h + '</head>\n<body>\n' + body + '\n</body>\n</html>\n'
    open(out,'w',encoding='utf-8').write(doc)

def hero(depth, crumbs, h1, lead, seed, alt):
    c = ' <span>/</span> '.join('<a href="%s">%s</a>'%(href(depth,p),n) if p is not None else '<span>%s</span>'%n for n,p in crumbs)
    return '<main><section class="ph"><nav class="crumb" aria-label="Fil d\'Ariane">%s</nav><h1>%s</h1><p class="lead">%s</p><div class="acts"><a class="btn" href="%s" data-cursor>Demander un devis</a><a class="btn alt" href="#details" data-cursor>En savoir plus</a></div></section><div class="hero-img">%s</div>' % (c, h1, lead, href(depth,'contact/'), img(seed, alt))

# ---------- pages palaces ----------
def faq_palace(p):
    return [("Êtes-vous photographe de mariage au %s ?"%p['name'], "Nous photographions des mariages dans les palaces parisiens. Pour une réception au %s (%s), contactez-nous avec votre date : nous indiquons nos disponibilités et préparons le planning avec votre wedding planner."%(p['name'],p['addr'])),
            ("Comment organiser les photos au %s ?"%p['name'], p['orga']),
            ("Quelle lumière attendre au %s ?"%p['name'], p['lumiere']),
            ("Faut-il une autorisation pour photographier au %s ?"%p['name'], "Les conditions dépendent de l'établissement et de l'événement : confirmez-les auprès de l'hôtel ou de votre organisateur. Nous nous adaptons à ce qui est permis.")]
def palace_pages():
    for p in PALACES:
        path='palaces/%s/'%p['slug']; d=2
        t='Photographe mariage %s | Le Couple Photographe'%p['name']
        desc='Photographe de mariage au %s, %s. Reportage complet, portraits et lumière naturelle. Demandez votre devis.'%(p['name'],p['area'])
        faqs=faq_palace(p)
        ld=[BIZ,breadcrumb_ld([('Accueil',''),('Palaces parisiens','palaces/'),(p['name'],path)]),faq_ld(faqs),{"@context":"https://schema.org","@type":"Service","serviceType":"Photographe de mariage","name":"Photographe mariage %s"%p['name'],"provider":{"@type":"Photographer","name":NAME},"areaServed":"Paris"}]
        others=[(o['name'],'palaces/%s/'%o['slug']) for o in PALACES if o['slug']!=p['slug']][:6]
        body = header(d)+hero(d,[('Accueil',''),('Palaces',"palaces/"),(p['name'],None)],'Photographe de mariage au <em>%s</em>'%esc(p['name']),esc(p['hook']),20+PALACES.index(p)%5,'Mariage au %s à Paris'%p['name'])
        body += '<section class="facts" id="details"><div><small>Adresse</small><b>%s</b></div><div><small>Quartier</small><b>%s</b></div><div><small>Prestation</small><b>Reportage de mariage</b></div><div><small>Livraison</small><b>Galerie privée en ligne</b></div></section>'%(esc(p['addr']),esc(p['area']))
        body += '<section class="cols"><div><div class="eyebrow">Le lieu</div><h2 style="margin-top:18px">Se marier au <em>%s</em></h2></div><div class="prose"><p>%s</p><h3>La lumière</h3><p>%s</p><h3>L\'organisation de la journée</h3><p>%s</p></div></section>'%(esc(p['name']),esc(p['lieu']),esc(p['lumiere']),esc(p['orga']))
        body += strip(30+PALACES.index(p)*4,'Photographe mariage %s'%p['name'])
        body += faq_html(faqs)+cta(d)+links_block(d,'Autres palaces parisiens',others+[('Photographe mariage Paris','villes/paris/'),('Tous les palaces','palaces/')])+footer(d)
        page(path,d,t,desc,ld,body)
def hub_palaces():
    d=1; path='palaces/'
    ld=[BIZ,breadcrumb_ld([('Accueil',''),('Palaces parisiens',path)])]
    tiles=''.join('<a class="tile rv" href="%s" data-cursor><div class="im">%s</div><h3>%s</h3><span>%s</span></a>'%(href(d,'palaces/%s/'%p['slug']),img(40+i,'Mariage au %s'%p['name']),esc(p['name']),esc(p['area'])) for i,p in enumerate(PALACES))
    body=header(d)+hero(d,[('Accueil',''),('Palaces parisiens',None)],'Photographe de mariage dans les <em>palaces parisiens</em>','Ritz, Bristol, Plaza Athénée, Meurice, Crillon : retrouvez nos pages dédiées aux plus beaux palaces de Paris pour votre mariage.',50,'Mariage dans un palace parisien')+'<section class="sec" id="details"><div class="tiles">%s</div></section>'%tiles
    body+=cta(d)+footer(d)
    page(path,d,'Photographe mariage palace Paris | Le Couple Photographe','Photographe de mariage dans les palaces parisiens : Ritz, Bristol, Plaza Athénée, Meurice, Crillon, Shangri-La. Découvrez nos pages par lieu.',ld,body)

# ---------- villes ----------
def city_pages():
    for c in CITIES:
        path='villes/%s/'%c['slug']; d=2; i=CITIES.index(c)
        faqs=[("Êtes-vous photographe de mariage à %s ?"%c['name'],"Oui. Nous photographions des mariages à %s (%s) et nous nous déplaçons partout en France. Écrivez-nous avec votre date et votre lieu pour connaître nos disponibilités."%(c['name'],c['reg'])),
              ("Comment préparer un mariage à %s ?"%c['name'],c['plan']+" Des frais de déplacement peuvent s'ajouter selon la distance depuis Paris, détaillés dans votre devis."),
              ("Quels sont les meilleurs lieux pour les photos à %s ?"%c['name'],"Parmi nos suggestions : %s. Nous choisissons avec vous selon votre style et la météo."%', '.join(c['lieux'])),
              ("Quelle lumière attendre à %s ?"%c['name'],c['lum'])]
        ld=[BIZ,breadcrumb_ld([('Accueil',''),('Villes',"villes/"),(c['name'],path)]),faq_ld(faqs),{"@context":"https://schema.org","@type":"Service","serviceType":"Photographe de mariage","name":"Photographe mariage %s"%c['name'],"provider":{"@type":"Photographer","name":NAME},"areaServed":{"@type":"City","name":c['name']}}]
        others=[('Photographe mariage '+o['name'],'villes/%s/'%o['slug']) for o in CITIES if o['slug']!=c['slug']][:8]
        body=header(d)+hero(d,[('Accueil',''),('Villes','villes/'),(c['name'],None)],'Photographe de mariage à <em>%s</em>'%esc(c['name']),esc(c['hook'])+' Reportage complet de votre mariage.',60+i%6,'Mariage à %s'%c['name'])
        body+='<section class="facts" id="details"><div><small>Ville</small><b>%s</b></div><div><small>Région</small><b>%s</b></div><div><small>Déplacement</small><b>Partout en France</b></div><div><small>Livraison</small><b>Galerie privée en ligne</b></div></section>'%(esc(c['name']),esc(c['reg']))
        body+='<section class="cols"><div><div class="eyebrow">Mariage à %s</div><h2 style="margin-top:18px">Votre mariage <em>à %s</em></h2></div><div class="prose"><p>%s Nous vous accompagnons de la préparation à la soirée, avec un reportage naturel et des portraits soignés.</p><h3>Où photographier à %s</h3><p>Parmi nos suggestions : %s.</p><h3>La lumière</h3><p>%s</p><h3>À prévoir</h3><p>%s</p></div></section>'%(esc(c['name']),esc(c['name']),esc(c['hook']),esc(c['name']),esc(', '.join(c['lieux'])),esc(c['lum']),esc(c['plan']))
        body+=strip(70+i*4,'Photographe de mariage %s'%c['name'])+faq_html(faqs)+cta(d)+links_block(d,'Autres villes',others+[('Toutes les villes','villes/')])+footer(d)
        page(path,d,'Photographe mariage %s | Le Couple Photographe'%c['name'],'Photographe de mariage à %s (%s). Reportage naturel, portraits soignés, déplacement possible. Demandez votre devis.'%(c['name'],c['reg']),ld,body)
def hub_villes():
    d=1;path='villes/'
    tiles=''.join('<a class="tile rv" href="%s" data-cursor><div class="im">%s</div><h3>%s</h3><span>%s</span></a>'%(href(d,'villes/%s/'%c['slug']),img(90+i,'Mariage à %s'%c['name']),esc(c['name']),esc(c['reg'])) for i,c in enumerate(CITIES))
    body=header(d)+hero(d,[('Accueil',''),('Villes',None)],'Photographe de mariage <em>dans toute la France</em>','Paris, Versailles, Lyon, Bordeaux, Nice, Strasbourg : nous nous déplaçons là où vous vous mariez.',100,'Mariage en France')+'<section class="sec" id="details"><div class="tiles">%s</div></section>'%tiles+cta(d)+footer(d)
    page(path,d,'Photographe mariage en France | Le Couple Photographe','Photographe de mariage à Paris, Lyon, Bordeaux, Marseille, Nice, Lille, Strasbourg et partout en France. Découvrez nos pages par ville.',[BIZ,breadcrumb_ld([('Accueil',''),('Villes',path)])],body)

# ---------- cultures ----------
def culture_pages():
    for c in CULTURES:
        path='cultures/%s/'%c['slug']; d=2; i=CULTURES.index(c)
        faqs=[("Photographiez-vous les mariages %ss ?"%c['adj'],"Oui. Nous photographions des mariages %ss en Île-de-France et partout en France, de la soirée du henné à la soirée dansante."%c['adj']),
              ("Combien de temps dure la couverture d'un mariage %s ?"%c['adj'],"Une journée de mariage %s est longue et comporte plusieurs temps forts. Nous proposons une couverture adaptée, étendue sur plusieurs temps si vous le souhaitez, détaillée dans votre devis."%c['adj']),
              ("Pouvez-vous photographier la soirée du henné ?","Oui, c'est un moment important que nous photographions volontiers, avec discrétion et respect de l'intimité de chacun."),
              ("Comment préparer notre mariage %s avec vous ?"%c['adj'],"Dites-nous les temps forts, les tenues et les personnes à ne pas oublier. Nous en tenons compte dans un planning que nous construisons avec vous.")]
        ld=[BIZ,breadcrumb_ld([('Accueil',''),('Cultures','cultures/'),(c['name'],path)]),faq_ld(faqs),{"@context":"https://schema.org","@type":"Service","serviceType":"Photographe de mariage","name":"Photographe "+c['name'].lower(),"provider":{"@type":"Photographer","name":NAME},"areaServed":"Île-de-France"}]
        body=header(d)+hero(d,[('Accueil',''),('Cultures','cultures/'),(c['name'],None)],'Photographe %s <em>à Paris et en Île-de-France</em>'%c['name'].lower(),esc(c['lead']),110+i,c['name'])
        body+='<section class="cols" id="details"><div><div class="eyebrow">Les temps forts</div><h2 style="margin-top:18px">Chaque tradition, <em>chaque détail</em></h2></div><div class="moments">%s</div></section>'%''.join('<div class="rv"><h3>%s</h3><p>%s</p></div>'%(esc(a),esc(b)) for a,b in c['moments'])
        body+='<section class="cols"><div><div class="eyebrow">Conseils</div><h2 style="margin-top:18px">Bien <em>préparer</em></h2></div><div class="prose">%s<p>Nous intervenons à Paris, dans toute l\'Île-de-France et dans toute la France.</p></div></section>'%''.join('<p>%s</p>'%esc(t) for t in c['tips'])
        body+=strip(120+i*4,c['name'])+faq_html(faqs)+cta(d)+links_block(d,'À découvrir aussi',[(o['name'],'cultures/%s/'%o['slug']) for o in CULTURES if o['slug']!=c['slug']]+[('Photographe mariage Paris','villes/paris/'),('Palaces parisiens','palaces/')])+footer(d)
        page(path,d,'Photographe %s Paris | Le Couple Photographe'%c['name'].lower(),'Photographe de %s à Paris et en Île-de-France : henné, tenues traditionnelles, entrée des mariés, soirée. Demandez votre devis.'%c['name'].lower(),ld,body)
def hub_cultures():
    d=1;path='cultures/'
    tiles=''.join('<a class="tile rv" href="%s" data-cursor><div class="im">%s</div><h3>%s</h3><span>Paris &amp; Île-de-France</span></a>'%(href(d,'cultures/%s/'%c['slug']),img(130+i,c['name']),esc(c['name'])) for i,c in enumerate(CULTURES))
    body=header(d)+hero(d,[('Accueil',''),('Cultures',None)],'Photographe de mariage <em>marocain, tunisien, algérien</em>','Henné, tenues traditionnelles, zaffa, youyous : nous photographions les mariages maghrébins avec soin et respect.',135,'Mariage maghrébin')+'<section class="sec" id="details"><div class="tiles">%s</div></section>'%tiles+cta(d)+footer(d)
    page(path,d,'Photographe mariage marocain, tunisien, algérien | Le Couple Photographe','Photographe de mariage marocain, tunisien et algérien à Paris et en Île-de-France. Henné, tenues, soirée. Demandez votre devis.',[BIZ,breadcrumb_ld([('Accueil',''),('Cultures',path)])],body)

# ---------- contact ----------
def contact():
    d=1;path='contact/'
    form='''<section class="sec ct" id="contact"><div class="ct-g"><div class="side"><div class="eyebrow">Contact</div><h2 style="margin-top:24px">Parlons de <em>votre histoire</em></h2><p>Dites-nous où et quand vous vous mariez. Nous revenons vers vous avec disponibilités et tarifs.</p><a class="ig" href="%s" target="_blank" rel="noopener" data-cursor>@le_couple_photographe ↗</a></div>
<form id="form" novalidate><div class="r2"><div class="fld"><label for="nom">Vos prénoms</label><input id="nom" autocomplete="name" required></div><div class="fld"><label for="mail">Email</label><input id="mail" type="email" autocomplete="email" required></div></div>
<div class="r2"><div class="fld"><label for="date">Date</label><input id="date" type="date"></div><div class="fld"><label for="zone">Lieu</label><select id="zone"><option>Paris (75)</option><option>Seine-et-Marne (77)</option><option>Yvelines (78)</option><option>Essonne (91)</option><option>Hauts-de-Seine (92)</option><option>Seine-Saint-Denis (93)</option><option>Val-de-Marne (94)</option><option>Val-d'Oise (95)</option><option>Autre ville de France</option><option>Étranger</option></select></div></div>
<div class="fld"><label for="type">Projet</label><select id="type"><option>Reportage de mariage</option><option>Mariage marocain</option><option>Mariage tunisien</option><option>Mariage algérien</option><option>Séance couple avant mariage</option><option>Fiançailles / demande</option></select></div>
<div class="fld"><label for="msg">Votre message</label><textarea id="msg"></textarea></div><button class="btn" type="submit" data-cursor>Préparer mon message</button><p class="note" id="note" role="status"></p></form></div></section>'''%IG
    body=header(d)+'<main><section class="ph"><nav class="crumb"><a href="%s">Accueil</a> <span>/</span> <span>Contact</span></nav><h1>Demander <em>un devis</em></h1></section>'%href(d,'')+form+'</main>'+footer(d).replace('<a class="stick"','<a hidden class="stick"')
    page(path,d,'Devis photographe mariage | Le Couple Photographe','Demandez votre devis de photographe de mariage à Paris, en Île-de-France et partout en France.',[BIZ,breadcrumb_ld([('Accueil',''),('Contact',path)])],body)

# ---------- accueil ----------
def home():
    d=0
    b=open('src/home-body.html',encoding='utf-8').read()
    # retire script inline et ancien header/menu/footer, garde le contenu
    b=b[:b.index('<script>')]
    b=re.sub(r'<header class="nav">.*?</header>\n<div class="menu".*?</div>\n','',b,flags=re.S)
    b=re.sub(r'<div class="cur" id="cur"></div>\n','',b)
    b=re.sub(r'<div class="big".*',  '',b,flags=re.S)
    main=b[b.index('<div class="pre"'):]
    # sections de maillage interne
    palaces='<section class="sec" aria-labelledby="pl"><div class="sec-h"><div class="eyebrow">Lieux de prestige</div><h2 id="pl">Mariage dans un <em>palace parisien</em></h2></div><div class="tiles">%s</div><p style="margin-top:34px"><a class="btn alt" href="%s" data-cursor>Tous les palaces</a></p></section>'%(''.join('<a class="tile rv" href="%s" data-cursor><div class="im">%s</div><h3>%s</h3><span>%s</span></a>'%(href(d,'palaces/%s/'%p['slug']),img(40+i,'Mariage au '+p['name']),esc(p['name']),esc(p['area'])) for i,p in enumerate(PALACES[:4])),href(d,'palaces/'))
    cult='<section class="sec" aria-labelledby="cu"><div class="sec-h"><div class="eyebrow">Traditions</div><h2 id="cu">Mariage <em>marocain, tunisien, algérien</em></h2></div><div class="tiles">%s</div></section>'%''.join('<a class="tile rv" href="%s" data-cursor><div class="im">%s</div><h3>%s</h3><span>Paris &amp; Île-de-France</span></a>'%(href(d,'cultures/%s/'%c['slug']),img(130+i,c['name']),esc(c['name'])) for i,c in enumerate(CULTURES))
    vil='<section class="sec" aria-labelledby="vi"><div class="sec-h"><div class="eyebrow">Partout en France</div><h2 id="vi">Photographe de mariage <em>dans votre ville</em></h2></div><div class="links">%s</div></section>'%''.join('<a href="%s">%s</a>'%(href(d,'villes/%s/'%c['slug']),esc(c['name'])) for c in CITIES)
    from data_services import SERVICES as _S
    from data_places import PLACES as _P
    sv='<section class="sec" aria-labelledby="sv"><div class="sec-h"><div class="eyebrow">Prestations</div><h2 id="sv">Photographe et vidéaste <em>pour chaque moment</em></h2></div><div class="tiles">%s</div></section>'%''.join('<a class="tile rv" href="%s" data-cursor><div class="im">%s</div><h3>%s</h3><span>Photo &amp; vidéo</span></a>'%(href(d,'services/%s/'%x['slug']),img(150+i,x['nom']),esc(x['name'])) for i,x in enumerate(_S))
    zn='<section class="sec" aria-labelledby="zn"><div class="sec-h"><div class="eyebrow">Paris &amp; Île-de-France</div><h2 id="zn">Votre photographe <em>dans votre ville</em></h2></div><div class="links">%s<a href="%s">Toutes les zones →</a></div></section>'%(''.join('<a href="%s">%s</a>'%(href(d,'zones/%s/'%x['slug']),esc(x['name'])) for x in _P),href(d,'zones/'))
    main=main.replace('<section class="sec" id="prestations"',sv+palaces+cult+vil+zn+'<section class="sec" id="prestations"')
    main=main.replace('href="#contact"','href="%s"'%href(d,'contact/'))
    main=re.sub(r'<footer>.*?</footer>','',main,flags=re.S)
    # les sections main
    ld=[BIZ,faq_ld([("Intervenez-vous dans toute l'Île-de-France ?","Oui. Nous photographions les mariages à Paris et dans les huit départements d'Île-de-France : 75, 77, 78, 91, 92, 93, 94 et 95. Nous nous déplaçons aussi dans toute la France."),("Combien de temps à l'avance faut-il réserver ?","Dès que votre date et votre lieu sont fixés, idéalement 9 à 12 mois avant le mariage."),("Quand recevrons-nous nos photos ?","Un aperçu arrive rapidement après le grand jour. La galerie complète est livrée dans une galerie privée en ligne dont le délai est précisé dans votre devis."),("Photographiez-vous les mariages marocains, tunisiens et algériens ?","Oui. Nous avons des pages dédiées et nous couvrons la soirée du henné comme le jour J.")])]
    body=header(d)+main+footer(d)
    page('',d,'Photographe mariage Paris et Île-de-France | Le Couple Photographe','Photographe de mariage à Paris, en Île-de-France et partout en France. Palaces parisiens, mariages marocains, tunisiens et algériens. Demandez votre devis.',ld,body)

# ---------- fichiers techniques ----------
def tech(urls):
    if ART: return
    open('robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n'%DOMAIN)
    x='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>%s/%s</loc><priority>%s</priority></url>\n'%(DOMAIN,u,'1.0' if u=='' else '0.8') for u in urls)+'</urlset>\n'
    open('sitemap.xml','w').write(x)

if __name__=='__main__':
    for f in ('style.css','app.js','photos.js'):
        src = 'style.base.css' if f=='style.css' else f
        if ART: shutil.copy(src, os.path.join(OUT,f)) if os.path.isdir(OUT) else (os.makedirs(OUT,exist_ok=True), shutil.copy(src, os.path.join(OUT,f)))
        elif f=='style.css': shutil.copy(src,f)
    os.makedirs(OUT,exist_ok=True)
    home(); hub_palaces(); palace_pages(); hub_villes(); city_pages(); hub_cultures(); culture_pages(); contact()
    urls=['','palaces/','villes/','cultures/','contact/']+['palaces/%s/'%p['slug'] for p in PALACES]+['villes/%s/'%c['slug'] for c in CITIES]+['cultures/%s/'%c['slug'] for c in CULTURES]
    import build_idf; urls+=build_idf.run()
    tech(urls); print(len(urls),'pages')
