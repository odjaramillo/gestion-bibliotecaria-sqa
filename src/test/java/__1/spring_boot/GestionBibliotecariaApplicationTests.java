package __1.spring_boot;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest(properties = "spring.autoconfigure.exclude=")
@ActiveProfiles("test")
@Tag("regresion")
class GestionBibliotecariaApplicationTests {

	@Test
	void contextLoads() {
	}

}
