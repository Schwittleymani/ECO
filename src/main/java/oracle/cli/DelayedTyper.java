package oracle.cli;

/**
 * Created by mrzl on 09.04.2016.
 */
public class DelayedTyper{
    private String textToType;
    private long delayMillisPerCharacter;
    private CLI cli;
    private long startMillis;

    public DelayedTyper( CLI cli ) {
        textToType = "";
        this.cli = cli;
        delayMillisPerCharacter = 50;
        startMillis = System.currentTimeMillis();
    }

    public void addText( String text ) {
        textToType += text;
        startMillis = System.currentTimeMillis();
    }

    public void addDelay( long millis ) {
        startMillis += millis;
    }

    public boolean isWaiting() {
        return System.currentTimeMillis() - startMillis > delayMillisPerCharacter;
    }

    /**
     * @return whether a new line should be set
     */
    public boolean update() {
        if( !isEmpty() ){
            if( !isWaiting() ){
                cli.type( textToType.charAt( 0 ) );
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

    public boolean isEmpty() {
        return textToType.isEmpty();
    }

    public String getText() {
        return textToType;
    }
}
