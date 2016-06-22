package oracle;

import oracle.markov.MarkovChain;
import oracle.markov.MarkovQueue;
import oracle.markov.MarkovResult;
import processing.core.PApplet;

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by mrzl on 06.04.2016.
 */
public class MarkovManager extends ArrayList< MarkovChain >{

    private int maxAnswerLength = 150;
    private String authorName;

    public MarkovManager() {
    }

    String[] strip( String input ) {
        input = input.replace( "?", "" )
                .replace( "!", "" )
                .replace( ".", "" )
                .replace( ",", "" )
                .replace( "#", "" )
                .replace( "?", "" )
                .replace( "$", "" )
                .replace( "%", "" )
                .replace( "&", "" )
                .replace( "/", "" )
                .replace( "(", "" )
                .replace( ")", "" )
                .replace( "=", "" )
                .replace( ";", "" )
                .replace( ":", "" )
                .replace( "_", "" )
                .toLowerCase();
        String[] inputWords = input.split( " " );
        return inputWords;
    }

    public String getAnswer( String input ) {
        String answer = "";

        answer = check( strip( input ) );

        if( answer.equals( "nothing" ) ){
            String noAnswer = "i don't care about this. let's talk about \"" + get( 0 ).generateSentence().split( " " )[ 0 ] + "\" instead?";
            //noAnswer = check( get( 0 ).generateSentence().split( " " )[ 0 ].split( " " ) );

            answer = getRandomAnswer();
            //return answer;
        }

        if( answer.length() > maxAnswerLength ){
            //answer = answer.substring( 0, maxAnswerLength );
            answer = cropTooLongAnswer( answer, maxAnswerLength );
        }

        ArrayList< String > charsToRemove = new ArrayList<>();
        charsToRemove.add( "€" );
        charsToRemove.add( "˜" );
        charsToRemove.add( "â" );
        charsToRemove.add( "™" );
        charsToRemove.add( "œ" );
        charsToRemove.add( "¦" );

        for ( String s : charsToRemove ) {
            answer = answer.replace( s, "" );
        }

        answer.replace( "“", "\"" );
        answer.replace( "”", "\"" );
        answer.replace( "’", "'" );
        answer.replace( "?", "?" );

        answer = answer.trim();
        return answer;
    }

    private String cropTooLongAnswer( String answer, int maxAnswerLength ) {
        int index = answer.indexOf( "." );
        while ( index >= 0 ) {
            index = answer.indexOf( ".", index + 1 );
            if( index > maxAnswerLength ){
                return answer.substring( 0, index );
            }
        }

        return answer;
    }

    /**
     * TODO: merge this method with getMarkovDepthOrder()
     * @param input
     * @return
     */
    private String check( String[] input ) {
        MarkovQueue queue = new MarkovQueue( input.length );
        if( queue.getOrder() - 1 >= size() ){
            input = Arrays.copyOfRange( input, 0, size() - 1 );
            queue = new MarkovQueue( input.length );
        }

        for ( String s : input ) {
            queue.addLast( s );
        }
        String result = get( queue.getOrder() - 1 ).generateSentence( queue );
        if( result.equals( "nothing" ) ){
            if( input.length < 2 ){
                return "nothing";
            }

            String[] subarray = Arrays.copyOfRange( input, 0, input.length - 1 );
            result = check( subarray );
        }

        return result;
    }

    /**
     * TODO: merge this function with check()
     *
     * @param input
     * @return
     */
    public int getMarkovDepthOrder( String[] input ) {
        MarkovQueue queue = new MarkovQueue( input.length );
        if( queue.getOrder() - 1 >= size() ){
            input = Arrays.copyOfRange( input, 0, size() - 1 );
            queue = new MarkovQueue( input.length );
        }

        for ( String s : input ) {
            queue.addLast( s );
        }
        String result = get( queue.getOrder() - 1 ).generateSentence( queue );

        int depth = input.length;
        if( result.equals( "nothing" ) ){
            if( input.length < 2 ){
                return 0;
            }

            String[] subarray = Arrays.copyOfRange( input, 0, input.length - 1 );
            depth = getMarkovDepthOrder( subarray );
        }
        return depth;
    }

