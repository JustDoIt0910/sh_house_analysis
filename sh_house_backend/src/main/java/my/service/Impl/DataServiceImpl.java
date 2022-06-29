package my.service.Impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import my.dao.CityMapper;
import my.dao.InfoMapper;
import my.dao.RegionMapper;
import my.dto.*;
import my.pojo.City;
import my.pojo.Info;
import my.pojo.PriceAndDate;
import my.pojo.Region;
import my.predict.Predictor;
import my.service.DataService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.text.SimpleDateFormat;
import java.util.*;
import java.util.function.Predicate;
import java.util.stream.Collectors;

@Service
public class DataServiceImpl implements DataService {

    @Autowired
    private RegionMapper regionMapper;
    @Autowired
    private CityMapper cityMapper;
    @Autowired
    private InfoMapper infoMapper;

    @Override
    public C1Data getC1Data(String city) {
        List<Region> regions = getRegionsInCity(city, "name", "deal", "onsail");
        C1Data data = new C1Data();
        for(Region region: regions) {
            data.getRegions().add(region.getName());
            data.getOnSailCount().add(region.getOnSail());
            data.getDealCount().add(region.getDeal());
        }
        return data;
    }

    @Override
    public C2Data getC2Data(String city) {
        C2Data data = new C2Data();
        int cid = getCityId(city);
        int total = infoMapper.getDealCountByCid(cid);
        double cnt = 0;
        for(String type: data.getTypes()) {
            if(type.equals("其他"))
                continue;
            double p = (float)infoMapper.getDealCountByCidAndType(cid, type) / total;
            p = accuracyConvert(p, 2);
            data.getDProportions().add(p);
            cnt += p;
        }
        double r = accuracyConvert(1 - cnt, 2);
        data.getDProportions().add(r);

        total = infoMapper.getSailCountByCid(cid);
        cnt = 0;
        for(String type: data.getTypes()) {
            if(type.equals("其他"))
                continue;
            double p = (float)infoMapper.getSailCountByCidAndType(cid, type) / total;
            p = accuracyConvert(p, 2);
            data.getOProportions().add(p);
            cnt += p;
        }
        r = accuracyConvert(1 - cnt, 2);
        data.getOProportions().add(r);

        return data;
    }

    @Override
    public C3Data getC3Data(String city) {
        C3Data data = new C3Data();
        List<Region> regions = getRegionsInCity(city, "id", "name");
        for(Region region: regions) {
            data.getRegions().add(region.getName());
            Double dealAvg = infoMapper.getDealPriceAvgByRegionId(region.getId());
            if(dealAvg == null)
                dealAvg = 0.0;
            Double onSailAvg = infoMapper.getSailPriceAvgByRegionId(region.getId());
            if(onSailAvg == null)
                onSailAvg = 0.0;
            data.getDealAvg().add(accuracyConvert(dealAvg, 2));
            data.getOnSailAvg().add(accuracyConvert(onSailAvg, 2));
        }
        return data;
    }

    @Override
    public C4Data getC4Data(String[] cities) {
        C4Data data = new C4Data(cities);
        for(String city: data.getCities()) {
            int cid = getCityId(city);
            Double dealAvg = infoMapper.getDealPriceAvgByCityId(cid);
            Double onSailAvg = infoMapper.getSailPriceAvgByCityId(cid);
            if(dealAvg == null)
                dealAvg = 0.0;
            if(onSailAvg == null)
                onSailAvg = 0.0;
            data.getDealAvg().add(accuracyConvert(dealAvg, 2));
            data.getOnSailAvg().add(accuracyConvert(onSailAvg,2));
        }
        return data;
    }

    @Override
    public List<Double> getC5Data(C5Param param) {
        List<Double> data = new ArrayList<>();
        int cid = getCityId(param.getCity());
        int total = infoMapper.getSailCountByCid(cid);
        double cnt = 0.0;
        for(Integer[] range: param.getAreaRanges()) {
            int count = infoMapper.getSailAreaRangeCountByCityId(cid, range[0], range[1]);
            double p = accuracyConvert((double) count / total, 2);
            data.add(p);
            cnt += p;
        }
        data.add(accuracyConvert(1 - cnt, 2));
        return data;
    }

    @Override
    public C6Data getC6Data(String city, String type) {
        int cid = getCityId(city);
        int isDeal = type.equals("deal") ? 1 : 0;
        List<String> faces = infoMapper.getDistinctFaces(cid, isDeal);
        List<String> facesFiltered = faces.stream().filter(s -> !s.equals("暂无数据")).collect(Collectors.toList());
        List<Integer> floors = infoMapper.getDistinctFloors(cid, isDeal);
        List<Integer> floorsFiltered = floors.stream().filter(f -> f != 0).collect(Collectors.toList());

        Collections.sort(floorsFiltered);
        C6Data data = new C6Data();
        data.setFace(facesFiltered);
        data.setFloor(floorsFiltered);
        for(int i = 0; i < facesFiltered.size(); i++)
            for(int j = 0; j < floorsFiltered.size(); j++) {
                Double avgPrice =
                        infoMapper.getCityAvgPriceByFaceAndFloor(cid, facesFiltered.get(i), floorsFiltered.get(j));
                avgPrice = avgPrice == null ? 0.0 : accuracyConvert(avgPrice, 2);
                data.getData().add(new Double[]{(double) i, (double) j, avgPrice});
            }
        return data;
    }

