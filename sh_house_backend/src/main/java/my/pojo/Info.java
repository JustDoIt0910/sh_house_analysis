package my.pojo;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Data
@NoArgsConstructor
@AllArgsConstructor
@TableName("t_info")
public class Info {
    private String name;

    private String type;

    private Double area;

    private Double totalPrice;

    private Double unitPrice;

    private String face;

    private Integer floor;

    private Date dealTime;
}
