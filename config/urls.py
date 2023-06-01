from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json
import requests
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.conf import settings


def filter_by_keys(source, keys):
    filtered_data = {}

    for k, v in source.items():
        if k in keys:
            filtered_data[k] = v
    return filtered_data


@dataclass
class Pokemon:
    id: int
    name: str
    height: int
    weight: int
    base_experience: int

    @classmethod
    def from_raw_data(cls, raw_data):
        filtered_data = filter_by_keys(raw_data, Pokemon.__dataclass_fields__.keys()) # noqa
        return cls(**filtered_data)


TTL = timedelta(seconds=5)
POKEMONS: dict[str, list[Pokemon, datetime]] = {}


def get_pokemon_from_api(name):
    url = settings.POKEAPI_BASE_URL + f"/{name}"
    response = requests.get(url)
    raw_data = response.json()

    return Pokemon.from_raw_data(raw_data)


def _get_pokemon(name):
    if name in POKEMONS:
        pokemon, created_at = POKEMONS[name]
        if datetime.now() > created_at + TTL:
            del POKEMONS[name]
            return _get_pokemon(name)
    else:
        pokemon: Pokemon = get_pokemon_from_api(name)
        POKEMONS[name] = [pokemon, datetime.now()]

    return pokemon


def delete_pokemon_by_cache(request, name):
    if name in POKEMONS:
        del POKEMONS[name]
    else:
        None


@csrf_exempt
def get_pokemon(request, name):
    if request.method == "GET":
        pokemon = _get_pokemon(name)
        return HttpResponse(
            content_type="application/json", content=json.dumps(asdict(pokemon)) # noqa
        )
    elif request.method == "DELETE":
        delete_pokemon_by_cache(request, name)
        return HttpResponse()


def get_pokemon_for_mobile(request, name):
    pokemon = _get_pokemon(name)

    result = filter_by_keys(asdict(pokemon), ["id", "name", "base_experience"])

    return HttpResponse(content_type="application/json", content=json.dumps(result)) # noqa


def return_all_pokemons_by_cache(request):
    pokemons = {}

    for name, info in POKEMONS.items():
        pokemon, created_at = info
        pokemons[name] = asdict(pokemon)

    return HttpResponse(content_type="application/json", content=json.dumps(pokemons)) # noqa


def get_csrf_token(request):
    token = get_token(request)
    response = HttpResponse(content=token)
    response["Access-Control-Allow-Origin"] = "*"
    return response


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/pokemon/<name>/", get_pokemon),
    path("api/pokemon/mobile/<name>/", get_pokemon_for_mobile),
    path("api/pokemon/delete/<name>/", delete_pokemon_by_cache),
    path("api/pokemons/", return_all_pokemons_by_cache),
    path("api/csrf_token/", get_csrf_token),
]
