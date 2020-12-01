import sys
import os
import re
from cmd import Cmd
from PIL import Image
from abc import ABCMeta, abstractmethod


class GilliamPrompt(Cmd):
    doc_header = "Here are the list of commands in help.\n To get help on a " \
                 "command, enter 'help' followed by command name'."

    def __init__(self, diagram_painter, view_image, prep_file, analyze_file,file_content):
        Cmd.__init__(self)
        #self.js_file_content = ""
        self.arg = ""
        self.diagram = diagram_painter
        self.view = view_image
        self.prep = prep_file
        self.js_file = file_content
        self.analyze = analyze_file


    def do_help_list(self, arg):
        """Enter 'help_list to see a list of all the commands in help """
        """and what they do."""
        print("analyzer\t\tEnter 'analyzer' to analysis the selected file.\n"
              "\ndraw\t\tEnter 'draw' to draw the selected file.\n"
              "\nhelp_list\t\tEnter 'help_list to see a list of all the "
              "commands in help and what they do.\n"
              "\nselect_file\t\tEnter 'select_file' to enter the file "
              "path of the JavaScript file that requires a UML diagram.\n"
              "\ndisplay\t\tEnter 'display' to view the drawing.\n"
              "\nshut\t\tEnter 'shut y' To leave the program.")

        def get_do_help_list(self):
            result = self.do_help_list(self)
            return self.do_help_list(self)
            print(result)

    def do_select_file(self, arg):
        """Enter 'select_file' to enter the file path of the JavaScript"""
        """file that requires a UML diagram """
        print('Enter the file path and file name of the file that ' +
              'requires analyzing')
        # call file opener
        self.prep.select_file(arg)
        self.prep.open_file(arg)

    def do_analyse(self, js_file):
        """Enter 'analyzer' to analysis the selected file."""
        self.analyze.find_class(js_file)
        self.analyze.find_property(js_file)
        self.analyze.find_function_1(js_file)

    def do_draw(self, arg):
        """Enter 'draw' to draw the selected file."""
        self.diagram.draw(self)

    def do_display(self, arg):
        """Enter 'display' to view the drawing."""
        self.view.display(self)

    """def do_pickle(self, arg):
        Enter 'pickle' to save as a pickle file.
       # pickler = Pickles(self.js_file_content)
       # pickler.create_pickle()"""

    """def do_open_pickle(self, arg):
        Enter 'open_pickle' to open the pickle file
        #pickler = Pickles(self.js_file_content)
        #pickler.open_pickle()"""

    def do_shut(self, args):
        """ Enter 'shut y' To leave the program."""
        if args == "y":
            sys.exit()
        else:
            print("Welcome back. Enter a command!")


class AbstractPreparer(metaclass=ABCMeta):
    @abstractmethod
    def select_file(self, arg):
        pass

    @abstractmethod
    def open_file(self, file_name):
        pass


class Preparer(AbstractPreparer):
    def select_file(self, arg):
        if (arg.endswith(".js")):
            file_name = arg
            print('You selected ', file_name, "\n")
            self.open_file(file_name)
        else:
            print("The file is not a JavaScript file")

    def open_file(self, file_name):
        if file_name != '':
            try:
                file = open(file_name)
            except FileNotFoundError:
                print("The file does not exist at that location\n"
                      "Please check your file and try again")
            else:
                self.js_file_content = file.read()
                print("\n Hi", file_name, "\n")
                print(self.js_file_content)


class AbstractAnalyzer(metaclass=ABCMeta):
    @abstractmethod
    def find_class(self, js_file):
        pass

    @abstractmethod
    def find_property(self, js_file):
        pass

    @abstractmethod
    def find_function_1(self, js_file):
        pass


class Analyzer(AbstractAnalyzer):

    def find_class(self, js_file):
        try:
            self.class_name = re.search(r'class.(\w+)', self.js_file)
            if self.js_file == '':
                raise Exception
        except Exception as e:
            print('A JS file needs to be selected to run the analyzer')
        else:
            if self.class_name is not None:
                self.class_name = self.class_name.group().split()[-1]
                print(self.class_name, 'a')

    def get_class_name(self):
        return self.class_name

    def find_property(self, js_file):
        try:
            self.property_name = re.findall(r'this.(\w+)', self.js_file)
            if self.js_file == '':
                raise Exception
        except Exception as e:
            print('A JS file needs to be selected to run the analyzer')
        else:
            if self.property_name is not None:
                first_list = self.property_name
                print(first_list)
                first_list = [i.lower() for i in first_list]
                self.property_name = list(dict.fromkeys(first_list))
                self.property_name = (['{}\l'.format(i)
                                       for i in self.property_name])
                self.property_name = " ".join(self.property_name)
                print(self.property_name, 'a')

    def get_property_name(self):
        return self.property_name

    def find_function_1(self, js_file):
        try:
            self.function_name = re.findall(r'function.(\w+)', self.js_file)
            if self.js_file == '':
                raise Exception
        except Exception as e:
            print('A JS file needs to be selected to run the analyzer')
        else:
            if self.function_name is not None:
                self.function_name = self.function_name
                self.function_name = (['{}()\l'.format(i) for i in
                                       self.function_name])
                self.function_name = " ".join((self.function_name))
                print(self.function_name)

    def get_function_name(self):
        return self.function_name

    def get_no_file(self, js_file):
        if self.js_file == '':
            return 'A JS file needs to be selected to run the analyzer'




class AbstractDrawer(metaclass=ABCMeta):
    @abstractmethod
    def draw(self, arg):
        pass


class Drawer(AbstractDrawer):
    def draw(self, arg):
        os.system("Graphviz\\bin\\dot.exe  -Tpng -O classfile.dot")
        print("Drawing UML diagram")


class AbstractDisplay(metaclass=ABCMeta):
    @abstractmethod
    def display(self, arg):
        pass


class Display(AbstractDisplay):
    def display(self, arg):
        view = Image.open('classfile.dot.png')
        view.show()


if __name__ == '__main__':
    prompt = GilliamPrompt(Drawer(), Display(), Preparer(), Analyzer(), file_content)
    prompt.prompt = '>->-> '
    prompt.cmdloop('\nWelcome to Gilliam the JS class diagram drawer.\
                        \nType help or ? for a list of commands')
    uml_image = GilliamPrompt(Drawer())
    uml_image.do_draw()
    show_image = GilliamPrompt(Display())
    show_image.do_display()
    file_preper = GilliamPrompt(Preparer())
    file_preper.do_select_file()
    class_analyser = GilliamPrompt(Analyzer())
    class_analyser.do_analyse()
