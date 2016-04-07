package oracle.ostern;

import processing.core.PApplet;

/**
 * Created by mrzl on 07.04.2016.
 */
public abstract class EasterEgg {

    static Jesus jesus;
    public final Jesus.EASTEREGG_TYPE type;

    protected static PApplet parent;
    private long durationMillis;
    private long startedMillis;

    public EasterEgg(Jesus.EASTEREGG_TYPE type) {
        this.type = type;
        jesus.addEasterEgg(this);
    }

    public abstract void drawBefore ();

    public abstract boolean drawAfter ();


    public EasterEgg start (long durationMillis) {
        this.durationMillis = durationMillis;
        startedMillis = System.currentTimeMillis( );
        return this;
    }

    public boolean isRunning () {
        return Jesus.jesusTime > startedMillis
                && Jesus.jesusTime < startedMillis + durationMillis;
    }
}
