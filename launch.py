import subprocess
import sys
import os

def main():
    """
    A user-friendly script to launch the Quantum Smart Farming Dashboard.

    This script ensures the app is run from the correct directory and applies
    custom theme settings for a consistent look and feel.
    """
    print("🌾 Starting Quantum Smart Farming Dashboard...")

    # --- Pre-flight Checks ---
    if not os.path.exists('app.py'):
        print("\n❌ ERROR: app.py not found.")
        print("Please run this script from the project's root directory.")
        sys.exit(1)

    if sys.prefix == sys.base_prefix:
         print("\n⚠️ WARNING: It looks like your virtual environment is not activated.")
         print("Please activate it first with: venv\\Scripts\\activate")
         if input("Continue anyway? (y/n): ").lower() != 'y':
             sys.exit(1)

    # --- Construct and Run the Streamlit Command ---
    # CORRECTED: Removed internal quotes from all theme values.
    command = [
        sys.executable,
        '-m', 'streamlit', 'run', 'app.py',
        '--server.port=8501',
        '--server.address=localhost',
        '--theme.primaryColor=#00bf63',
        '--theme.backgroundColor=#ffffff',
        '--theme.secondaryBackgroundColor=#f0f2f6',
        '--theme.textColor=#0a0a0a',
        '--theme.font=sans serif'
    ]

    print("\n🚀 Launching Streamlit... Press Ctrl+C here to stop the server.")
    print(f"   Your dashboard will be available at: http://localhost:8501")

    try:
        subprocess.run(command, check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard stopped by user. Have a great day!")
    except Exception as e:
        print(f"\n❌ An error occurred while trying to launch Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()