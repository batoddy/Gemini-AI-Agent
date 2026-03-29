# Adaptive AI Personal Assistant Agent

This project is a command-line based adaptive AI agent built with the Google Gemini API.  
The main goal of the project is not only to generate responses, but also to design the system using clean software architecture principles, SOLID principles, and design patterns.

The agent can:

- communicate with the user in natural language,
- remember the conversation during the session,
- decide when a tool is needed,
- execute tools dynamically,
- use the tool result to generate a final response.

## Project Goal

This project was developed for an assignment focused on building an adaptive AI agent with a modular and extensible architecture.

The system follows the **Reason → Act → Observe** idea:

1. The user sends a request.
2. The agent sends the conversation context to Gemini.
3. Gemini either answers directly or requests a tool call.
4. The agent executes the requested tool.
5. The tool result is added to memory.
6. Gemini uses that result to produce the final answer.

## Architecture

The project is divided into separate components to satisfy separation of concerns.

### Main Components

- **Agent**  
  Controls the main ReAct loop and coordinates the system.

- **MemoryManager**  
  Stores conversation history during the session.

- **ToolRegistry**  
  Registers tools and executes them dynamically by name.

- **BaseTool**  
  Abstract tool interface used by all tools.

- **GeminiLLMClient**  
  Handles communication with the Gemini API.

- **Observers**  
  Used for logging and usage tracking without coupling these concerns to the main agent logic.

## Design Patterns Used

### Strategy Pattern

Each tool is implemented as a separate strategy:

- CalculatorTool
- TimeTool
- WeatherTool
- FileReaderTool

### Registry / Factory Pattern

Tools are not hardcoded inside the agent.  
Instead, they are registered in `ToolRegistry` and executed dynamically.

### Observer Pattern

The agent emits events, and observers listen to those events.
This is used for:

- console logging,
- usage tracking.

## Tools

The agent currently supports four tools:

- **CalculatorTool**  
  Evaluates arithmetic expressions.

- **TimeTool**  
  Returns the current local date and time.

- **WeatherTool**  
  Gets the current weather of a city using the Open-Meteo API.

- **FileReaderTool**  
  Reads `.txt` and `.md` files from a restricted sandbox folder.

### Custom Tools

The two custom tools in this project are:

- `WeatherTool`
- `FileReaderTool`

## Memory

The agent keeps conversation history in memory during runtime.  
This allows the model to use previous user messages, assistant responses, and tool results in later steps of the conversation.

For debugging purposes, memory can also be dumped into a text file.

## LLM Trace Logging

For debugging and understanding the agent flow, the system can write:

- what is sent to the LLM,
- what is returned by the LLM,
- parsed tool calls or final answers

into a trace file.

This makes it easier to observe how function calling works internally.

## Error Handling

The system includes basic error handling for:

- missing API key,
- invalid tool arguments,
- unknown tools,
- API request failures,
- missing files,
- invalid city names for weather queries.

The goal is to keep the system running gracefully whenever possible.

## Project Structure

```text
project/
│
├── main.py
├── requirements.txt
├── .env
│
├── app/
│   ├── config.py
│   └── exceptions.py
│
├── core/
│   ├── agent.py
│   ├── llm_client.py
│   ├── memory.py
│   ├── registry.py
│   ├── observer.py
│   ├── events.py
│   └── trace_logger.py
│
├── tools/
│   ├── base_tool.py
│   ├── calculator_tool.py
│   ├── time_tool.py
│   ├── weather_tool.py
│   └── file_reader_tool.py
│
├── observers/
│   ├── logging_observer.py
│   └── usage_observer.py
│
└── sandbox/

Installation

Install the required packages:

pip install -r requirements.txt
Environment Variables

Create a .env file in the project root and define the following variables:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.1-flash-lite-preview
AGENT_DEBUG=true
SANDBOX_PATH=sandbox
MEMORY_DUMP_PATH=debug/memory_dump.txt
LLM_TRACE_PATH=debug/llm_trace.txt
Running the Project

Run the application from the terminal:

python main.py

The program starts an interactive CLI session.

Example inputs:

hi
what time is it
calculate 4*4*4*4
what is the weather in Istanbul
read sample_notes.txt

To exit:

exit
Example Flow

Example for a tool-based request:

User asks: what time is it
Gemini requests the time tool
The agent executes TimeTool
The result is stored in memory
Gemini generates the final natural language response
Notes
The agent memory is session-based.
The project focuses mainly on software architecture and extensibility.
New tools can be added without changing the core Agent logic.
Conclusion

This project demonstrates how an LLM-based assistant can be designed with clean architecture principles instead of monolithic scripting.
The final system is modular, easier to extend, and suitable for experimenting with tool-based AI agent behavior.



```
