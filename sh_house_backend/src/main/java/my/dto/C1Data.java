package my.dto;

import java.util.ArrayList;
import java.util.List;

public class C1Data {
    private final List<String> regions = new ArrayList<>();
    private final List<Integer> dealCount = new ArrayList<>();
    private final List<Integer> onSailCount = new ArrayList<>();

    public List<String> getRegions() {
        return regions;
    }

    public List<Integer> getDealCount() {
        return dealCount;
    }

    public List<Integer> getOnSailCount() {
        return onSailCount;
    }

    public C1Data() {
    }
}
