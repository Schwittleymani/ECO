package oracle.ostern;

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

    int MAX_FLAKES = 20;
    int INIT_FLAKES = 4;
    float FLAKE_CHANCE = 0.015f;

    Range radiusRange = new Range(30,70);
    Range xMoveSpeedRange = new Range(0.04f,0.08f);
    Range yMoveSpeedRange = new Range(0.3f,0.7f);
    Range xMoveRandomRange = new Range(-0.1f,0.1f);
    Range xMoveMaxRange = new Range(0.5f,1f);

    //private PImage emojiSheet;

    //ArrayList<PImage> emojiSet = new ArrayList<PImage>();
    PImage heart;

    public EmojiEasterEgg () {
        super(Jesus.EASTEREGG_TYPE.ANSWER,null);
        //emojiSheet = parent.loadImage("sheet_32.png");
        //emojiSet.add(getEmoji(3, 7)); // heart
        heart = oracle.loadImage("heart.png");
        for(int i=0; i < INIT_FLAKES;i++)
            flakes.add(new Flake());
    }

    @Override
    public void drawBefore () {
        if (isRunning()) {
            for (Iterator<Flake> iterator = flakes.iterator(); iterator.hasNext(); ) {
                Flake c = iterator.next();
                if(!c.foreground){
                    c.draw();
                }
            }
        }
        if(super.isRunning()) {
            if (flakes.size() < MAX_FLAKES && oracle.random(1) < FLAKE_CHANCE)
                flakes.add(new Flake());
        }
    }

    @Override
    public boolean drawAfter() {
        if (isRunning()) {
            for (Iterator<Flake> iterator = flakes.iterator(); iterator.hasNext(); ) {
                Flake c = iterator.next();
                if (c.done) {
                    iterator.remove();
                } else if(c.foreground){
                    c.draw();
                }
            }
            return true;
        } else
            return false;
    }

    public boolean isRunning() {
        return super.isRunning() || flakes.size() > 0;
    }

    @Override
    public void start(Object obj) {

    }

    class Flake {

        PVector pos;
        boolean foreground;
        boolean done = false;
        private int index;
        PImage emoji;
        float radius;
        float phaseShift = oracle.random(oracle.TAU);
        float xMoveSpeed;
        float yMoveSpeed;
        float xMoveMax;


        Flake() {
            radius = radiusRange.get();
            pos = new PVector(oracle.random(oracle.width), -radius);
            xMoveSpeed = xMoveSpeedRange.get();
            yMoveSpeed = yMoveSpeedRange.get();
            xMoveMax = xMoveMaxRange.get();
            index = nextIndex++;
            emoji = heart;//emojiSet.get((int)parent.random(emojiSet.size()));
            foreground = oracle.random(1) <0.5f;
        }

        void updatePos() {
            float xOff = oracle.sin(phaseShift+(index+oracle.frameCount)*xMoveSpeed) * xMoveMax
                    +xMoveRandomRange.get();
            float yAdd = oracle.map(oracle.abs(xOff), 0, 1, 0.4f, -0.2f);

            pos.add(xOff, yMoveSpeed + yAdd);
            if (pos.y > oracle.height + radius) {
                done = true;
            }
        }

        void draw() {
            updatePos();
            oracle.image(emoji,pos.x,pos.y,radius,radius);
        }
    }


    /*PImage getEmoji(int x, int y) {
        return emojiSheet.get(x*32, y*32, 32, 32);
    }*/

    class Range {

        float min, max;

        Range(float min, float max) {
            this.min = min;
            this.max = max;
        }

        float get() {
            return oracle.random(min, max);
        }
    }
}
