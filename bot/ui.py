from __future__ import absolute_import

import multiprocessing
import sys
import pathlib
from bot.messages import StopMsg, SayMsg, RequestRegularsMsg, AddRegularMsg, RemoveRegularMsg

from PySide import QtGui, QtCore, QtUiTools
try:
    from PySide import QtGui, QtCore, QtUiTools

    HAVE_QT = True
except ImportError:
    HAVE_QT = False

    # Make the code below parse well enough
    class QtCore(object):
        @staticmethod
        def Slot():
            def wrap(f):
                return f
            return wrap

        class QThread(object):
            pass

    class QtGui(object):

        class QMainWindow(object):
            pass


class UI(object):
    def __init__(self, in_queue, out_queue):
        """
        :param multiprocessing.Queue in_queue:
        :param multiprocessing.Queue out_queue:
        """
        self._in_queue = in_queue
        self._out_queue = out_queue
        self._running = True

    def append_to_console(self, channel, message):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def set_channels(self, channels):
        pass

    def add_regular_to_list(self, channel, nick):
        pass

    def remove_regular_from_list(self, channel, nick):
        pass

    def run(self):
        while self._running:
            msg = self._in_queue.get()
            msg.set_ui(self)
            msg.process()


class NoneUI(UI):
    NAME = "None"

    def __init__(self, in_queue, out_queue):
        super(NoneUI, self).__init__(in_queue, out_queue)

    def stop(self):
        self._running = False

    def append_to_console(self, channel, message):
        sys.stdout.write("{0}: {1}".format(channel, message))


class QtMessageQueue(QtCore.QThread):
    def __init__(self, ui, in_queue):
        self._ui = ui
        self._in_queue = in_queue

        super(QtMessageQueue, self).__init__()

    def run(self):
        while self._ui._running:
            msg = self._in_queue.get()
            msg.set_ui(self._ui)
            msg.process()


class MainWindow(QtGui.QMainWindow):
    def __init__(self, ui):
        super(MainWindow, self).__init__()

        self.ui = ui
        self._load_ui()

    def _get_ui_path(self):
        path = pathlib.Path('.')
        return path / 'ui'

    def _get_main_ui_path(self):
        return self._get_ui_path() / 'main.ui'

    def _load_ui(self):
        QtGui.QIcon.setThemeSearchPaths(str(self._get_ui_path()))
        loader = QtUiTools.QUiLoader(self)
        ui_file = QtCore.QFile(str(self._get_main_ui_path()))
        ui_file.open(QtCore.QFile.ReadOnly)
        window = loader.load(ui_file)
        ui_file.close()

        self.setCentralWidget(window)

        QtCore.QMetaObject.connectSlotsByName(self)

    def closeEvent(self, event):
        self.ui.quit()
        event.accept()

    def activate_selected_tab(self):
        tab_widget = self.findChild(QtGui.QTabWidget, "tabWidget")
        current_tab = tab_widget.currentWidget()
        active_tab = current_tab.objectName()

        def _null():
            pass

        getattr(self, "on_" + active_tab + "_activate", _null)()

    def on_regularsTab_activate(self):
        regulars_list = self.findChild(QtGui.QListView, "regularsList")
        regulars_list.model().clear()
        self.ui.send_message(RequestRegularsMsg(self.ui.channel))

    @QtCore.Slot()
    def on_tabWidget_currentChanged(self):
        self.activate_selected_tab()

    @QtCore.Slot()
    def on_actionQuit_triggered(self):
        self.ui.quit()

    @QtCore.Slot()
    def on_actionAbout_triggered(self):
        sys.stdout.write("About the bot")

    @QtCore.Slot()
    def on_removeRegulars_pressed(self):
        regulars_list = self.findChild(QtGui.QListView, "regularsList")
        indexes = regulars_list.selectedIndexes()

        for index in indexes:
            nick = index.data()
            self.ui.send_message(RemoveRegularMsg(self.ui.channel, nick))

    @QtCore.Slot()
    def on_addRegularLineEdit_returnPressed(self):
        line_edit = self.findChild(QtGui.QLineEdit, "addRegularLineEdit")
        msg = AddRegularMsg(self.ui.channel, line_edit.text())
        line_edit.setText("")
        self.ui.send_message(msg)

    @QtCore.Slot()
    def on_saySomething_returnPressed(self):
        line_edit = self.findChild(QtGui.QLineEdit, "saySomething")
        msg = SayMsg(self.ui.channel, line_edit.text())
        line_edit.setText("")
        self.ui.send_message(msg)

    @QtCore.Slot()
    def on_channelSelection_currentIndexChanged(self):
        combo = self.findChild(QtGui.QComboBox, "channelSelection")
        self.ui.set_channel(combo.currentText())
        self.ui.rewrite_console()
        self.activate_selected_tab()


