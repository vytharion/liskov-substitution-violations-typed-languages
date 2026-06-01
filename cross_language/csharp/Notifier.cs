using System;

namespace CrossLanguage
{
    public class DeliveryFailed : Exception
    {
        public DeliveryFailed(string message) : base(message) { }
    }

    public class FlakyNetworkError : Exception
    {
        // Sibling of DeliveryFailed, NOT a subclass. C# has no checked
        // exceptions, so the compiler cannot catch the broadening — but
        // the LSP violation is exactly the same as the Java case: a
        // `catch (DeliveryFailed)` clause written against the parent's
        // documented surface will not catch this class.
        public FlakyNetworkError(string message) : base(message) { }
    }

    public class BaseNotifier
    {
        // Documented exception surface: Notify() either returns or
        // throws DeliveryFailed. The documentation is the only contract
        // — C#'s lack of checked exceptions means nothing in the type
        // system stops a subclass from broadening the throw set.
        public virtual void Notify(string message)
        {
            if (string.IsNullOrEmpty(message))
            {
                throw new DeliveryFailed("message must be non-empty");
            }
        }
    }

    public class SmsNotifier : BaseNotifier
    {
        // Exception broadening: this override silently adds
        // FlakyNetworkError to its visible throw set. Callers wired
        // `try / catch (DeliveryFailed)` around the documented contract
        // crash on the broader exception class.
        private readonly string? _failOn;

        public SmsNotifier(string? failOn = null)
        {
            _failOn = failOn;
        }

        public override void Notify(string message)
        {
            base.Notify(message);
            if (_failOn != null && message.Contains(_failOn))
            {
                throw new FlakyNetworkError($"carrier hiccup on '{message}'");
            }
        }
    }

    public static class NotifierDriver
    {
        public static string Deliver(BaseNotifier notifier, string message)
        {
            // Encodes the documented BaseNotifier contract: catch
            // DeliveryFailed, treat anything wider as a bug. The point
            // of the exercise is that "anything wider" is exactly what
            // SmsNotifier produces.
            try
            {
                notifier.Notify(message);
            }
            catch (DeliveryFailed exc)
            {
                return $"failed: {exc.Message}";
            }
            return "ok";
        }

        public static void Run()
        {
            Console.WriteLine(Deliver(new BaseNotifier(), "ping"));
            Console.WriteLine(Deliver(new BaseNotifier(), ""));
            try
            {
                BaseNotifier sms = new SmsNotifier("STORM");
                Console.WriteLine(Deliver(sms, "warning STORM imminent"));
            }
            catch (FlakyNetworkError exc)
            {
                Console.WriteLine($"caller crashed on broadened surface: {exc.Message}");
            }
        }
    }
}
