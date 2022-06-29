package my.dto;

import java.util.ArrayList;
import java.util.List;

public class C4Data {
    private final String[] cities;
    private final List<Double> dealAvg = new ArrayList<>();
    private final List<Double> onSailAvg = new ArrayList<>();

    public List<Double> getDealAvg() {
        return dealAvg;
    }

    public List<Double> getOnSailAvg() {
        return onSailAvg;
    }

    public String[] getCities() {
        return cities;
    }

    public C4Data(String[] cities) {
        this.cities = cities;
    }
}
