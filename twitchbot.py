from __future__ import absolute_import

import argparse
import multiprocessing
import time
import os

from threading import Thread
from bot.bot import Bot
from bot.ircwrapper import IRCWrapper
from bot.utils import log, set_log_file, is_frozen
from bot.utils import ThreadCallRelay
from bot.ui import get_ui_choices, get_ui
from bot.messages import StopMsg

import settings


def start_ui(ui):
    """

    :param bot.ui.UI ui:
    :return:
    """
    ui.run()


def main():
    multiprocessing.freeze_support()
    ui_choices = get_ui_choices()

    default_ui = "Qt" if is_frozen() else "None"

    ap = argparse.ArgumentParser()
    ap.add_argument("--ui", default=default_ui, choices=ui_choices)

    options = ap.parse_args()

    ui, in_queue, out_queue = get_ui(options.ui)

    if not ui:
        raise RuntimeError("Couldn't instantiate UI {}".format(ui))

    process = multiprocessing.Process(
        target=start_ui, args=(ui,)
    )

    if options.ui != "None":
        process.start()

    if settings.LOG_FILE:
        set_log_file(settings.LOG_FILE)

    # Set LUA_PATH environment variable so our Lua code can find the libraries
    os.environ["LUA_PATH"] = settings.LUA_PATH

    ui_queues = {
        "in": in_queue,
        "out": out_queue
    }

    wrapper = ThreadCallRelay()
    bot = Bot(settings, ui_queues=ui_queues, wrapper=wrapper, irc_wrapper=IRCWrapper, logger=log)
    wrapper.set_call_object(bot)

    def run():
        bot.run()

    thread = Thread(target=run)
    thread.daemon = True
    thread.start()

    try:
        if options.ui == "None":
            while True:
                time.sleep(1)
        else:
            running = True
            while running:
                msg = out_queue.get()
                if msg.__class__ == StopMsg:
                    running = False
                    wrapper.stop()
                else:
                    msg.set_bot(bot)
                    msg.process()
    finally:
        in_queue.put(StopMsg())
        wrapper.stop()

        if options.ui != "None":
            process.join()



if __name__ == "__main__":
    main()