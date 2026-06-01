// Cross-language demonstration: TypeScript's exception model is
// completely untyped — `throws` is not part of the signature — so the
// LSP violation is the same as the C# case, just with even less help
// from the compiler.

export class DeliveryFailed extends Error {
    constructor(message: string) {
        super(message);
        this.name = "DeliveryFailed";
    }
}

export class FlakyNetworkError extends Error {
    // Sibling of DeliveryFailed, NOT a subclass. An `instanceof
    // DeliveryFailed` check written against the parent's documented
    // surface evaluates to false here, so the catch clause leaks.
    constructor(message: string) {
        super(message);
        this.name = "FlakyNetworkError";
    }
}

export class Notifier {
    // Documented exception surface: notify() either returns normally or
    // throws DeliveryFailed. TypeScript has no throws clause to bind
    // that promise, so the contract lives in the doc comment alone.
    notify(message: string): void {
        if (!message) {
            throw new DeliveryFailed("message must be non-empty");
        }
    }
}

export class SmsNotifier extends Notifier {
    // Exception broadening: this override silently adds
    // FlakyNetworkError to its visible throw set. Callers that wrote
    // `try { ... } catch (e) { if (e instanceof DeliveryFailed) ... }`
    // against the documented contract see the broader exception leak.
    private readonly failOn: string | null;

    constructor(failOn: string | null = null) {
        super();
        this.failOn = failOn;
    }

    notify(message: string): void {
        super.notify(message);
        if (this.failOn !== null && message.includes(this.failOn)) {
            throw new FlakyNetworkError(`carrier hiccup on '${message}'`);
        }
    }
}

export function deliver(notifier: Notifier, message: string): string {
    // Encodes the documented Notifier contract: catch DeliveryFailed,
    // treat anything wider as a programming bug. The point of the
    // exercise is that "anything wider" is exactly what SmsNotifier
    // produces.
    try {
        notifier.notify(message);
    } catch (exc) {
        if (exc instanceof DeliveryFailed) {
            return `failed: ${exc.message}`;
        }
        throw exc;
    }
    return "ok";
}
