package oracle.ostern;

import processing.core.PApplet;
import processing.core.PImage;
import processing.core.PVector;

import java.util.ArrayList;
import java.util.Iterator;

/**
 * Created by mrzl on 07.04.2016.
 */
public class EmojiEasterEgg extends
        EasterEgg {


    ArrayList<Flake> flakes = new ArrayList<Flake>();
    static int nextIndex = 0;

    int MAX_FLAKES = 10;
    int INIT_FLAKES = 4;
    float FLAKE_CHANCE = 0.02f;

    Range radiusRange = new Range(12,30);
    Range xMoveSpeedRange = new Range(0.04f,0.08f);
    Range yMoveSpeedRange = new Range(0.3f,0.7f);
    Range xMoveRandomRange = new Range(-0.1f,0.1f);
    Range xMoveMaxRange = new Range(0.5f,1f);

    private PImage emojiSheet;

    ArrayList<PImage> emojiSet = new ArrayList<PImage>();


    public EmojiEasterEgg ( PApplet parent, float durationSeconds ) {
        super( parent, durationSeconds );

        emojiSheet = parent.loadImage("sheet_32.png");
        emojiSet.add(getEmoji(3, 7)); // heart
        for(int i=0; i < INIT_FLAKES;i++)
            flakes.add(new Flake());
    }

    @Override
    public void drawBefore () {
        if ( isRunning( ) ) {
            parent.println("EMOJI TIME");
            for (Iterator<Flake> iterator = flakes.iterator(); iterator.hasNext(); ) {
                Flake c = iterator.next();
                if (c.done) {
                    iterator.remove();
                } else if(!c.foreground){
                    c.draw();
                }
            }
        }
        if(super.isRunning()) {
            if (flakes.size() < MAX_FLAKES && parent.random(1) < FLAKE_CHANCE)
                flakes.add(new Flake());
        }
    }

    @Override
    public void drawAfter () {
        if ( isRunning( ) ) {
            for (Iterator<Flake> iterator = flakes.iterator(); iterator.hasNext(); ) {
                Flake c = iterator.next();
                if (c.done) {
                    iterator.remove();
                } else if(c.foreground){
                    c.draw();
                }
            }
        }
    }




    public boolean isRunning() {
        return super.isRunning() && flakes.size() == 0;
    }

    class Flake {

        PVector pos;
        boolean foreground;
        boolean done = false;
        private int index;
        PImage emoji;
        float radius;
        float phaseShift = parent.random(parent.TAU);
        float xMoveSpeed;
        float yMoveSpeed;
        float xMoveMax;


        Flake() {
            radius = radiusRange.get();
            pos = new PVector(parent.random(parent.width), 0);
            xMoveSpeed = xMoveSpeedRange.get();
            yMoveSpeed = yMoveSpeedRange.get();
            xMoveMax = xMoveMaxRange.get();
            index = nextIndex++;
            emoji = emojiSet.get((int)parent.random(emojiSet.size()));
            foreground = parent.random(1) <0.5f;
        }

        void updatePos() {
            float xOff = parent.sin(phaseShift+(index+parent.frameCount)*xMoveSpeed) * xMoveMax
                    +xMoveRandomRange.get();
            float yAdd = parent.map(parent.abs(xOff), 0, 1, 0.4f, -0.2f);

            pos.add(xOff, yMoveSpeed + yAdd);
            if (pos.y > parent.height + radius) {
                done = true;
            }
        }

        void draw() {
            updatePos();
            parent.image(emoji,pos.x,pos.y,radius,radius);
        }
    }


    PImage getEmoji(int x, int y) {
        return emojiSheet.get(x*32, y*32, 32, 32);
    }

    class Range {

        float min, max;

        Range(float min, float max) {
            this.min = min;
            this.max = max;
        }

        float get() {
            return parent.random(min, max);
        }
    }
}
