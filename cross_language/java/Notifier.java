package crosslanguage;

public class Notifier {

    public static class DeliveryFailed extends Exception {
        public DeliveryFailed(String message) {
            super(message);
        }
    }

    public static class FlakyNetworkError extends Exception {
        // Sibling of DeliveryFailed, NOT a subclass. A `catch
        // (DeliveryFailed e)` clause written against the documented
        // surface will not catch this exception.
        public FlakyNetworkError(String message) {
            super(message);
        }
    }

    public static class BaseNotifier {
        // Documented exception surface: notify() either returns normally
        // or throws DeliveryFailed. Java's checked-exception system
        // enforces this — adding a new checked exception to an override
        // would not compile, which is exactly what motivates the
        // unchecked-broadening trick the subclass below uses.
        public void notify(String message) throws DeliveryFailed {
            if (message == null || message.isEmpty()) {
                throw new DeliveryFailed("message must be non-empty");
            }
        }
    }

    public static class SmsNotifier extends BaseNotifier {
        // Exception broadening via unchecked subclass: FlakyNetworkError
        // extends Exception only via a workaround path — a real-world
        // codebase would make it a RuntimeException to slip past the
        // checked-throws clause. The point is that nothing in the
        // BaseNotifier.notify() signature prepares callers for this
        // failure class, yet substitutability requires they handle it.
        private final String failOn;

        public SmsNotifier(String failOn) {
            this.failOn = failOn;
        }

        @Override
        public void notify(String message) throws DeliveryFailed {
            super.notify(message);
            if (failOn != null && message.contains(failOn)) {
                throw new RuntimeException(
                    new FlakyNetworkError("carrier hiccup on '" + message + "'")
                );
            }
        }
    }

    public static String deliver(BaseNotifier notifier, String message) {
        // Encodes the documented BaseNotifier contract — the only
        // protocol-level failure mode the caller anticipates is
        // DeliveryFailed. Anything broader escapes here and the caller
        // crashes with an exception its catch clause never saw.
        try {
            notifier.notify(message);
        } catch (DeliveryFailed exc) {
            return "failed: " + exc.getMessage();
        }
        return "ok";
    }

    public static void main(String[] args) {
        System.out.println(deliver(new BaseNotifier(), "ping"));
        System.out.println(deliver(new BaseNotifier(), ""));
        try {
            BaseNotifier sms = new SmsNotifier("STORM");
            System.out.println(deliver(sms, "warning STORM imminent"));
        } catch (RuntimeException exc) {
            System.out.println("caller crashed on broadened surface: " + exc.getCause());
        }
    }
}
