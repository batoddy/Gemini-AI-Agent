# core/trace_logger.py

from datetime import datetime
from pathlib import Path
from typing import Optional


class LLMTraceLogger:
    """Writes LLM inputs and outputs to a trace file for debugging."""

    def __init__(self, trace_file_path: Path) -> None:
        self._trace_file_path = trace_file_path

    def log_section(self, title: str, content: str) -> None:
        self._trace_file_path.parent.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self._trace_file_path.open("a", encoding="utf-8") as file:
            file.write("\n")
            file.write("=" * 80 + "\n")
            file.write(f"[{timestamp}] {title}\n")
            file.write("=" * 80 + "\n")
            file.write(content)
            file.write("\n")

    def log_llm_input(self, prompt: str) -> None:
        self.log_section("LLM INPUT", prompt)

    def log_raw_response(self, raw_response: str) -> None:
        self.log_section("LLM RAW OUTPUT", raw_response)

    def log_parsed_response(
        self,
        response_type: str,
        content: str,
    ) -> None:
        self.log_section(
            f"LLM PARSED OUTPUT ({response_type})",
            content,
        )
