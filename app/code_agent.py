import sys
import io

class FataCodeAgent:
    def execute_python(self, code: str) -> str:
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        
        try:
            exec(code, {"__builtins__": __builtins__})
            output = redirected_output.getvalue()
            return output if output else "✅ Code executed successfully with no printed output."
        except Exception as e:
            return f"❌ Execution Error: {str(e)}"
        finally:
            sys.stdout = old_stdout

fata_code_agent = FataCodeAgent()