import subprocess


def execute_cmd(command: str | list[str], shell: bool = True) -> str:
    """
    Executes a shell command using subprocess and returns its output.
    If the command fails, it returns the error message.
    """
    try:
        # Run the command, capturing both stdout and stderr
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()  # Return standard output if successful
    except subprocess.CalledProcessError as e:
        # Return error message if the command execution fails
        return f"Error: {e.stderr.strip()}"


def execute_yt_dlp(command: str):
    execute_cmd("yt-dlp" + command)


def execute_idle():
    execute_cmd("python -m idlelib")


# Example usage:
if __name__ == "__main__":
    # cmd = input(">>>")
    # output = execute_cmd(cmd)
    # print("Output:", output)
    execute_idle()
