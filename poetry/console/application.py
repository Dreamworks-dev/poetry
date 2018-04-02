import os

from cleo import Application as BaseApplication
from cleo.inputs import ArgvInput
from cleo.outputs import ConsoleOutput

from poetry import __version__

from poetry.io.raw_argv_input import RawArgvInput

from .commands import AboutCommand
from .commands import AddCommand
from .commands import BuildCommand
from .commands import CheckCommand
from .commands import ConfigCommand
from .commands import InstallCommand
from .commands import LockCommand
from .commands import NewCommand
from .commands import PublishCommand
from .commands import RemoveCommand
from .commands import RunCommand
from .commands import ShowCommand
from .commands import UpdateCommand
from .commands import VersionCommand

from .commands.debug import DebugInfoCommand
from .commands.debug import DebugResolveCommand


class Application(BaseApplication):

    def __init__(self):
        super().__init__('Poetry', __version__)

        self._poetry = None
        self._skip_io_configuration = False

    @property
    def poetry(self):
        from poetry.poetry import Poetry

        if self._poetry is not None:
            return self._poetry

        self._poetry = Poetry.create(os.getcwd())

        return self._poetry

    def reset_poetry(self) -> None:
        self._poetry = None

    def run(self, i=None, o=None) -> int:
        if i is None:
            i = ArgvInput()

        if o is None:
            o = ConsoleOutput()

        name = i.get_first_argument()
        if name == 'run':
            self._skip_io_configuration = True
            i = RawArgvInput()

        return super().run(i, o)

    def do_run(self, i, o):
        name = self.get_command_name(i)

        if name != 'run':
            return super().do_run(i, o)

        command = self.find(name)

        self._running_command = command
        status_code = command.run(i, o)
        self._running_command = None

        return status_code

    def configure_io(self, i, o):
        if self._skip_io_configuration:
            return

        super().configure_io(i, o)

    def get_default_commands(self) -> list:
        commands = super(Application, self).get_default_commands()

        commands += [
            AboutCommand(),
            AddCommand(),
            BuildCommand(),
            CheckCommand(),
            ConfigCommand(),
            InstallCommand(),
            LockCommand(),
            NewCommand(),
            PublishCommand(),
            RemoveCommand(),
            RunCommand(),
            ShowCommand(),
            UpdateCommand(),
            VersionCommand(),
        ]

        # Debug commands
        commands += [
            DebugInfoCommand(),
            DebugResolveCommand(),
        ]

        return commands
