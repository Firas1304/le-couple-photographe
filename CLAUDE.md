# Le Couple Photographe — site statique

Site vitrine d'un couple de photographes et vidéastes (Paris et Île-de-France). Instagram : @le_couple_photographe.
Priorité commerciale : le mariage (aussi marocain, tunisien, algérien). Style voulu : site « wow » façon Awwwards, rapide, très bon SEO local.

## Structure
- `build.py` : génère toutes les pages à la racine (accueil, palaces, villes, cultures, contact) puis appelle `build_idf.py`.
- `build_idf.py` : pages prestations (12), zones (66), prestation × zone (180, villes de `PRIORITY`).
- `data_services.py` : texte des 12 prestations (écrit à la main, doit rester unique).
- `data_places.py` : 66 lieux (20 arrondissements + communes IDF) avec spots réels. `PRIORITY` = villes qui ont des pages croisées.
- `src/home-body.html` : corps de la page d'accueil (inclut l'intro appareil photo + flash).
- `style.base.css` -> copié en `style.css` par le build. `app.js` : intro, curseur, galerie horizontale, formulaire.
- `check_unique.py` : mesure la ressemblance entre pages (viser : moyenne < 0,15, pire cas < 0,45).
- Régénérer : `python3 build.py`. Les `index.html` générés sont versionnés (déploiement direct sans build).

## Photos (à faire)
Toutes les images sont des visuels de remplacement générés (`data-ph="N"` dans les pages). Pour mettre les vraies photos :
1. Copier les photos compressées (~1600 px de large, JPEG ≤ 250 Ko) dans `photos/`. Source locale : disque « DD Bleu ».
2. Renseigner `window.PHOTOS = [...]` (chemins) dans un `photos.js` chargé avant `app.js`, l'index correspond à `data-ph`.
3. Ajouter un `alt` descriptif propre à chaque page (lieu, moment) pour le SEO.
Mariage en priorité : accueil (index 0-2), galerie (3-10), bandeau (9), journée de mariage (11-14).

## Points ouverts
- Nom de domaine réel : remplacer `DOMAIN` dans `build.py` (actuellement lecouplephotographe.fr, exemple).
- Vérifier les textes de lieux/palaces/cultures (écrits sans source externe).
- Pas de tarifs, avis ni adresse inventés : à fournir par le client.
- Le formulaire de contact ne peut pas envoyer : il copie le message. À brancher sur un service (Formspree, etc.).
- Les pages croisées prestation × ville sont limitées à 15 villes pour éviter le contenu dupliqué (risque Google).

## Règle de synchronisation (obligatoire)
Le propriétaire travaille en alternance sur le bureau (session locale, dossier sur le disque « DD Bleu ») et sur son téléphone (session cloud). GitHub est le point commun.
- Au début de chaque session : `git pull` sur la branche `claude/great-cray-w6pth2` pour récupérer le dernier travail.
- Après CHAQUE mise à jour : régénérer (`python3 build.py`), `git add -A`, `git commit` avec un message clair, puis `git push`. Ne jamais laisser du travail seulement en local.
- Ne pousser que des photos compressées (~250 Ko, 1600 px de large) ; les originaux restent sur le disque.
- Ne pas créer de pull request sans demande explicite.

## Déploiement
GitHub Pages via `.github/workflows/pages.yml` (build + déploiement à chaque push sur main ou sur la branche de travail). Réglage à faire une fois dans GitHub : Settings > Pages > Source = « GitHub Actions ». Pour un domaine perso : créer un fichier `CNAME` à la racine avec le domaine, régler `DOMAIN` dans `build.py`, puis configurer les DNS chez le registrar.

## Google Analytics / Search Console
`GA_ID` (G-XXXXXXXXXX) et `GSC_TOKEN` (jeton de la balise meta de vérification) sont à renseigner en haut de `build.py`, puis `python3 build.py`. Vides = rien n'est chargé. GA4 ne se charge qu'après consentement (bandeau cookies dans `app.js`). À faire une fois le domaine réel en ligne : ajouter la propriété Search Console (méthode « Préfixe d'URL » ou DNS), soumettre `sitemap.xml`.

## Contenu par lieu et prestation (état au 10/10/2026)
- 66 lieux (20 arrondissements de Paris + 46 communes IDF) × 12 prestations = 792 pages `services/<prestation>/<lieu>/`, chacune avec un texte écrit à la main dans `content/<lieu>.json` (champs `scene`, `conseil`, `faq` x2 par prestation).
- Règles de rédaction : `content/RULES.md` (faits locaux uniquement depuis `content/briefs/<lieu>.txt`, GEO inclus). Validateur : `python3 check_content.py content/<lieu>.json <lieu>`.
- Ajouter un lieu : l'ajouter dans `data_places.py`, régénérer les fiches (`content/briefs/`), faire écrire le JSON (un agent par lieu), valider, `python3 build.py`.
- Contrôle d'unicité : `python3 check_unique.py` (dernier relevé : pages prestation × lieu, ressemblance moyenne 0,07, pire 0,28).
- GEO : encadré « En bref » sur chaque page, JSON-LD enrichi, `llms.txt`, robots IA autorisés.
