import sys
from main import LMSApp

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python initiation_logic.py input_file_path")
        sys.exit(1)

    input_file = sys.argv[1]
    app = LMSApp()
    app.process_commands(input_file)
