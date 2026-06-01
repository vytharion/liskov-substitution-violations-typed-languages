from notifications import FeedReader, StreamingFeedReader, summarize_twice


def test_base_feed_reader_returns_recent_window() -> None:
    reader = FeedReader(["a", "b", "c", "d"])
    assert list(reader.recent(2)) == ["c", "d"]


def test_base_feed_reader_supports_repeated_iteration() -> None:
    reader = FeedReader(["a", "b", "c"])
    window = reader.recent(3)
    assert list(window) == ["a", "b", "c"]
    assert list(window) == ["a", "b", "c"]


def test_summarize_twice_against_base_observes_matching_counts() -> None:
    first, second = summarize_twice(FeedReader(["a", "b", "c"]), 3)
    assert first == 3
    assert second == 3


def test_streaming_feed_reader_is_statically_a_feed_reader() -> None:
    assert isinstance(StreamingFeedReader(["a"]), FeedReader)


def test_streaming_feed_reader_first_pass_returns_items() -> None:
    reader = StreamingFeedReader(["a", "b", "c"])
    assert list(reader.recent(2)) == ["b", "c"]


def test_streaming_feed_reader_second_pass_is_silently_empty() -> None:
    reader = StreamingFeedReader(["a", "b", "c"])
    window = reader.recent(3)
    assert list(window) == ["a", "b", "c"]
    assert list(window) == []


def test_summarize_twice_against_streaming_drops_to_zero_on_second_pass() -> None:
    reader: FeedReader = StreamingFeedReader(["a", "b", "c"])
    first, second = summarize_twice(reader, 3)
    assert first == 3
    assert second == 0
