# Plan de Aseguramiento de Calidad (PAC)

| Campo | Valor |
|---|---|
| Proyecto | Sistema de Gestión Bibliotecaria |
| Versión | 1.0.0 |
| Backend | gestion_bibliotecaria 0.0.1-SNAPSHOT |
| Frontend | gestion-bibliotecaria 0.1.0 |

## 1. Alcance y Propósito

Sistema web para gestión de préstamos, catálogo y usuarios de una biblioteca. (Incluye administracios de reseñas, comentarios y amonestaciones por retrasos [transacciones monetarias simuladas]).


Stack tecnológico: Backend: Maven (21, 3.4.5). Frontend: npm / vue-cli (Vue 3.2.13).

## 2. Stack Tecnológico

### Backend
- **Build tool:** Maven
- **Java:** 21
- **Spring Boot:** 3.4.5
- lombok (org.projectlombok)
- mysql-connector-java (mysql)
- spring-boot-starter-data-jpa (org.springframework.boot)
- spring-boot-starter-data-jpa (org.springframework.boot)
- spring-boot-starter-security (org.springframework.boot)
- spring-boot-starter-test (org.springframework.boot)
- spring-boot-starter-web (org.springframework.boot)

### Frontend
- **Build tool:** npm / vue-cli
- **Vue:** 3.2.13
- axios @1.9.0
- core-js @3.8.3
- vue @3.2.13

## 3. Inventario de Artefactos

### Documentación
- `BRIEF EQUIPO 58 1 - v1.1.pdf`
- `DAS Equipo 58-1 v1.5.pdf`
- `Diagrama de Clases UML - Equipo 58-1.pdf`
- `ERS Equipo 58 1 v.1.2.pdf`
- `Equipo 58-1_ Diagrama de contexto, contenedores y componentes (6).pdf`

### Código Fuente
- **Java:** 26 archivos, 1362 LOC
- **Vue:** 15 archivos, 2262 LOC

## 4. Objetivos de Calidad

[FORMATEO GEMINI NO DISPONIBLE: 4. Objetivos de Calidad]

## 5. Gestión y Organización

[FORMATEO GEMINI NO DISPONIBLE: 5. Gestión y Organización]

## 6. Estándares Aplicables

- Objetivos de Calidad (ISO/IEC 25010)
- Gestión y Organización
- Documentación, Estándares y Guías
- Métricas y Control Estadístico
- Ejecución y Cronograma

## 7. Herramientas Tecnológicas

Ver matriz completa en `sqa/PACS-Fase2-Herramientas.md`

## 8. Métricas

[FORMATEO GEMINI NO DISPONIBLE: 8. Métricas]

## 9. Análisis de Riesgos

[FORMATEO GEMINI NO DISPONIBLE: 9. Análisis de Riesgos]

## 10. Cronograma

[FORMATEO GEMINI NO DISPONIBLE: 10. Cronograma]

## 11. Gestión de Defectos

Los defectos detectados durante las revisiones de documentos y artefactos se gestionan mediante tickets en Jira, siguiendo los workflows de resolución definidos por el equipo SQA.

> **Nota:** El análisis de defectos de código fuente está planificado para la **Segunda Entrega** (Fase 2: Pruebas Dinámicas).

## 12. CI/CD

### Workflows de GitHub Actions
- `auditoria_sqa.yml`
- `wf1_auditoria_requisitos.yml`
- `wf2_inspeccion_arquitectura.yml`
- `wf3_generacion_pruebas.yml`
- `wf4_orquestador.yml`