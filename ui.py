import datetime
import sys
import os.path
import time
import traceback
from collections import defaultdict

import PySide6
from PySide6 import QtCore
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from ui_main_window import Ui_MainWindow
from ui_sub_window import Ui_Form

from prog import hash_comp


class dir_widget(QWidget):
    """
    widget
    """

    def __init__(self):
        super(dir_widget, self).__init__()
        if not self.objectName():
            self.setObjectName(u"dir_item")
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.layout = QHBoxLayout()
        self.dir_input = QLineEdit(self)
        self.dir_input.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        self.dir_btn = QToolButton(self)
        self.dir_btn.setObjectName(u"dir_button")
        self.dir_btn.setText("...")
        self.dir_btn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.del_btn = QToolButton(self)
        self.del_btn.setObjectName(u"del_button")
        self.del_btn.setText("X")
        self.del_btn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.setLayout(self.layout)
        self.layout.addWidget(self.dir_input)
        self.layout.addWidget(self.dir_btn)
        self.layout.addWidget(self.del_btn)

        # self.dir_input.returnPressed.connect(self.dir_entered)
        self.dir_btn.clicked.connect(self.dir_btn_clicked)
        self.del_btn.clicked.connect(self.del_btn_clicked)

    def dir_btn_clicked(self):
        """
        show file dialog to choose directory
        """
        # print("dir_btn")
        path = QFileDialog.getExistingDirectory(self, "Directory", "C:/", QFileDialog.ShowDirsOnly)
        # print(f"path : {path}")
        self.dir_input.setText(path)

    def del_btn_clicked(self):
        """
        delete widget
        """
        # print("del_btn")
        # print(f"delete dir_widget {self} : {self.dir_input.text()}")
        self.deleteLater()


class sub_window(QWidget):
    """
    draw sub window
    """

    def __init__(self, parent=None):
        super(sub_window, self).__init__()
        self.parent = parent
        self.ui_sub = Ui_Form()
        self.ui_sub.setupUi(self)
        self.ui_sub.retranslateUi(self)
        self.ui_sub.progressBar.setValue(0)
        self.dirs = None
        self.fast = None
        self.prog = hash_comp()
        self.threadpool = QThreadPool()

        # keep scroll to bottom
        bar = self.ui_sub.listWidget.verticalScrollBar()
        bar.rangeChanged.connect(lambda x, y: bar.setValue(bar.maximum()))

    def cleanup(self):
        self.threadpool.clear()
        self.ui_sub.progressBar.setValue(0)
        self.ui_sub.pushButton_2.setDisabled(False)
        self.dirs = None
        self.fast = None
        self.prog.clear()
        self.ui_sub.listWidget.clear()
        self.ui_sub.listWidget_2.clear()
        self.threadpool.clear()

    def cancel_btn_clicked(self):
        """
            hide window
        """
        # print("sub_window cancel")
        self.cleanup()
        self.hide()
        self.parent.show()

    def delete_btn_clicked(self):
        """
            delete selected items
        """
        # print("sub_window delete")
        # print(f"items count : {self.ui_sub.listWidget_2.count()}")

        # test code
        """
        self.ui_sub.progressBar.setValue(0)
        worker2 = worker_obj(self.test)
        worker2.signal.finished.connect(self.complete)
        worker2.signal.progress.connect(self.progress)
        self.threadpool.start(worker2)
        """

        if self.ui_sub.listWidget_2.count() == 0:
            self.ui_sub.pushButton_2.setDisabled(True)
            return

        self.ui_sub.progressBar.setValue(0)
        worker = worker_obj(self.remover)
        worker.signal.finished.connect(self.complete)
        worker.signal.progress.connect(self.progress)
        self.threadpool.start(worker)

    def test(self, progress_callback):
        for i in range(1, 10000):
            progress_callback.emit(i / 9999 * 100, f"test text {i / 9999 * 100:.4f}%")

    def remover(self, progress_callback):
        selected = []
        complete = 0
        failed = 0
        count = 0
        text = None
        # get list of files to delete
        for index in range(self.ui_sub.listWidget_2.count()):
            if self.ui_sub.listWidget_2.item(index).checkState() == Qt.Checked:
                selected.append(self.ui_sub.listWidget_2.item(index).text())
        total = len(selected)

        if total == 0:
            return

        for target in selected:
            try:
                os.remove(target)
                text = f"remove {target}"
                complete += 1
            except(OSError,):
                text = f"failed to remove {target}"
                failed += 1
            finally:
                count += 1
                progress_callback.emit(count / total * 100, text)
        progress_callback.emit(100, "delete complete")
        progress_callback.emit(100, f"total : {count} , successful : {complete} , failed : {failed}")

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        """
        :param event:
        """
        # print("sub_window hide")
        self.cleanup()
        self.parent.show()

    def set_param(self, directory, fast):
        self.dirs = directory
        self.fast = fast

    def progress(self, n=None, s=None):
        """
        :param n: value shows in progressBar
        :param s: log string in listWidget
        """
        time = datetime.datetime.now().__str__()[:-2]
        if n:
            self.ui_sub.progressBar.setValue(n)
        if s:
            self.ui_sub.listWidget.addItem(time + "\t" + s)
        # self.ui_sub.listWidget.scrollToBottom() # <-- causes gui freezing

    def execute(self, progress_callback):
        """
        :param progress_callback:
        :return:
        """
        self.prog.set_param(self.dirs, self.fast)
        progress_callback.emit(0, f"directories : {self.dirs}, fast : {self.fast}")
        if self.fast:
            progress_callback.emit(5, f"collecting file list from {self.dirs}")
            self.prog.get_items_by_size()
            progress_callback.emit(20, f"file count : {self.prog.item_count}")

            progress_callback.emit(25, f"sorting files by size")
            self.prog.get_items_by_size_dupe()
            progress_callback.emit(30,
                                   f"size count : {self.prog.same_size_count}, "
                                   f"file count : {self.prog.same_size_item_count}")

            progress_callback.emit(35, f"getting hash values from file's first 1k bits")
            self.prog.get_hash_1k_list()
            progress_callback.emit(60,
                                   f"hash count : {self.prog.hash1k_count}, "
                                   f"file count : {self.prog.hash1k_item_count}")

            progress_callback.emit(90, f"sorting files by 1k hash values")
            self.prog.get_same_hash_1k_list()
            progress_callback.emit(100,
                                   f"hash count: {self.prog.same_hash1k_count}, "
                                   f"file count : {self.prog.same_hash1k_item_count}")

            return self.prog.hash1k
        else:
            progress_callback.emit(5, f"collecting file list from {self.dirs}")
            self.prog.get_items_by_size()
            progress_callback.emit(20, f"file count : {self.prog.item_count}")

            progress_callback.emit(25, f"sorting files by size")
            self.prog.get_items_by_size_dupe()
            progress_callback.emit(30,
                                   f"size count : {self.prog.same_size_count}, "
                                   f"file count : {self.prog.same_size_item_count}")

            progress_callback.emit(35, f"getting hash values from file's first 1k bits")
            self.prog.get_hash_1k_list()
            progress_callback.emit(60,
                                   f"hash count : {self.prog.hash1k_count}, "
                                   f"file count : {self.prog.hash1k_item_count}")

            progress_callback.emit(65, f"sorting files by 1k hash values")
            self.prog.get_same_hash_1k_list()
            progress_callback.emit(70,
                                   f"hash count: {self.prog.same_hash1k_count}, "
                                   f"file count : {self.prog.same_hash1k_item_count}")

            progress_callback.emit(75, f"sorting files by hash values")
            self.prog.get_hash_list()
            progress_callback.emit(90,
                                   f"hash count: {self.prog.hash_count}, "
                                   f"file count : {self.prog.hash_item_count}")

            progress_callback.emit(95, f"sorting files by hash values")
            self.prog.get_same_hash_list()
            progress_callback.emit(100,
                                   f"hash count: {self.prog.same_hash_count}, "
                                   f"file count : {self.prog.same_hash_item_count}")

            return self.prog.hash

    def result(self, r):
        # todo: check by directory, check reverse, mouse right click menu...
        for key in r:
            self.ui_sub.listWidget_2.addItem(f"count : {len(r[key])} size : {key[0]}\n hash : {key[1]}")
            count = 0
            for item in r[key]:
                target = QListWidgetItem(f"{item}")
                target.setFlags(target.flags() | QtCore.Qt.ItemIsUserCheckable)
                count += 1
                if count == len(r[key]):
                    # if count == 1:
                    target.setCheckState(QtCore.Qt.Unchecked)
                else:
                    target.setCheckState(QtCore.Qt.Checked)
                self.ui_sub.listWidget_2.addItem(target)
        pass

    def complete(self):
        # print("thread complete")
        # self.ui_sub.listWidget.scrollToBottom()
        pass

    def run_worker(self):
        worker = worker_obj(self.execute)
        worker.signal.result.connect(self.result)
        worker.signal.finished.connect(self.complete)
        worker.signal.progress.connect(self.progress)
        self.threadpool.start(worker)


