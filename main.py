# main.py

from pathlib import Path

from app.config import AppConfig
from app.exceptions import AgentError, ConfigurationError
from core.agent import Agent
from core.llm_client import GeminiLLMClient
from core.memory import MemoryManager
from core.registry import ToolRegistry
from core.trace_logger import LLMTraceLogger
from observers.logging_observer import LoggingObserver
from observers.usage_observer import UsageObserver
from tools.calculator_tool import CalculatorTool
from tools.file_reader_tool import FileReaderTool
from tools.time_tool import TimeTool
from tools.weather_tool import WeatherTool


def ensure_sandbox_exists(sandbox_path: Path) -> None:
    """Create the sandbox directory if it does not exist."""
    sandbox_path.mkdir(parents=True, exist_ok=True)


def build_agent(config: AppConfig) -> tuple[Agent, UsageObserver]:
    """
    Build and wire the complete agent system.
    """
    memory_manager = MemoryManager(dump_file_path=config.memory_dump_path)

    tool_registry = ToolRegistry()

    trace_logger = LLMTraceLogger(trace_file_path=config.llm_trace_path)

    llm_client = GeminiLLMClient(
        api_key=config.gemini_api_key,
        model_name=config.model_name,
        trace_logger=trace_logger,
    )

    tool_registry.register(CalculatorTool())
    tool_registry.register(TimeTool())
    tool_registry.register(WeatherTool())
    tool_registry.register(FileReaderTool(config.sandbox_path))

    agent = Agent(
        llm_client=llm_client,
        memory_manager=memory_manager,
        tool_registry=tool_registry,
        max_iterations=5,
    )

    logging_observer = LoggingObserver()
    usage_observer = UsageObserver()

    agent.attach(logging_observer)
    agent.attach(usage_observer)

    return agent, usage_observer


def run_cli() -> None:
    """Run the interactive CLI loop."""
    try:
        config = AppConfig.from_env()
        ensure_sandbox_exists(config.sandbox_path)

        agent, usage_observer = build_agent(config)

        print("Personal Assistant Agent started.")
        print("Type 'exit' to quit.\n")

        while True:
            user_input = input("You: ").strip()

            if not user_input:
                print("Agent: Please enter a message.")
                continue

            if user_input.lower() in {"exit", "quit"}:
                print("\nSession summary:")
                print(usage_observer.get_summary())
                print("Goodbye!")
                break

            try:
                response = agent.handle_user_input(user_input)
                print(f"Agent: {response}\n")
            except AgentError as exc:
                print(f"Agent error: {exc}\n")
            except Exception as exc:
                print(f"Unexpected error: {exc}\n")

    except ConfigurationError as exc:
        print(f"Configuration error: {exc}")
    except Exception as exc:
        print(f"Startup error: {exc}")


if __name__ == "__main__":
    run_cli()
