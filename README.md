#Makitso

Utilities around server provisioning and install/config built upon the [Fabric](http://fabfile.org) [Python](http://python.org) framework.

The `makitso.sh` shell script wrapper is the entry point to this library. It is designed to be symlinked into the parent directory of the makitso submodule. You can call the symlink whatever you want. I like calling it "do", but use whatever name you like. So all commands take the form:

    ./do <command>...

Note that `do` should be invoked as "./do" or your shell will think you mean the "do" shell keyword used in "for"/"while" loops. The `do` script will ensure the prerequisites are installed, which involves:

* A python virtualenv in `./python`

#Dependencies

* a modern bourne-ish shell. Bash 4 or zsh 4 or newer should work fine
* [Python](http://python.org) 2.6 or newer
* A python development environment (needed to compile native C portions for some of the Fabric packages), such as the python-dev Ubuntu/Debian package
* [virtualenv](http://pypi.python.org/pypi/virtualenv/) 1.7 or newer
    * makitso will automatically download virtualenv.py as needed
* [Fabric](http://fabfile.org) 1.4 or newer
    * maktiso will automatically install `fabric` via `pip`

#How to use makitso in your project

* Install makitso as a git submodule

    git submodule add git@github.com:focusaurus/makitso.git

* Symlink the `do` script (again you can name it whatever you like)

    ln -s makitso/makitso.sh ./do

* Define your `fabfile.py` in the root of your project
* Make use of the `makitso` package and the helper modules therein

#License

```
The MIT License (MIT)
Copyright (c) 2012 Peter Lyons LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
