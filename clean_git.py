import subprocess
import os
import sys

def run_command(command, cwd=None):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, check=True, text=True, cwd=cwd)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}")
        print(e)
        sys.exit(1)

def main():
    # Safety check: confirm with user before destructive operation
    confirm = input(
        "WARNING: This will rewrite your git history to remove 'credentials.json' and force push.\n"
        "Make sure you have backed up your repo.\n"
        "Continue? (yes/no): "
    )
    if confirm.lower() != "yes":
        print("Aborted.")
        sys.exit(0)

    # Path to your BFG jar - update this to where you saved bfg.jar
    bfg_path = "path/to/bfg.jar"  # e.g. "C:/Users/YourUser/Downloads/bfg.jar"

    # Verify BFG jar exists
    if not os.path.isfile(bfg_path):
        print(f"Cannot find BFG jar at {bfg_path}. Please update the path.")
        sys.exit(1)

    # Run BFG to remove credentials.json
    print("Running BFG to delete credentials.json from history...")
    run_command(["java", "-jar", bfg_path, "--delete-files", "credentials.json"])

    # Run git cleanup commands
    print("Cleaning up git reflog and pruning...")
    run_command(["git", "reflog", "expire", "--expire=now", "--all"])
    run_command(["git", "gc", "--prune=now", "--aggressive"])

    # Force push to remote
    print("Force pushing cleaned history to remote...")
    run_command(["git", "push", "--force"])

    print("Done! 'credentials.json' removed from git history and changes pushed.")

if __name__ == "__main__":
    main()
