import glob
import json
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError
from jsonschema.protocols import Validator

from fediverse_jsonschema.validation import make_validator


def _get_root_errors(errors: list[ValidationError]):
    messages = set()
    for error in errors:
        if not error.context:
            messages.add(error.message)
        else:
            for m in _get_root_errors(error.context):
                messages.add(m)
    return messages


def _test_document(docpath: Path, validator: Validator):
    with open(docpath) as fp:
        instance = json.load(fp)
        errors = list(validator.iter_errors(instance))
        expected_failure = "invalid" in str(docpath)
        if len(errors) > 1:
            print(errors)
        if expected_failure:
            assert len(errors) > 0, "Expected a failure"
            if "#failure_message" in instance:
                failure_message = instance["#failure_message"]
                for error in errors:
                    for ctx_error in error.context:
                        if failure_message in ctx_error.message:
                            return  # passes test
                raise AssertionError(f"Didn't find failure message: {failure_message}")
        else:
            if len(errors) > 0:
                for message in sorted(_get_root_errors(errors)):
                    print(f"VALIDATION ERROR: {message}")
            assert len(errors) == 0, "Unexpected failure"


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


@pytest.fixture(scope="session")
def as2_validator(schema_dir):
    return make_validator(schema_dir, "schema:as2/activitystreams2")


@pytest.mark.parametrize("docpath", _test_docs("activitystreams2"), ids=_test_id)
def test_w3c_as2_docs(docpath, as2_validator: Validator):
    _test_document(docpath, as2_validator)


@pytest.fixture(scope="session")
def ap_validator(schema_dir):
    return make_validator(schema_dir, "schema:ap/activitypub")


@pytest.mark.parametrize("docpath", _test_docs("activitypub"), ids=_test_id)
def test_activitypub_docs(docpath, ap_validator: Validator):
    _test_document(docpath, ap_validator)


@pytest.fixture(scope="session")
def mastodon_validator(schema_dir):
    return make_validator(schema_dir, "schema:mastodon/mastodon")


@pytest.mark.parametrize("docpath", _test_docs("mastodon"), ids=_test_id)
def test_mastodon_docs(docpath, mastodon_validator: Validator):
    _test_document(docpath, mastodon_validator)


@pytest.fixture(scope="session")
def jrd_validator(schema_dir):
    return make_validator(schema_dir, "schema:jrd")


@pytest.mark.parametrize("docpath", _test_docs("jrd"), ids=_test_id)
def test_jrd_docs(docpath, jrd_validator: Validator):
    _test_document(docpath, jrd_validator)


@pytest.fixture(scope="session")
def etc_validator(schema_dir):
    return make_validator(schema_dir, "schema:jrd")


@pytest.mark.parametrize(
    "docpath", _test_docs("etc/pleroma_test_data/activitypub"), ids=_test_id
)
def test_etc_pleroma_ap(docpath, ap_validator: Validator):
    _test_document(docpath, ap_validator)
