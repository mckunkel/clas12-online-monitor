from __future__ import print_function, division

import sys
import os
import numpy as np

from clas12monitor.ui import QtGui, uic
from clas12monitor.dc import plots, DCComponents, dc_wire_occupancy
from clas12monitor.dc import CrateTab, DBTab, TBTab, SetRunDialogue, DCRB, STBTab

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        curdir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(os.path.join(curdir,'ui','MainWindow.ui'), self)
        self.dcwires = DCComponents()
        self.loadRun(1)
        #self.dcwires.initialize_session()

        # This part requires actual run data to be loaded

        #self.run_number.setValue(int(DCWires.runnum))
        #self.run_number.valueChanged.connect(self.run_number.show)

        #if (self.run_number.value.Changed() :
            #print(self.run_number.value())


        ### Explorer Tabs
        self.explorer_tabs = QtGui.QTabWidget()

        #Loading in the crate tab
        self.crate = CrateTab(self)
        self.crate.setMinimumWidth(750)
        self.crate.setMaximumHeight(1000)
        crate_vbox = QtGui.QVBoxLayout(self.crate)
        self.explorer_tabs.addTab(self.crate, 'Crates')

        #Loading in the distribution board tab
        self.dboard = DBTab(self)
        self.dboard.setMinimumWidth(750)
        dboard_vbox = QtGui.QVBoxLayout(self.dboard)
        self.explorer_tabs.addTab(self.dboard, 'Distribution Boards')

        #Loading in the translation board tab
        self.tboard = TBTab(self)
        self.tboard.setMinimumWidth(750)
        tboard_vbox = QtGui.QVBoxLayout(self.tboard)
        self.explorer_tabs.addTab(self.tboard, 'Translation Boards')

        #Loading in the DC readout board tab
        self.dcrb = DCRB(self)
        self.dcrb.setMinimumWidth(750)
        dcrb_vbox = QtGui.QVBoxLayout(self.dcrb)
        self.explorer_tabs.addTab(self.dcrb, 'Drift Chamber Readout Board')

        #Loading in the Signal Translation Board
        self.stb = STBTab(self)
        self.stb.setMinimumWidth(750)
        stb_vbox = QtGui.QVBoxLayout(self.stb)
        self.explorer_tabs.addTab(self.stb, 'Signal Translation Board')

        self.explorer_tabs.setMinimumWidth(750)
        self.explorer_tabs.setSizePolicy(
                                   QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Expanding)


        explorer_vbox = QtGui.QVBoxLayout()
        explorer_vbox.addWidget(self.explorer_tabs)
        self.explorer_holder.setLayout(explorer_vbox)


        ### Chooser Sidebar
        #self.sidebar = Sidebar(self.session)
        #sidebar_vbox = QtGui.QVBoxLayout()
        #sidebar_vbox.addWidget(self.sidebar)
        #self.chooser_holder.setLayout(sidebar_vbox)

        ### Wiremap
        self.wiremaps = plots.DCWireStack(self)
        wmap_vbox = QtGui.QVBoxLayout()
        wmap_vbox.addWidget(self.wiremaps)
        self.wiremap_holder.setLayout(wmap_vbox)

        def update_wiremap(sec,data):
            #if loop allows this method to narrow in on a specific sector
            if sec is not None:
                self.wiremaps.setCurrentIndex(sec+1)
            else:
                self.wiremaps.setCurrentIndex(0)
            #set the data passed in
            self.wiremaps.data = data

        #self.sidebar.post_update = update_wiremap

        def f(i):
            print('explorer tab changed. index:',self.explorer_tabs.currentIndex())
            print('    sub index:',self.explorer_tabs.currentWidget().currentIndex())

            if (i == 0):
                self.wiremaps.setCurrentIndex(0)
            else:
                #Making sure the wiremap corresponds to the chosen sector
                self.wiremaps.setCurrentIndex(self.explorer_tabs.currentWidget().currentIndex() + 1)
        #connect the explorer tab signal to this method
        self.explorer_tabs.currentChanged.connect(f)


        #this method will send which ever component array is called on
        def changeViewTab():
            if self.explorer_tabs.currentIndex() == 0:
                self.crate.sendCrateArray()
            if self.explorer_tabs.currentIndex() == 1:
                self.dboard.sendDBArray()
            if self.explorer_tabs.currentIndex() == 2:
                self.tboard.sendTBArray()
            if self.explorer_tabs.currentIndex() == 3:
                self.dcrb.sendDCRBArray()
            if self.explorer_tabs.currentIndex() == 4:
                self.stb.sendSTBArray()

        #connect the explorere tab to this method
        self.explorer_tabs.currentChanged.connect(changeViewTab)


        self.setModeExplorer()
        self.show()

    #Initialize explorer mode with default view of crate 1
    def setModeExplorer(self):
        self.actionExplorer.setChecked(True)
        self.actionChooser.setChecked(False)
        self.left_stacked_widget.setCurrentIndex(0)
        self.crate.sendCrateArray()

    #switching over to the search query
    def setModeChooser(self):
        self.actionExplorer.setChecked(False)
        self.actionChooser.setChecked(True)
        self.left_stacked_widget.setCurrentIndex(1)

    #this will set the actual run display number
    def setRunDialogue(self):
        run,ok = SetRunDialogue.getRunNum()
        if ok:
            self.loadRun(run)
    #this is fetching the runnumber data from the given data base
    def loadRun(self, runnumber):
        self.rundisplay.setNum(runnumber)
        self.dcwires.run = runnumber
        self.dcwires.fetch_data()



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
