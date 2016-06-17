package oracle.markov;

/**
 * Created by mrzl on 17.06.2016.
 */
public class MarkovResult{
    private int markovDepth;
    private String answer;

    public MarkovResult( String answer, int depth ) {
        this.answer = answer;
        this.markovDepth = depth;
    }

    public String getAnswer() {
        return this.answer;
    }

    public int getMarkovDepth() {
        return this.markovDepth;
    }
}
