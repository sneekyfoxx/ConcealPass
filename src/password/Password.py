from curses import initscr, echo, noecho, cbreak, nocbreak, endwin


class Password(object):
    __slots__: tuple[str, ...] = ('prompt', 'mask', 'tty', '__ENTER')

    def __new__(cls: type['Password'], /, *, prompt: str = "Enter password: ", mask: bool = False) -> 'Password':
        assert isinstance(prompt, str), f"The '{prompt}' parameter must be a string"
        assert isinstance(mask, bool), f"The '{mask}' parameter must be a boolean"
        
        cls.__instance = None
        if cls.__instance is not None:
            return cls.__instance
        else:
            cls.__instance = super(Password, cls).__new__(cls)
            return cls.__instance

    def __init__(self: 'Password', /, *, prompt: str = "Enter password: ", mask: bool = False) -> None:
        self.prompt = prompt
        self.mask = mask
        self.tty = None
        self.__ENTER = '\n'

    def __str__(self: "Password", /) -> str:
        return f"Password(prompt={self.prompt}, mask={self.mask})"

    def __repr__(self: "Password", /) -> str:
        return self.__str__()

    def __dir__(self: 'Password', /) -> list[str]:
        attrs = list()
        attrs.append('__slots__')
        attrs.append('__new__')
        attrs.append('__init__')
        attrs.append('__str__')
        attrs.append('__dir__')
        attrs.append('__call__')
        attrs.append('prompt')
        attrs.append('mask')
        attrs.append('tty')
        attrs.append('plain')
        attrs.append('masked')
        attrs.sort()
        return attrs

    def plain(self: "Password", /) -> str | None:
        buffer = list()

        if self.mask is False:
            self.tty = initscr()
            noecho()
            cbreak()
            try:
                self.tty.addstr(self.prompt)
                while (char := self.tty.getch()) and char != self.__ENTER:
                    buffer.append(chr(char))
                    self.tty.addch(chr(char))
                else:
                    nocbreak()
                    echo()
                    endwin()
                    return "".join(buffer)
            except KeyboardInterrupt:
                nocbreak()
                echo()
                endwin()
                return None
        else:
            raise ValueError("The 'mask' parameter must be 'False'")

    def masked(self: "Password", /) -> str | None:
        buffer = list()

        if self.mask is True:
            self.tty = initscr()
            noecho()
            cbreak()
            try:
                self.tty.addstr(self.prompt)
                while (char := self.tty.getch()) and chr(char) != self.__ENTER:
                    buffer.append(chr(char))
                    self.tty.addch('*')
                else:
                    nocbreak()
                    echo()
                    endwin()
                    return "".join(buffer)
            except KeyboardInterrupt:
                nocbreak()
                echo()
                endwin()
                return None
        else:
            raise ValueError("The 'mask' parameter must be 'True'")

    def __call__(self: "Password", /) -> str | None:
        if self.mask is False:
            return self.plain()
        else:
            return self.masked()
