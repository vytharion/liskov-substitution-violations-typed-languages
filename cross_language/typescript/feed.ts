// Cross-language demonstration: TypeScript's structural type system
// accepts the same covariant return narrowing that Java and C# accept
// nominally. The result is identical — a single-pass iterator slipped
// past a re-iterable contract.

export class FeedReader {
    // Documented return contract: recent(n) returns an Iterable<string>
    // that may be iterated more than once. Caches and audit replays
    // rely on this re-iterability.
    protected readonly items: string[];

    constructor(items: string[]) {
        this.items = [...items];
    }

    recent(n: number): Iterable<string> {
        const from = Math.max(0, this.items.length - n);
        return this.items.slice(from);
    }
}

export class StreamingFeedReader extends FeedReader {
    // Covariant return abuse: TypeScript permits an override to narrow
    // Iterable<string> to IterableIterator<string>. Structurally the
    // override is still an Iterable, so the compiler is satisfied. At
    // runtime the iterator is single-pass — callers that walked the
    // parent's return value twice silently observe an empty sequence
    // on the second walk.
    *recent(n: number): IterableIterator<string> {
        const from = Math.max(0, this.items.length - n);
        for (let i = from; i < this.items.length; i++) {
            yield this.items[i];
        }
    }
}

export function summarizeTwice(reader: FeedReader, n: number): [number, number] {
    // Encodes the documented re-iterable contract. Against the base
    // both counts match; against StreamingFeedReader the second count
    // collapses to zero because the iterator is exhausted.
    const window = reader.recent(n);
    let first = 0;
    for (const _ of window) {
        first++;
    }
    let second = 0;
    for (const _ of window) {
        second++;
    }
    return [first, second];
}
