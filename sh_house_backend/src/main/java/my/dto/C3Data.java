package my.dto;

import java.util.ArrayList;
import java.util.List;

public class C3Data {
    private final List<String> regions = new ArrayList<>();
    private final List<Double> dealAvg = new ArrayList<>();
    private final List<Double> onSailAvg = new ArrayList<>();

    public List<String> getRegions() {
        return regions;
    }

    public List<Double> getDealAvg() {
        return dealAvg;
    }

    public List<Double> getOnSailAvg() {
        return onSailAvg;
    }

    public C3Data() {
    }
}
