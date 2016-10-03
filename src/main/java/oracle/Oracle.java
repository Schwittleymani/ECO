package oracle;

import gifAnimation.Gif;
import http.requests.PostRequest;
import oracle.cli.CLI;
import oracle.gif.GifDisplayer;
import oracle.web.Webserver;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import processing.core.PApplet;


import java.awt.event.KeyEvent;
import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by mrzl on 31.03.2016.
 * <p>
 * This is the main starting point for the Electronic Chaos Oracle (ECO)
 */

public class Oracle extends PApplet {
    public CLI cli;
    Webserver server;
    OracleLogger logger;
    public Settings settings;

    long millisLastInteraction;

    boolean useLyrik = true;
    boolean startWebserver = true;
    private ArrayList<MarkovManager> markovs;
    boolean lyrikRequestDone = false;
    String newLyrikAnswer = "";

    GifDisplayer gifDisplayer;
    List<Gif> testGifs = new ArrayList<Gif>();


    public static void main(String[] args) {
        PApplet.main("oracle.Oracle");
    }

    public void settings() {
        size(640 * 2, 480, P2D);
        logger = new OracleLogger();

        //fullScreen( P2D, SPAN );

        settings = new Settings();

        useLyrik = Settings.USE_LYRIK;
        // TODO connectivity check

        startWebserver = Settings.START_WEBSERVER;
        if (startWebserver) {
            server = new Webserver(this);
            Settings.printIps();
        }

        millisLastInteraction = System.currentTimeMillis();
    }

    public void setup() {
        gifDisplayer = new GifDisplayer(this);
        //gifDisplayer.getGiyGifsAsnyc(new String[]{"dog","king"},4);

        imageMode(CENTER);

        cli = new CLI(this);
        if (!useLyrik) {
            loadMarkovs();
        }

        noCursor();
    }

    private void loadMarkovs() {
        String[] files = loadStrings("authors.txt");

        markovs = new ArrayList<>();

                /*
        for ( String author : files ) {
            MarkovManager m = new MarkovManager();
            m.train( "text" + File.separator + "oraclev2" + File.separator + author, author, true );
            markovs.add( m );
        }
            */

        for (String author : files) {
            MarkovManager m = new MarkovManager();
            m.load(author);
            markovs.add(m);
        }

    }

    public void draw() {
        background( 0 );
        cli.draw();

        if ( lyrikRequestDone )
        {
            cli.interceptTypeNow( newLyrikAnswer );
            lyrikRequestDone = false;
        }

        // TODO just a test. not loaded in setup...
        if (gifDisplayer.getAsyncGifysAvailable()) {
            testGifs = gifDisplayer.getAsyncGifys();
            testGifs.stream().forEach(Gif::play);
        }
        if (testGifs.size() > 0){
            int x = Settings.GIFY_X;
            int y = Settings.GIFY_Y;
            int w = Settings.GIFY_W;
            int h = Settings.GIFY_H;
            image( testGifs.get( ( frameCount / 5 ) % testGifs.size() ), x, y, w, h );

        }
        if (System.currentTimeMillis() > millisLastInteraction + Settings.CLI_RESET_DELAY_MILLIS) {
            cli.reset();
        }
    }

    public void keyPressed() {
        millisLastInteraction = System.currentTimeMillis();

        if (cli.isActive() || !cli.isReadyForInput()) {
            key = 0;
            return;
        }

        if (key == CODED) {
            switch (keyCode) {
                case KeyEvent.VK_F1:
                    cli.reset();
                    break;
            }
        } else {
            switch (key) {
                case BACKSPACE:
                    cli.backspace();
                    break;
                case ENTER:
                    if (!cli.available()) {
                        return;
                    }
                    processInput();
                    break;
                case TAB:
                case DELETE:
                    break;
                case ESC:
                    key = 0;
                    cli.reset();
                    break;
                default:
                    if (!cli.isActive()) {
                        cli.type(key);
                    }
                    break;
            }
        }
    }

    private void askLyrikViaThread(String text ) {
        cli.finishHack();
        String[] textSplit = text.split("\\s+");
        gifDisplayer.getGiyGifsAsnyc(textSplit,1);
        Thread thread = new Thread( () -> {
            lyrikRequestDone = false;
            newLyrikAnswer = askLyrik( text );
            lyrikRequestDone = true;
        } );
        thread.start();
    }

    private void processInput(){
        String inputText = cli.getUserInput().trim();
        String text = removeSpecialCharacters(inputText);

        String result = "";
        String logResult = "";

        //inputText = inputText.trim();
        if (useLyrik) {
            askLyrikViaThread(text);
            logResult = result;
        } else { // good old markov chain
            println(text);
            String[] results =  askLocalMarkov(text);
            result = results[0];
            logResult = results[1];
        }

        logger.log(logger.USER, inputText);
        logger.log( logger.ORACLE, logResult );

        System.out.println("u:::" + inputText);
        System.out.println("o:::" + logResult);

        //long delayMillis = cli.finish(result);
        if (startWebserver) {
            //server.sendTexts(inputText, result, delayMillis);
        }
    }

    private String askLyrik(String text) {
        PostRequest post = new PostRequest(Settings.LYRIK_URL);

        post.addData("inputS", text );
        try {
            long millis = millis();
            post.send();

            if (post != null) {
                println("Reponse Content: " + post.getContent());
                println("Reponse Content-Length Header: " + post.getHeader("Content-Length"));
                long millisDiff = millis() - millis;
                println("That took " + millisDiff + "ms");

                JSONParser json = new JSONParser();
                Object obj = json.parse(post.getContent());
                JSONObject mainJson = (JSONObject) (obj);
                String result = (String) mainJson.get("response");

                System.out.println("Received result: " + result);

                return result;
            }
        } catch (Exception exc) {
            exc.printStackTrace();
            return "yeah";
        }

        return "nothing";
    }

    private String[] askLocalMarkov(String text) {
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
        return new String[]{result,logResult};
    }

    private String removeSpecialCharacters(String input) {
        Pattern p = Pattern.compile("\\W*");
        Matcher matcher = p.matcher(input);
        matcher.find();
        if (matcher.start() == 0) {
            return matcher.replaceFirst("");
        } else
            return input;
    }

    public void webSocketServerEvent(String msg) {
        server.webSocketServerEvent(msg);
    }

    public void intercept(String message) {
        if (cli.interceptTypeNow(message)) {
            logger.log(logger.INTERCEPTION, message);
        }
    }

}
