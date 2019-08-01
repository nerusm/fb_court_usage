__author__ = 'suren'
import serial
import logging.config
import logging

logging.config.fileConfig('logging.ini')
logging.basicConfig()
logger = logging.getLogger(__name__)
ser0 = serial.Serial("/dev/tnt0",9600, timeout=0.5)
ser1 = serial.Serial("/dev/tnt1",9600, timeout=0.5)
print ser0.portstr
logger.info("heLLO")
ser0.write('helooo')