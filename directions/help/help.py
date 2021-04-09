from command_enum import Command
from mode_enum import Mode

class Help:
    @staticmethod
    def get_help(self, msg) -> list:

        response = ""

        if msg in Command.help_modes.value:
            response = "Все имеющиеся режимы:\n"
            for mode in Mode:
                response += mode.value[0] + ": /" + mode.value[1] + "\n"
            return response

        if msg in Command.help_commands.value:
            response = "Все имеющиеся команды:\n"
            for cmd_num, cmd in enumerate(Command):
                response += str(cmd_num) + ") " + cmd.value[0]
                for i, value in enumerate(cmd.value, 1):
                    try:
                        response += " | " + cmd.value[i]
                    except:
                        break
                response += "\n"
            return response

        if msg in Command.main_menu.value:
            return self.change_mode(Mode.default)

        if msg not in Command:
            response = "Команда не распознана"
            return response

