import argparse
import pyfiglet
from pyfiglet import FigletFont
import traceback

PH_PS1 = "{PS1}"
""" The placeholder for the PS1 prefix. """

PH_BANNER = "{BANNER}"
""" The placeholder for the pyfiglet banner. """

PH_SUBTITLE = "{SUBTITLE}"
""" The placeholder for the PS1 prefix. """

DEFAULT_TOP = \
"""# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
# Copyright 2020 University of Waikato, Hamilton, NZ. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ==============================================================================

export PS1="\[\e[31m\]{PS1}\[\e[m\] \[\e[33m\]\w\[\e[m\] > "
export TERM=xterm-256color
alias grep="grep --color=auto"
alias ls="ls --color=auto"

echo -e "\e[1;31m"
cat<<DBG
"""

DEFAULT_BOTTOM = \
"""
DBG
echo -e "\e[0;33m"

if [[ $EUID -eq 0 ]]; then
  cat <<WARN
WARNING: You are running this container as root, which can cause new files in
mounted volumes to be created as the root user on your host machine.

To avoid this, run the container by specifying your user's userid:

$ docker run -u \$(id -u):\$(id -g) args...
WARN
else
  cat <<EXPL
You are running this container as user with ID $(id -u) and group $(id -g),
which should map to the ID and group for your user on the Docker host. Great!
EXPL
fi

# Turn off colors
echo -e "\e[m"
"""


DEFAULT_TEMPLATE = DEFAULT_TOP + "{BANNER}\n" + DEFAULT_BOTTOM

DEFAULT_TEMPLATE_SUBTITLE = DEFAULT_TOP + "{BANNER}\n{SUBTITLE}\n" + DEFAULT_BOTTOM


def generate(banner, font="standard", subtitle=None, template=None, template_file=None, ps1="docker",
             width=80, output=None):
    """
    Generates the bash.bashrc file.

    :param banner: the banner text to push through pyfiglet
    :type banner: str
    :param font: the figlet font to use, default: standard
    :type font: str
    :param subtitle: the subtitle to use, ignored if none: default: None
    :type subtitle: str
    :param template: the template string to use if not using the built-in one, default: None
    :type template: str
    :param template_file: the template file to use if not using the built-in one, default: None
    :type template_file: str
    :param ps1: the text to use in the PS1 environment variable (part of the prompt text)
    :type ps1: str
    :param width: the maximum width for the text in characters, default: 80
    :type width: int
    :param output: the file to store the generated output in, prints to stdout if None, default: None
    :type output: str
    """

    # configure template string
    if template is not None:
        _template = template
    elif template_file is not None:
        with open(template_file, "r") as tf:
            lines = tf.readlines()
            _template = "".join(lines)
    else:
        if subtitle is None:
            _template = DEFAULT_TEMPLATE
        else:
            _template = DEFAULT_TEMPLATE_SUBTITLE

    # generate banner
    if "\\n" in banner:
        banner_parts = banner.split("\\n")
    else:
        banner_parts = [banner]
    banner_parts_text = []
    for banner_part in banner_parts:
        banner_text = pyfiglet.figlet_format(banner_part, font=font, width=width)
        escaped = []
        for c in banner_text:
            if (c == "`") or (c == "\\"):
                escaped.append("\\")
            escaped.append(c)
        banner_text = "".join(escaped)
        banner_parts_text.append(banner_text)
    banner_text_all = "\n".join(banner_parts_text)

    # replace placeholders
    bashrc = _template\
        .replace(PH_BANNER, banner_text_all)\
        .replace(PH_PS1, ps1)
    if subtitle is not None:
        bashrc = bashrc.replace(PH_SUBTITLE, subtitle)

    # output content
    if output is None:
        print(bashrc)
    else:
        with open(output, "w") as of:
            of.write(bashrc)


def print_templates():
    """
    Outputs the default templates and supported placeholders to stdout.
    """

    print("\n--> No subtitle:\n")
    print(DEFAULT_TEMPLATE)
    print("\n--> With subtitle:\n")
    print(DEFAULT_TEMPLATE_SUBTITLE)
    print("\n--> Supported placeholders:")
    print(" - banner: " + PH_BANNER)
    print(" - subtitle: " + PH_SUBTITLE)
    print(" - PS1: " + PH_PS1)


def list_fonts():
    """
    Outputs the available fonts on stdout with a short description.
    """

    names = []
    for f in FigletFont.getFonts():
        names.append(f)
    names.sort()
    for name in names:
        print(name)
        desc = FigletFont.infoFont(name, short=True)
        if len(desc.strip()) == 0:
            desc = "-no description-"
        print("   ", desc)


def print_font_info(font, short=False):
    """
    Outputs information about the font on stdout.

    :param font: the name of the font to output the information for
    :type font: str
    :param short: whether to output short or long description
    :type short: bool
    """

    print(FigletFont.infoFont(font, short=short))


def main(args=None):
    """
    Performs the bash.bashrc generation.
    Use -h to see all options.

    :param args: the command-line arguments to use, uses sys.argv if None
    :type args: list
    """

    parser = argparse.ArgumentParser(
        description='Generates bash.bashrc templates for docker with a custom banner (ASCII art via pyfiglet).',
        prog="docker-banner-gen",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--template", dest="template", metavar="FILE", required=False, help="The banner template to use if not using the built-in one; use placeholders {BANNER} and {PS1} in the template.")
    parser.add_argument("-b", "--banner", dest="banner", metavar="TEXT", required=False, default="Banner", help="The text to use for the banner (processed by pyfiglet). Use the string '\\n' (not the newline character) to signal a line-break in the banner text.")
    parser.add_argument("-s", "--subtitle", dest="subtitle", metavar="TEXT", required=False, help="The subtitle text to use below the banner (regular text), e.g., a version number.")
    parser.add_argument("-f", "--font", dest="font", metavar="FONT", required=False, default="standard", help="The figlet font to use for generating the banner.")
    parser.add_argument("-p", "--ps1", dest="ps1", metavar="TEXT", required=False, default="docker", help="The text to use in the PS1 environment variable (used in the prompt).")
    parser.add_argument("-w", "--width", dest="width", metavar="COLS", required=False, default=80, type=int, help="The maximum width for the banner.")
    parser.add_argument("-o", "--output", dest="output", metavar="FILE", required=False, default=None, help="The file to store the generated bash.bashrc code in; prints to stdout if not provided.")
    parser.add_argument("-i", "--print_templates", action="store_true", required=False, help="Outputs the default templates to stdout.")
    parser.add_argument("-L", "--list_fonts", action="store_true", required=False, help="Outputs the available fonts.")
    parser.add_argument("-F", "--print_font_info", metavar="FONT", required=False, help="Outputs information about the specified font.")
    parsed = parser.parse_args(args=args)
    if parsed.print_templates:
        print_templates()
    elif parsed.list_fonts:
        list_fonts()
    elif parsed.print_font_info is not None:
        print_font_info(parsed.print_font_info, short=False)
    else:
        generate(banner=parsed.banner, subtitle=parsed.subtitle, template_file=parsed.template, font=parsed.font,
                 ps1=parsed.ps1, width=parsed.width, output=parsed.output)


def sys_main():
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    :rtype: int
    """

    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())
