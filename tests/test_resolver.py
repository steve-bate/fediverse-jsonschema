from pathlib import Path

from fediverse_jsonschema.validation import SchemaResolver


def test_resolver(test_dir: Path):
    resolver = SchemaResolver(test_dir / ".." / "schemas")
    resource = resolver.resolve("schema:as2/activity")
    assert resource is not None