    MarkovResult query( String[] input ) {
        return new MarkovResult( check( input ), getMarkovDepthOrder( input ) );
    }

    public void train( String fileName, String authorName, boolean doExport ) {
        this.authorName = authorName;

        System.out.println( "Trainging with text from " + fileName + ".txt" );
        for ( int i = 1; i < Settings.MAX_INPUT_WORDS + 1; i++ ) {
            String text = loadText( "data" + File.separator + fileName + ".txt" );
            MarkovChain chain = new MarkovChain( i );

            chain.train( text );
            add( chain );
            System.out.println( "Training chain with order " + i );
        }
        if( doExport ){
            for ( MarkovChain chain : this ) {
                String _fileName = "data" + File.separator + "bin" + File.separator + authorName + "_" + chain.getOrder() + ".data";
                try {
                    ObjectOutputStream obj_out = new ObjectOutputStream(
                            new FileOutputStream( _fileName )
                    );
                    obj_out.writeObject( chain );
                } catch ( FileNotFoundException e ) {
                    e.printStackTrace();
                } catch ( IOException e ) {
                    e.printStackTrace();
                }
                System.out.println( "Saved markov chain to " + _fileName );
            }
        }
    }

    public void load( String authorName ) {
        this.authorName = authorName;
        try {
            for ( int i = 1; i < Settings.MAX_INPUT_WORDS + 1; i++ ) {
                String fileName = "data" + File.separator + "bin" + File.separator + authorName + "_" + i + ".data";
                FileInputStream f_in = new FileInputStream( fileName );
                ObjectInputStream obj_in = new ObjectInputStream( f_in );
                Object obj = obj_in.readObject();

                if( obj instanceof MarkovChain ){
                    add( ( MarkovChain ) obj );
                }

                System.out.println( "Loaded from " + fileName + ". With order " + get( size() - 1 ).getOrder() );
            }
        } catch ( FileNotFoundException e ) {
            e.printStackTrace();
        } catch ( ClassNotFoundException e ) {
            e.printStackTrace();
        } catch ( IOException e ) {
            e.printStackTrace();
        }
    }

    private String loadText( String fileName ) {
        String completeText = "";

        try {
            FileInputStream in = new FileInputStream( fileName );
            BufferedReader br = new BufferedReader( new InputStreamReader( in ) );
            String strLine;

            while ( ( strLine = br.readLine() ) != null ) {
                if( !strLine.isEmpty() ){
                    completeText += stripTextFromSpecialCharacters( strLine );
                }
            }

        } catch ( Exception e ) {
            System.out.println( e );
        }

        return completeText.toLowerCase();
    }

    private String stripTextFromSpecialCharacters( String line ) {

        ArrayList< String > charactersToRemove = new ArrayList<>();
        charactersToRemove.add( ")" );
        charactersToRemove.add( "”" );
        charactersToRemove.add( "\"" );
        charactersToRemove.add( "(" );
        charactersToRemove.add( "[" );
        charactersToRemove.add( "]" );
        charactersToRemove.add( "—" );
        charactersToRemove.add( "-" );
        charactersToRemove.add( "_" );
        charactersToRemove.add( "“" );
        charactersToRemove.add( "’" );
        charactersToRemove.add( ":" );
        charactersToRemove.add( ";" );
        charactersToRemove.add( "," );

        line = line.replaceAll( "\\(.*\\)", "" );
        line = line.replaceAll( "\\[.*\\]", "" );

        for ( String s : charactersToRemove ) {
            line = line.replace( s, "" );
        }

        return line;
    }

    public String getRandomAnswer() {
        return Settings.RANDOM_ANSWERS.get( ( PApplet.floor( ( float ) Math.random() * Settings.RANDOM_ANSWERS.size() ) ) ).toLowerCase();
    }

    public String getAuthorName() {
        return authorName;
    }
}
