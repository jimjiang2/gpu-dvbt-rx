#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Sun Oct 29 12:20:07 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import dtv
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import dvbt_rx
import sys


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.dvbt_rx_sync_cc_0 = dvbt_rx.sync_cc()
        self.dvbt_rx_superframe_0 = dvbt_rx.superframe()
        self.dvbt_rx_gpu_viterbi_0 = dvbt_rx.gpu_viterbi()
        self.dvbt_rx_demap_0 = dvbt_rx.demap()
        self.dtv_dvbt_reed_solomon_dec_0 = dtv.dvbt_reed_solomon_dec(2, 8, 0x11d, 255, 239, 8, 51, 8)
        self.dtv_dvbt_energy_descramble_0 = dtv.dvbt_energy_descramble(8)
        self.dtv_dvbt_convolutional_deinterleaver_0 = dtv.dvbt_convolutional_deinterleaver(136, 12, 17)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_char*1, 3024)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*10240, "/tmp/dvb_res_today.cfile", False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, "/tmp/rx.ts", False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.dvbt_rx_sync_cc_0, 0))    
        self.connect((self.blocks_vector_to_stream_0, 0), (self.dvbt_rx_superframe_0, 0))    
        self.connect((self.dtv_dvbt_convolutional_deinterleaver_0, 0), (self.dtv_dvbt_reed_solomon_dec_0, 0))    
        self.connect((self.dtv_dvbt_energy_descramble_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.dtv_dvbt_reed_solomon_dec_0, 0), (self.dtv_dvbt_energy_descramble_0, 0))    
        self.connect((self.dvbt_rx_demap_0, 0), (self.dvbt_rx_gpu_viterbi_0, 0))    
        self.connect((self.dvbt_rx_gpu_viterbi_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.dvbt_rx_superframe_0, 0), (self.dtv_dvbt_convolutional_deinterleaver_0, 0))    
        self.connect((self.dvbt_rx_sync_cc_0, 1), (self.dvbt_rx_demap_0, 0))    
        self.connect((self.dvbt_rx_sync_cc_0, 0), (self.dvbt_rx_demap_0, 1))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
