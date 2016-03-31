package oracle;

import processing.core.PApplet;
import processing.core.PSurface;

import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

/**
 * Created by mrzl on 31.03.2016.
 */
public class LacunaLabOracle extends PApplet {

    private CLI cli;

    public void settings() {
        size( 1920, 1080 );
        //fullScreen( );
    }

    static final void removeExitEvent(final PSurface surf) {
        final java.awt.Window win
                = ((processing.awt.PSurfaceAWT.SmoothCanvas) surf.getNative()).getFrame();

        for (final java.awt.event.WindowListener evt : win.getWindowListeners())
            win.removeWindowListener(evt);
    }

    public void setup() {
        removeExitEvent( getSurface() );

        cli = new CLI();
    }

    public void draw() {
    }

    public void keyPressed( ) {
        if( key == CODED ){
            switch( keyCode ) {
            }
        } else {
            switch( key ) {
                case BACKSPACE:
                    cli.backspace();
                    break;
                case ENTER:
                    cli.clear();
                    break;
                case TAB:
                case ESC:
                case DELETE:
                    break;
                default:
                    cli.type( key );
                    break;
            }
        }

        System.out.println( cli.getText() );
    }
}