class main_window(QMainWindow):
    """
    draw main window
    """

    def __init__(self):
        super(main_window, self).__init__()
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self)
        self.ui_main.retranslateUi(self)
        self.ui_main.verticalLayout_2.addWidget(dir_widget())  # initial single directory widget

        self.ui_sub = sub_window(self)

    def add_btn_clicked(self):
        """
        add widget
        """
        # print("main_window add")
        # print(self.ui.verticalLayout.count())
        # self.ui.verticalLayout.insertWidget(self.ui.verticalLayout.count(), dir_widget())
        self.ui_main.verticalLayout_2.addWidget(dir_widget())
        self.adjustSize()  # resize window to fit widget sizes

    def ok_btn_clicked(self):
        """
        execute duplicate search program
        """
        # print("main_window ok")
        fast = self.ui_main.checkBox.isChecked()
        child = self.findChildren(dir_widget)
        dirs = []

        for item in child:
            directory = item.dir_input.text()
            dirs.append(directory)

        # print(f"given params - directory : {dirs}, isfast : {fast}")
        self.ui_sub.set_param(dirs, fast)
        # Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.ui_sub.setWindowTitle(QCoreApplication.translate("Form", u"Running", None))
        self.ui_sub.run_worker()
        self.ui_sub.show()
        self.ui_sub.parent.hide()

    @staticmethod
    def cancel_btn_clicked():
        """
        exit program
        """
        # print("main_window cancel")
        sys.exit()

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        """
        :param event:
        """
        # print("main_window destroyed")
        # self.thread.thread().quit()
        self.ui_sub.cleanup()


class worker_signal(QObject):
    """
    signals available from worker
    """
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int, str)


class worker_obj(QRunnable):
    """
    threading class
    """

    def __init__(self, fn, *args, **kwargs):
        super(worker_obj, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signal = worker_signal()

        self.kwargs['progress_callback'] = self.signal.progress

    @Slot()
    def run(self):
        """
        :return: signals from worker_signal and result
        """
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signal.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signal.result.emit(result)
        finally:
            self.signal.finished.emit()
