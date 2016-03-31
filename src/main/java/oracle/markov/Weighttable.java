package oracle.markov;

import java.util.Hashtable;
import java.util.Random;
import java.util.stream.Collectors;

/**
 * A weight table is used to have keys that contain an ordered set of N strings corresponding to values that are string-
 * integer pairs.
 * @author Alek Ratzloff <alekratz@gmail.com>
 *
 */
public class Weighttable extends Hashtable<String, Integer> {
    /*
     * This is to kill the warnings
     */
    private static final long serialVersionUID = 570882516693488244L;
    private Random random = new Random();

    /**
     * Constructs a new weight table with default everything for the hashtable.
     */
    public Weighttable() {
        super();
    }

    /**
     * Adds a weight to a specified word. If the word doesn't exist in the table, its weight is assumed to be 0 and is added.
     * @param word
     * @param weight
     */
    public void addWeight(String word, int weight) {
        if(this.contains(word)) {
            this.put(word, this.get(word) + weight);
        } else {
            this.put(word, weight);
        }
    }

    /**
     * Gets a string, based on the weight that it holds in the table.
     * @return a random word based on the weights of the table.
     */
    public String getRandomWord() {

        Object[] words = this.keySet().toArray();
        int range = this.values().stream().collect(Collectors.summingInt(i -> i));
        int choice = random.nextInt(range);
        int sum = 0;
        for(Object word : words) {
            int weight = this.get(word);
            sum += weight;
            if(sum > choice)
                return (String)word;
        }

        return ".";
    }
}