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

Or download and install a Debian package, if you are running Debian/Ubuntu.

## Usage

```
usage: docker-banner-gen [-h] [-t FILE] [-b TEXT] [-s TEXT] [-f FONT]
                         [-p TEXT] [-w COLS] [-o FILE] [-i] [-L] [-F FONT]

Generates bash.bashrc templates for docker with a custom banner (ASCII art via
pyfiglet).

optional arguments:
  -h, --help            show this help message and exit
  -t FILE, --template FILE
                        The banner template to use if not using the built-in
                        one; use placeholders {BANNER} and {PS1} in the
                        template. (default: None)
  -b TEXT, --banner TEXT
                        The text to use for the banner (processed by
                        pyfiglet). Use the string '\n' (not the newline
                        character) to signal a line-break in the banner text.
                        (default: Banner)
  -s TEXT, --subtitle TEXT
                        The subtitle text to use below the banner (regular
                        text), e.g., a version number. (default: None)
  -f FONT, --font FONT  The figlet font to use for generating the banner.
                        (default: standard)
  -p TEXT, --ps1 TEXT   The text to use in the PS1 environment variable (used
                        in the prompt). (default: docker)
  -w COLS, --width COLS
                        The maximum width for the banner. (default: 80)
  -o FILE, --output FILE
                        The file to store the generated bash.bashrc code in;
                        prints to stdout if not provided. (default: None)
  -i, --print_templates
                        Outputs the default templates to stdout. (default:
                        False)
  -L, --list_fonts      Outputs the available fonts. (default: False)
  -F FONT, --print_font_info FONT
                        Outputs information about the specified font.
                        (default: None)
```

## Example

Using the following command-line:

```commandline
docker-banner-gen \
    -b "TF ObjDet" \
    -s 1.14.0_2019-08-31 \
    -p tf-objdet \
    -o $HOME/bash.bashrc
```

The generated `$HOME/bash.bashrc` file looks like this:


```bash
# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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

export PS1="\[\e[31m\]tf-objdet\[\e[m\] \[\e[33m\]\w\[\e[m\] > "
export TERM=xterm-256color
alias grep="grep --color=auto"
alias ls="ls --color=auto"

echo -e "\e[1;31m"
cat<<DBG
 _____ _____    ___  _     _ ____       _   
|_   _|  ___|  / _ \\| |__ (_)  _ \\  ___| |_ 
  | | | |_    | | | | '_ \\| | | | |/ _ \\ __|
  | | |  _|   | |_| | |_) | | |_| |  __/ |_ 
  |_| |_|      \\___/|_.__// |____/ \\___|\\__|
                        |__/                

1.14.0_2019-08-31

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
```

The following outputs get generated by this script:

* running as root

    ```
     _____ _____    ___  _     _ ____       _   
    |_   _|  ___|  / _ \| |__ (_)  _ \  ___| |_ 
      | | | |_    | | | | '_ \| | | | |/ _ \ __|
      | | |  _|   | |_| | |_) | | |_| |  __/ |_ 
      |_| |_|      \___/|_.__// |____/ \___|\__|
                            |__/                
    
    1.14.0_2019-08-31
    
    WARNING: You are running this container as root, which can cause new files in
    mounted volumes to be created as the root user on your host machine.
    
    To avoid this, run the container by specifying your user's userid:
    
    $ docker run -u \$(id -u):\$(id -g) args...
    
    tf-objdet / > 
    ```

* running as regular user

    ```
     _____ _____    ___  _     _ ____       _   
    |_   _|  ___|  / _ \| |__ (_)  _ \  ___| |_ 
      | | | |_    | | | | '_ \| | | | |/ _ \ __|
      | | |  _|   | |_| | |_) | | |_| |  __/ |_ 
      |_| |_|      \___/|_.__// |____/ \___|\__|
                            |__/                
    
    1.14.0_2019-08-31
    
    You are running this container as user with ID 12345 and group 12345,
    which should map to the ID and group for your user on the Docker host. Great!
    
    tf-objdet / >
    ```
