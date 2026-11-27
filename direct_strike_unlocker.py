import hashlib
import random
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

ALPHA = "jA42TfnHo8r1ap6YWziG73tsZB5mdyUC9PqRXkJKchvgQNMVxEewLbFDu"
DS_BANK_NAME = "llIIIllllllIIIll"
STARLIGHT_BANK_NAME = "Starlight"
PREMIUM_SECTION = "IIlIlIlIIIlllllI"

EARLY_XP = [
    2000, 3000, 5000, 10000, 15000, 20000, 30000, 40000, 55000, 70000,
    95000, 110000, 125000, 140000, 160000, 180000, 200000, 220000, 240000, 260000,
    280000, 300000, 325000, 350000, 375000, 400000,
]

KEY_GLOBAL = ("IllllIllllIlIlII", "lllIlllIIlIlIlll")
SLOT_KEYS = [
    ("lllIIlllIIIIIlII", "lIlIlllllIIIlllI", "lIlIIIIlllIlIlll", "lIlIIlIIIllIllIl"),
    ("lllIIIllllIIIIII", "IIlIlllIIlllllll", "lllllIllIIlIllll", "lIIlIIIlIIIIIllI"),
    ("IlIIlIIllIlIIIll", "llIllllllllllllI", "lIlIIlllIlIllIll", "IlllIlIllllIllII"),
    ("IlIlIIlllIllllIl", "IIlIIllIllllIIll", "IIIlIIlIIlllllII", "lIlllIlIlllIllIl"),
    ("lllIlIIIllllllll", "lIlIIlIIllIIlllI", "IllIllllIIllIlIl", "llIIIlllIlllIIII"),
    ("lIllIIlllIIlIllI", "llIIllIllIIlIllI", "IIIIllllIIllllll", "lIlllllIIIlIlIIl"),
    ("lIIIlIIlIllIllIl", "lIIIIIIIIllllIIl", "IlIllIlIlllllllI", "lIlIIIIllllllIll"),
    ("llIIIlIlIIllllIl", "IllIIlIIlIllIIIl", "IIIIIlllIIIlllIl", "llllIIlIlIIlIIII"),
    ("IIllIlIIlIIllIII", "IIllllllllIlllII", "IIIIIlIllllIlIll", "llllIIlIllIIIlII"),
    ("lIlIllIIIIIlllIl", "IIllllIlllllIlII", "IlllIIlIIllIlIII", "lIIIIIllIIlIlIII"),
]


def level_to_xp(level: int) -> int:
    if not (1 <= level <= 2400):
        raise ValueError("Le niveau doit être compris entre 1 et 2400.")
    if level <= len(EARLY_XP):
        return sum(EARLY_XP[: level - 1])
    return level * 400_000 - 6_790_000


def encode_block(val: int) -> str:
    chars = []
    for _ in range(4):
        chars.append(ALPHA[val % 57])
        val //= 57
    return "".join(chars)


def generate_mastery_code(player_handle: str, xp: int) -> str:
    region, _, subregion, pid = player_handle.split("-")
    r = random.randint(100, 999)
    s25 = f"{r:03d}{subregion}{1_000_000_000 + xp + r}{1_000_000_000 + int(pid) + r}{region}"
    checksum = 100 + sum(int(c) for c in s25)
    s28 = f"{s25}{checksum:03d}"
    return "-".join(encode_block(int(s28[i : i + 7])) for i in range(0, 28, 7))


def compute_sc2_signature(author: str, player: str, bank_name: str, sections: dict) -> str:
    parts = [author, player, bank_name]
    for sec in sorted(sections.keys()):
        parts.append(sec)
        for key in sorted(sections[sec].keys()):
            val_type, val_str = sections[sec][key]
            parts.extend([key, "Value", val_type, val_str])
    return hashlib.sha1("".join(parts).encode("utf-8")).hexdigest().upper()


def xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def load_bank(path: Path) -> dict:
    sections = {}
    if not path.exists():
        return sections
    root = ET.parse(path).getroot()
    for sec in root.findall("Section"):
        s_name = sec.attrib["name"]
        sections[s_name] = {}
        for key in sec.findall("Key"):
            k_name = key.attrib["name"]
            val = key.find("Value")
            if val is not None and val.attrib:
                val_type, val_str = next(iter(val.attrib.items()))
                sections[s_name][k_name] = (val_type, val_str)
    return sections


