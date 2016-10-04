package oracle.gif;

import gifAnimation.Gif;
import oracle.Oracle;
import oracle.Settings;

import java.io.File;
import java.util.*;
import java.util.List;

/**
 * Created by raminsoleymani on 30/09/16.
 */
public class GifDisplayer {

    Oracle oracle;
    String baseFolder = "gifs/";
    Gify gify;

    public boolean downloadGifys;

    //private boolean asynGifyRequestRunning = false;
    private boolean asyncGifysAvailable = false;
    private List<Gif> receivedGifs = new ArrayList<Gif>();
    private List<Gif> runningGifs = new ArrayList<Gif>();

    boolean doReset = false;

    public GifDisplayer(Oracle oracle) {
        this.oracle = oracle;
        downloadGifys = oracle.settings.DOWNLOAD_GIFY;
        gify = new Gify();
        gify.downloadFolder = oracle.sketchPath() + "/data/gifs/gify/";
    }

    public Gif getRandomCleanGif() {
        return getRandomGif("clean");
    }

    public Gif getRandomGif(String gifFolder) {
        File folder = new File(oracle.sketchPath() + "/data/gifs/" + gifFolder);
        String[] files = folder.list();
        Random rnd = new Random();
        System.out.println(gifFolder + "/" + files[rnd.nextInt(files.length)]);
        return new Gif(oracle, baseFolder + gifFolder + "/" + files[rnd.nextInt(files.length)]);
    }


    /**
     * @param searchWords
     * @param number      maximum number of gifs (-1) for all
     * @return a list of gifs
     */
    public List<Gif> getGiyGifs(String[] searchWords, int number) {
        List<String> gifs = gify.getSearchURLs(searchWords, number);

        //gifs.stream().forEach(System.out::println);
        if(downloadGifys) {
            StringJoiner joiner = new StringJoiner("_");
            Arrays.stream(searchWords).forEach(w -> joiner.add(w));
            gifs = gify.downloadGifs(joiner.toString(), gifs);
        }

        // this crap was nicer then the stream in the end cuz it allows to catch exceptions
        ArrayList<Gif> gg= new ArrayList<Gif>();
        int counter = 0;
        for(String s : gifs) {
            System.out.println(s);
            try {
                gg.add(new Gif(oracle, s));
                if (++counter == number) {
                    break;
                }
            } catch (NullPointerException damn) {
                System.out.println("missing gif"+ counter);
            }

        }
        return gg;
    }

    public void getGiyGifsAsnyc(String[] searchWords, int number) {
        Thread getGifysThread = new Thread(new Runnable() {
            List<Gif> gg;
            @Override
            public void run() {
                asyncGifysAvailable = false;
                receivedGifs = getGiyGifs(searchWords,number);
                asyncGifysAvailable = true;
            }
        });
        getGifysThread.start();
    }

    public boolean getAsyncGifysAvailable() {
        return asyncGifysAvailable;
    }

    public void input(String input){
        doReset = true;
        String[] textSplit = input.split("\\s+");
        getGiyGifsAsnyc(textSplit,1);
    }

    public void result(String result) {
        String[] textSplit = result.split("\\s+");
        getGiyGifsAsnyc(textSplit,1);
    }

    public void update(){
        if(doReset) {
            runningGifs.clear();
            doReset = false;
        }
        if (getAsyncGifysAvailable()) {
            receivedGifs.stream().forEach(Gif::play);
            runningGifs.addAll(receivedGifs);
            receivedGifs.clear();
        }
        if (runningGifs.size() > 0){
            int x = Settings.GIFY_X;
            int y = Settings.GIFY_Y;
            int w = Settings.GIFY_W;
            int h = Settings.GIFY_H;
            oracle.tint(0,255,0);
            oracle.image( runningGifs.get( ( oracle.frameCount / 15 ) % runningGifs.size() ), x, y, w, h );
        }
        oracle.filter(oracle.POSTERIZE, 8);
    }


}
