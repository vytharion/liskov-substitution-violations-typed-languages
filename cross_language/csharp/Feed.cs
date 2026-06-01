using System;
using System.Collections.Generic;
using System.Linq;

namespace CrossLanguage
{
    public class FeedReader
    {
        // Documented return contract: Recent(n) returns an IEnumerable
        // that may be enumerated more than once and yields the same
        // items on each pass. Caches and audit replays depend on it.
        protected readonly List<string> Items;

        public FeedReader(IEnumerable<string> items)
        {
            Items = items.ToList();
        }

        public virtual IEnumerable<string> Recent(int n)
        {
            int from = Math.Max(0, Items.Count - n);
            return Items.GetRange(from, Items.Count - from);
        }
    }

    public class StreamingFeedReader : FeedReader
    {
        // Covariant return abuse via C# 9 covariant return types: the
        // override narrows IEnumerable<string> to a single-pass iterator
        // backed by `yield return`. The compiler accepts it because
        // IEnumerator<T> is structurally compatible at the call site of
        // covariant overrides, but callers that walked the parent's
        // return value twice silently observe an empty second pass.
        public StreamingFeedReader(IEnumerable<string> items) : base(items) { }

        public override IEnumerable<string> Recent(int n)
        {
            int from = Math.Max(0, Items.Count - n);
            for (int i = from; i < Items.Count; i++)
            {
                yield return Items[i];
            }
        }
    }

    public static class FeedDriver
    {
        public static (int First, int Second) SummarizeTwice(FeedReader reader, int n)
        {
            // Encodes the documented re-enumerable contract: ask for a
            // window, walk it twice, expect matching counts. Against a
            // streaming subclass the second walk collapses to zero
            // because the underlying iterator is exhausted.
            IEnumerable<string> window = reader.Recent(n);
            int first = window.Count();
            int second = window.Count();
            return (first, second);
        }

        public static void Run()
        {
            var seed = new[] { "a", "b", "c" };
            var baseResult = SummarizeTwice(new FeedReader(seed), 3);
            var streamingResult = SummarizeTwice(new StreamingFeedReader(seed), 3);
            Console.WriteLine($"base first={baseResult.First} second={baseResult.Second}");
            Console.WriteLine($"streaming first={streamingResult.First} second={streamingResult.Second}");
        }
    }
}
