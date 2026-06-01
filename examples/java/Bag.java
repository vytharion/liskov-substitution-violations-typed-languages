package com.vytharion.lsp.bags;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Bag {
    protected List<String> items;

    public Bag(List<String> items) {
        this.items = new ArrayList<>(items);
    }

    public void add(String item) {
        items.add(item);
    }

    public List<String> snapshot() {
        return Collections.unmodifiableList(new ArrayList<>(items));
    }

    public Bag duplicate() {
        return new Bag(items);
    }
}