def write_bank(path: Path, author: str, player: str, bank_name: str, sections: dict) -> str:
    if path.exists():
        bak = path.with_suffix(".SC2Bank.bak")
        if not bak.exists():
            shutil.copy2(path, bak)
    sig = compute_sc2_signature(author, player, bank_name, sections)
    lines = ['<?xml version="1.0" encoding="utf-8"?>', '<Bank version="1">']
    for sec_name, keys in sections.items():
        lines.append(f'    <Section name="{xml_escape(sec_name)}">')
        for key_name, (val_type, val_str) in keys.items():
            lines.append(f'        <Key name="{xml_escape(key_name)}">')
            lines.append(f'            <Value {val_type}="{xml_escape(val_str)}"/>')
            lines.append("        </Key>")
        lines.append("    </Section>")
    lines.append(f'    <Signature value="{sig}"/>')
    lines.append("</Bank>")
    path.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")
    return sig


def build_starlight_section(stats: list[int]) -> dict:
    g0 = random.randint(10_000_000, 40_000_000)
    g1 = random.randint(10_000_000, 40_000_000)
    sec = {
        KEY_GLOBAL[0]: ("int", str(g0)),
        KEY_GLOBAL[1]: ("int", str(g1)),
    }
    for slot, val in enumerate(stats):
        r0 = random.randint(10_000_000, 40_000_000)
        r1 = random.randint(10_000_000, 40_000_000)
        k0, k1, k2, k3 = SLOT_KEYS[slot]
        sec[k0] = ("int", str(r0 + g0))
        sec[k1] = ("int", str(r1 + g1))
        sec[k2] = ("int", str(val + r0 + g1))
        sec[k3] = ("int", str(val + r1 + g0))
    return sec


def find_ds_banks() -> list[Path]:
    home = Path.home()
    roots = [
        home / "Documents" / "StarCraft II" / "Accounts",
        home / "OneDrive" / "Documents" / "StarCraft II" / "Accounts",
    ]
    found = []
    for root in roots:
        if root.exists():
            for p in root.rglob(f"{DS_BANK_NAME}.SC2Bank"):
                if p.parent.name.lower() != "backup" and p not in found:
                    found.append(p)
    return found


def main():
    print("Assure-toi que StarCraft II est complètement fermé avant de continuer.\n")
    banks = find_ds_banks()
    if not banks:
        print("Aucune sauvegarde Direct Strike trouvée (lance d'abord 1 partie normale).")
        return

    if len(banks) == 1:
        ds_path = banks[0]
    else:
        print("Plusieurs comptes détectés :")
        for idx, p in enumerate(banks, 1):
            print(f"  [{idx}] Profil {p.parents[2].name} (auteur {p.parent.name})")
        choice = int(input("Numéro du compte à modifier : ").strip())
        ds_path = banks[choice - 1]

    author_handle = ds_path.parent.name
    player_handle = ds_path.parents[2].name
    print(f"Compte détecté : {player_handle} | Auteur : {author_handle}")

    lvl_str = input("Niveau souhaité (1 à 2400, vide pour ne pas toucher au niveau) : ").strip()
    if lvl_str:
        level = int(lvl_str)
        xp = level_to_xp(level)
        sections = load_bank(ds_path)
        sections.setdefault("IIlIlIIlllIIII", {})["IllIIIIIlIIIII"] = ("int", str(xp))
        code = generate_mastery_code(player_handle, xp)
        sections.setdefault("7KMP6J5N5MX7WPDT", {})["1VC1C5S8E4C3KL65"] = ("string", code)
        sig = write_bank(ds_path, author_handle, player_handle, DS_BANK_NAME, sections)
        print(f"OK -> Niveau {level} ({xp:,} XP) appliqué | Signature : {sig}")

    prem = input("Activer PremiumReward dans Starlight.SC2Bank ? (o/n) : ").strip().lower()
    if prem in ("o", "oui", "y", "yes"):
        sl_path = ds_path.parent / f"{STARLIGHT_BANK_NAME}.SC2Bank"
        sl_sections = load_bank(sl_path)
        sl_sections[PREMIUM_SECTION] = build_starlight_section([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        sig_sl = write_bank(sl_path, author_handle, player_handle, STARLIGHT_BANK_NAME, sl_sections)
        print(f"OK -> PremiumReward activé dans Starlight.SC2Bank | Signature : {sig_sl}")


if __name__ == "__main__":
    main()
