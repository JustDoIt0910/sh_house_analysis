package my.dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import my.pojo.City;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CityMapper extends BaseMapper<City> {

    @Select({"select t_cities.name from t_cities where t_cities.id = " +
            "(select t_regions.cityId from t_regions where t_regions.name = #{region} limit 1)"})
    String getCityNameByRegionName(@Param("region") String region);
}
