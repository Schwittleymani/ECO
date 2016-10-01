package oracle.ostern;

import processing.data.JSONObject;

import java.util.Arrays;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Created by raminsoleymani on 01/10/16.
 */
public class GifsEasterEgg extends EasterEgg{

    public GifsEasterEgg(JSONObject config) {
        super(Jesus.EASTEREGG_TYPE.ANSWER,config);
    }

    @Override
    public void drawBefore() {

    }

    @Override
    public boolean drawAfter() {
        return false;
    }

    @Override
    public void start(Object obj) {
        String botResponse = (String) obj;
        String[] words = botResponse.split(" ");
        // get the longest word
       Optional<String> longest = Arrays.stream(words).collect(Collectors.maxBy((w1, w2) -> w1.length() - w2.length()));
        if(longest.isPresent()) {
            System.out.println(longest.get());
            oracle.gifDisplayer.getGiyGifsAsnyc(new String[] {longest.get()},2);
        }
    }
}
