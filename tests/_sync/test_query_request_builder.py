import pytest
from httpx import Headers, QueryParams

from postgrest import SyncQueryRequestBuilder
from postgrest.utils import SyncClient


@pytest.fixture
def query_request_builder():
    with SyncClient() as client:
        yield SyncQueryRequestBuilder(
            client, "/example_table", "GET", Headers(), QueryParams(), {}
        )


def test_constructor(query_request_builder: SyncQueryRequestBuilder):
    builder = query_request_builder

    assert builder.path == "/example_table"
    assert len(builder.headers) == 0
    assert len(builder.params) == 0
    assert builder.http_method == "GET"
    assert builder.json == {}
