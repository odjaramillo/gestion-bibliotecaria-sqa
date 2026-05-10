"""Análisis visual de diagramas e imágenes mediante Gemini.

Este módulo extiende las capacidades de auditoría del SQA para cubrir
diagramas C4, UML, wireframes y cualquier imagen extraída de los PDFs
de documentación.

Compatible con Python 3.10+.
"""
from __future__ import annotations

import base64
import json
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger("sqa_image_analysis")


class DiagramType(Enum):
    """Tipos de diagrama soportados para análisis visual."""

    C4_CONTEXT = "c4_context"
    C4_CONTAINER = "c4_container"
    C4_COMPONENT = "c4_component"
    UML_CLASS = "uml_class"
    UML_SEQUENCE = "uml_sequence"
    WIREFRAME = "wireframe"
    UNKNOWN = "unknown"


@dataclass
class VisualFinding:
    """Hallazgo detectado en análisis visual de un diagrama."""

    id: str
    diagram_type: DiagramType
    description: str
    severity: str  # Crítica | Alta | Media | Baja
    page_reference: str
    evidence: str


class ImageAnalyzer:
    """Analiza imágenes de diagramas usando Gemini multimodal.

    Requiere un GeminiClient inicializado (desde scripts.sqa_core.clients).
    """

    # Prompts especializados por tipo de diagrama
    _PROMPTS: dict[DiagramType, str] = {
        DiagramType.C4_CONTEXT: (
            "Sos un auditor SQA analizando un diagrama C4 de Nivel 1 (Contexto). "
            "Tu trabajo es detectar inconsistencias, omisiones y defectos. "
            "Analizá el diagrama y devolvé ESTRICTAMENTE JSON con este formato:\n"
            '{"findings": [{"id": "VIS-XXX-NN", "diagram_type": "c4_context", '
            '"description": "...", "severity": "Alta|Media|Baja", '
            '"page_reference": "...", "evidence": "..."}]}\n\n'
            "Criterios de auditoría C4 Contexto:\n"
            "1. ¿Todos los actores/usuarios del sistema están representados?\n"
            "2. ¿Los sistemas externos con los que interactúa están identificados?\n"
            "3. ¿Las relaciones tienen dirección y propósito claros?\n"
            "4. ¿Falta algún sistema o actor mencionado en el ERS/BRIEF?\n"
            "5. ¿El diagrama sigue la notación C4 (cajas, personas, líneas etiquetadas)?\n\n"
            "Contexto del sistema: {context}"
        ),
        DiagramType.C4_CONTAINER: (
            "Sos un auditor SQA analizando un diagrama C4 de Nivel 2 (Contenedores). "
            "Detectá defectos y devolvé ESTRICTAMENTE JSON:\n"
            '{"findings": [{"id": "VIS-XXX-NN", "diagram_type": "c4_container", '
            '"description": "...", "severity": "Alta|Media|Baja", '
            '"page_reference": "...", "evidence": "..."}]}\n\n'
            "Criterios de auditoría C4 Contenedores:\n"
            "1. ¿Todos los contenedores de la aplicación están representados?\n"
            "2. ¿Cada contenedor tiene su tecnología indicada?\n"
            "3. ¿Las comunicaciones entre contenedores usan protocolos válidos?\n"
            "4. ¿Falta algún contenedor presente en el código (ej. base de datos, frontend, backend)?\n"
            "5. ¿Hay contenedores en el diagrama que NO existen en el código?\n\n"
            "Contexto del sistema: {context}"
        ),
        DiagramType.C4_COMPONENT: (
            "Sos un auditor SQA analizando un diagrama C4 de Nivel 3 (Componentes). "
            "Detectá defectos y devolvé ESTRICTAMENTE JSON:\n"
            '{"findings": [{"id": "VIS-XXX-NN", "diagram_type": "c4_component", '
            '"description": "...", "severity": "Alta|Media|Baja", '
            '"page_reference": "...", "evidence": "..."}]}\n\n'
            "Criterios de auditoría C4 Componentes:\n"
            "1. ¿Cada componente del diagrama existe en el código fuente?\n"
            "2. ¿Las interfaces entre componentes están documentadas?\n"
            "3. ¿Hay componentes huérfanos (sin relaciones)?\n"
            "4. ¿Las dependencias son acíclicas?\n"
            "5. ¿Los nombres de componentes coinciden con las clases/paquetes reales?\n\n"
            "Contexto del sistema: {context}"
        ),
        DiagramType.UML_CLASS: (
            "Sos un auditor SQA analizando un diagrama de Clases UML. "
            "Detectá defectos y devolvé ESTRICTAMENTE JSON:\n"
            '{"findings": [{"id": "VIS-XXX-NN", "diagram_type": "uml_class", '
            '"description": "...", "severity": "Alta|Media|Baja", '
            '"page_reference": "...", "evidence": "..."}]}\n\n'
            "Criterios de auditoría UML Clases:\n"
            "1. ¿Todas las clases del diagrama existen en el código?\n"
            "2. ¿Los atributos y métodos visibles coinciden con la implementación?\n"
            "3. ¿Las relaciones (herencia, asociación, composición) son correctas?\n"
            "4. ¿Faltan clases que sí existen en el código?\n"
            "5. ¿Las multiplicidades están indicadas donde corresponde?\n\n"
            "Contexto del sistema: {context}"
        ),
        DiagramType.WIREFRAME: (
            "Sos un auditor SQA analizando un wireframe o mockup de interfaz de usuario. "
            "Detectá defectos y devolvé ESTRICTAMENTE JSON:\n"
            '{"findings": [{"id": "VIS-XXX-NN", "diagram_type": "wireframe", '
            '"description": "...", "severity": "Alta|Media|Baja", '
            '"page_reference": "...", "evidence": "..."}]}\n\n'
            "Criterios de auditoría Wireframes:\n"
            "1. ¿Todos los campos de formulario tienen etiquetas claras?\n"
            "2. ¿Hay validaciones visuales indicadas (ej. campo obligatorio)?\n"
            "3. ¿Los botones de acción principales son distinguibles?\n"
            "4. ¿Faltan elementos mencionados en las historias de usuario?\n"
            "5. ¿Hay inconsistencias con el flujo descrito en el ERS?\n\n"
            "Contexto del sistema: {context}"
        ),
        DiagramType.UNKNOWN: (
            "Sos un auditor SQA analizando una imagen de un documento de software. "
            "La imagen puede contener diagramas, tablas, wireframes o capturas de pantalla. "
            "Detectá defectos y devolvé ESTRICTAMENTE JSON:\n"
            '{"findings": [{"id": "VIS-XXX-NN", "diagram_type": "unknown", '
            '"description": "...", "severity": "Alta|Media|Baja", '
            '"page_reference": "...", "evidence": "..."}]}\n\n'
            "Criterios generales de auditoría visual:\n"
            "1. ¿La imagen tiene resolución suficiente para ser legible?\n"
            "2. ¿Hay elementos cortados o incompletos?\n"
            "3. ¿Los textos dentro de la imagen son legibles?\n"
            "4. ¿Hay inconsistencias entre esta imagen y el texto del documento?\n"
            "5. ¿Faltan leyendas, títulos o numeración de figuras?\n\n"
            "Contexto del sistema: {context}"
        ),
    }

    # Bloques few-shot por dominio visual para reducir falsos positivos.
    # Meta de precision esperada: >= 70% de hallazgos validos tras validacion humana.
    FEW_SHOT_C4: str = (
        "\n\n=== EJEMPLOS DE HALLAZGOS ===\n"
        "[POSITIVOS - Buen Hallazgo: Violacion valida y accionable]\n"
        "- EJEMPLO 1: Actor externo 'Biblioteca Externa' mencionado en el ERS pero ausente en el diagrama de contexto.\n"
        "- EJEMPLO 2: Contenedor 'API Gateway' documentado en el DAS pero no representado en el diagrama de contenedores.\n"
        "- EJEMPLO 3: Relacion entre 'Frontend' y 'Backend' sin direccion ni protocolo indicado, impidiendo inferir el flujo de datos.\n\n"
        "[NEGATIVOS - Falso Positivo: Cosmetico o subjetivo]\n"
        "- EJEMPLO 1: 'El color azul de las cajas es confuso' — cosmetico, no afecta la arquitectura.\n"
        "- EJEMPLO 2: 'Las cajas del diagrama estan desalineadas' — preferencia estilistica, no es un defecto estructural.\n"
        "- EJEMPLO 3: 'Preferiria que se usen iconos diferentes para los actores' — subjetivo, no accionable."
    )

    FEW_SHOT_UML: str = (
        "\n\n=== EJEMPLOS DE HALLAZGOS ===\n"
        "[POSITIVOS - Buen Hallazgo: Violacion valida y accionable]\n"
        "- EJEMPLO 1: Clase 'PrestamoController' aparece en el diagrama pero no existe en el codigo fuente.\n"
        "- EJEMPLO 2: Multiplicidad omitida en la asociacion entre 'Usuario' y 'Prestamo', critica para entender cardinalidad.\n"
        "- EJEMPLO 3: Herencia indicada en el diagrama entre 'Usuario' y 'Administrador' que contradice la implementacion actual.\n\n"
        "[NEGATIVOS - Falso Positivo: Cosmetico o subjetivo]\n"
        "- EJEMPLO 1: 'La tipografia del diagrama es pequena pero aun legible' — no es un defecto funcional.\n"
        "- EJEMPLO 2: 'El color de las flechas de asociacion deberia ser rojo' — preferencia estilistica.\n"
        "- EJEMPLO 3: 'Los nombres de las clases suenan poco elegantes' — subjetivo, no es una inconsistencia tecnica."
    )

    FEW_SHOT_WIREFRAME: str = (
        "\n\n=== EJEMPLOS DE HALLAZGOS ===\n"
        "[POSITIVOS - Buen Hallazgo: Violacion valida y accionable]\n"
        "- EJEMPLO 1: Campo obligatorio 'ISBN' en el formulario de alta de libro no tiene etiqueta ni indicador de requerido.\n"
        "- EJEMPLO 2: Boton de accion principal 'Confirmar Prestamo' ausente en el wireframe respecto a la historia de usuario HU-03.\n"
        "- EJEMPLO 3: Flujo del wireframe muestra confirmacion antes de validacion, contradiciendo el ERS seccion 4.2.\n\n"
        "[NEGATIVOS - Falso Positivo: Cosmetico o subjetivo]\n"
        "- EJEMPLO 1: 'El color verde del boton Guardar no me gusta' — preferencia subjetiva de diseno.\n"
        "- EJEMPLO 2: 'Sugiero aumentar el espaciado entre campos' — cosmetico, no afecta usabilidad funcional.\n"
        "- EJEMPLO 3: 'Preferiria que la barra lateral este a la derecha' — layout subjetivo, no es un defecto."
    )

    FEW_SHOT_UNKNOWN: str = (
        "\n\n=== EJEMPLOS DE HALLAZGOS ===\n"
        "[POSITIVOS - Buen Hallazgo: Violacion valida y accionable]\n"
        "- EJEMPLO 1: Elemento importante del documento (tabla, diagrama o figura) esta cortado o incompleto en la imagen.\n"
        "- EJEMPLO 2: Texto dentro de la imagen es ilegible o de muy baja resolucion, impidiendo su verificacion.\n"
        "- EJEMPLO 3: Numeracion o titulo de figura en la imagen no coincide con la referencia del texto del documento.\n\n"
        "[NEGATIVOS - Falso Positivo: Cosmetico o subjetivo]\n"
        "- EJEMPLO 1: 'La imagen tiene bordes blancos' — cosmetico, no afecta el contenido.\n"
        "- EJEMPLO 2: 'Preferiria que la figura este centrada en la pagina' — preferencia de maquetacion.\n"
        "- EJEMPLO 3: 'La calidad de la imagen podria ser mejor' — subjetivo sin evidencia de ilegibilidad."
    )

    _FEW_SHOT_MAP: dict[DiagramType, str] = {
        DiagramType.C4_CONTEXT: FEW_SHOT_C4,
        DiagramType.C4_CONTAINER: FEW_SHOT_C4,
        DiagramType.C4_COMPONENT: FEW_SHOT_C4,
        DiagramType.UML_CLASS: FEW_SHOT_UML,
        DiagramType.UML_SEQUENCE: FEW_SHOT_UML,
        DiagramType.WIREFRAME: FEW_SHOT_WIREFRAME,
        DiagramType.UNKNOWN: FEW_SHOT_UNKNOWN,
    }

    @staticmethod
    def _few_shot_for(diagram_type: DiagramType) -> str:
        """Devuelve el bloque few-shot correspondiente al tipo de diagrama."""
        return ImageAnalyzer._FEW_SHOT_MAP.get(diagram_type, ImageAnalyzer.FEW_SHOT_UNKNOWN)

    def __init__(self, gemini_client: Any) -> None:
        """Inicializa con un GeminiClient (scripts.sqa_core.clients)."""
        self.gemini = gemini_client

    def analyze_image(
        self,
        image_path: Path,
        diagram_type: DiagramType,
        context: str,
    ) -> list[VisualFinding]:
        """Analiza una imagen y devuelve hallazgos estructurados.

        Args:
            image_path: Ruta al archivo de imagen (PNG, JPEG).
            diagram_type: Tipo de diagrama para seleccionar el prompt adecuado.
            context: Contexto del sistema (descripción breve).

        Returns:
            Lista de VisualFinding. Vacía si hay error o no hay hallazgos.
        """
        if not image_path.exists():
            logger.warning("Imagen no encontrada: %s", image_path)
            return []

        try:
            image_bytes = image_path.read_bytes()
        except OSError as exc:
            logger.error("Error leyendo imagen %s: %s", image_path, exc)
            return []

        # Codificar en base64 para enviar a Gemini
        b64_data = base64.b64encode(image_bytes).decode("utf-8")
        mime_type = self._infer_mime_type(image_path)

        prompt = self._build_prompt(diagram_type, context)

        try:
            # Gemini multimodal: prompt + imagen
            # El cliente GeminiClient tiene un método generate() que recibe texto.
            # Para imágenes necesitamos usar la API de Gemini directamente o extender el cliente.
            # Por ahora, construimos un mensaje multimodal.
            raw = self._generate_multimodal(prompt, b64_data, mime_type)
        except Exception as exc:
            logger.error("Error en análisis visual de %s: %s", image_path, exc)
            return []

        return self._parse_findings(raw, diagram_type)

    def batch_analyze(
        self,
        images: list[tuple[Path, DiagramType, str]],
    ) -> list[tuple[Path, list[VisualFinding]]]:
        """Analiza múltiples imágenes en batch.

        Args:
            images: Lista de (path, diagram_type, context).

        Returns:
            Lista de (path, findings) — solo para imágenes que existen.
        """
        results: list[tuple[Path, list[VisualFinding]]] = []
        for image_path, diagram_type, context in images:
            if not image_path.exists():
                logger.warning("Skipping missing image: %s", image_path)
                continue
            findings = self.analyze_image(image_path, diagram_type, context)
            results.append((image_path, findings))
        return results

    def _build_prompt(self, diagram_type: DiagramType, context: str) -> str:
        """Construye el prompt para Gemini incluyendo contexto y ejemplos few-shot.

        Meta de precision esperada: >= 70% de hallazgos validos tras validacion humana.
        """
        template = self._PROMPTS.get(diagram_type, self._PROMPTS[DiagramType.UNKNOWN])
        few_shot = self._few_shot_for(diagram_type)
        # Usamos replace en lugar de format para no interpretar las llaves JSON
        base = template.replace("{context}", context or "Sistema de Gestion Bibliotecaria")
        return f"{base}{few_shot}"

    def _infer_mime_type(self, path: Path) -> str:
        """Infiere el MIME type de la imagen por extensión."""
        ext = path.suffix.lower()
        mapping = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        return mapping.get(ext, "image/png")

    def _generate_multimodal(
        self, prompt: str, b64_image: str, mime_type: str
    ) -> str:
        """Envía prompt + imagen a Gemini y devuelve la respuesta en texto.

        NOTA: Esto requiere acceso a la API subyacente de google.generativeai.
        Si GeminiClient no expone el modelo subyacente, este método fallará
        y deberá adaptarse.
        """
        # Intentar acceder al modelo subyacente del GeminiClient
        model = getattr(self.gemini, "model", None)
        if model is None:
            # Fallback: usar generate() con texto plano (no multimodal)
            # Esto no es ideal pero permite testing sin acceso al modelo real
            logger.warning(
                "GeminiClient no expone el modelo subyacente; "
                "usando modo texto-only (no se enviará la imagen)."
            )
            return self.gemini.generate(prompt)

        # API multimodal de Gemini
        response = model.generate_content(
            [
                prompt,
                {
                    "mime_type": mime_type,
                    "data": b64_image,
                },
            ]
        )
        return response.text

    def _parse_findings(
        self, raw: str, default_type: DiagramType
    ) -> list[VisualFinding]:
        """Parsea la respuesta JSON de Gemini en VisualFinding objects."""
        try:
            data: dict[str, Any] = json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.warning("Respuesta de Gemini no es JSON válido: %s", exc)
            return []

        findings_data = data.get("findings", [])
        if not isinstance(findings_data, list):
            logger.warning("Campo 'findings' no es una lista")
            return []

        findings: list[VisualFinding] = []
        for item in findings_data:
            try:
                findings.append(
                    VisualFinding(
                        id=str(item.get("id", "VIS-UNKNOWN")),
                        diagram_type=DiagramType(
                            item.get("diagram_type", default_type.value)
                        ),
                        description=str(item.get("description", "")),
                        severity=self._normalize_severity(
                            str(item.get("severity", "Media"))
                        ),
                        page_reference=str(item.get("page_reference", "")),
                        evidence=str(item.get("evidence", "")),
                    )
                )
            except (KeyError, ValueError) as exc:
                logger.warning("Hallazgo malformado, se omite: %s", exc)
                continue

        return findings

    @staticmethod
    def _normalize_severity(sev: str) -> str:
        """Normaliza severidad a valores estándar del proyecto."""
        mapping = {
            "critical": "Crítica",
            "critica": "Crítica",
            "high": "Alta",
            "alta": "Alta",
            "medium": "Media",
            "media": "Media",
            "low": "Baja",
            "baja": "Baja",
        }
        return mapping.get(sev.lower(), sev)
