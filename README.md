# docker-banner-gen
The **docker-banner-gen** command-line tool allows you to generate
`bash.bashrc` files to be used within Docker containers. 
It is based on TensorFlow's `bash.bashrc` and uses pyfiglet to
generate the banner.

## Installation

You can install the tool with `pip` as follows (best to install it in a [virtual
environment](https://virtualenv.pypa.io/en/latest/)):

```commandline
pip install docker-banner-gen
```

## Usage

```
usage: docker-banner-gen [-h] [-t FILE] [-b TEXT] [-s TEXT] [-f FONT]
                         [-p TEXT] [-o FILE] [-i]

Generates bash.bashrc templates for docker with a custom banner (ASCII art via
pyfiglet).

optional arguments:
  -h, --help            show this help message and exit
  -t FILE, --template FILE
                        the banner template to use if not using the built-in
                        one; use placeholders {BANNER} and {PS1} in the
                        template (default: None)
  -b TEXT, --banner TEXT
                        the text to use for the banner (processed by pyfiglet)
                        (default: Banner)
  -s TEXT, --subtitle TEXT
                        the subtitle text to use below the banner (regular
                        text), e.g., a version number (default: None)
  -f FONT, --font FONT  the figlet font to use for generating the banner
                        (default: standard)
  -p TEXT, --ps1 TEXT   the text to use in the PS1 environment variable (used
                        in the prompt) (default: docker)
  -o FILE, --output FILE
                        the file to store the generated bash.bashrc code in;
                        prints to stdout if not provided (default: None)
  -i, --print_templates
                        outputs the default templates to stdout (default:
                        False)
```
