package oracle.cli;

import processing.core.PApplet;

/**
 * Created by mrzl on 09.04.2016.
 */
public class BlinkingRectangle{
    private PApplet parent;
    private CLI cli;

    public BlinkingRectangle( PApplet parent, CLI cli ) {
        this.parent = parent;
        this.cli = cli;
    }

    public void draw() {
        parent.pushStyle();
        parent.strokeWeight( 2 );

        int textColor = ( parent.millis() % ( 255 * 4 ) ) / 4;
        parent.stroke( 0, textColor, 0 );
        float textWidth = parent.textWidth( cli.getLastLine().getText() );
        if( parent.random( 1 ) < 0.04f ){
            parent.noFill();
        }
        parent.rect( 40 + textWidth, cli.getLastLine().y - ( cli.textSize ),
                cli.cursorBlockWidth, cli.textSize + 10 * parent.noise( parent.frameCount * 0.01f ) );


        parent.popStyle();
    }
}
