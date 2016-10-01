package oracle.ostern;

import oracle.Oracle;
import processing.data.JSONObject;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by raminsoleymani on 07/04/16.
 * Jesus manages the easter eggs
 */
public class Jesus {

    public enum EASTEREGG_TYPE {PAUSE,INTERRUPT,ANSWER}

    Oracle parent;

    protected static long jesusTime;

    private List<EasterEgg > easterEggs = new ArrayList<EasterEgg>();
    ArrayList<EasterEgg> runningEggs = new ArrayList<>();

    public Jesus(Oracle p) {
        parent = p;

        EasterEgg.oracle = p;
        EasterEgg.jesus = this;
        loadEastereggConfig();
    }

    public void tryStartAnswer(String response) {
        for(EasterEgg egg : easterEggs) {
            if (egg.type == EASTEREGG_TYPE.ANSWER) {
                boolean started = egg.tryStart();
                egg.start(response);
                if(started) {
                    runningEggs.add(egg);
                    return;
                }
            }
        }
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


    private void loadEastereggConfig() {
        JSONObject json = parent.loadJSONObject("eastereggs.json");
        // gifs
        new GifsEasterEgg(json.getJSONObject("Gifs"));
    }

    protected void addEasterEgg(EasterEgg egg) {
        easterEggs.add(egg);
    }
}
