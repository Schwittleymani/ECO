package oracle.cli;

/**
 * Created by raminsoleymani on 01/10/16.
 */
public class BoxValues {

    public float top,bottom,left,right;
    public float width, height; // calculated

    public BoxValues(float top, float bottom, float left, float right) {
        this.top = top;
        this.bottom = bottom;
        this.left = left;
        this.right = right;
    }

    public BoxValues(float top, float bottom, float left, float right,float parentWidth, float parentHeight) {
        this.top = top;
        this.bottom = bottom;
        this.left = left;
        this.right = right;
        calculateWH_FromParentSize(parentWidth,parentHeight);
    }

    public BoxValues(float top_bottom, float left_right) {
        this.top = top_bottom;
        this.bottom = top_bottom;
        this.left = left_right;
        this.right = left_right;
    }

    public void calculateWH_FromParentSize(float parentWidth, float parentHeight) {
        this.width = parentWidth - (this.left + this.right);
        this.height = parentHeight - (this.top + this.bottom);
    }
}
