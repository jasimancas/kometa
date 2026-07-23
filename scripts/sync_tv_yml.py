#!/usr/bin/env python3
import re
from pathlib import Path
from ruamel.yaml import YAML

OWNER = "jasimancas"
REPO = "kometa"
BRANCH = "main"

ASSETS_DIR = Path("metadata/tv/assets")
YML_PATH = Path("metadata/tv/tv.yml")

RAW_BASE = f"https://github.com/{OWNER}/{REPO}/raw/{BRANCH}/metadata/tv/assets/"

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.width = 4096  # evita que corte las URLs largas y deje espacios finales

# Posters de serie:
#   1396.jpg
#   1396-breaking-bad.jpg
#
# Posters de temporada:
#   1396_S01.jpg
#   1396-breaking-bad_S01.jpg
IMG_RE = re.compile(
    r"^(?P<id>\d+)(?:-.+?)?(?:_S(?P<season>\d{2}))?\.(jpg|jpeg|png|webp)$",
    re.IGNORECASE,
)


def main():
    if not ASSETS_DIR.exists():
        raise SystemExit(f"No existe la carpeta: {ASSETS_DIR}")

    data = {}
    if YML_PATH.exists():
        data = yaml.load(YML_PATH.read_text(encoding="utf-8")) or {}

    data.setdefault("metadata", {})
    metadata = data["metadata"]

    for img in sorted(ASSETS_DIR.iterdir()):
        if not img.is_file():
            continue

        m = IMG_RE.match(img.name)
        if not m:
            raise SystemExit(
                f"Nombre inválido: {img.name}. "
                "Usa TMDBID-algo.jpg o TMDBID-algo_S01.jpg"
            )

        tmdb_id = int(m.group("id"))
        season = m.group("season")
        url = RAW_BASE + img.name

        entry = metadata.get(tmdb_id) or {}

        if season:
            season_num = int(season)
            entry.setdefault("seasons", {})
            season_entry = entry["seasons"].get(season_num) or {}
            season_entry["url_poster"] = url
            entry["seasons"][season_num] = season_entry
        else:
            entry["url_poster"] = url

        metadata[tmdb_id] = entry

    with YML_PATH.open("w", encoding="utf-8") as f:
        yaml.dump(data, f)

    print("tv.yml actualizado correctamente")


if __name__ == "__main__":
    main()
