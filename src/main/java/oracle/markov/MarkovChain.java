package oracle.markov;

/**
 * Created by mrzl on 31.03.2016.
 */
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

import org.json.simple.JSONObject;
import org.json.simple.JSONValue;

/**
 * Represents a Markov chain, with connections and the like.
 * @author Alek Ratzloff <alekratz@gmail.com>
 *
 */
public class MarkovChain {

    private Hashtable<MarkovQueue, Weighttable> chain = new Hashtable<>();
    private Random random = new Random();
    private int order;

    public MarkovChain() {
        order = 1;
    }

    public MarkovChain(int order) {
        assert(order > 0);
        this.order = order;
    }

    /**
     * Trains the Markov chain on some snippet of text.
     * @param text the text to train the chain on
     */
    public void train(String text) {
        Scanner scanner = new Scanner(text);
        String token;

        MarkovQueue tokenList = new MarkovQueue(order);
        while(scanner.hasNext()) {
            token = scanner.next();

            MarkovQueue listClone = tokenList.clone();

            if(!chain.containsKey(listClone)) {
                chain.put(listClone, new Weighttable());
            }
            // get the hashtable for this key
            Weighttable weights = chain.get(listClone);
            if(!weights.containsKey(token)) {
                weights.put(token, 1);
            } else {
                Integer val = weights.get(token) + 1;
                weights.put(token, val);
            }
            tokenList.addLast(token);
        }
        scanner.close();
    }

    /**
     * Generates an entire paragraph with the given number of sentences.
     * @param count the number of sentences in the paragraph.
     * @return a generated paragraph based on the markov chain.
     */
    public String generateParagraph(int count) {
        // choose a random seed
        return generateParagraph(count, getRandomSeed());
    }

    /**
     * Generates an entire paragraph with the given number of sentences, and a fixed starting word.
     * @param count the number of sentences in the paragraph.
     * @param seed the word to start the paragraph with.
     * @return the generated paragraph.
     */
    public String generateParagraph(int count, MarkovQueue seed) {
        String paragraph = "";

        for(int i = 0; i < count; i++) {
            paragraph += generateSentence(seed);
            // move along the seed
            Weighttable weights = chain.get(seed);
            String word = weights.getRandomWord();
            // skip past the words we just added; the generateSentence method will automatically add these on for us.
            for(int j = 0; j < order; j++) {
                seed.addLast(word);
                weights = chain.get(seed);
                word = weights.getRandomWord();
            }
        }
        return paragraph;
    }

    /**
     * Generates a random sentence based on the markov chain.
     * @return the random sentence generated.
     */
    public String generateSentence() {
        return generateSentence(getRandomSeed());
    }

    /**
     * Generates a random sentence based on the markov chain, and a fixed starting word.
     * @param seed the word to start the sentence with.
     * @return the random sentence generated.
     */
    public String generateSentence(MarkovQueue seed) {
        MarkovQueue words = seed;
        String sentence = "";
        Stack<Character> quotes = new Stack<>();
        // sentence will start out as appending of all the words in the first seed
        for(String s : words) {
            sentence += s + " ";
        }

        String word;
        do{
            Weighttable weights = chain.get(words);

            // Sometimes the chain doesn't have any start states for the word in question
            // So it should just be save to cut it off here
            if(weights == null) {
                //sentence += ".";
                break;
            }

            String append = word = weights.getRandomWord();
            if(word.startsWith("\"") || word.startsWith("'")) {
                quotes.push(word.charAt(0));
            }
            if(word.endsWith("\"") || word.endsWith("'")) {
                char c = word.charAt(word.length() - 1);
                if(quotes.size() == 0) {
                    // there's no quotes on the stack, so just get rid of the quote
                    append = word.substring(0, word.length() - 2);
                } else if(c != quotes.peek()) {
                    // there's a quote in the stack - but it's mismatched
                    append = word.replace(c, quotes.pop());
                } else {
                    // same quotes - pop from the stack
                    quotes.pop();
                }
            }

            sentence += append + " ";
            words.addLast(word);
        } while (!word.endsWith(".") && !word.endsWith("!") && !word.endsWith("?"));

        // append quotes at the end
        while(quotes.size() > 0) {
            sentence += quotes.pop();
        }

        return sentence;
    }

    /**
     * Gets a random word to seed a markov chain with.
     * @return the random word
     */
    public MarkovQueue getRandomSeed() {
        // choose a random seed
        int which = random.nextInt(chain.keySet().size());
        return (MarkovQueue)chain.keySet().toArray()[which];
    }

    /**
     * Returns a random word in the Markov chain.
     * @param seed gets a random word based on a seed
     * @return the word chosen
     */
    public String getRandomWord(MarkovQueue seed) {
        if(!chain.containsKey(seed)) {
            return ".";
        }

        Weighttable weights = chain.get(seed);
        return weights.getRandomWord();
    }

    /**
     * Saves this instance of a Markov chain to a JSON-encoded file.
     * @param path the location to save to
     * @throws IOException
     */
    @SuppressWarnings("unchecked")
    public void saveToFile(String path) throws IOException {
        File file = new File(path);
        if(file.exists()) { // overwrite files
            file.delete();
        }

        FileWriter writer = new FileWriter(file);
        JSONObject root = new JSONObject();
        chain.forEach((queue, table) -> {
            String jsonKey = queue.toString(); // this gives a comma-separated list of the words
            JSONObject queueRule = new JSONObject();
            table.forEach(queueRule::put);
            root.put(jsonKey, queueRule);
        });

        writer.write(root.toJSONString());
        writer.close();
    }

    /**
     * Loads and merges the contents of a JSON-encoded Markov chain into this current Markov chain.
     * @param path the location of the JSON encoded file
     * @throws FileNotFoundException
     */
    public void loadFromFile(String path) throws FileNotFoundException {
        File file = new File(path);
        FileReader reader =  new FileReader(file);
        JSONObject root = (JSONObject) JSONValue.parse(reader);

        root.forEach((wordObj, valueObj) -> {
            MarkovQueue queue = new MarkovQueue(((String) wordObj).split(" "));
            if(queue.getOrder() != getOrder()) {
                if (getOrder() == 1 && count() == 0) {
                    // if the order is equal to 1, and there hasn't been anything added to the chain yet, then we can infer
                    // that the order is going to be the same order as the queue
                    order = queue.getOrder();
                } else {
                    // TODO: make this message less confusing
                    throw new RuntimeException("Mismatched Markov chain order; " + path + " order is " + queue.getOrder() +
                            " versus established order of " + order);
                }
            }
            JSONObject value = (JSONObject)valueObj;
            Weighttable weights = new Weighttable();
            value.forEach((word, weight) -> {
                weights.addWeight((String)word, ((Long)weight).intValue());
            });
            chain.put(queue, weights);
        });
    }

    /**6
     * Merges the contents of two Markov chains.
     * @param markovChain
     */
    public void merge(MarkovChain markovChain) {
        // yay java 8 loops
        markovChain.chain.forEach((queue, mergeTable) -> {
            if(chain.contains(queue)) {
                // merge the weight tables for this queue
                Weighttable thisTable = chain.get(queue);
                mergeTable.forEach((word, weight) -> thisTable.addWeight(word, weight));
            } else {
                chain.put(queue, mergeTable);
            }
        });
    }

    /**
     * Gets the number of words that have a rule for them.
     * @return the number of nodes in the Markov chain
     */
    public int count() {
        return chain.size();
    }

    /**
     * Gets the the number of items to put in the pool when generating a Markov chain.
     * @return
     */
    public int getOrder() {
        return order;
    }
}
