package com.biblioteca.unit;

import com.biblioteca.repository.AmonestacionRepository;
import com.biblioteca.service.AmonestacionService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

/**
 * TC-FIAB-007 — Tabla de decisión de {@code eliminarAmonestacion} (TCI-M5.1..M5.3).
 * 2 decisiones: rol de bibliotecario y existencia de la amonestación.
 *
 * @see com.biblioteca.service.AmonestacionService#eliminarAmonestacion(Integer, String)
 */
@ExtendWith(MockitoExtension.class)
@Tag("regresion")
class EliminarAmonestacionTest {

    private static final Integer AMONESTACION_ID = 1;

    @Mock
    private AmonestacionRepository amonestacionRepository;

    @InjectMocks
    private AmonestacionService amonestacionService;

    @Test
    @DisplayName("TCI-M5.1 — rol distinto de BIBLIOTECARIO rechaza sin consultar el repositorio")
    void rolNoBibliotecario_rechazaSinConsultarRepositorio() {
        String resultado = amonestacionService.eliminarAmonestacion(AMONESTACION_ID, "USUARIO");

        assertEquals("Solo los bibliotecarios pueden eliminar amonestaciones.", resultado);
        verifyNoInteractions(amonestacionRepository);
    }

    @Test
    @DisplayName("TCI-M5.2 — rol BIBLIOTECARIO con amonestación inexistente")
    void bibliotecarioConAmonestacionInexistente_rechazaConMensaje() {
        when(amonestacionRepository.existsById(AMONESTACION_ID)).thenReturn(false);

        String resultado = amonestacionService.eliminarAmonestacion(AMONESTACION_ID, "BIBLIOTECARIO");

        assertEquals("Amonestación no encontrada.", resultado);
        verify(amonestacionRepository, never()).deleteById(AMONESTACION_ID);
    }

    @Test
    @DisplayName("TCI-M5.3 — rol BIBLIOTECARIO con amonestación existente elimina con éxito")
    void bibliotecarioConAmonestacionExistente_eliminaConExito() {
        when(amonestacionRepository.existsById(AMONESTACION_ID)).thenReturn(true);

        String resultado = amonestacionService.eliminarAmonestacion(AMONESTACION_ID, "BIBLIOTECARIO");

        assertEquals("Amonestación eliminada con éxito.", resultado);
        verify(amonestacionRepository).deleteById(AMONESTACION_ID);
    }
}
