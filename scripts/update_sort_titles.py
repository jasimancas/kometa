import os
import re
import time
from pathlib import Path

import requests
import yaml

TMDB_API_KEY = os.environ["TMDB_API_KEY"]
MOVIES_FILE = Path("metadata/movies/movies.yml")

session = requests.Session()


def log(msg):
    print(msg, flush=True)


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
    log("===== INICIO UPDATE SORT TITLES =====")

    if not MOVIES_FILE.exists():
        raise FileNotFoundError(f"No existe {MOVIES_FILE}")

    with MOVIES_FILE.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    metadata = data.get("metadata", {})

    metadata_key_by_tmdb_id = {
        str(movie_id): movie_id
        for movie_id in metadata.keys()
    }

    log(f"Películas en YAML: {len(metadata)}")

    collection_cache = {}
    changed = False
    processed = 0
    with_collection = 0

    for movie_id in metadata.keys():
        movie_id_str = str(movie_id)
        processed += 1

        try:
            movie = tmdb_get(f"/movie/{movie_id_str}", language="es-ES")
        except Exception as e:
            log(f"[ERROR] TMDb movie {movie_id_str}: {e}")
            continue

        title = movie.get("title", "???")

        collection = movie.get("belongs_to_collection")

        if not collection:
            log(f"[SKIP] {title} ({movie_id}) → sin colección")
            continue

        with_collection += 1

        collection_id = collection["id"]
        collection_name = collection["name"]

        log(f"[COL] {title} → {collection_name}")

        if collection_id not in collection_cache:
            try:
                collection_cache[collection_id] = tmdb_get(
                    f"/collection/{collection_id}",
                    language="es-ES",
                )
            except Exception as e:
                log(f"[ERROR] TMDb collection {collection_id}: {e}")
                continue

        collection_details = collection_cache[collection_id]
        collection_slug = slugify_collection_name(collection_details["name"])

        parts = sort_parts(collection_details.get("parts", []))

        log(f"     → slug: {collection_slug}")
        log(f"     → total en colección: {len(parts)}")

        for index, part in enumerate(parts, start=1):
            part_id = str(part["id"])

            if part_id not in metadata_key_by_tmdb_id:
                continue

            metadata_key = metadata_key_by_tmdb_id[part_id]
            wanted_sort_title = f"{collection_slug}_{index:02d}"

            current_sort_title = metadata[metadata_key].get("sort_title")

            if current_sort_title != wanted_sort_title:
                log(
                    f"     [UPDATE] {metadata_key}: "
                    f"{current_sort_title} → {wanted_sort_title}"
                )
                metadata[metadata_key]["sort_title"] = wanted_sort_title
                changed = True

    log("===== RESUMEN =====")
    log(f"Procesadas: {processed}")
    log(f"Con colección: {with_collection}")

    if not changed:
        log("No hay cambios.")
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

    log("movies.yml actualizado correctamente.")
    log("===== FIN =====")


if __name__ == "__main__":
    main()
