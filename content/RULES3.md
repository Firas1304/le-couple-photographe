# Règles : accueil, prestations, cultures — version « réponse citable » pour les assistants IA

Objectif : que ChatGPT, Gemini, Perplexity, Claude citent ce site quand quelqu'un cherche « photographe et vidéaste [prestation] à Paris / en Île-de-France / en France ».
Les IA citent des passages courts, factuels, autonomes. Chaque bloc doit donc se comprendre SEUL, nommer l'entité (« Le Couple Photographe ») et le sujet, sans pronom ambigu.

## Faits autorisés
- Ta fiche `content/briefs3/<type>-<slug>.txt` (c'est le contenu actuel : améliore-le, ne le contredis pas).
- Connaissances très générales et sûres. INTERDIT : prix, tarifs, années d'expérience, nombre de mariages, avis, adresse, téléphone, partenaires, récompenses, dates, délais chiffrés précis,
  règlements. Si une information manque, ne pas l'inventer : renvoyer au devis personnalisé.
- Vouvoiement. Pas de superlatifs creux (« meilleur », « incontournable », « magique »), pas d'émojis.
- Ne jamais dire que l'équipe a « déjà photographié » un lieu précis.

## Format de sortie : `content/pages/<type>-<slug>.json`
```json
{
 "reponse": "55 à 85 mots. Définition/réponse directe : qui (Le Couple Photographe, duo de photographes et vidéastes), quoi (la prestation), où (Paris, Île-de-France, toute la France), comment (photo + vidéo, devis personnalisé). Une seule idée par phrase.",
 "intro": "2 paragraphes séparés par \n\n, 110 à 170 mots au total, ton chaleureux mais factuel.",
 "etapes": [{"titre": "...", "texte": "30 à 55 mots"}, ... exactement 4 ...],
 "faq": [{"q": "...", "a": "..."}, ... exactement 6 ...]
}
```
- `faq` : 6 vraies questions qu'un client taperait dans Google/ChatGPT ; réponses de 35 à 70 mots, autonomes (répéter le sujet et « Le Couple Photographe » au moins dans 3 réponses), pas de prix ni de chiffres inventés.
  Couvrir : combien de temps / comment ça se passe / quoi préparer / photo+vidéo / zones / réservation.
- Pour l'accueil (`home`) : `reponse` = présentation du duo ; `intro` = notre approche ; `etapes` = comment nous travaillons (échange, planification, jour J, livraison) ; `faq` = 6 questions générales (zones, prestations, mariages marocain/tunisien/algérien, photo+vidéo, comment réserver, livraison). Pas d'info inventée.
- Pour une culture (marocain/tunisien/algérien) : respect des traditions, ne pas affirmer de détails rituels non fournis dans la fiche ; `etapes` = les 4 grands temps de la journée tirés de la fiche.

## Variété
Chaque page doit avoir un angle propre ; évite les mêmes formules d'une prestation à l'autre.

## Contrôle
`python3 check_content3.py content/pages/<type>-<slug>.json` doit afficher OK.
