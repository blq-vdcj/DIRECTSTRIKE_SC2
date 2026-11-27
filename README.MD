# Direct Strike Bank Unlocker (StarCraft II)

Outil Python en ligne de commande permettant d'éditer et de re-signer proprement les sauvegardes locales (`.SC2Bank`) de la carte Arcade **Direct Strike** sur StarCraft II : définition du niveau de maîtrise (de `1` à `2 400`) et activation optionnelle de l'upgrade `PremiumReward` en partie.

> **Avertissement** — Projet publié à des fins éducatives et de rétro-ingénierie des formats `.SC2Bank` et Galaxy Script. Utilisez cet outil à vos risques et périls ; une copie de sauvegarde (`.SC2Bank.bak`) est automatiquement créée avant toute modification.

---

## Fonctionnalités

* **Détection automatique multi-comptes et multi-régions** : scanne automatiquement `Documents` et `OneDrive` pour détecter les profils Battle.net (EU, US, KR) ainsi que les identifiants auteur/joueur requis pour la signature.
* **Définition précise du niveau (`1` à `2 400`)** : calcule l'XP exact correspondant au niveau souhaité selon la courbe officielle du jeu (jusqu'au plafond de `953 210 000` XP au niveau `2 400`) tout en conservant intacts vos compteurs existants (parties, victoires, kills, pertes).
* **Recalcul complet des signatures** : régénère à la volée le code de maîtrise (`1VC1C5S8E4C3KL65`) et la balise native `<Signature>` (SHA-1) de StarCraft II.
* **Activation optionnelle de `PremiumReward`** : injecte une section valide dans `Starlight.SC2Bank` pour activer les avantages locaux liés à `PremiumReward` (+30 points de maîtrise, personnalisation de la zone de préparation, récompenses associées).
* **Zéro dépendance externe** : fonctionne uniquement avec la bibliothèque standard de Python 3.

---

## Portée et limites

| Contenu | Pris en charge | Explication |
| :--- | :---: | :--- |
| Niveau de maîtrise (`1` à `2 400`), badges, étoiles et points de maîtrise | **Oui** | Stocké localement dans `llIIIllllllIIIll.SC2Bank`. |
| Statut `PremiumReward` en partie (+30 points, personnalisation de zone, ouvriers/décorations liés) | **Oui** | Déclenché via la section `IIlIlIlIIIlllllI` de `Starlight.SC2Bank`. |
| Modes / lobbies payants (Commanders premium, bonus timer AFK) | **Non** | Vérifié côté Battle.net via la licence (`PlayerHasLicense`). |
| Skins Vespene et packs abonnés (Patreon) | **Non** | Contrôlé par des listes blanches d'identifiants codées en dur dans les archives `.s2ma`. |

---

## Prérequis

* **Python 3.10+** installé sur votre machine.
* Avoir déjà lancé **au moins une partie normale** (hors mode Sandbox) sur Direct Strike afin que les fichiers `.SC2Bank` existent dans votre dossier StarCraft II.
* **Fermer complètement StarCraft II** avant toute exécution du script.

---

## Utilisation

1. Téléchargez `direct_strike_unlocker.py` (ou clonez le dépôt) :
   ```bash
   git clone [https://github.com/](https://github.com/)<votre-utilisateur>/<votre-repo>.git
   cd <votre-repo>
