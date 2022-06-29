package my.dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import my.dto.C7Data;
import my.pojo.Info;
import my.pojo.PriceAndDate;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface InfoMapper extends BaseMapper<Info> {

    @Select({"select count(*) from t_info where cityId = #{cid} and regionId = 0"})
    Integer getCountByCid(@Param("cid") Integer cid);

    @Select({"select count(*) from t_info where deal = 0 and cityId = #{cid} and regionId = 0"})
    Integer getSailCountByCid(@Param("cid") Integer cid);

    @Select({"select count(*) from t_info where deal = 1 and cityId = #{cid} and regionId = 0"})
    Integer getDealCountByCid(@Param("cid") Integer cid);

    @Select({"select count(*) from t_info where cityId = #{cid} and regionId = 0 and deal = 1 and type = #{hType}"})
    Integer getDealCountByCidAndType(@Param("cid") Integer cid, @Param("hType") String hType);

    @Select({"select count(*) from t_info where cityId = #{cid} and regionId = 0 and deal = 0 and type = #{hType}"})
    Integer getSailCountByCidAndType(@Param("cid") Integer cid, @Param("hType") String hType);

    @Select({"select avg(unitPrice) from t_info where deal = 1 and regionId = #{rid}"})
    Double getDealPriceAvgByRegionId(@Param("rid") Integer rid);

    @Select({"select avg(unitPrice) from t_info where deal = 0 and regionId = #{rid}"})
    Double getSailPriceAvgByRegionId(@Param("rid") Integer rid);

    @Select({"select avg(unitPrice) from t_info where deal = 1 and cityId = #{cid} and regionId = 0"})
    Double getDealPriceAvgByCityId(@Param("cid") Integer cid);

    @Select({"select avg(unitPrice) from t_info where deal = 0 and cityId = #{cid} and regionId = 0"})
    Double getSailPriceAvgByCityId(@Param("cid") Integer cid);

    @Select({"select count(*) from t_info " +
            "where deal = 0 and regionId = 0 and cityId = #{cid} " +
            "and area > #{low} and area <= #{high}"})
    Integer getSailAreaRangeCountByCityId(@Param("cid") Integer cid,
                                          @Param("low") Integer low,
                                          @Param("high") Integer high);

    @Select({"select distinct face from t_info where cityId = #{cid} and regionId = 0 and deal = #{isDeal}"})
    List<String> getDistinctFaces(@Param("cid") Integer cid, @Param("isDeal") Integer isDeal);

    @Select({"select distinct floor from t_info where cityId = #{cid} and regionId = 0 and deal = #{isDeal}"})
    List<Integer> getDistinctFloors(@Param("cid") Integer cid, @Param("isDeal") Integer isDeal);

    @Select({"select avg(unitPrice) from t_info where cityId = #{cid} and regionId = 0 " +
            "and face = #{face} and floor = #{floor}"})
    Double getCityAvgPriceByFaceAndFloor(@Param("cid") Integer cid,
                                         @Param("face") String face, @Param("floor") Integer floor);

    @Select({"select avg(unitPrice) as unitPrice, dealTime from t_info where regionId = 0 and cityId = #{cid} and deal = 1 group by dealTime"})
    List<PriceAndDate> getCityDealPriceTrend(@Param("cid") Integer cid);
}
