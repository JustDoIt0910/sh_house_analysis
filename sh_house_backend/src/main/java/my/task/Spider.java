package my.task;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class Spider {

    @Value("${spider.script-path}")
    private String scriptPath;

    @Scheduled(cron = "0 0 0 1/2 * ?")
    public void craw() {
        System.out.println("--------updating data------");
        String[] cmd = new String[]{"python",scriptPath};
        try {
            Process process = Runtime.getRuntime().exec(cmd);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
