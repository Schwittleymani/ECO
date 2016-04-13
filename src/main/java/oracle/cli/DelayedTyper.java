package oracle.cli;

/**
 * Created by mrzl on 09.04.2016.
 */
public class DelayedTyper{
    private CLI cli;

    private String textToType;
    private long startMillis, delayMillisPerCharacter, initDelayStartMillis, initDelayMillis;

    public DelayedTyper( CLI cli ) {
        textToType = "";
        this.cli = cli;
        delayMillisPerCharacter = 50;
        startMillis = System.currentTimeMillis();
        initDelayStartMillis = System.currentTimeMillis();
        initDelayMillis = 0;
    }

    public void addText( String text ) {
        textToType += text;
        startMillis = System.currentTimeMillis();
    }

    public void addDelay( long millis ) {
        startMillis += millis;
        initDelayStartMillis = System.currentTimeMillis();
        initDelayMillis = millis;
    }

    public boolean isNotWaiting() {
        return System.currentTimeMillis() - startMillis > delayMillisPerCharacter;
    }

    public boolean isInitDelay() {
        return System.currentTimeMillis() - initDelayStartMillis < initDelayMillis;
    }

    /**
     * @return whether a new line should be set
     */
    public boolean update() {
        if( !isEmpty() ){
            if( isNotWaiting() ){
                type( textToType.charAt( 0 ) );
                textToType = textToType.substring( 1, textToType.length() );

                startMillis = System.currentTimeMillis();
            }
            if( isEmpty() ){
                // if last character was typed
                return true;
            }
        }

        return false;
    }

    public void type( char key ) {
        if( key == ' ' && cli.getLastLine().limitReachedOffset() ){
            cli.newLine();
        } else {
            cli.getLastLine().add( new String( String.valueOf( key ) ) );
        }
    }

    public void type( String string ) {
        String[] words = string.split( " " );
        Line act = cli.getLastLine();
        float actWidth = cli.getTextWidth( act.getText( false ) );
        for ( int i = 0; i < words.length; i++ ) {
            if( actWidth + cli.getTextWidth( words[ i ] ) > cli.getMaxLineWidth() ){
                cli.newLine();
                act = cli.getLastLine();
                actWidth = cli.getTextWidth( act.getText() );
            } else {
                act.add( words[ i ] + " " );
                actWidth = cli.getTextWidth( act.getText() );
            }
        }
    }

    public boolean isEmpty() {
        return textToType.isEmpty();
    }

    public String getText() {
        return textToType;
    }
}
