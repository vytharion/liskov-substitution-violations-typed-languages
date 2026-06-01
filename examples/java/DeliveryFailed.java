package com.vytharion.lsp.notifications;

public class DeliveryFailed extends Exception {
    public DeliveryFailed(String message) {
        super(message);
    }
}
