from __future__ import print_function


def ffmpeg_opts(parser):
    group = parser.add_argument_group("rephrase-vs-ffmpeg")

    group.add(
        "--request",
        "-request",
        type=str,
        required=True,
        help="Natural language request to generate relevant ffmpeg code.",
    )

    group.add(
        "--input_files",
        "-input_files",
        type=str,
        nargs="+",
        help="Files over which the ffmpeg command should be executed. Please note that the files should be in the code directory.",
    )

    group.add(
        "--output_file_name",
        "-output_file_name",
        type=str,
        help="Output file name for the ffmpeg command, prevents overwrites. Extension will automatically be taken care of by the tool.",
    )

    group.add(
        "--preview",
        "-preview",
        action="store_true",
        help="If passed, you will be able to preview the generated ffmpeg command before it acts on your input files.",
    )

    group.add(
        "--debug_mode",
        "-debug_mode",
        action="store_true",
        help="If passed, you can provide your own ffmpeg command to be debugged, along with the request for intended functionality.",
    )

    group.add(
        "--command", "-command", type=str, help="Your ffmpeg command to be debugged."
    )

def moderation_opts(parser):
    group = parser.add_argument_group("rephrase-content-moderator")

    group.add(
        "--inp_text",
        "-inp_text",
        type=str,
        required=True,
        help="User's natural language request for video generation.",
    )

    group.add(
        "--model",
        "-model",
        type=str,
        default="gpt-4",
        help="Completion model to be used. Note that while GPT-4 has a better understanding of the world, davinci models on OpenAI playground seemed actually enough for our usecase.",
    )

def animation_opts(parser):
    group = parser.add_argument_group("rephrase-animator")

    group.add(
        "--theme",
        "-theme",
        type=str,
        required=True,
        help="Theme for generating beautiful animations using p5.js.",
    )

    group.add(
        "--added_creativity",
        "-added_creativity",
        action="store_true",
        help="If passed, the prompt is engineered to generate more creative outputs. Note that this increases the probability of garbage results.",
    )

    group.add(
        "--duration",
        "-duration",
        type=int,
        default=1,
        help="Specifies duration of animation in seconds.",
    )