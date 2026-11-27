# Direct Strike Bank Unlocker (StarCraft II)

Command-line Python tool for cleanly editing and re-signing local save files (`.SC2Bank`) for the **Direct Strike** Arcade map in StarCraft II: set your mastery level (from `1` to `2,400`) and optionally enable the `PremiumReward` upgrade in-game.

> **Disclaimer** — Project published for educational purposes and reverse-engineering of `.SC2Bank` and Galaxy Script formats. Use this tool at your own risk; a backup copy (`.SC2Bank.bak`) is automatically created before any modification.

---

## Features

- **Automatic multi-account and multi-region detection**: automatically scans `Documents` and `OneDrive` to detect Battle.net profiles (EU, US, KR) as well as the author/player IDs required for signing.
- **Precise level setting (`1` to `2,400`)**: calculates the exact XP corresponding to the desired level based on the game's official curve (up to the cap of `953,210,000` XP at level `2,400`) while keeping your existing counters intact (games, wins, kills, losses).
- **Full signature recalculation**: regenerates the mastery code (`1VC1C5S8E4C3KL65`) and StarCraft II's native `<Signature>` tag (SHA-1) on the fly.
- **Optional `PremiumReward` activation**: injects a valid section into `Starlight.SC2Bank` to enable local `PremiumReward` perks (+30 mastery points, staging area customization, associated rewards).
- **Zero external dependencies**: runs exclusively on the Python 3 standard library.

---

## Scope and Limitations

| Content | Supported | Explanation |
| :--- | :---: | :--- |
| Mastery level (`1` to `2,400`), badges, stars, and mastery points | **Yes** | Stored locally in `llIIIllllllIIIll.SC2Bank`. |
| In-game `PremiumReward` status (+30 points, staging area customization, associated workers/decorations) | **Yes** | Triggered via the `IIlIlIlIIIlllllI` section of `Starlight.SC2Bank`. |
| Paid modes / lobbies (premium Commanders, AFK timer bonus) | **No** | Verified server-side on Battle.net via license check (`PlayerHasLicense`). |
| Vespene skins and subscriber packs (Patreon) | **No** | Controlled by hardcoded ID whitelists inside the `.s2ma` archives. |

---

## Prerequisites

- **Python 3.10+** installed on your machine.
- Having already played **at least one normal match** (outside Sandbox mode) on Direct Strike so that the `.SC2Bank` files exist in your StarCraft II folder.
- **Completely close StarCraft II** before running the script.

---

## Usage

1. Download `direct_strike_unlocker.py` (or clone the repository):
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/<your-repo>.git
   cd <your-repo>
   ```
