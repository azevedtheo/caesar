import sys
from pathlib import Path

def read_input(text: str | None, input_file: Path | None) -> str:
    if text: return text
    if input_file: return input_file.read_text(encoding = "utf-8")
    if not sys.stdin.isatty(): return sys.stdin.read() 
    raise ValueError("No input provided")
    
def write_output(
    content: str,
    output_file: Path | None,
    quiet: bool,
) -> None:
    if output_file is not None:
        output_file.write_text(
                                content,
                                encoding = "utf-8"
                              )
        if not quiet:
            print(f"Output written to {output_file}")

        return
        
    if not quiet:
        print(content)

def validate_key(key: int) -> None:
    if not 0 <= key <= 26:
        raise ValueError("Key must be between 0 and 26, got {0}".format(key))
