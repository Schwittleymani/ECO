package oracle;

import oracle.markov.MarkovChain;
import oracle.markov.MarkovQueue;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Created by mrzl on 06.04.2016.
 */
public class MarkovManager extends ArrayList< MarkovChain >{

    private int maxAnswerLength = 150;

    public MarkovManager() {
    }

    public String getAnswer( String input ) throws Exception {
        String answer = "";

        input.replace( "?", "" )
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
        answer = check( inputWords );

        if( answer.equals( "nothing" ) ) {
            String noAnswer = "i don't care about this. let's talk about \"" + get( 0 ).generateSentence().split( " " )[ 0 ] + "\" instead?";
            //noAnswer = check( get( 0 ).generateSentence().split( " " )[ 0 ].split( " " ) );

            answer = noAnswer;
            throw new Exception(  );
        }

        //System.out.println( "New answer: " + get( 0 ).generateSentence().split( " " )[ 0 ].split( " " ) );

        if( answer.length() > maxAnswerLength ){
            answer = answer.substring( 0, maxAnswerLength );
        }

        return answer;
    }

    String check( String[] input ) {
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

    public void save( String fileName ) {
        for ( int i = 1; i < LacunaLabOracle.MAX_INPUT_WORDS + 1; i++ ) {
            MarkovChain chain = new MarkovChain( i );
            chain.train( loadText( "data" + File.separator + fileName ) );
            add( chain );
            System.out.println( "Training chain with order " + i );
        }

        for ( MarkovChain chain : this ) {
            String _fileName = "data" + File.separator + LacunaLabOracle.EXPORT_FILENAME_PREFIX + chain.getOrder() + ".data";
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

    public void load() {
        try {
            for ( int i = 1; i < LacunaLabOracle.MAX_INPUT_WORDS + 1; i++ ) {
                String fileName = "data" + File.separator + LacunaLabOracle.EXPORT_FILENAME_PREFIX + i + ".data";
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
        System.out.println( "Loaded markov chain from " + LacunaLabOracle.EXPORT_FILENAME_PREFIX );
    }

    private String loadText( String fileName ) {
        String completeText = "";
        try ( Stream< String > stream = Files.lines( Paths.get( fileName ), StandardCharsets.UTF_8 ) ) {

            String s = stream.collect( Collectors.joining() );
            completeText += s;

        } catch ( IOException e ) {
            e.printStackTrace();
        }

        return completeText.toLowerCase();
    }
}
