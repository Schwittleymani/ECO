package oracle.gif;

import http.requests.GetRequest;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.io.DataInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.net.InetAddress;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;
import java.util.StringJoiner;
import java.util.stream.Collectors;

/**
 * Created by raminsoleymani on 30/09/16.
 */
public class Gify {

    final String host = "http://api.giphy.com";
    final String searchPath = "/v1/gifs/search";
    // IMPORTANT. READ IT FROM A .gitignored file when not public anymore
    String apiKey = "dc6zaTOxFJmzC";

    int maxDownload = -1; // probably not very usefull...   

    //
    String[] GifyQualities = {"fixed_width", "downsized_still", "fixed_height_small_still",
            "fixed_width_downsampled", "fixed_width_small_still", "downsized_large",
            "fixed_width_still", "original_still", "fixed_height_still",
            "fixed_width_small", "fixed_height_downsampled", "looping",
            "downsized", "downsized_medium", "fixed_height", "original"
            , "fixed_height_small"};

    String useGifyQuality = "downsized";
    public String downloadFolder;

    public List<String> getSearchURLs(String[] searchWords, int searchLimit) {
        String searchURL = host + searchPath;

        String searchWordParam = buildParameter("q", searchWords);
        String apiKeyParam = buildParameter("api_key", apiKey);

        StringJoiner joiner = new StringJoiner("&", "?", "");
        joiner.add(searchWordParam);
        joiner.add(apiKeyParam);

        if(searchLimit != -1) {
            String searchLimitParam = buildParameter("limit", String.valueOf(searchLimit));
            joiner.add(searchLimitParam);
        }

        //System.out.println(searchURL + joiner.toString());
        GetRequest get = new GetRequest(searchURL + joiner.toString());
        try {
            get.send();
            if (get != null) {
                JSONParser json = new JSONParser();
                JSONObject obj = (JSONObject) json.parse(get.getContent());
                Long status = (Long) ((JSONObject) obj.get("meta")).get("status");
                //System.out.println("Gify Search Status: " + status);
                // lets get this party started
                if (status == 200) {
                    JSONArray images = (JSONArray) obj.get("data");
                    List<String> urls = (List<String>) images.stream().
                            map(img ->
                                    ((JSONObject) ((JSONObject) ((JSONObject) img).get("images")).get(useGifyQuality)).get("url"))
                            .collect(Collectors.toList());
                    return urls;
                }
            }
        } catch (Exception exc) {
            exc.printStackTrace();
            return new ArrayList<String>();
        }
        return new  ArrayList<String>();
    }

    public List<String> downloadGifs(String baseName, List<String> addresses) {
        int counter = 0;
        ArrayList<String> paths = new ArrayList<>();
        for(String address : addresses) {
            String filePath = "gifs"+ File.separator+"gify" + File.separator + baseName + "_" + counter + ".gif";
            downloadGif("data" + File.separator + filePath, address);
            paths.add(filePath);
            counter++;
            if(counter == maxDownload)
                break;
        }
        return paths;
    }

    private String buildParameter(String param, String value) {
        return buildParameter(param, new String[]{value});
    }

    private String buildParameter(String param, String[] values) {
        StringJoiner joiner = new StringJoiner("+", param + "=", "");
        for (String val : values) {
            joiner.add(val);
        }
        return joiner.toString();
    }

    public void downloadGif(String fileName, String address) {
        DataInputStream di = null;
        FileOutputStream fo = null;
        byte [] b = new byte[1];

        try {
            // input
            URL url = new URL(address);
            URLConnection urlConnection = url.openConnection();
            urlConnection.connect();
            di = new DataInputStream(urlConnection.getInputStream());

            // output
            fo = new FileOutputStream(fileName);

            //  copy the actual file
            //   (it would better to use a buffer bigger than this)
            while(-1 != di.read(b,0,1))
                fo.write(b,0,1);
            di.close();
            fo.close();
        }
        catch (Exception ex) {
            //System.out.println("Oups!!!");
            ex.printStackTrace();
            //System.exit(1);
        }
        //System.out.println("done.");
    }
}
