package oracle.markov;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.TreeMap;

/**
 * Created by mrzl on 01.04.2016.
 */
public class MarkovChain2 {
    private final static String START_WORD = "phone";
    private final static String PUNCTUATIONS = ".,!?:;";
    private static TreeMap< String, List< NextWord > > map;

    private static class NextWord {
        private String word;
        private int count;  // keeps track of frequency

        public void increaseCount () {
            count++;
        }

        public int getCount () {
            return count;
        }

        public String getWord () {
            return word;
        }

        public NextWord ( String word, int count ) {
            this.word = word;
            this.count = count;
        }
    }

    private static void addToMarkovChain ( ArrayList< String > sentence ) {
        for ( int i = 1; i < sentence.size( ) - 2; i++ ) {
            String key = sentence.get( i ) + "+" + sentence.get( i + 1 );
            String nextWord = sentence.get( i + 2 );
            if ( i == 1 ) key = sentence.get( 0 ) + "+" + key;  // only first key contains three words
            if ( map.containsKey( key ) ) {
                List< NextWord > list = map.get( key );
                boolean seen = false;
                for ( NextWord w : list ) {
                    if ( w.getWord( ).equals( nextWord ) ) {
                        w.increaseCount( );
                        seen = true;
                        break;
                    }
                }
                if ( !seen ) list.add( new NextWord( nextWord, 1 ) );
            } else {
                List< NextWord > list = new ArrayList< NextWord >( );
                list.add( new NextWord( nextWord, 1 ) );
                map.put( key, list );
            }
        }
    }

    private static String sentenceWithStartKey ( String key ) {
        String strippedKey = key.replace( START_WORD + "+", "" );
        String firstWord = strippedKey.substring( 0, strippedKey.indexOf( "+" ) );  // get substring before '+'
        String secondWord = strippedKey.substring( strippedKey.indexOf( "+" ) + 1 );  // get substring after '+'
        String result = firstWord + " " + secondWord;
        while ( map.containsKey( key ) ) {  // build the sentence
            List< NextWord > list = map.get( key );
            NextWord next = list.get( 0 );  // if only one case, pick that
            if ( list.size( ) > 1 ) {        // if multiple cases could follow, pick randomly according to frequency
                int totalCount = 0;
                for ( NextWord w : list ) totalCount += w.getCount( );
                int randNum = ( int ) Math.ceil( Math.random( ) * totalCount );
                for ( int i = 0; i < list.size( ); i++ ) {
                    randNum -= list.get( i ).getCount( );
                    if ( randNum <= 0 ) {
                        next = list.get( i );
                        break;  // pick the next word according to probability
                    }
                }
            }
            result = ( PUNCTUATIONS.contains( next.getWord( ) ) ) ? result + next.getWord( ) : result + " " + next.getWord( );
            key = secondWord + "+" + next.getWord( );  // build the next key to continue on the chain
            secondWord = next.getWord( );
        }
        return result;
    }

    public static void main ( String[] args ) {
        try {
            String filename = "lacuna_lab_texts.txt";  //String filename = "tao_te_ching.txt";
            Scanner in = new Scanner( new File( filename ) );
            ArrayList< String > sentence = new ArrayList< String >( );  // to hold a sentence temporarily for processing
            sentence.add( START_WORD );
            map = new TreeMap< String, List< NextWord > >( String.CASE_INSENSITIVE_ORDER );  // case insensitive for keys
            while ( in.hasNext( ) ) {
                String word = in.next( );
                word = word.replace( "\"", "" ).replaceAll( "[0-9]", "" );  // removes double quotes and numbers
                if ( word.length( ) == 0 ) continue;  // ignore empty line
                if ( word.contains( "." ) || word.contains( "?" ) || word.contains( "!" ) ) {  // is ending word
                    sentence.add( word.substring( 0, word.length( ) - 1 ) );  // add the word
                    sentence.add( word.substring( word.length( ) - 1 ) );     // add the end punctuation
                    addToMarkovChain( sentence );  // process the sentence
                    sentence.clear( );
                    sentence.add( START_WORD );
                } else {  // in the middle of a sentence
                    if ( word.contains( ":" ) || word.contains( "," ) ) {  // contains other allowed punctuations
                        sentence.add( word.substring( 0, word.length( ) - 1 ) );  // add the word
                        sentence.add( word.substring( word.length( ) - 1 ) );     // add the punctuation
                    } else
                        sentence.add( word );
                }
            }
            System.out.println( "Printing out 20 sample sentences:\n--------------------------------------------------------------------------" );
            int i = 0;
            for ( String s : map.keySet( ) )
                if ( s.contains( START_WORD ) && i++ < 20 ) System.out.println( sentenceWithStartKey( s ) );
        } catch ( FileNotFoundException exception ) {
            System.out.println( "File not found" );
        }
    }
}