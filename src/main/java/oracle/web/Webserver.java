package oracle.web;

import http.DynamicResponseHandler;
import http.ResponseBuilder;
import http.SimpleHTTPServer;
import oracle.Oracle;
import oracle.Settings;
import processing.core.PApplet;
import processing.data.JSONObject;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Stream;

/**
 * Created by raminsoleymani on 09/04/16.
 */
public class Webserver {

    SimpleHTTPServer server;
    Oracle Pparent;

    String input = "";
    boolean waitingForResponse;

    public Webserver(PApplet parent) {
        server = new SimpleHTTPServer(parent);
        this.Pparent = ( Oracle )parent;

        server.createContext("getLog", new DynamicResponseHandler(new SessionLog(), "application/json"));
        server.createContext("intercept", new DynamicResponseHandler(new Intercepter(), "application/json"));

        Settings.printIps();
    }

    public void sendInput(String input) {
        this.input = input;
        waitingForResponse = true;
    }


    class SessionLog extends ResponseBuilder {

        public  String getResponse(String requestBody) {
            JSONObject json = new JSONObject();
            StringBuilder sb = new StringBuilder();
            try (Stream<String> stream = Files.lines(Paths.get(Pparent.sketchPath()+"/session.log"))) {
                stream.forEach(sb::append);
            } catch (IOException e) {
                e.printStackTrace();
            }
            json.setString("text", sb.toString());
            return json.toString();
        }
    }

    class Intercepter extends ResponseBuilder {
        public String getResponse(String requestBody) {
            //Pparent.println("req body",requestBody);
            if (!requestBody.equals("")) {
                //Pparent.println("req:",requestBody);
                JSONObject req = Pparent.parseJSONObject(requestBody);
                if (req.hasKey("requestInput")) {
                    //Pparent.println("-");
                    JSONObject json = new JSONObject();
                    json.setString("text", input);
                    return json.toString();
                } else if (req.hasKey("response")) {
                    String response = req.getString("response");
                    Pparent.responseFromTheWeb(response);
                    waitingForResponse = false;
                    JSONObject json = new JSONObject();
                    json.setString("status", "okay");
                    return json.toString();
                }
            }
            JSONObject json = new JSONObject();
            Pparent.intercept();
            input = "";
            waitingForResponse = false;
            json.setString("status", "okay");
            return json.toString();
            /*if(Pparent.intercept() || input.equals("")) { // not yet intercepting
                input = "";
                waitingForResponse = false;
                json.setString("status", "okay");
                return json.toString();
            } else { // input already typed in


            }*/
        }
    }
}
