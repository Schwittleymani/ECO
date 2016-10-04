package oracle.web;

import http.ResponseBuilder;
import http.SimpleHTTPServer;

import oracle.Oracle;
import processing.data.JSONObject;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Stream;


/**
 * Created by raminsoleymani on 09/04/16.
 */
public class Webserver{

    SimpleHTTPServer server;
    OracleWebsocketServer websocketServer;
    Oracle Pparent;

    public Webserver( Oracle parent ) {
        server = new SimpleHTTPServer( parent,9000);
        server.serve("pre-texts.js");
        websocketServer = new OracleWebsocketServer( parent );
        this.Pparent = parent;
    }

    public void sendInput(String input) {
        websocketServer.sendInput( input );
    }

    public void sendResult(String result, long timeout){
        websocketServer.sendResult(result,timeout);
    }

    public void finnish(String answer){
        websocketServer.sendFinnish(answer);
    }

    class SessionLog extends ResponseBuilder{

        public String getResponse( String requestBody ) {
            JSONObject json = new JSONObject();
            StringBuilder sb = new StringBuilder();
            try ( Stream< String > stream = Files.lines( Paths.get( Pparent.sketchPath() + "/session.log" ) ) ) {
                stream.forEach( sb::append );
            } catch ( IOException e ) {
                e.printStackTrace();
            }
            json.setString( "text", sb.toString() );
            return json.toString();
        }
    }


    public void webSocketServerEvent( String msg ) {
        websocketServer.webSocketServerEvent( msg );
    }
}
