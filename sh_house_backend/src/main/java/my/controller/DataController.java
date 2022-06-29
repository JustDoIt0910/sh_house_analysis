package my.controller;

import my.dto.*;
import my.pojo.Info;
import my.service.DataService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import javax.sql.rowset.RowSetWarning;
import java.util.List;


@RestController
@RequestMapping("/data")
public class DataController {

    @Autowired
    private DataService service;

    @GetMapping("/c1/{city}")
    public C1Data RegionWithHouseCount(@PathVariable("city") String city) {
        return service.getC1Data(city);
    }

    @GetMapping("/c2/{city}")
    public C2Data RegionHouseTypeProportion(@PathVariable("city") String city) {
        return service.getC2Data(city);
    }

    @GetMapping("/c3/{city}")
    public C3Data CityAvgPrice(@PathVariable("city") String city) {
        return service.getC3Data(city);
    }

    @GetMapping("/c4")
    public C4Data RegionAvgPrice(@RequestParam("cities") String[] cities) {
        return service.getC4Data(cities);
    }

    @PostMapping("/c5")
    public List<Double> CityHouseAreaProportion(@RequestBody C5Param param) {
        return service.getC5Data(param);
    }

    @GetMapping("/c6/{city}/{type}")
    public C6Data FloorFacePrice3D(@PathVariable("city") String city, @PathVariable("type") String type) {
        return service.getC6Data(city, type);
    }

    @GetMapping("/c7/{city}")
    public C7Data GetCityDealPriceTrend(@PathVariable("city") String city) {
        return service.getDealTrend(city);
    }

    @GetMapping("/raw")
    public RawData GetRaw(RawParam param) {
        return service.getRaw(param);
    }

    @GetMapping("/predict")
    public PredictData predict(@RequestParam("region") String region,
                               @RequestParam("type") String type,
                               @RequestParam("floor") Integer floor) {
        return service.predict(region, type, floor);
    }

    @GetMapping("/cityOptions")
    public List<List<String>> getCityOptions() {
        return service.getCityOptions();
    }
}
