package oracle.test;

import gifAnimation.Gif;
import oracle.Oracle;
import oracle.gif.GifDisplayer;
import processing.core.PApplet;

/**
 * Created by raminsoleymani on 16/10/16.
 */
public class GifMemoryTest extends Oracle {

    GifDisplayer gif;
    Gif display;

    boolean roll = true;
    long lastSwitch = 0;
    long runTime = 3000;

    public static void main(String[] args) {
        PApplet.main( "oracle.test.GifMemoryTest" );
    }

    public void settings() {
        size(640, 480, P3D);

    }

    public void setup() {

        gif = new GifDisplayer(this);
        display = gif.getRandomGif("gify");
        display.loop();
    }

    public void draw() {

        if(roll) {
            if(millis() > lastSwitch + runTime){
                if(display != null) {
                    display.stop();
                    display.dispose();
                    System.gc();
                }
                display = gif.getRandomGif("gify");
                display.loop();
                lastSwitch = millis();
            }
        }

        if(display != null){
            image(display,0,0);
        }
    }
}
