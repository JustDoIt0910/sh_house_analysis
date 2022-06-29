package my.service;

import my.dto.*;
import my.pojo.Info;

import java.util.List;

public interface DataService {
    C1Data getC1Data(String city);

    C2Data getC2Data(String city);

    C3Data getC3Data(String city);

    C4Data getC4Data(String[] cities);

    List<Double> getC5Data(C5Param param);

    C6Data getC6Data(String city, String type);

    List<List<String>> getCityOptions();

    PredictData predict(String regionId, String type, Integer floor);

    C7Data getDealTrend(String city);

    RawData getRaw(RawParam param);
}
