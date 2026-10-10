# Règles : pages « villes de France » et « palaces parisiens » (contenu unique et citable par les IA)

Objectif : une page de mariage vraiment unique par ville de France ou par palace parisien, pour Google ET pour les assistants IA
(ChatGPT, Gemini, Perplexity, Claude). Le site est celui d'un duo de photographes et vidéastes de mariage (Paris, Île-de-France, toute la France).
Pages dupliquées = déclassées : ton texte doit être sans équivalent dans les 25 autres pages (angle, structure, vocabulaire).

## Faits autorisés
- Ta fiche `content/briefs2/<type>-<slug>.txt` (adresse, accroche, lieux, lumière, organisation).
- Connaissances très générales et SÛRES : monuments, quartiers, places, parcs et sites naturels célèbres de la ville (ex. Lyon : Vieux-Lyon, colline de Fourvière,
  place Bellecour, quais du Rhône et de la Saône ; Bordeaux : place de la Bourse, miroir d'eau, Saint-Émilion). Pour un palace : son adresse, son quartier, ce qui est célèbre autour (place, avenue, jardin, vue), sans détail intérieur.
- INTERDIT : prix, dates, chiffres, capacités, horaires, règlements, noms de salles/restaurants/chefs/décorateurs, anecdotes ou récits historiques précis, détails intérieurs d'un hôtel,
  « photos autorisées/interdites » affirmées, partenariats, mention que l'équipe y a déjà travaillé. Dis « nous aimons », « nous vous proposons », « nous pouvons », « à confirmer auprès de l'hôtel/du lieu ».
- Pas de superlatifs creux (« meilleur », « incontournable », « magique », « exceptionnel »), pas d'émojis, vouvoiement.

## Format de sortie : `content/pages/<type>-<slug>.json`
```json
{
 "intro": "2 paragraphes séparés par \n\n, 90 à 150 mots au total. Premier paragraphe = réponse directe, autonome et citable (qui, quoi, où : « Pour un mariage à X, Le Couple Photographe ... »). Deuxième = angle propre à ce lieu.",
 "lieux": [{"nom": "Nom exact d'un lieu réel", "texte": "30 à 55 mots : ce que l'on y photographie/filme pour un mariage"}, ... 4 ou 5 lieux ...],
 "conseil": "40 à 70 mots : conseil pratique (lumière, trajets, météo, organisation de la journée) propre à ce lieu",
 "saison": "30 à 60 mots : quelle saison / quelle heure pour ce lieu et pourquoi",
 "faq": [{"q": "...", "a": "..."}, ... exactement 4 ...]
}
```
- FAQ : questions réalistes tapées dans Google/ChatGPT (« Combien de temps prévoir pour les photos de mariage à X ? », « Peut-on faire des photos de couple à Y avant le cocktail ? »…),
  réponses de 30 à 60 mots, autonomes (nom du lieu répété), sans prix.
- Palaces : `lieux` = 4 ou 5 points de prise de vue autour du palace (rue, place, jardin, avenue, vue) ou espaces génériques (« entrée », « jardin » seulement si la fiche le mentionne). Ne jamais inventer de salle.
- Villes : `lieux` = 4 ou 5 lieux célèbres réels de la ville ou des environs immédiats.

## Variété obligatoire
Ne commence pas deux phrases de la même façon ; évite les formules génériques valables pour n'importe quelle ville ; chaque page doit contenir au moins 3 détails visuels propres au lieu (matières, perspectives, eau, pierre, reliefs...).

## Contrôle
`python3 check_content2.py content/pages/<type>-<slug>.json` doit afficher OK.
