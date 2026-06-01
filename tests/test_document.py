import pytest

from contracts import Document, DocumentLocked, RevisableDocument


def snapshot_then_attempt_edit(doc: Document, suffix: str) -> tuple[str, str]:
    before = doc.body
    doc.edit(doc.body + suffix)
    after = doc.body
    return before, after


def test_document_starts_unpublished_with_supplied_body() -> None:
    doc = Document("draft")
    assert doc.body == "draft"
    assert doc.published is False


def test_document_allows_edit_before_publish() -> None:
    doc = Document("hello")
    doc.edit("hello world")
    assert doc.body == "hello world"


def test_document_rejects_edit_after_publish() -> None:
    doc = Document("hello")
    doc.publish()
    with pytest.raises(DocumentLocked):
        doc.edit("rewritten")


def test_document_publish_is_a_one_way_transition() -> None:
    doc = Document("hello")
    doc.publish()
    assert doc.published is True
    with pytest.raises(DocumentLocked):
        doc.edit("anything")


def test_snapshot_helper_records_change_on_unpublished_document() -> None:
    doc = Document("foo")
    before, after = snapshot_then_attempt_edit(doc, "bar")
    assert before == "foo"
    assert after == "foobar"


def test_snapshot_helper_raises_on_published_base_document() -> None:
    doc = Document("foo")
    doc.publish()
    with pytest.raises(DocumentLocked):
        snapshot_then_attempt_edit(doc, "bar")


def test_revisable_document_silently_edits_after_publish() -> None:
    doc = RevisableDocument("draft")
    doc.publish()
    doc.edit("rewritten")
    assert doc.body == "rewritten"


def test_snapshot_helper_lies_against_published_revisable_document() -> None:
    doc = RevisableDocument("foo")
    doc.publish()
    before, after = snapshot_then_attempt_edit(doc, "bar")
    assert before == "foo"
    assert after == "foobar"
    assert doc.published is True


def test_revisable_document_is_statically_a_document() -> None:
    doc = RevisableDocument()
    assert isinstance(doc, Document)
