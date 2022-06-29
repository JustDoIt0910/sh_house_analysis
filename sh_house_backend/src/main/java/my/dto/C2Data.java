package my.dto;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class C2Data {
    private final List<String> types = Arrays.asList("1室0厅", "1室1厅",
            "2室1厅", "2室2厅", "3室1厅", "3室2厅", "4室2厅", "其他");
    private final List<Double> dproportions = new ArrayList<>();
    private final List<Double> oproportions = new ArrayList<>();

    public List<String> getTypes() {
        return types;
    }

    public List<Double> getDProportions() {
        return dproportions;
    }

    public List<Double> getOProportions() {
        return oproportions;
    }
}


