import os
import re
import warnings

import subprocess
import openai
from utils.parser import ArgumentParser
from utils.opts import ffmpeg_opts


def generate_ffmpeg(prompt, inputs):
    """
    Generate ffmpeg command for an intended use case, powered by the completion API (GPT-3).
    """
    # -- Code Generation Prompt -> tested on playground
    prompt = f"Generate an ffmpeg command in response to the prompt below. Do not add anything other than the ffmpeg command in your response. Name the output file 'output' with the appropriate extension except in the case of repeating outputs where you use a pattern.\n\nRequest: {prompt}\n\nInput files: {inputs}"

    # -- Temperature was set to 0.0 to get only the most obvious outputs, no creativity

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        n=1,
        max_tokens=500,
    )

    # return completion.choices[0].text
    return completion.choices[0].message.content


def ffmpeg_debug(command, prompt):
    """
    Debug a generated ffmpeg command, powered by GPT-3.
    """
    # -- Debugging Prompt -> Tested on playground
    prompt = f"Fix the following ffmpeg command. The intended functionality is to {prompt}.\n\n{command}"

    # -- Temperature was set to 0.0 to get only the most obvious outputs, no creativity
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.0,
    )

    # -- Return the fixed command
    return completion.choices[0].text


def security_checks(command):
    """
    Check for malicious intent in the code generated by the Completion API.
    This is not a comprehensive list, but I've tried to include some of the more obvious culprits which may be generated alongside ffmpeg commands.
    """
    patterns = [
        r"rm -rf",  # -- shouldn't delete files
        r"wget",  # -- shouldn't download anything (noted some trojan warnings in available apps)
        r"curl",  # -- shouldn't transfer files
        r"python",  # -- shouldn't run python files
        r"bash",  # -- shell scripts
        r"zsh",  # -- shell scripts
        r"&&",  # -- shell scripts
        r"apt-get",  # -- installations
        r"pip",  # -- installations
        r"git",  # -- installations / cloning malicious repos
        r"chmod",  # -- change file permissions
        r"echo",  # -- function definition vulnerabilities
        r"cat",  # -- code injection vulnerabilities
        r"awk",  # -- https://gtfobins.github.io/gtfobins/awk/
        r"grep",  # -- Not privy with the details, but grep can be used to carry out a DoS attack
    ]

    # -- Search patterns
    for pattern in patterns:
        if re.search(pattern, command):
            return False

    # If none of the patterns were found, return True
    return True


def code_generation(args):
    assert args.input_files != None, "Input files for processing not provided."

    input_files = ", ".join([f for f in args.input_files])

    # -- Generate ffmpeg command with OpenAI completion
    command = generate_ffmpeg(args.request, input_files)

    # -- Replace output with provided output file name
    if args.output_file_name:
        command = command.replace(
            "output", '"' + os.path.abspath(".") + f"/{args.output_file_name}"
        )

    while True:
        if security_checks(command):
            # -- Security checks cleared, continue
            if args.preview:
                print(f"Preview of generated ffmpeg command: {command}")
                debug = input("Do you want to debug the code for errors (y/n)?")

                if debug.lower() == "n":
                    break

                # -- Prompt GPT-4 to debug generated command
                command = ffmpeg_debug(command, args.request)

        else:
            # Command has potentially extreneous or malicious arguments that shouldn't be run
            print(red + "Potentially harmful command generated. Aborting.")
            print(red + "Failed command: " + command)

    # -- Execute ffmpeg command as subprocess
    print(green + "Running command: " + command)
    subprocess.run(command, shell=True)


def code_debugging(args):
    assert args.command != None, "ffmpeg command to be debugged not provided"
    assert (
        args.output_file_name == None
    ), "output file will remain the same as that input in the command"

    command = args.command

    # -- Prompt GPT-4 to debug generated command
    command = ffmpeg_debug(command, args.request)
    print(f"Corrected Command: {command}")

    # -- Raise warning if the updated command fails security checks
    if not security_checks(command):
        warnings.warn(
            red
            + "The fixed ffmpeg command seems to harbor malicious content. It is not recommended that it be executed."
        )


def _get_parser():
    parser = ArgumentParser(description="app.py")
    ffmpeg_opts(parser)
    return parser


def main():
    openai.api_key = os.environ["API_KEY"]

    # -- Initialize parser
    parser = _get_parser()
    args = parser.parse_args()

    # -- Define ANSI color codes as globals
    global green, red
    green = "\033[32m"
    red = "\033[31m"

    if not args.debug_mode:
        code_generation(args)
    else:
        code_debugging(args)


if __name__ == "__main__":
    main()