import json
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


class SchemaResolver:
    def __init__(self, schema_dir: str):
        self.schema_dir = schema_dir

    @lru_cache
    def resolve(self, uri):
        url = urlparse(uri)
        filepath = Path(self.schema_dir) / f"{url.path}-schema.json"
        with open(filepath) as fp:
            response = fp.read()
        contents = json.loads(response)
        return Resource.from_contents(contents)


def make_validator(schema_dir: str, schema_uri: str, check_format: bool = True):
    resolver = SchemaResolver(schema_dir)
    return Draft202012Validator(
        resolver.resolve(schema_uri).contents,
        registry=Registry(retrieve=resolver.resolve),
        format_checker=Draft202012Validator.FORMAT_CHECKER if check_format else None,
    )


def _remove_nulls(instance):
    for key, value in list(instance.items()):
        if value is None:
            instance.pop(key)
        elif isinstance(value, dict):
            _remove_nulls(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _remove_nulls(item)


def preprocess_instance(instance):
    _remove_nulls(instance)
    return instance
