package oracle.lyrik;

import http.requests.PostRequest;
import oracle.Settings;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.util.Optional;
import java.util.StringJoiner;

/**
 * Created by raminsoleymani on 03/10/16.
 */
public class Lyrik {

    boolean requestDone = false;
    Optional<String[]> newAnswer = Optional.empty();


    public boolean isRequestDone() {
        return requestDone;
    }

    public void askLyrikAsync(String text ) {
        Thread thread = new Thread( () -> {
            requestDone = false;
            newAnswer = askLyrik( text );
            requestDone = true;
        });
        thread.start();
    }

    public Optional<String[]> getNewAnswer(){
        return newAnswer;
    }

    public Optional<String[]> askLyrik(String text) {
        try {

            PostRequest post = new PostRequest(Settings.LYRIK_URL);
            post.addData("inputS", text );
            long millis = System.currentTimeMillis();
            post.send();

            if (post != null) {
                //println("Reponse Content: " + post.getContent());
                //println("Reponse Content-Length Header: " + post.getHeader("Content-Length"));
                long millisDiff = System.currentTimeMillis() - millis;
                System.out.println("askLyrik took " + millisDiff + "ms");

                JSONParser json = new JSONParser();
                Object obj = json.parse(post.getContent());
                JSONObject mainJson = (JSONObject) (obj);
                String result = (String) mainJson.get("response");
                String logResult = result;
                System.out.println("Received result: " + result);
                String[] returns = {result,logResult};
                return Optional.of(returns);
            }
        } catch (Exception exc) {
            //exc.printStackTrace();
            System.out.println("yeah. no lyrik. local markov for now");
            return Optional.empty();

        }
        return Optional.of(new String[] {"nothing","kindof lame exit"}); // TODO fix, make issue;
    }

}
