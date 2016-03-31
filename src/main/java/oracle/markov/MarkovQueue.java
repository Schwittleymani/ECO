package oracle.markov;

import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.stream.Collectors;

/**
 * Implements an ordered table of strings, with deep hashing and off-the-edge pushing to the end of the queue.
 * @author Alek Ratzloff <alekratz@gmail.com>
 *
 */
public class MarkovQueue extends ArrayDeque<String> {

    private static final long serialVersionUID = 7678929707313035652L;

    private int order;

    /**
     * Creates a queue for a Markov chain that will have a limited number of items in it. The order is the limit.
     * @param order the number of phrases for each state in the markov chain to hold.
     */
    public MarkovQueue(int order) {
        this.order = order;
    }

    /**
     * Creates a queue for a Markov chain that will infer its order from the length of the items
     * @param items the items to create the queue from.
     */
    public MarkovQueue(String[] items) {
        this.order = items.length;
        Arrays.stream(items).forEach(s -> push(s));
    }

    /**
     * Adds the given string to the front of the queue.
     * @param e the string at the front
     */
    @Override
    public void addFirst(String e) {
        while(this.size() >= order) {
            this.removeLast();
        }
        super.addFirst(e);
    }

    /**
     * Adds the given string to the back of the queue.
     * @param e the string at the back
     */
    @Override
    public void addLast(String e) {
        while(this.size() >= order) {
            this.removeFirst();
        }
        super.addLast(e);
    }

    /**
     * Gets the hashcode of this entire queue.
     */
    @Override
    public int hashCode() {
        int h = 1;
        for(String s : this) {
            h += 31 * h + (s == null ? 0 : s.hashCode());
        }
        return h;
    }

    /**
     * Checks the equality of the markov queue.
     * @param queue the other queue to compare
     * @return whether the elements of this queue are equal.
     */
    @Override
    public boolean equals(Object queue) {
        return ((MarkovQueue)queue).hashCode() == hashCode();
    }

    /**
     * Creates a copy of the markov queue. This is useful for creating markov chains. This creates a shallow clone as far
     * as strings are concerned (i.e., string references are copied and not entire strings).
     * @return the shallow clone of this queue.
     */
    @Override
    public MarkovQueue clone() {
        MarkovQueue c = new MarkovQueue(order);
        for(String s : this)
            c.add(s);
        return c;
    }

    /**
     * Joins all of the words in this queue together separated by spaces.
     * @return the stringified version of this queue.
     */
    @Override
    public String toString() {
        return this.stream().collect(Collectors.joining(" "));
    }

    /**
     * How many items the queue can hold before the last or first item gets pushed off the queue.
     * @return the order of the queue.
     */
    public int getOrder() {
        return order;
    }

}