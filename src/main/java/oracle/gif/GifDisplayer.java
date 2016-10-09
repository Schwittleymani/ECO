package oracle.gif;

import gifAnimation.Gif;
import oracle.Oracle;
import oracle.Settings;
import processing.core.PImage;

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

    int retreiveFactor = 2; // retreiveFactor number

    int gifSwapSpeed = 15; // fps swap speed

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
        List<String> gifs = gify.getSearchURLs(searchWords, number * retreiveFactor);
        ArrayList<Gif> gg = new ArrayList<Gif>();
        if (gifs.size() > 0) {
            Collections.shuffle(gifs);
            gifs = gifs.subList(0, number);

            //gifs.stream().forEach(System.out::println);
            if (downloadGifys) {
                StringJoiner joiner = new StringJoiner("_");
                Arrays.stream(searchWords).forEach(w -> joiner.add(w));
                gifs = gify.downloadGifs(joiner.toString(), gifs);
            }

            // this crap was nicer then the stream in the end cuz it allows to catch exceptions

            int counter = 0;
            for (String s : gifs) {
                System.out.println(s);
                try {
                    gg.add(new Gif(oracle, s));
                    if (++counter == number) {
                        break;
                    }
                } catch (NullPointerException damn) {
                    System.out.println("missing gif" + counter);
                }

            }
        }
        return gg;
    }

    public void getGiyGifsAsnyc(String[] searchWords, int number) {
        Thread getGifysThread = new Thread(() -> {
            asyncGifysAvailable = false;
            receivedGifs = getGiyGifs(searchWords, number);
            asyncGifysAvailable = true;
        });
        getGifysThread.start();
    }

    public boolean getAsyncGifysAvailable() {
        return asyncGifysAvailable;
    }

    public void input(String input) {

        String[] textSplit = input.split("\\s+");
        getGiyGifsAsnyc(textSplit, Settings.GIFS_PER_PART);
    }

    public void result(String result) {
        doReset = true;
        String[] textSplit = result.split("\\s+");
        getGiyGifsAsnyc(textSplit, Settings.GIFS_PER_PART);
    }

    public void setNewGifSwapSpeed() {
        gifSwapSpeed = (int) oracle.random(Settings.GIF_SWAP_SPEED_MIN, Settings.GIF_SWAP_SPEED_MAX);
    }

    public void update() {
        if (getAsyncGifysAvailable()) {
            receivedGifs.stream().forEach(Gif::play);
            if (doReset) {
                for(Gif gif : runningGifs){
                    gif.dispose();
                }
                runningGifs.clear();
                doReset = false;
                setNewGifSwapSpeed();
            }
            runningGifs.addAll(receivedGifs);
            receivedGifs.clear();
        }
        if (runningGifs.size() > 0) {
            int x = Settings.GIFY_X;
            int y = Settings.GIFY_Y;
            int w = Settings.GIFY_W;
            int h = Settings.GIFY_H;
            oracle.tint(0, 255, 0);
            oracle.image(runningGifs.get((oracle.frameCount / gifSwapSpeed) % runningGifs.size()), x, y, w, h);
        }
        //oracle.filter(oracle.POSTERIZE, 8);
    }

    public void reset() {
        doReset = true;
    }
}
