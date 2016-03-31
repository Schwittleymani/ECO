package oracle;

import java.util.ArrayList;

/**
 * Created by mrzl on 31.03.2016.
 */
public class CLI {

    private ArrayList< String > characters;

    public CLI() {
        characters = new ArrayList<>( );
    }

    public void type( char key ) {
        characters.add( new String( String.valueOf( key ) ) );
    }

    public void clear() {
        characters.clear( );
    }

    public String getText() {
        return String.join( "", characters );
    }

    public void backspace() {
        if( characters.size() == 0 ) {
            return;
        }
        characters.remove( characters.size( ) - 1 );
    }
}
