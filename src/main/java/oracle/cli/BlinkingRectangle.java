package oracle.cli;

import processing.core.PApplet;
import processing.core.PVector;

/**
 * Created by mrzl on 09.04.2016.
 */
public class BlinkingRectangle{
    private PApplet parent;
    private CLI cli;

    private float cursorBlockWidth;

    public BlinkingRectangle( PApplet parent, CLI cli ) {
        this.parent = parent;
        this.cli = cli;

        cursorBlockWidth = parent.textWidth( "a" );
    }

    public void draw( boolean doRotate) {
        float textWidth = parent.textWidth( cli.getLastLine().getText() );
        parent.pushMatrix();
        parent.translate( textWidth, - cli.textSize);

        float blockHeight = parent.constrain(cli.getTextSize() * parent.noise( parent.frameCount * 0.01f ) * 2,
                cli.getTextSize() * 0.7f,cli.getTextSize() * 1.3f);
        blockHeight = cli.textSize;

        if( doRotate ) {
            // rotates the blinking square when its thinking
            PVector centerOfBlinkingBox = new PVector(   cursorBlockWidth / 2 ,   blockHeight / 2  );
            parent.translate( centerOfBlinkingBox.x, centerOfBlinkingBox.y );
            parent.rotate( ( parent.frameCount ) );
            parent.translate( - centerOfBlinkingBox.x, - centerOfBlinkingBox.y );
        }
        parent.pushStyle();
        parent.strokeWeight( 2 );

        int textColor = ( parent.millis() % ( 255 * 4 ) ) / 4;
        parent.stroke( 0, textColor, 0 );

        if( parent.random( 1 ) < 0.04f ){
            parent.noFill();
        }

         parent.rect(0, 0 ,
                cursorBlockWidth,blockHeight);
        // for debugging
        //parent.fill(255);
        //parent.ellipse(0,0,6,6);

        parent.popStyle();
        parent.popMatrix();
    }
}
