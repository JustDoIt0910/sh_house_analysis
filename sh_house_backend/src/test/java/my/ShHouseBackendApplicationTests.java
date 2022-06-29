package my;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class ShHouseBackendApplicationTests {

    @Value("${spider.script-path}")
    private String sp;

    @Test
    void contextLoads() {
        System.out.println(sp);
    }

}
