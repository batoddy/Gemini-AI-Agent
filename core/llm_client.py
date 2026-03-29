# core/llm_client.py

import json
from typing import Any, Dict, List, Optional

import google.generativeai as genai

from app.exceptions import LLMClientError
from core.trace_logger import LLMTraceLogger


class GeminiLLMClient:
    """Wrapper around the Gemini API for agent use."""

    def __init__(
        self,
        api_key: str,
        model_name: str,
        trace_logger: Optional[LLMTraceLogger] = None,
    ) -> None:
        self._model_name = model_name
        self._trace_logger = trace_logger

        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_name=self._model_name, tools=[])

    def generate(
        self,
        history: List[Dict[str, Any]],
        tool_declarations: List[dict],
    ) -> Dict[str, Any]:
        """
        Send the conversation history and tool declarations to Gemini.
        """
        try:
            self._model = genai.GenerativeModel(
                model_name=self._model_name, tools=tool_declarations
            )

            prompt = self._build_prompt(history)

            if self._trace_logger is not None:
                self._trace_logger.log_llm_input(prompt)

            response = self._model.generate_content(prompt)

            if self._trace_logger is not None:
                self._trace_logger.log_raw_response(str(response))

            parsed = self._parse_response(response)

            if self._trace_logger is not None:
                self._trace_logger.log_parsed_response(
                    response_type=parsed["type"],
                    content=json.dumps(parsed, ensure_ascii=False, indent=2),
                )

            return parsed

        except Exception as exc:
            if self._trace_logger is not None:
                self._trace_logger.log_section(
                    "LLM ERROR",
                    str(exc),
                )

            raise LLMClientError(f"Gemini generation failed: {exc}") from exc

    def _build_prompt(self, history: List[Dict[str, Any]]) -> str:
        """
        Convert internal memory history into a single textual prompt.
        """
        lines = []

        system_instruction = (
            "You are an adaptive personal assistant agent. "
            "Use tools only when needed. "
            "If a tool result is already available in the conversation history, "
            "do not call the same tool again with the same arguments. "
            "Instead, use the tool result to produce the final answer. "
            "If no tool is needed, answer directly in natural language."
        )
        lines.append(f"SYSTEM: {system_instruction}")

        for message in history:
            role = message.get("role")
            content = message.get("content")

            if role == "user":
                lines.append(f"USER: {content}")

            elif role == "assistant":
                lines.append(f"ASSISTANT: {content}")

            elif role == "tool":
                tool_name = message.get("tool_name", "unknown_tool")
                tool_content = json.dumps(content, ensure_ascii=False)
                lines.append(f"TOOL ({tool_name}): {tool_content}")

            elif role == "system":
                lines.append(f"SYSTEM: {content}")

            else:
                raise LLMClientError(f"Unsupported memory role: {role}")

        return "\n".join(lines)

    def _parse_response(self, response: Any) -> Dict[str, Any]:
        """
        Parse Gemini response and normalize it for the Agent.
        """
        try:
            parts = response.candidates[0].content.parts

            for part in parts:
                function_call = getattr(part, "function_call", None)
                if function_call:
                    tool_name = function_call.name
                    args = dict(function_call.args) if function_call.args else {}

                    return {
                        "type": "tool_call",
                        "tool_name": tool_name,
                        "args": args,
                    }

            text = ""
            if hasattr(response, "text") and response.text:
                text = response.text.strip()

            if not text:
                text_parts = []
                for part in parts:
                    maybe_text = getattr(part, "text", None)
                    if maybe_text:
                        text_parts.append(maybe_text)
                text = "\n".join(text_parts).strip()

            if not text:
                raise LLMClientError("Gemini returned neither text nor tool call.")

            return {
                "type": "final",
                "content": text,
            }

        except Exception as exc:
            raise LLMClientError(f"Failed to parse Gemini response: {exc}") from exc
