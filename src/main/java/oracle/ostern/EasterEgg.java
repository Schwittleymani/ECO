package oracle.ostern;

import processing.core.PApplet;

/**
 * Created by mrzl on 07.04.2016.
 */
public abstract class EasterEgg {
    public enum EASTEREGG_TYPE {EMOJI}

    protected PApplet parent;
    private long durationMillis;
    private long startedMillis;



    public abstract void drawBefore ();

    public abstract void drawAfter ();

    public EasterEgg ( PApplet parent, float durationSeconds ) {
        this.parent = parent;
        this.durationMillis = ( long ) ( durationSeconds * 1000 );
    }

    public void start () {
        startedMillis = System.currentTimeMillis( );
    }

    public void stop () {
        startedMillis = System.currentTimeMillis( ) + durationMillis;
    }

    public boolean isRunning () {
        return System.currentTimeMillis( ) > startedMillis && System.currentTimeMillis( ) < startedMillis + durationMillis;
    }
}
