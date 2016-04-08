package oracle;

import oracle.cli.CLI;
import processing.core.PApplet;

import java.awt.event.KeyEvent;
import java.util.logging.Logger;

/**
 * Created by mrzl on 31.03.2016.
 */
public class LacunaLabOracle extends PApplet {

    public static String EXPORT_FILENAME_PREFIX = "lacuna_markov_export-order";
    public static int MAX_INPUT_WORDS = 8;
    private CLI cli;
    private MarkovManager markov;

    Logger allnowingLogger = Logger.getLogger("input");

    long millisLastInteraction;
    long idleDelay = 120 * 1000; // 2 minutes

    public void settings() {
        size(640, 480);
        new OracleLogger();
        allnowingLogger.setUseParentHandlers(false);
        //fullScreen( );

        millisLastInteraction = System.currentTimeMillis();
    }

    public void setup() {
        cli = new CLI(this);
        markov = new MarkovManager();

        //markov.save();
        markov.load();

        noCursor();
    }

    public void draw() {
        background(0);
        cli.draw();

        if( System.currentTimeMillis() > millisLastInteraction + idleDelay ) {
            cli.reset();
        }
    }

    public void keyPressed() {
        millisLastInteraction = System.currentTimeMillis();

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
                    String inputWordsString = cli.getLastLine().getText(true);
                    String result = markov.getAnswer(inputWordsString);

                    if (result.contains("lacuna")) {
                        cli.startEmojiEasterEgg();
                    }

                    allnowingLogger.severe("u:::" + inputWordsString);
                    allnowingLogger.severe("o:::" + result);

                    System.out.println(result);
                    cli.finish(result, calculateDelayByInputLength(inputWordsString.split(" ").length));
                    break;
                case TAB:
                case DELETE:
                    break;
                case ESC:
                    cli.reset();
                    break;
                default:
                    cli.type(key);
                    break;
            }
        }
    }

    private long calculateDelayByInputLength(int length) {
        return (long) map(length, 1, 8, 400, 5000);
    }
}
