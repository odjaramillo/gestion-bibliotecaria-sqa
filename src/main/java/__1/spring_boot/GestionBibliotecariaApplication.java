package __1.spring_boot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication(scanBasePackages = {
		"com.biblioteca",
		"__1.spring_boot"
})
@EntityScan("com.biblioteca.model")
@EnableJpaRepositories("com.biblioteca.repository")
public class GestionBibliotecariaApplication {

	public static void main(String[] args) {
		SpringApplication.run(GestionBibliotecariaApplication.class, args);
	}

}
