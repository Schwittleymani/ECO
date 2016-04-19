package oracle.ostern;

import processing.core.PApplet;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Optional;

/**
 * Created by raminsoleymani on 07/04/16.
 * Jesus manages the easter eggs
 */
public class Jesus {

    public enum EASTEREGG_TYPE {MONOLOG, EMOJI}

    PApplet parent;

    protected static long jesusTime;

    private HashMap< EASTEREGG_TYPE, EasterEgg > easterEggs = new HashMap<>();
    ArrayList<EasterEgg> runningEggs = new ArrayList<>();

    public Jesus(PApplet p) {
        parent = p;

        EasterEgg.parent = p;
        EasterEgg.jesus = this;
        new EmojiEasterEgg();
    }

    public void start(EASTEREGG_TYPE type, long durationSeconds) {
        runningEggs.add(easterEggs.get(type).start(durationSeconds*1000));
    }

    public void drawBeforeEaster() {
        jesusTime = System.currentTimeMillis();
        for(EasterEgg egg : runningEggs)
            egg.drawBefore();
    }

    public void drawAfterEaster() {
        ArrayList<EasterEgg> removeEggs = new ArrayList<>();
        for(EasterEgg egg : runningEggs)
            if(!egg.drawAfter())
                removeEggs.add(egg);
        runningEggs.removeAll(removeEggs);
    }

    public void addEasterEgg(EasterEgg egg) {
        easterEggs.put(egg.type,egg);
    }

}
