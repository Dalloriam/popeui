![Engel](http://i.imgur.com/pc32vxY.jpg)

[![PyPI](https://img.shields.io/pypi/v/engel.svg)](https://pypi.python.org/pypi/engel) [![PyPI](https://img.shields.io/pypi/l/engel.svg)](https://pypi.python.org/pypi/engel) [![PyPI](https://img.shields.io/pypi/dm/engel.svg)](https://pypi.python.org/pypi/engel) [![Code Climate](https://codeclimate.com/github/Dalloriam/engel/badges/gpa.svg)](https://codeclimate.com/github/Dalloriam/engel)

Engel is an opinionated framework that allows you to painlessly build cross-platform web interfaces for your projects.

Take a look at the [documentation](http://engel.readthedocs.io/en/latest/index.html) for more details.



## Installation

### Via `pip`

```shell
$ pip install engel
```

### Manually

```shell
$ git clone https://github.com/Dalloriam/engel
$ cd engel
$ python setup.py install
```



## Running the tests

```shell
$ python setup.py test
```



## Building a basic web interface with Engel

In this example, we will build a web front-end to a text file. Exciting, right?

**Specifications**

* Write lines to a text file.
* Display all lines of a text file.

```python
from engel.application import Application, View

from engel.widgets.structure import List
from engel.widgets.forms import Button, TextBox
from engel.widgets.text import Title, Span

from engel.libraries import bootstrap4

from engel.resource import R


class FileService(object):
    """Services are the main way of interacting with the outside world with Engel.
    This service encapsulates all interactions with our file, and will be made
    available to our application.
    """

    def __init__(self):
        self.f = R('myfile.txt')
        self.f.open('a').close()

    def get_all(self):
        with self.f.open('rU') as infile:
            return list(filter(bool, infile.readlines()))

    def add(self, txt):
        with self.f.open('a') as outfile:
            outfile.write(txt + "\n")


class MainFileView(View):
    """With Engel, views represent the structure of the page currently displayed
    as well as the different actions handled by the program.
    """
    title = "MyFile.txt"

    current_id = 0

    libraries = [bootstrap4]

    def build(self):
        """The build() method is called when the application is rendering the page to
        HTML. It is responsible for building the DOM and enqueuing the event handlers required by the view.
        """

        # We create a bootstrap Container() object and anchor it to the root of the page.
        main_panel = bootstrap4.Container(id="containerMain", parent=self.root)
        Title(id="pageTitle", text="Contents of myfile.txt", parent=main_panel)

        # Here, we define a List() object. Contrary to Container(), List() is more than
        # a simple wrapper around <ul>. The List object provides an interface very similar to python's list,
        # and at the same time provides the auto-updating capabilities of Engel widgets.
        self.lines_list = List(id="lstLines", parent=main_panel)

        # We get the list of active services from the view's context & call the
        # method allowing us to retrieve all lines in the file.
        for ln in self.context.services["FileService"].get_all():
            self.append_line(ln)

        self.txtNew = TextBox(id="txtNew", name="txtNew", parent=main_panel)
        btn = Button(id="btnSubmit", text="Add Line", parent=main_panel)

        # Note: The framework handles seamlessly the forwarding of events from the
        # client to the server, so we can set a server-side method as callback
        # for a client event.
        self.on(event="click", callback=self.create_line, selector="#" + btn.id)

    def append_line(self, ln):
        self.lines_list.add_child(Span(id="line_" + str(self.current_id), text=ln))
        self.current_id += 1

    def create_line(self, event, interface):
        new_line = self.txtNew.text
        self.context.services["FileService"].add(new_line)
        self.append_line(new_line)

        # Note: The framework also handles the updating of client widgets from the server. This means
        # that the HTML view is guaranteed to always be in sync with your python objects.
        self.txtNew.text = ""


class FileApp(Application):
    """The Application object is the central object tying your Engel app together.
    It holds all the information common to all views, as well as view and service
    definitions.
    """

    # The base title of the app.
    # The actual title of the page is set by App.base_title.format(view.title)
    base_title = "{0} | TextFileManager"

    def __init__(self, debug=False):
        super(FileApp, self).__init__(debug)

        self.views["default"] = MainFileView

        # Services are instanciated on app startup and are kept running for the
        # entire lifetime of the app.
        self.services["FileService"] = FileService


if __name__ == "__main__":
    app = FileApp(debug=True)
    app.start()

```

**Getting it running**

To start the app, simply run

```shell
$ python [appfilename].py
```

![App running](http://i.imgur.com/9U9sYEZ.png)

Not so pretty, but it works great!



## Requirements

* Python 3.5.1 (Not tested yet on earlier versions, should work with 3.x)
