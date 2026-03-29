# tools/calculator_tool.py

from typing import Any, Dict

from app.exceptions import ToolValidationError
from tools.base_tool import BaseTool


class CalculatorTool(BaseTool):
    """Tool for evaluating safe arithmetic expressions."""

    def __init__(self) -> None:
        self._allowed_chars = set("0123456789+-*/(). %")

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Evaluates arithmetic expressions safely."

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "expression": {
                        "type_": "STRING",
                        "description": "Arithmetic expression to evaluate, for example: 12 * (3 + 4)",
                    }
                },
                "required": ["expression"],
            },
        }

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        expression = kwargs.get("expression")

        if not expression or not isinstance(expression, str):
            raise ToolValidationError(
                "The 'expression' argument is required and must be a string."
            )

        cleaned_expression = expression.strip()
        if not cleaned_expression:
            raise ToolValidationError("The expression cannot be empty.")

        for char in cleaned_expression:
            if char not in self._allowed_chars:
                raise ToolValidationError(
                    f"Invalid character detected in expression: '{char}'"
                )

        try:
            result = eval(cleaned_expression, {"__builtins__": {}}, {})
        except ZeroDivisionError:
            return {
                "status": "error",
                "tool": self.name,
                "error": "Division by zero is not allowed.",
            }
        except Exception as exc:
            return {
                "status": "error",
                "tool": self.name,
                "error": f"Failed to evaluate expression: {exc}",
            }

        return {
            "status": "success",
            "tool": self.name,
            "expression": cleaned_expression,
            "result": result,
        }
