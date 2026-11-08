# Kometa: títulos y carátulas en español

Metadatos para [Kometa](https://kometa.wiki/) (antes Plex Meta Manager) que dejan la biblioteca de Plex con los
**títulos y las carátulas en español de España**, según las versiones de [TMDB](https://www.themoviedb.org/). Es solo
datos: no hay ninguna aplicación que instalar, Kometa lee los ficheros YAML y descarga las carátulas de este repo.

## Qué contiene

```text
metadata/
├── movies/
│   ├── movies.yml   metadatos de películas, indexados por ID de TMDB
│   └── assets/      carátulas (TMDBID.jpg), más de 14.000
└── tv/
    ├── tv.yml       metadatos de series, indexados por ID de TVDB
    └── assets/      carátulas de la serie y de sus temporadas
scripts/             automatizaciones que mantienen los YAML al día
tests/               validación de los YAML contra las carátulas
```

Cada entrada de `movies.yml` tiene como mucho estos campos (el título es opcional):

```yaml
metadata:
  11:                                   # ID de TMDB de la película
    title: "Star Wars - Ep. 4: Una nueva esperanza"
    sort_title: "star_wars_04"          # orden dentro de su colección (lo escribe un script)
    url_poster: https://github.com/jasimancas/kometa/raw/main/metadata/movies/assets/11.jpg
```

Las series (`tv.yml`) siguen el mismo esquema y admiten además `seasons:` con una `url_poster` por temporada.

## Cómo usarlo en Kometa

En la configuración de Kometa de tu biblioteca, apunta a los YAML con `metadata_files` (rutas `url`):

```yaml
libraries:
  Peliculas:
    metadata_files:
      - url: https://raw.githubusercontent.com/jasimancas/kometa/main/metadata/movies/movies.yml
  Series:
    metadata_files:
      - url: https://raw.githubusercontent.com/jasimancas/kometa/main/metadata/tv/tv.yml
```

Los nombres de las bibliotecas son los tuyos; la sintaxis completa está en la [documentación de Kometa](https://kometa.wiki/).
[Atrion](https://github.com/jasimancas/atrion) también lee estos dos YAML y publica sus carátulas en sus listados.

## Añadir una carátula

1. Copia la imagen **en JPG** a `metadata/movies/assets/` con el nombre `<IDTMDB>.jpg` (o `<IDTMDB>-algo.jpg`), o a
   `metadata/tv/assets/` con el ID de TVDB (`<IDTVDB>-nombre.jpg`; para temporadas, p. ej. `<ID>-nombre_S01.jpg`).
2. Abre un PR (o haz push a `main`). Los flujos de GitHub Actions hacen el resto:

| Flujo | Cuándo | Qué hace |
| --- | --- | --- |
| Compress images | al cambiar carátulas en `main` | Reduce las imágenes nuevas (máx. 1000x1500 px y 600 KB) |
| Sync Kometa movies.yml / tv.yml | al cambiar carátulas | Añade al YAML la entrada con su `url_poster` (`scripts/sync_movies_yml.py`, `scripts/sync_tv_yml.py`) |
| Update movie sort titles | a mano | Pone `sort_title` según la colección de TMDB para ordenar sagas (`scripts/update_sort_titles.py`; necesita el secreto `TMDB_API_KEY` del repo) |
| Tests | en cada PR | `yamllint --strict` y `tests/main.py` |
| Labeler | en cada PR | Etiqueta el PR según los ficheros que toca |

Para añadir el `title` de una película hay que editarlo a mano en `movies.yml`; el script de sincronización solo
escribe `url_poster`.

## Comprobar en local

```bash
pip install -r tests/requirements.txt
yamllint --strict .
python3 tests/main.py        # cada entrada tiene url_poster válida y no sobran ni faltan imágenes
```

`requirements.txt` (raíz) es solo para los scripts de sincronización.

## Referencias

Algunas colecciones usan carátulas de [The Poster DB](https://theposterdb.com/); créditos a sus autores:

| Set                                 | Author                                                      | Link                               |
| ----------------------------------- | ----------------------------------------------------------- | ---------------------------------- |
| Alien and Predator Universes        | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/109057 |
| Avatar Collection                   | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/215631 |
| Batman Collection (1989-1997)       | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/237026 |
| DC Extended Universe                | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/118189 |
| Deadpool Collection                 | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/118189 |
| Die Hard Collection                 | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/113089 |
| Creed Collection                    | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/113191 |
| Eastrail 177                        | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/116913 |
| Evangelion                          | [musikmann2000](https://theposterdb.com/user/musikmann2000) | https://theposterdb.com/set/131521 |
| MCU Universe                        | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/118188 |
| Mad Max Collection                  | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/113189 |
| Matrix Collection                   | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/116902 |
| Pirates of the Caribbean Collection | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/166380 |
| Rambo Collection                    | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/108949 |
| Rocky Collection                    | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/113190 |
| The Chronicles of Narnia Collection | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/116914 |
| The Dark Knight Collection          | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/116901 |
| The Expendables Collection          | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/113096 |
| The Lord of the Rings Collection    | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/113397 |
| The Hangover Collection             | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/113180 |
| The Hobbit Collection               | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/113398 |
| Terminator Collection               | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/108967 |
| Wolverine Collection                | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/113180 |
| X-Men Collection                    | [AMC](https://theposterdb.com/user/AMC)                     | https://theposterdb.com/set/109012 |
