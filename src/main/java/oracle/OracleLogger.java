package oracle;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

/**
 * Created by mrzl on 21.06.2016.
 */
public class OracleLogger{

    private File sessionLogFile;

    SimpleDateFormat dateFormatter = new SimpleDateFormat("MM/dd/yyyy_HH:mm:ss");


    public OracleLogger() {
        new File("logs").mkdir();
        sessionLogFile = new File( "logs" + File.separator + "session_" + timestamp() + ".log" );
        //sessionLogFile.mkdirs();
    }

    private String timestamp() {
        Calendar now = Calendar.getInstance();
        return String.format( "%1$ty%1$tm%1$td_%1$tH%1$tM%1$tS", now );
    }

    public void log( String input, String answer ) {
        BufferedWriter bw = null;

        try {
            try {
                bw = new BufferedWriter( new FileWriter( sessionLogFile.getAbsolutePath(), true ) );
            } catch ( IOException e ) {
                e.printStackTrace();
            }
            String dateString  = dateFormatter.format(new Date());
            bw.write(dateString+":::u:::" + input );
            bw.newLine();
            bw.write(dateString+":::o:::" + answer );
            bw.newLine();
            bw.flush();
        } catch ( IOException ioe ) {
            ioe.printStackTrace();
        } finally {
            if( bw != null ) try {
                bw.close();
            } catch ( IOException ioe2 ) {
                ioe2.printStackTrace();
            }
        }
    }
}