class QtUI(UI):
    NAME = "Qt"
    CONSOLE_HISTORY = 10000

    def __init__(self, in_queue, out_queue):
        self.app = None
        self.main_window = None
        self.window = None
        self.console = None
        self.channel = None
        self._message_buffer = []
        self._channels = []
        self._console_messages = {}

        super(QtUI, self).__init__(in_queue, out_queue)

    def _start_qt(self):

        self.app = QtGui.QApplication([])
        self._build_ui()
        self.app.exec_()

    def _build_ui(self):
        self.main_window = MainWindow(self)

        self.console = self.main_window.findChild(QtGui.QPlainTextEdit,
                                                  "console")
        self.regulars_list = self.main_window.findChild(QtGui.QListView,
                                                        "regularsList")

        self._init_regulars_list()

        self.main_window.show()

        self.main_window.activate_selected_tab()

        if self._channels:
            self.set_channels(self._channels)

        self.rewrite_console()

    def rewrite_console(self):
        self.console.clear()
        if self.channel and self.console:
            self._init_console(self.channel)
            for msg in self._console_messages[self.channel]:
                self._write_to_console(msg)

    def _init_regulars_list(self):
        self.regulars_model = QtGui.QStandardItemModel(self.regulars_list)
        self.regulars_list.setModel(self.regulars_model)

    def add_regular_to_list(self, name):
        item = QtGui.QStandardItem(name)
        self.regulars_model.appendRow(item)

    def remove_regular_from_list(self, name):
        for item in self.regulars_model.findItems(name):
            self.regulars_model.removeRow(item.row())

    def set_channel(self, channel):
        self.channel = channel

    def run(self):
        if not HAVE_QT:
            raise RuntimeError("Cannot start Qt UI, PyQt5 library not found.")

        mq = QtMessageQueue(self, self._in_queue)
        mq.start()

        self.set_channel("#lietu")

        self._start_qt()

    def send_message(self, msg):
        self._out_queue.put(msg)

    def set_channels(self, channels):
        self._channels = channels

        if not self.main_window:
            return

        combo = self.main_window.findChild(QtGui.QComboBox, "channelSelection")
        combo.model().clear()

        for channel in channels:
            combo.addItem(channel)

            if not self.channel:
                self.set_channel(channel)

    def _init_console(self, channel):
        if channel not in self._console_messages:
            self._console_messages[channel] = []

    def quit(self):
        self._running = False
        self._out_queue.put(StopMsg())

    def stop(self):
        self.main_window.close()

    def append_to_console(self, channel, message):
        self._init_console(channel)

        messages = self._console_messages[channel]
        messages.append(message)
        self._console_messages[channel] = messages[self.CONSOLE_HISTORY * -1:]

        if channel == self.channel and self.console:
            self._write_to_console(message)

    def _write_to_console(self, message):
        cursor = self.console.textCursor()
        cursor.clearSelection()
        cursor.movePosition(
            QtGui.QTextCursor.End,
            QtGui.QTextCursor.MoveAnchor
        )

        cursor.insertText(message + "\n")


def get_ui_choices():
    choices = []

    for subclass in UI.__subclasses__():
        choices.append(subclass.NAME)

    return choices


def get_ui(name):
    in_queue = multiprocessing.Queue()
    out_queue = multiprocessing.Queue()

    for subclass in UI.__subclasses__():
        if subclass.NAME == name:
            ui = subclass(in_queue, out_queue)

            return ui, in_queue, out_queue

    return None, None, None
