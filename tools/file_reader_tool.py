# tools/file_reader_tool.py

from pathlib import Path
from typing import Any, Dict

from app.exceptions import ToolValidationError
from tools.base_tool import BaseTool


class FileReaderTool(BaseTool):
    """Tool for reading text files from a restricted sandbox directory."""

    def __init__(self, sandbox_path: Path) -> None:
        self._sandbox_path = sandbox_path

    @property
    def name(self) -> str:
        return "file_reader"

    @property
    def description(self) -> str:
        return "Reads text-based files from the sandbox directory."

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "filename": {
                        "type_": "STRING",
                        "description": "Name of the file to read from the sandbox directory.",
                    }
                },
                "required": ["filename"],
            },
        }

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        filename = kwargs.get("filename")

        if not filename or not isinstance(filename, str):
            raise ToolValidationError(
                "The 'filename' argument is required and must be a string."
            )

        cleaned_filename = filename.strip()
        if not cleaned_filename:
            raise ToolValidationError("The filename cannot be empty.")

        if "/" in cleaned_filename or "\\" in cleaned_filename:
            raise ToolValidationError(
                "Only plain filenames are allowed, not full paths."
            )

        if not cleaned_filename.endswith((".txt", ".md")):
            return {
                "status": "error",
                "tool": self.name,
                "error": "Only .txt and .md files are supported.",
            }

        file_path = self._sandbox_path / cleaned_filename

        if not file_path.exists():
            return {
                "status": "error",
                "tool": self.name,
                "error": f"File not found: {cleaned_filename}",
            }

        if not file_path.is_file():
            return {
                "status": "error",
                "tool": self.name,
                "error": f"'{cleaned_filename}' is not a file.",
            }

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as exc:
            return {
                "status": "error",
                "tool": self.name,
                "error": f"Could not read file: {exc}",
            }

        return {
            "status": "success",
            "tool": self.name,
            "filename": cleaned_filename,
            "content": content,
        }
