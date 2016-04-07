package oracle.ostern;

import processing.core.PApplet;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Optional;

/**
 * Created by raminsoleymani on 07/04/16.
 * Jesus manages the easter eggs
 */
public class Jesus {

    public enum EASTEREGG_TYPE {EMOJI}

    PApplet parent;

    protected static long jesusTime;

    private HashMap< EASTEREGG_TYPE, EasterEgg > easterEggs = new HashMap<>();
    Optional<EasterEgg> runningEgg;

    public Jesus(PApplet p) {
        parent = p;
        runningEgg = Optional.empty();
        EasterEgg.parent = p;
        EasterEgg.jesus = this;
        new EmojiEasterEgg();
    }

    public void start(EASTEREGG_TYPE type, long durationSeconds) {
        if(!runningEgg.isPresent()) {
            runningEgg = Optional.of(easterEggs.get(type).start(durationSeconds*1000));
        }
    }

    public void drawBeforeEaster() {
        jesusTime = System.currentTimeMillis();
        if(runningEgg.isPresent())
                runningEgg.get().drawBefore();
    }

    public void drawAfterEaster() {
        if(runningEgg.isPresent())
            if(!runningEgg.get().drawAfter())
                runningEgg = Optional.empty();
    }

    public void addEasterEgg(EasterEgg egg) {
        easterEggs.put(egg.type,egg);
    }

}
