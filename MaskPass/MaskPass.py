"""A module for user password input."""

from curses import initscr, echo, noecho, cbreak, nocbreak, endwin


class MaskPass(object):
    """Conatin methods for revealed and masked user password input."""
    __slots__: tuple[str, ...] = ('prompt', 'mask', 'tty', '__ENTER')

    def __new__(cls: type['MaskPass'], /, *, prompt: str = "Enter password: ", mask: bool = False) -> 'MaskPass':
        """Create a new 'MaskPass' object."""
        assert isinstance(prompt, str), f"The '{prompt}' parameter must be a string"
        assert isinstance(mask, bool), f"The '{mask}' parameter must be a boolean"
        
        cls.__instance = None
        if cls.__instance is not None:
            return cls.__instance
        else:
            cls.__instance = super(MaskPass, cls).__new__(cls)
            return cls.__instance

    def __init__(self: 'MaskPass', /, *, prompt: str = "Enter password: ", mask: bool = False) -> None:
        """Initialize 'MaskPass' instance variables."""
        self.prompt = prompt
        self.mask = mask
        self.tty = None
        self.__ENTER = '\n'

    def __str__(self: "MaskPass", /) -> str:
        """Return a string version of the 'MaskPass' object."""
        return f"MaskPass(prompt={self.prompt}, mask={self.mask})"

    def __repr__(self: "MaskPass", /) -> str:
        """Return a representation of the 'MaskPass' object string."""
        return self.__str__()

    def __dir__(self: 'MaskPass', /) -> list[str]:
        """List the 'MaskPass' instance attributes."""
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

    def revealed(self: "MaskPass", /) -> str | None:
        """Display the password in plain text."""
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

    def concealed(self: "MaskPass", /) -> str | None:
        """Display the password in asterisk form."""
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

    def __call__(self: "MaskPass", /) -> str | None:
        """A convienence method for simpler use."""
        if self.mask is False:
            return self.revealed()
        else:
            return self.concealed()
