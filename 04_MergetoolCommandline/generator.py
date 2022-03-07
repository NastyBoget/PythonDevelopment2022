import cmd
import inspect
from collections import defaultdict
import random

import pynames


class NameGenerator(cmd.Cmd):
    intro = 'Welcome to the generator shell. Type help or ? to list commands.\n'
    prompt = '(generator) '

    def __init__(self):
        super().__init__()
        self.language = "native"
        self.genders = {
            "male": pynames.GENDER.MALE,
            "female": pynames.GENDER.FEMALE
        }
        self.classes = defaultdict(dict)

        for module_name, module_data in inspect.getmembers(pynames.generators, inspect.ismodule):
            for class_name, class_data in inspect.getmembers(module_data, inspect.isclass):
                if class_name.endswith("Generator"):
                    try:
                        self.classes[module_name.lower()][class_name.lower()] = class_data()
                    except (NotImplementedError, TypeError):
                        pass

    def do_generate(self, arg):
        """
        Generate the name of class: generate class gender
        Generate the name of subclass: generate class subclass gender
        Default gender is male
        """
        args = arg.lower().strip().split(" ")
        generator = self.__get_generator(args)
        if generator is None:
            print("Invalid arguments")
            return
        gender = self.genders[args[-1]] if args[-1] in self.genders else self.genders["male"]
        try:
            print(generator.get_name_simple(gender, self.language))
        except KeyError:
            print(generator.get_name_simple(gender, "native"))

    def do_info(self, arg):
        """
        Get the number of names or the list of languages
        Number of names: info class gender
        If gender isn't set, both male and female are counted
        List of languages: info class language
        """
        args = arg.lower().strip().split(" ")
        if len(args) == 0:
            return
        if args[-1] == "language":
            args = args[:-1]
            generator = self.__get_generator(args)
            if generator is not None:
                print(" ".join(generator.languages))
            print("Invalid arguments")
        else:
            generator = self.__get_generator(args)
            if generator is not None:
                if args[-1] in self.genders:
                    print(generator.get_names_number(self.genders[args[-1]]))
                else:
                    print(generator.get_names_number())
            else:
                print("Invalid arguments")

    def do_language(self, arg):
        """
        Set the language: language RU
        Default language is native
        If the language not supported, native is used
        """
        args = arg.lower().strip().split(" ")
        if len(args) != 1:
            print("Invalid arguments")
        self.language = args[0]

    def __get_generator(self, args):
        cls = None
        if len(args) == 1:
            cls = self.__get_class(*args)
        elif len(args) == 2:
            if args[-1] in self.genders:
                cls = self.__get_class(args[0])
            else:
                cls = self.__get_subclass(*args)
        elif len(args) == 3:
            if args[-1] in self.genders:
                cls = self.__get_subclass(args[0], args[1])
        return cls

    def __get_class(self, class_name):
        if class_name not in self.classes:
            return
        return random.choice(list(self.classes[class_name].items()))[1]

    def __get_subclass(self, class_name, subclass_name):
        if class_name not in self.classes:
            return
        for cls_name in self.classes[class_name]:
            if cls_name.startswith(subclass_name):
                return self.classes[class_name][cls_name]


if __name__ == "__main__":
    NameGenerator().cmdloop()
