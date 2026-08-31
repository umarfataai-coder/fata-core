import sys
import io
import traceback

class FataCodeAgent:
    def __init__(self):
        print("Agentic Code Interpreter: Active.")

    def execute_python_code(self, code_str: str) -> str:
        """Gudanar da lambar Python a keɓe sannan a maido sakamako"""
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        
        try:
            # Gudanar da lamba
            exec(code_str, {"__builtins__": __builtins__})
            output = redirected_output.getvalue()
            sys.stdout = old_stdout
            return f"✅ **Sakamakon Aiki (Execution Output):**\n```\n{output}\n```"
        except Exception as e:
            sys.stdout = old_stdout
            error_msg = traceback.format_exc()
            return f"❌ **Kuskure a Lambar (Code Error):**\n```\n{error_msg}\n```"

fata_code_agent = FataCodeAgent()