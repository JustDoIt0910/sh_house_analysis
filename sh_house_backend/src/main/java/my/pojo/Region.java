package my.pojo;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@TableName("t_regions")
public class Region {
    private int id;
    private String name;
    private int cityId;
    private int deal;
    private int onSail;
}
