import argparse
import pyfiglet
import traceback

PH_PS1 = "{PS1}"
""" The placeholder for the PS1 prefix. """

PH_BANNER = "{BANNER}"
""" The placeholder for the pyfiglet banner. """

DEFAULT_TEMPLATE = \
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
{BANNER}
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


def generate(banner, font="standard", template=None, template_file=None, ps1="docker", output=None):
    """
    Generates the bash.bashrc file.

    :param banner: the banner text to push through pyfiglet
    :type banner: str
    :param font: the figlet font to use, default: standard
    :type font: str
    :param template: the template string to use if not using the built-in one, default: None
    :type template: str
    :param template_file: the template file to use if not using the built-in one, default: None
    :type template_file: str
    :param ps1: the text to use in the PS1 environment variable (part of the prompt text)
    :type ps1: str
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
        _template = DEFAULT_TEMPLATE

    # generate banner
    banner_text = pyfiglet.figlet_format(banner, font=font)

    # replace placeholders
    bashrc = _template\
        .replace(PH_BANNER, banner_text)\
        .replace(PH_PS1, ps1)

    # output content
    if output is None:
        print(bashrc)
    else:
        with open(output, "w") as of:
            of.write(bashrc)


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
    parser.add_argument("-t", "--template", dest="template", metavar="FILE", required=False, help="the banner template to use if not using the built-in one; use placeholders {BANNER} and {PS1} in the template")
    parser.add_argument("-b", "--banner", dest="banner", metavar="TEXT", required=True, help="the text to use for the banner (processed by pyfiglet)")
    parser.add_argument("-f", "--font", dest="font", metavar="FONT", required=False, default="standard", help="the figlet font to use for generating the banner")
    parser.add_argument("-p", "--ps1", dest="ps1", metavar="TEXT", required=False, default="docker", help="the text to use in the PS1 environment variable (used in the prompt)")
    parser.add_argument("-o", "--output", dest="output", metavar="FILE", required=False, default=None, help="the file to store the generated bash.bashrc code in; prints to stdout if not provided")
    parsed = parser.parse_args(args=args)
    generate(banner=parsed.banner, template_file=parsed.template, font=parsed.font, ps1=parsed.ps1, output=parsed.output)


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
