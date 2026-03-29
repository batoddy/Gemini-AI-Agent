# app/config.py

import os
from pathlib import Path

from dotenv import load_dotenv

from app.exceptions import ConfigurationError


class AppConfig:
    """Central application configuration."""

    def __init__(
        self,
        gemini_api_key: str,
        model_name: str,
        sandbox_path: Path,
        debug: bool,
        memory_dump_path: Path,
        llm_trace_path: Path,
    ) -> None:
        self.gemini_api_key = gemini_api_key
        self.model_name = model_name
        self.sandbox_path = sandbox_path
        self.debug = debug
        self.memory_dump_path = memory_dump_path
        self.llm_trace_path = llm_trace_path

    @classmethod
    def from_env(cls) -> "AppConfig":
        load_dotenv()

        gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not gemini_api_key:
            raise ConfigurationError("Missing GEMINI_API_KEY environment variable.")

        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()

        debug_value = os.getenv("AGENT_DEBUG", "false").strip().lower()
        debug = debug_value in {"1", "true", "yes", "on"}

        sandbox_raw = os.getenv("SANDBOX_PATH", "sandbox").strip()
        sandbox_path = Path(sandbox_raw).resolve()

        memory_dump_raw = os.getenv("MEMORY_DUMP_PATH", "debug/memory_dump.txt").strip()
        memory_dump_path = Path(memory_dump_raw).resolve()

        llm_trace_raw = os.getenv("LLM_TRACE_PATH", "debug/llm_trace.txt").strip()
        llm_trace_path = Path(llm_trace_raw).resolve()

        return cls(
            gemini_api_key=gemini_api_key,
            model_name=model_name,
            sandbox_path=sandbox_path,
            debug=debug,
            memory_dump_path=memory_dump_path,
            llm_trace_path=llm_trace_path,
        )
