package oracle.cli;

import oracle.ostern.Jesus;
import processing.core.PApplet;
import processing.core.PFont;
import processing.core.PVector;

import java.util.ArrayList;

/**
 * Created by mrzl on 31.03.2016.
 */
public class CLI {
    private ArrayList<Line> lines = new ArrayList<>();
    private PApplet parent;
    private PFont font;
    private Jesus jesus;

    int textSize = 20;
    private int currentY;
    int lineHeight = 30;
    int paddingTop = 40;
    int paddingLeft = 50;
    int maxLineWidth = 540;
    float cursorBlockWidth;
    public static String inputPreChars = "[ ] ";

    long cliUpdateDelayMillis = 50;
    long lastCliUpdateCheck;

    String stringToType = "";
    boolean doNewLineWhenFinishedTyping = false;
    long thinkUntil;

    public CLI(PApplet p) {
        this.parent = p;
        this.font = p.createFont("Glass_TTY_VT220.ttf", textSize);
        p.textFont(this.font);

        reset();
        jesus = new Jesus(p);

        parent.textSize(textSize);
        setupWidth();
        thinkUntil = System.currentTimeMillis();
        lastCliUpdateCheck = System.currentTimeMillis();
    }

    public void setupWidth() {
        // just one block
        cursorBlockWidth = parent.textWidth("a");
        // limit for the input line
        String widthTestString = "";
        do {
            widthTestString += "a";
        } while (parent.textWidth(widthTestString) < maxLineWidth);
        Line.CHAR_LIMIT = widthTestString.length();
    }

    public void update() {
        if (isThinking()) {
            return;
        }

        if (stringToType.isEmpty()) {
            if (doNewLineWhenFinishedTyping) {
                newLine(true);
                doNewLineWhenFinishedTyping = false;
            }

            return;
        }
        type(stringToType.charAt(0));
        stringToType = stringToType.substring(1, stringToType.length());
    }

    public void draw() {
        if( System.currentTimeMillis() > lastCliUpdateCheck + cliUpdateDelayMillis ) {
            lastCliUpdateCheck = System.currentTimeMillis();
            update();
        }

        parent.fill(0, 255, 0);

        jesus.drawBeforeEaster();

        pushLinesUp();
        lines.forEach(Line::draw);

        if (isThinking()) {
            parent.pushMatrix();
            float blockHeight = textSize + 10 * parent.noise(parent.frameCount * 0.01f);
            PVector centerOfBlinkingBox = new PVector(50 + parent.textWidth(getLastLine().getText()) + ( cursorBlockWidth/2), getLastLine().y - (textSize) + (blockHeight / 2));
            parent.translate(centerOfBlinkingBox.x, centerOfBlinkingBox.y);
            parent.rotate((parent.frameCount));
            parent.translate(-centerOfBlinkingBox.x, -centerOfBlinkingBox.y);
        }
        drawBlinkingLine();
        if (isThinking()) {

            parent.popMatrix();
        }
        jesus.drawAfterEaster();
    }

    private boolean isThinking() {
        return System.currentTimeMillis() < thinkUntil;
    }

    private void pushLinesUp() {
        int moveUp = 1;
        for (; moveUp > 0; moveUp--) {
            if (lines.get(lines.size() - (moveUp)).y > parent.height)
                break;
        }
        for (int i = 0; i < moveUp; i++) {
            lines.remove(0);
        }
        resetYs();
    }

    void resetYs() {
        currentY = paddingTop;
        for (Line line : lines) {
            line.y = currentY;
            currentY += lineHeight;
        }

    }

    private void drawBlinkingLine() {
        parent.pushStyle();
        parent.strokeWeight(2);

        int textColor = (parent.millis() % (255 * 4)) / 4;
        parent.stroke(0, textColor, 0);
        float textWidth = parent.textWidth(getLastLine().getText());
        if (parent.random(1) < 0.04f) {
            parent.noFill();
        }
        parent.rect(50 + textWidth, getLastLine().y - (textSize),
                cursorBlockWidth, textSize + 10 * parent.noise(parent.frameCount * 0.01f));


        parent.popStyle();
    }

    public void type(char key) {
        if (!getLastLine().limitReached()) {
            getLastLine().add(new String(String.valueOf(key)));
        } else {
            newLine();
        }

    }

    public void type(String string) {
        String[] words = string.split(" ");
        Line act = getLastLine();
        float actWidth = parent.textWidth(act.getText(false));
        for (int i = 0; i < words.length; i++) {
            if (actWidth + parent.textWidth(words[i]) > maxLineWidth) {
                newLine();
                act = getLastLine();
                actWidth = parent.textWidth(act.getText());
            } else {
                act.add(words[i] + " ");
                actWidth = parent.textWidth(act.getText());
            }
        }
    }

    public void backspace() {
        getLastLine().backspace();
    }

    public void finish(String answer, long delayMillis) {
        newLine();
        stringToType = answer;
        doNewLineWhenFinishedTyping = true;
        thinkUntil = System.currentTimeMillis() + delayMillis;
    }

    private void newLine() {
        newLine(false);
    }

    private void newLine(boolean inputChars) {
        currentY += lineHeight;
        Line newLine = new Line(this.parent);
        newLine.setPos(paddingLeft, currentY);
        lines.add(newLine);
        if (inputChars) {
            type(inputPreChars);
        }
    }

    public Line getLastLine() {
        return lines.get(lines.size() - 1);
    }

    public void reset() {
        lines.clear();

        currentY = paddingTop;
        Line line = new Line(this.parent);
        line.setPos(paddingLeft, currentY);
        lines.add(line);
        type(inputPreChars);
    }

    public boolean available() {
        return getLastLine().getText().split(" ").length > inputPreChars.split(" ").length && stringToType.isEmpty();
    }

    public void startEmojiEasterEgg() {
        jesus.start(Jesus.EASTEREGG_TYPE.EMOJI, 10);
    }
}
