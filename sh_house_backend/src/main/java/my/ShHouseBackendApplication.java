package my;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@MapperScan("my.dao")
//@EnableScheduling
public class ShHouseBackendApplication {

    public static void main(String[] args) {
        SpringApplication.run(ShHouseBackendApplication.class, args);
    }

}
