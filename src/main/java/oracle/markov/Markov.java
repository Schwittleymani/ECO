package oracle.markov;

import oracle.MarkovManager;
import oracle.Oracle;
import oracle.Settings;
import oracle.cli.CLI;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Optional;
import java.util.stream.IntStream;

/**
 * Created by raminsoleymani on 03/10/16.
 */
public class Markov {

    private Oracle oracle;
    private ArrayList<MarkovManager> markovs = new ArrayList<>();

    public Markov(Oracle oracle) {
        this.oracle = oracle;
        this.markovs = new ArrayList<>();

        boolean doTraining = Settings.DO_LOCAL_MARKOV_TRAINING;
        if( doTraining ){
            System.out.println( "Training Markov" );
            trainMarkovs();
        } else {
            System.out.println( "Loading Markov" );
            loadMarkovs(); // can be changed if u wanna speed or selections... for just load all our stuff
        }
    }

    private void trainMarkovs() {
        MarkovManager m = new MarkovManager();
        String[] files = oracle.loadStrings("authors.txt");
        for( String s : files ){
            m.train( "text/" + File.separator + s, s, Settings.EXPORT_MARKOV_TRAINING );
        }
        markovs.add(m);
    }

    private void loadMarkovs() {
        loadMarkovs(-1);
    }

    private void loadAuthor(String author){
        MarkovManager m = new MarkovManager();
        m.load(author);
        markovs.add(m);
    }

    private void loadMarkovs(final int number) {
        String[] files = oracle.loadStrings("authors.txt");
        IntStream.range(0,files.length)
                .filter(i -> number == -1 || i < number)
                .forEach(i -> loadAuthor(files[i]));
    }

    public Optional<String[]> askLocalMarkov(String text) {
        text = text.replace( CLI.LINE_PREFIX_CHARS, "");
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
