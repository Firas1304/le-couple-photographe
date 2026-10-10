# Règles de rédaction : contenu unique par page « prestation × lieu »

Objectif : pour UN lieu (arrondissement ou commune), écrire 12 textes locaux, un par prestation. Chaque texte sera inséré dans une page
« Photographe et vidéaste [prestation] à [lieu] ». Google déclasse les pages quasi identiques : chaque texte doit donc être réellement différent
des 11 autres du même fichier, et différent de ce que ferait un autre lieu.

## Sources autorisées
- Le lieu : ligne commençant par `<slug>|` dans `data_places.py` (nom, intro, ambiance, lumière, accès, spots avec description).
- Les prestations : `data_services.py` (slug, nom, lead, conseils, saison, faq).
- Rien d'autre comme faits. Interdit d'inventer : noms de salles/hôtels/restaurants non listés, dates, chiffres, horaires, prix, règlements précis,
  anecdotes historiques non fournies. Les noms de spots viennent UNIQUEMENT de la ligne du lieu. Tu peux utiliser des connaissances très générales et sûres
  (la Seine existe, le soleil se couche à l'ouest) mais pas de détails invérifiables.
- Ne jamais dire que l'équipe a déjà photographié à cet endroit. Écrire « nous aimons », « nous vous proposons », « nous pouvons ».

## Format de sortie : `content/<slug>.json`
```json
{
 "mariage": {"scene": "...", "conseil": "...", "faq": [{"q": "...", "a": "..."}, {"q": "...", "a": "..."}]},
 "grossesse": {...}, "couple": {...}, "famille": {...}, "gender-reveal": {...}, "professionnels": {...},
 "evenements-professionnels": {...}, "solo": {...}, "anniversaire": {...}, "diplome": {...}, "naissance": {...}, "nouveau-ne": {...}
}
```
- `scene` : 55 à 100 mots. Décrit des idées de prises de vue CONCRÈTES propres à la prestation, en citant 2 ou 3 spots du lieu par leur nom exact,
  et en reliant chaque spot à un moment ou un geste de la prestation. Mentionner « photographe et vidéaste » une seule fois dans le fichier entier
  par entrée au plus ; varier la façon de parler de la vidéo (film, séquence, images en mouvement, teaser...).
- `conseil` : 25 à 60 mots. Un conseil pratique ancré dans ce lieu (lumière, accès, affluence, météo) et adapté à la prestation.
- `faq` : exactement 2 questions/réponses (réponses de 25 à 60 mots), propres au couple prestation+lieu, qu'un client taperait vraiment dans Google
  (ex. « Où faire un shooting grossesse à Sceaux ? », « Peut-on filmer la cérémonie à ... ? »). Les deux questions doivent différer d'une prestation à l'autre.

## Variété obligatoire
- Chaque `scene` commence différemment (pas deux entrées avec les 3 mêmes premiers mots). Alterner phrase courte/longue, questions, impératifs, constructions variées.
- Ne pas réutiliser une même formule d'une entrée à l'autre (« Pour une séance... nous aimons... » une seule fois maximum).
- Adapter le ton : gender reveal festif, naissance et nouveau-né doux et prudents (règles de la maternité, séance à domicile), professionnels et événements sobres,
  mariage et couple romantiques, anniversaire joyeux, diplôme fier.
- Pas de superlatifs creux (« meilleur », « incontournable », « magique »), pas de prix, pas de promesse de résultat, pas d'émojis, vouvoiement uniquement.
- Gender reveal : toujours rappeler de vérifier les règles du lieu pour confettis, fumigènes et ballons.
- Naissance : la prise de vue en maternité dépend de l'accord de l'établissement.

## Contrôle
Après écriture, lancer : `python3 check_content.py content/<slug>.json <slug>` et corriger jusqu'à ce qu'il affiche OK.
