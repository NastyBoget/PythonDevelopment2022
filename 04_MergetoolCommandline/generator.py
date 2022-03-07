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
        self.languages = []

        for module_name, module_data in inspect.getmembers(pynames.generators, inspect.ismodule):
            for class_name, class_data in inspect.getmembers(module_data, inspect.isclass):
                if class_name.endswith("Generator"):
                    try:
                        self.classes[module_name.lower()][self.__strip_name(class_name.lower())] = class_data()
                        self.languages.extend(list(class_data().languages))
                    except (NotImplementedError, TypeError):
                        pass
        self.languages = list(set(self.languages))

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

    def complete_generate(self, prefix, line, beg_idx, end_idx):
        prefix = prefix.lower().strip()
        words = line.lower().split()
        if len(words) == 4 or (len(words) == 3 and line.endswith(" ")):
            return [completion for completion in list(self.genders) if completion.startswith(prefix)]
        if len(words) == 3 or (len(words) == 2 and line.endswith(" ")):
            completion_list = list(self.classes[words[1]]) + list(self.genders) if words[1] in self.classes else list(self.genders)
            return [completion for completion in completion_list if completion.startswith(prefix)]
        if len(words) == 2 or (len(words) == 1 and line.endswith(" ")):
            return [completion for completion in self.classes if completion.startswith(prefix)]
        return []

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
            else:
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

    def complete_info(self, prefix, line, beg_idx, end_idx):
        prefix = prefix.lower().strip()
        words = line.lower().split()
        if len(words) == 4 or (len(words) == 3 and line.endswith(" ")):
            return [completion for completion in list(self.genders) + ['language'] if completion.startswith(prefix)]
        if len(words) == 3 or (len(words) == 2 and line.endswith(" ")):
            completion_list = list(self.classes[words[1]]) + list(self.genders) + ['language'] \
                if words[1] in self.classes else list(self.genders) + ['language']
            return [completion for completion in completion_list if completion.startswith(prefix)]
        if len(words) == 2 or (len(words) == 1 and line.endswith(" ")):
            return [completion for completion in self.classes if completion.startswith(prefix)]
        return []

    def do_language(self, arg):
        """
        Set the language: language RU
        Default language is native
        If the language not supported, native is used
        """
        args = arg.lower().strip().split(" ")
        if len(args) != 1 or args[0] not in self.languages:
            print(f"Invalid arguments, {' '.join(self.languages)} are available")
        else:
            self.language = args[0]

    def complete_language(self, prefix, line, beg_idx, end_idx):
        return [completion for completion in self.languages if completion.startswith(prefix.lower().strip())]

    def __strip_name(self, class_name):
        if class_name.endswith('namesgenerator'):
            return class_name[:-len('namesgenerator')]
        if class_name.endswith('fullnamegenerator'):
            return class_name[:-len('fullnamegenerator')]
        if class_name.endswith('generator'):
            return class_name[:-len('generator')]

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
        if subclass_name in self.classes[class_name]:
            return self.classes[class_name][subclass_name]


if __name__ == "__main__":
    NameGenerator().cmdloop()
