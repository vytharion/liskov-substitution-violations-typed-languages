package com.vytharion.lsp.notifications;

public class SmsNotifier extends Notifier {
    private final String failOn;

    public SmsNotifier(String failOn) {
        this.failOn = failOn;
    }

    @Override
    public void notify(String message) throws DeliveryFailed {
        super.notify(message);
        if (failOn != null && message.contains(failOn)) {
            throw new FlakyNetworkRuntimeException(
                "carrier hiccup on '" + message + "'"
            );
        }
    }
}
