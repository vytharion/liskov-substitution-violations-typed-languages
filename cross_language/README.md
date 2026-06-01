# Cross-language LSP demonstrations

Reference implementations of the same two violations in Java, C#, and
TypeScript. The Python versions live under `src/notifications/` and are
exercised by the pytest suite; these are static reference files showing
that the same contract gaps reproduce across statically typed languages.

## Files

- `java/Feed.java` — `FeedReader` (Iterable contract) and
  `StreamingFeedReader` (narrows return to `Iterator`).
- `java/Notifier.java` — `BaseNotifier` documents `DeliveryFailed`;
  `SmsNotifier` smuggles `FlakyNetworkError` past the checked-exception
  surface via an unchecked wrapper.
- `csharp/Feed.cs` — same Iterable/iterator covariant-return abuse,
  using C# 9 covariant return types.
- `csharp/Notifier.cs` — same exception broadening, exploiting the
  fact that C# has no checked exceptions.
- `typescript/feed.ts` — same Iterable/IterableIterator narrowing,
  accepted structurally by the TypeScript compiler.
- `typescript/notifier.ts` — same broadening, with even less help
  from the type system because `throws` is not part of TypeScript
  signatures.

## What the Python suite proves

The Python equivalents in `src/notifications/` are tested by
`tests/test_feed.py` and `tests/test_notifier.py`. Those tests pin the
same observable bugs the cross-language code exhibits — the second walk
of a streaming iterator collapses to zero, and a `FlakyNetworkError`
escapes a `try / except DeliveryFailed` boundary.
