package oracle.ostern;

/**
 * Created by mrzl on 08.04.2016.
 */
public class MonologueEasterEgg extends EasterEgg {

    int alpha;

    public MonologueEasterEgg() {

        super(Jesus.EASTEREGG_TYPE.MONOLOG);
    }

    @Override
    public EasterEgg start (long durationMillis) {
        super.start(durationMillis);

        alpha = 255;

        return this;
    }

    @Override
    public void drawBefore() {
        if( alpha > 0 ) {
            alpha--;
        }
        parent.fill( 0, 255, 0, alpha );
    }

    @Override
    public boolean drawAfter() {
        return false;
    }
}
