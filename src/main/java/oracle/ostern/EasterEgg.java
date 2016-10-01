package oracle.ostern;

import oracle.Oracle;
import processing.data.JSONObject;

import processing.core.PApplet;

/**
 * Created by mrzl on 07.04.2016.
 */
public abstract class EasterEgg {

    static Jesus jesus;
    public Jesus.EASTEREGG_TYPE type;

    protected static Oracle oracle;
    private long startedMillis;

    private float chance;
    private long durationMillis;

    public EasterEgg(Jesus.EASTEREGG_TYPE type, JSONObject config) {
        this.type = type;
        if(config.getBoolean("active")) {
            jesus.addEasterEgg(this);
            this.chance = config.getFloat("chance");
        }
    }

    public abstract void drawBefore ();

    public abstract boolean drawAfter ();

    public EasterEgg start () {
        startedMillis = System.currentTimeMillis( );
        return this;
    }

    public boolean isRunning () {
        return Jesus.jesusTime > startedMillis
                && Jesus.jesusTime < startedMillis + durationMillis;
    }

    public boolean tryStart(){
        if(Math.random() < chance) {
            start();
            return true;
        }
        else {
            return false;
        }
    }

    public abstract void start(Object obj);
}
