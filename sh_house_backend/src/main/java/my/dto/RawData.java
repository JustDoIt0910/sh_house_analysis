package my.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import my.pojo.Info;

import java.util.List;

@Data
@AllArgsConstructor
public class RawData {

    private String title;

    List<Info> infos;
}
