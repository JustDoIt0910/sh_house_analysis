package my.dto;

import lombok.Data;

import java.util.Date;

@Data
public class PredictData {
    private String from;
    private String to;
    private Integer span;
    private double[] coefficients;
}
