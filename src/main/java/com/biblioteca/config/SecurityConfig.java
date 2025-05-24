package com.biblioteca.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/usuarios/registro", "/api/usuarios/login").permitAll()
                .requestMatchers("/api/libros").permitAll()
                .requestMatchers("/api/libros").hasAuthority("BIBLIOTECARIO") 
                .requestMatchers("/api/prestamos/**").hasAuthority("BIBLIOTECARIO")
                .requestMatchers("/api/prestamos/**").hasRole("BIBLIOTECARIO")
                .anyRequest().authenticated()
            );
        return http.build();
    }
}