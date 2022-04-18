import pytest
from httpx import Headers, QueryParams

from postgrest import SyncFilterRequestBuilder
from postgrest.utils import SyncClient


@pytest.fixture
def filter_request_builder():
    with SyncClient() as client:
        yield SyncFilterRequestBuilder(
            client, "/example_table", "GET", Headers(), QueryParams(), {}
        )


def test_constructor(filter_request_builder: SyncFilterRequestBuilder):
    builder = filter_request_builder

    assert builder.path == "/example_table"
    assert len(builder.headers) == 0
    assert len(builder.params) == 0
    assert builder.http_method == "GET"
    assert builder.json == {}
    assert not builder.negate_next


def test_not_(filter_request_builder):
    builder = filter_request_builder.not_

    assert builder.negate_next


def test_filter(filter_request_builder):
    builder = filter_request_builder.filter(":col.name", "eq", "val")

    assert builder.params['":col.name"'] == "eq.val"


def test_multivalued_param(filter_request_builder):
    builder = filter_request_builder.lte("x", "a").gte("x", "b")

    assert str(builder.params) == "x=lte.a&x=gte.b"


def test_match(filter_request_builder):
    builder = filter_request_builder.match({"id": "1", "done": "false"})
    assert str(builder.params) == "id=eq.1&done=eq.false"


def test_contains(filter_request_builder):
    builder = filter_request_builder.contains("x", "a")

    assert str(builder.params) == "x=cs.a"


def test_contains_dictionary(filter_request_builder):
    builder = filter_request_builder.contains("x", {"a": "b"})

    # {"a":"b"}
    assert str(builder.params) == "x=cs.%7B%22a%22%3A+%22b%22%7D"


def test_contains_any_item(filter_request_builder):
    builder = filter_request_builder.contains("x", ["a", "b"])

    # {a,b}
    assert str(builder.params) == "x=cs.%7Ba%2Cb%7D"


def test_contains_in_list(filter_request_builder):
    builder = filter_request_builder.contains("x", '[{"a": "b"}]')

    # [{"a":+"b"}] (the + represents the space)
    assert str(builder.params) == "x=cs.%5B%7B%22a%22%3A+%22b%22%7D%5D"


def test_contained_by_mixed_items(filter_request_builder):
    builder = filter_request_builder.contained_by("x", ["a", '["b", "c"]'])

    # {a,["b",+"c"]}
    assert str(builder.params) == "x=cd.%7Ba%2C%5B%22b%22%2C+%22c%22%5D%7D"
