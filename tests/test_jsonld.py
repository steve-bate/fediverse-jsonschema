import glob
import json
from pathlib import Path

import pytest
from pyld import jsonld


def _document_loader(uri, _):
    project_dir = Path(__file__).parent.parent
    with open(project_dir / "data" / "activitystreams2-context.json") as fp:
        return {
            "contextUrl": None,
            "documentUrl": uri,
            "document": json.load(fp),
        }


@pytest.fixture(scope="session", autouse=True)
def _initialize_jsonld():
    jsonld.set_document_loader(_document_loader)


AS_CONTEXT_URI = "https://www.w3.org/ns/activitystreams"


def _normalize_context(instance):
    context = instance.get("@context")
    if context is None:
        context = []
    elif isinstance(context, str):
        context = [context]
    if AS_CONTEXT_URI not in context:
        context.insert(0, AS_CONTEXT_URI)
    instance["@context"] = context
    return instance


def _test_document(docpath: Path):
    with open(docpath) as fp:
        instance = _normalize_context(json.load(fp))
        expanded = jsonld.expand(instance, {"isFrame": True})
        # Smoke test
        # Remove the context entry
        instance.pop("@context")
        # An instance with only an "@id" after context is removed
        # will result in an empty context (step 19 of the expansion algorithm)
        if "id" in instance:
            instance.pop("id")
        assert len(instance) == 0 or len(expanded) > 0


def _test_docs(group_dir: str):
    proj_path = Path(__file__).parent
    docs_path = str(proj_path / "docs" / group_dir / "**" / "*.json")
    return (
        f
        for f in glob.glob(docs_path, recursive=True)
        if not f.endswith("package.json")
    )


def _test_id(p):
    return Path(p).name


@pytest.mark.parametrize("docpath", _test_docs("activitystreams2"), ids=_test_id)
def test_w3c_as2_docs(docpath):
    _test_document(docpath)


@pytest.mark.parametrize("docpath", _test_docs("activitypub"), ids=_test_id)
def test_activitypub_docs(docpath):
    _test_document(docpath)


@pytest.mark.parametrize("docpath", _test_docs("mastodon"), ids=_test_id)
def test_mastodon_docs(docpath):
    _test_document(docpath)


@pytest.mark.parametrize(
    "docpath", _test_docs("etc/pleroma_test_data/activitypub"), ids=_test_id
)
def test_etc_pleroma_ap(docpath):
    _test_document(docpath)
