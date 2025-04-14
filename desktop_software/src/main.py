import sys,os,traceback
from PySide6.QtWidgets import QApplication

from src.gui.gui import SheetSavvyUX
from src.serial_interface.serial_interface_impl import SerialInterfaceImpl
from src.post_processor import post_processor
from src.sheet_music_generator.sheet_music_generator_impl import SheetMusicGeneratorImpl

BASE_SCORE_PATH = "src/archive/base_score.xml"

TEST_DEVICE_PORT = "COM11"
BAUD_RATE = 9600

def main(argv):

    app = QApplication(argv)
    ux = SheetSavvyUX()
    serial_interface = SerialInterfaceImpl(TEST_DEVICE_PORT,BAUD_RATE)
    music_generator = SheetMusicGeneratorImpl(BASE_SCORE_PATH)

    def prepare_sheet_music():
        music_generator.reset()
        notes,attrs = post_processor.process_data(serial_interface.json_data)
        music_generator.set_note_data(notes)
        music_generator.set_attr_data(attrs)
        music_generator()

    ux.si = serial_interface
    ux.smg = music_generator
    serial_interface.ux = ux
    serial_interface.prepare_sheet_music = prepare_sheet_music

    try:

        ux.click_reset_button()
        ux.show()
        app.exec()

    finally:

        if serial_interface.is_open():
            serial_interface.close()

if __name__=="__main__": main(sys.argv)