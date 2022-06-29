package my.dto;

import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Data
public class C6Data {
    private List<String> face = new ArrayList<>();
    private List<Integer> floor = new ArrayList<>();
    private List<Double[]> data = new ArrayList<>();
}
