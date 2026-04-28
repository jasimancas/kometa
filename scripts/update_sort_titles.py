import os
import re
import time
from pathlib import Path

import requests
import yaml

TMDB_API_KEY = os.environ["TMDB_API_KEY"]
MOVIES_FILE = Path("metadata/movies/movies.yml")

session = requests.Session()


def tmdb_get(path, **params):
    params["api_key"] = TMDB_API_KEY
    response = session.get(
        f"https://api.themoviedb.org/3{path}",
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    time.sleep(0.05)
    return response.json()


def slugify_collection_name(name):
    name = name.lower()
    name = name.replace("collection", "")
    name = name.replace("colección", "")

    if name.startswith("the "):
        name = name[4:]

    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def sort_parts(parts):
    return sorted(
        parts,
        key=lambda p: (
            p.get("release_date") or "9999-99-99",
            p.get("title") or "",
        ),
    )


def main():
    if not MOVIES_FILE.exists():
        raise FileNotFoundError(f"No existe {MOVIES_FILE}")

    with MOVIES_FILE.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    metadata = data.get("metadata", {})

    collection_cache = {}
    changed = False

    for movie_id in list(metadata.keys()):
        movie_id_str = str(movie_id)

        movie = tmdb_get(f"/movie/{movie_id_str}", language="es-ES")
        collection = movie.get("belongs_to_collection")

        if not collection:
            continue

        collection_id = collection["id"]

        if collection_id not in collection_cache:
            collection_cache[collection_id] = tmdb_get(
                f"/collection/{collection_id}",
                language="es-ES",
            )

        collection_details = collection_cache[collection_id]
        collection_slug = slugify_collection_name(collection_details["name"])
        parts = sort_parts(collection_details.get("parts", []))

        for index, part in enumerate(parts, start=1):
            part_id = str(part["id"])

            if part_id not in metadata:
                continue

            wanted_sort_title = f"{collection_slug}_{index:02d}"

            if metadata[part_id].get("sort_title") != wanted_sort_title:
                metadata[part_id]["sort_title"] = wanted_sort_title
                changed = True

    if not changed:
        print("No hay cambios.")
        return

    with MOVIES_FILE.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=1000,
        )

    print("movies.yml actualizado con sort_title de colecciones TMDb.")


if __name__ == "__main__":
    main()
