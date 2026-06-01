package crosslanguage;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;

public class Feed {

    public static class FeedReader {
        // Documented return contract: recent(n) returns an Iterable that
        // may be walked more than once and yields the same items on each
        // pass. Caches and audit replays rely on this re-iterability.
        protected final List<String> items;

        public FeedReader(List<String> items) {
            this.items = new ArrayList<>(items);
        }

        public Iterable<String> recent(int n) {
            int from = Math.max(0, items.size() - n);
            return new ArrayList<>(items.subList(from, items.size()));
        }
    }

    public static class StreamingFeedReader extends FeedReader {
        // Covariant return abuse: Java permits an override to narrow the
        // return type from Iterable<String> to Iterator<String>. The
        // compiler accepts it, but Iterator is single-pass — callers that
        // walked the parent's return value twice silently observe an
        // empty sequence on the second walk.
        public StreamingFeedReader(List<String> items) {
            super(items);
        }

        @Override
        public Iterator<String> recent(int n) {
            int from = Math.max(0, items.size() - n);
            final List<String> window = items.subList(from, items.size());
            return new Iterator<>() {
                private int index = 0;

                @Override
                public boolean hasNext() {
                    return index < window.size();
                }

                @Override
                public String next() {
                    if (!hasNext()) {
                        throw new NoSuchElementException();
                    }
                    return window.get(index++);
                }
            };
        }
    }

    public static int[] summarizeTwice(FeedReader reader, int n) {
        // Encodes the documented re-iterable contract. Against the base
        // both counts match; against StreamingFeedReader the second count
        // collapses to zero because the iterator is exhausted.
        Iterable<String> window = reader.recent(n);
        int first = 0;
        for (String ignored : window) {
            first++;
        }
        int second = 0;
        for (String ignored : window) {
            second++;
        }
        return new int[] { first, second };
    }

    public static void main(String[] args) {
        List<String> seed = List.of("a", "b", "c");
        int[] base = summarizeTwice(new FeedReader(seed), 3);
        int[] streaming = summarizeTwice(new StreamingFeedReader(seed), 3);
        System.out.println("base first=" + base[0] + " second=" + base[1]);
        System.out.println("streaming first=" + streaming[0] + " second=" + streaming[1]);
    }
}
