package my.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RawParam {
    private String city;

    private String region;

    private String type;

    private String face;

    private int floor;

    private int isDeal;
}
