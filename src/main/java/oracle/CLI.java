package oracle;

import processing.core.PApplet;

import java.util.ArrayList;
import java.util.Collections;

/**
 * Created by mrzl on 31.03.2016.
 */
public class CLI {


    int textSize = 20;
    int maxLineWidth = 560;
    int lineDistance = 10;
    private ArrayList< Line > lines = new ArrayList<>();
    private PApplet parent;

    public CLI( PApplet p ) {
        this.parent = p;
        lines.add(new Line());
    }

    void draw() {
        parent.fill( 0, 255, 0 );
        parent.textSize( textSize );

        for(int i=0; i < lines.size()-1;i++) {
            parent.text( lines.get(i).getText(), 50, 40 );
            parent.pushMatrix();
            parent.translate(0, textSize + lineDistance );
        }
        parent.text( getActLine().getText(), 50, 40 );
        float textWidth = parent.textWidth( getActLine().getText() );
            parent.pushStyle();
            parent.strokeWeight( 2 );
            int textColor = ( parent.millis() % (255*4)) / 4;
            parent.stroke( 0, textColor, 0 );
            parent.line(50 + textWidth + 5, 20, 50 + textWidth + 5, 25 + textSize);
            parent.popStyle();


        for(int i=0; i < lines.size()-1;i++) {
            parent.popMatrix();
        }
    }

    public void type( char key ) {
        Line act = getActLine();
        act.add( new String( String.valueOf( key ) ) );
        if(parent.textWidth(act.getText()) >= maxLineWidth) {
            lines.add(new Line());
        }
    }

    public void backspace() {
        getActLine().backspace();
    }

    public void clear() {
        lines.forEach(ArrayList::clear);
    }

    private Line getActLine() {
        return  lines.get(lines.size()-1);
    }

    class Line extends ArrayList<String> {

        public String getText() {
            return String.join( "", this );
        }

        public void backspace() {
            if( !isEmpty()) {
                remove( size( ) - 1 );
            }
        }
    }
}
