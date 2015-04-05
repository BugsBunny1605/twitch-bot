class Msg(object):
    def __init__(self):
        self.ui = None
        self.bot = None

    def set_ui(self, ui):
        self.ui = ui

    def set_bot(self, bot):
        self.bot = bot

    def process(self):
        raise NotImplementedError()


class StopMsg(Msg):
    def process(self):
        self.ui.stop()


class ConsoleMsg(Msg):
    def __init__(self, channel, message):
        self.channel = channel
        self.message = message

        super(ConsoleMsg, self).__init__()

    def process(self):
        self.ui.append_to_console(self.channel, self.message)


class SayMsg(Msg):
    def __init__(self, channel, message):
        self.channel = channel
        self.message = message

        super(SayMsg, self).__init__()

    def process(self):
        self.bot.wrapper._message(self.channel, self.message)


class AddRegularToListMsg(Msg):
    def __init__(self, name):
        self.name = name
        super(AddRegularToListMsg, self).__init__()

    def process(self):
        self.ui.add_regular_to_list(self.name)


class RemoveRegularFromListMsg(Msg):
    def __init__(self, name):
        self.name = name
        super(RemoveRegularFromListMsg, self).__init__()

    def process(self):
        self.ui.remove_regular_from_list(self.name)


class RequestRegularsMsg(Msg):
    def __init__(self, channel):
        self.channel = channel

        super(RequestRegularsMsg, self).__init__()

    def process(self):
        self.bot.send_regulars_to_ui(self.channel)


class AddRegularMsg(Msg):
    def __init__(self, channel, nick):
        self.channel = channel
        self.nick = nick

        super(AddRegularMsg, self).__init__()

    def process(self):
        self.bot.wrapper._add_regular(self.channel, self.nick)


class RemoveRegularMsg(Msg):
    def __init__(self, channel, nick):
        self.channel = channel
        self.nick = nick

        super(RemoveRegularMsg, self).__init__()

    def process(self):
        self.bot.wrapper._remove_regular(self.channel, self.nick)


class SetChannelsMsg(Msg):
    def __init__(self, channels):
        self.channels = channels

        super(SetChannelsMsg, self).__init__()

    def process(self):
        self.ui.set_channels(self.channels)

