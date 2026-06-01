package com.vytharion.lsp.notifications;

public class Notifier {
    public void notify(String message) throws DeliveryFailed {
        if (message == null || message.isEmpty()) {
            throw new DeliveryFailed("message must be non-empty");
        }
    }
}