    @Override
    public List<List<String>> getCityOptions() {
        // TODO 从配置文件里读取城市列表
        List<List<String>> options = new ArrayList<>();
        for(int i = 0; i < 7; i++)
            options.add(Arrays.asList("杭州", "上海", "济南", "保定", "开封"));
        return options;
    }

    @Override
    public PredictData predict(String region, String type, Integer floor) {
        QueryWrapper<Info> queryWrapper = new QueryWrapper<Info>()
                .select("unitPrice", "dealTime")
                .eq("regionId", getRegionId(region)).eq("deal", 1)
                .eq("type", type).eq("floor", floor).orderByAsc("dealTime");
        List<PriceAndDate> trend = infoMapper.selectList(queryWrapper).stream()
                .map(i -> new PriceAndDate(i.getUnitPrice(), i.getDealTime()))
                .collect(Collectors.toList());

        Date fromDate = trend.get(0).getDealTime();
        Date toDate = trend.get(trend.size() - 1).getDealTime();
        PredictData data = new PredictData();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        data.setFrom(sdf.format(fromDate));
        data.setTo(sdf.format(toDate));
        double[] x_axis = new double[trend.size()];
        x_axis[0] = 0.0;
        for(int i = 1; i < trend.size(); i++) {
            long diff = trend.get(i).getDealTime().getTime() - fromDate.getTime();
            int days = (int) (diff / (1000 * 60 * 60 * 24));
            x_axis[i] = days;
        }
        double[] y_axis = trend.stream().map(PriceAndDate::getUnitPrice).
                mapToDouble(Double::doubleValue).toArray();
        Predictor predictor = new Predictor(x_axis, y_axis, 3);
        data.setSpan((int)x_axis[x_axis.length - 1]);
        data.setCoefficients(predictor.getCoefficient());
        return data;
    }

    @Override
    public C7Data getDealTrend(String city) {
        int cid = getCityId(city);
        List<PriceAndDate> trends = infoMapper.getCityDealPriceTrend(cid);
        C7Data data = new C7Data();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        List<String> dates = trends.stream().map(PriceAndDate::getDealTime)
                .map(sdf::format).collect(Collectors.toList());
        List<Double> prices = trends.stream().map(PriceAndDate::getUnitPrice)
                .map(p -> accuracyConvert(p, 2))
                .collect(Collectors.toList());
        data.setDate(dates);
        data.setAvgPrice(prices);
        return data;
    }

    @Override
    public RawData getRaw(RawParam param) {
//        System.out.println(param);
        StringBuilder builder = new StringBuilder();
        QueryWrapper<Info> query = new QueryWrapper<Info>().
                select("name, type, area, totalPrice, unitPrice, face, floor, dealTime").eq("deal", param.getIsDeal());
        if(!param.getCity().equals("无")) {
            builder.append(param.getCity());
            int cid = getCityId(param.getCity());
            query = query.eq("cityId", cid);
            //按城市搜索
            if(param.getRegion().equals("无")) {
                query = query.eq("regionId", 0);
            }
            else {
                builder.append(param.getRegion());
                int rid = getRegionId(param.getRegion());
                query = query.eq("regionId", rid);
            }
        }
        else {
            if(param.getRegion().equals("无")) {
                int shanghai = getCityId("上海");
                builder.append("上海");
                query = query.eq("cityId", shanghai).eq("regionId", 0);
            }
            else {
                String cityName = cityMapper.getCityNameByRegionName(param.getRegion());
                builder.append(cityName);
                builder.append(param.getRegion());
                int rid = getRegionId(param.getRegion());
                query = query.eq("regionId", rid);
            }
        }
        if(!param.getType().equals("无")) {
            builder.append(param.getType());
            query = query.eq("type", param.getType());
        }
        if(!param.getFace().equals("无")) {
            builder.append("朝").append(param.getFace());
            query = query.eq("face", param.getFace());
        }
        if(param.getFloor() != 0) {
            builder.append(param.getFloor()).append("层");
            query = query.eq("floor", param.getFloor());
        }
        String stat = param.getIsDeal() == 0 ? "在售" : "成交";
        builder.append(stat);
        builder.append("二手房");
        return new RawData(builder.toString(), infoMapper.selectList(query));
    }

    private List<Region> getRegionsInCity(String city, String... selectFields) {
        QueryWrapper<City> cityQuery = new QueryWrapper<City>()
                .select("id").eq("name",  city);
        int cid = cityMapper.selectOne(cityQuery).getId();

        QueryWrapper<Region> regionQuery = new QueryWrapper<Region>()
                .select(selectFields).eq("cityId", cid);
        return regionMapper.selectList(regionQuery);
    }

    private int getCityId(String city) {
        QueryWrapper<City> cityQuery = new QueryWrapper<City>()
                .select("id").eq("name",  city);
        return cityMapper.selectOne(cityQuery).getId();
    }

    private int getRegionId(String region) {
        QueryWrapper<Region> regionQuery = new QueryWrapper<Region>()
                .select("id").eq("name",  region);
        return regionMapper.selectOne(regionQuery).getId();
    }

    private static double accuracyConvert(double num, int acc) {
        return (double) Math.round(num * (int)Math.pow(10, acc)) / Math.pow(10, acc);
    }
}