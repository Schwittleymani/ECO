package oracle.ostern;

/**
 * Created by mrzl on 08.04.2016.
 */
public class MonologueEasterEgg extends EasterEgg {

    int alpha;

    public MonologueEasterEgg() {

        super(Jesus.EASTEREGG_TYPE.PAUSE,null);
    }

    public EasterEgg start (long durationMillis) {
        super.start();

        alpha = 255;

        return this;
    }

    @Override
    public void drawBefore() {
        if( alpha > 0 ) {
            alpha--;
        }
        oracle.fill( 0, 255, 0, alpha );
    }

    @Override
    public boolean drawAfter() {
        return false;
    }

    @Override
    public void start(Object obj) {

    }
}
