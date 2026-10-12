# Plan 3D Monky Niort

- `index.html` : la maquette, autonome (à publier telle quelle).
- `tarifs.json` : **la seule source des prix**. Modifier ce fichier puis lancer `python scripts/build.py` (ou laisser le workflow « Reconstruire et publier » le faire).
- `scripts/check_tarifs.py` : compare chaque prix de `tarifs.json` avec la page monky.fr indiquée dans `source`.

## Automatisation
1. **Chaque lundi**, le workflow *Vérification des tarifs* lit les pages monky.fr. S'il manque un prix, il ouvre (ou complète) l'issue « Tarifs à vérifier » avec le détail.
2. Dans l'issue, écrire `@claude mets à jour tarifs.json d'après ce rapport` (app Claude GitHub installée) — ou demander à Claude dans une session liée au dépôt. Claude ouvre une pull request.
3. À la fusion, *Reconstruire et publier* régénère `index.html` et le publie sur GitHub Pages.

Les URL `source` de chaque activité dans `tarifs.json` sont à vérifier une fois (le site Niort n'était pas encore complet au moment de la création).
