package com.biblioteca.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/usuarios/registro", "/api/login").permitAll()
                .requestMatchers("/api/libros", "/api/libros/**").permitAll()
                .requestMatchers("/api/prestamos", "/api/prestamos/**", "/api/prestar").hasAuthority("BIBLIOTECARIO")
                .requestMatchers(HttpMethod.GET, "/api/resenas/**", "/api/comentarios-resena/**").permitAll()
                .requestMatchers(HttpMethod.POST, "/api/resenas/**", "/api/comentarios-resena/**").authenticated()
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .loginProcessingUrl("/api/login")
                .successHandler((request, response, authentication) -> response.setStatus(200))
                .permitAll()
            )
            .logout(logout -> logout
                .logoutUrl("/api/logout")
                .permitAll()
            );
        return http.build();
    }
}

// .requestMatchers("/api/libros").hasAuthority("BIBLIOTECARIO")