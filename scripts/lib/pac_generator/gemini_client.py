"""GeminiClient: Cliente para formateo de secciones del PAC con IA.

Este módulo encapsula la interacción con la API de Gemini (google-generativeai)
como EDITOR, no autor.  Solo formatea y profesionaliza la información
proporcionada por el líder de métricas.
"""
from __future__ import annotations

import importlib.util
import json


class GeminiClient:
    """Cliente determinista para formateo de secciones del PAC."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._cache: dict[int, str] = {}
        self._model: object | None = None

        if self.is_available():
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            self._model = genai.GenerativeModel("gemini-pro")

    @staticmethod
    def is_available() -> bool:
        """Retorna True si google-generativeai está instalado."""
        return importlib.util.find_spec("google.generativeai") is not None

    def format_section(self, section_name: str, directives: dict) -> str:
        """Formatea una sección del PAC usando Gemini como editor.

        Args:
            section_name: Nombre de la sección.
            directives: Directivas del líder de métricas.

        Returns:
            Texto markdown formateado, o mensaje de fallback si la API
            no está disponible o falla.
        """
        if not self.is_available() or self._model is None:
            return f"[FORMATEO GEMINI NO DISPONIBLE: {section_name}]"

        cache_key = hash((section_name, json.dumps(directives, sort_keys=True)))
        if cache_key in self._cache:
            return self._cache[cache_key]

        prompt = (
            "You are a technical writer specializing in IEEE 730-2014 Quality Assurance Plans.\n"
            "Format the following section professionally in markdown. Do NOT add information not provided.\n"
            "Do NOT invent metrics, dates, or roles. Only format what is given.\n\n"
            f"Section: {section_name}\n"
            f"Directives: {json.dumps(directives)}\n\n"
            "Write in Spanish. Use professional technical language."
        )

        try:
            response = self._model.generate_content(prompt)
            result = response.text
        except Exception:
            result = f"[FORMATEO GEMINI NO DISPONIBLE: {section_name}]"

        self._cache[cache_key] = result
        return result
