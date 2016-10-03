package oracle.markov;

import oracle.MarkovManager;
import oracle.Oracle;
import oracle.Settings;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Optional;
import java.util.stream.IntStream;

/**
 * Created by raminsoleymani on 03/10/16.
 */
public class Markov {

    Oracle oracle;
    private ArrayList<MarkovManager> markovs = new ArrayList<>();

    public Markov(Oracle oracle) {
        this.oracle = oracle;
        System.out.println("MARKOV");
        loadMarkovs(); // can be changed if u wanna speed or selections... for just load all our stuff
    }

    public void loadMarkovs() {
        loadMarkovs(-1);
    }

    public void loadAuthor(String author){
        MarkovManager m = new MarkovManager();
        m.load(author);
        markovs.add(m);
    }

    public void loadMarkovs(final int number) {
        String[] files = oracle.loadStrings("authors.txt");
        markovs = new ArrayList<>();
        // I removed some load "oraclev2" comment here
        // TODO this was training stuff. bring it back

        IntStream.range(0,files.length)
                .filter(i -> number == -1 || i < number)
                .forEach(i -> loadAuthor(files[i]));
    }

    public Optional<String[]> askLocalMarkov(String text) {
        ArrayList<Integer> markovDepths = new ArrayList<>();
        ArrayList<String> answers = new ArrayList<>();
        ArrayList<String> authors = new ArrayList<>();

        for (MarkovManager m : markovs) {
            int depth = m.getMarkovDepthOrder(m.strip(text));
            String answer = m.getAnswer(text);
            markovDepths.add(depth);
            answers.add(answer);
            authors.add(m.getAuthorName());
        }

        // if the depth of the selected answer is 0, that means
        // there was no proper answer of any author
        int index = Settings.maxIndex(markovDepths);
        String result = answers.get(index);
        String authorName = authors.get(index);
        String logResult = "(" + authorName + ") " + result;
        if (markovDepths.get(index) == 0) {
            authorName = "pre_defined_answer";
        }
        return Optional.of(new String[]{result,logResult});
    }

}
