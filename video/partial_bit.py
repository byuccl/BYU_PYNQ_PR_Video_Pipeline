import os
import pynq
import pynq.lib
import pynq.lib.video
import pynq.lib.audio
from pynq.pl import Bitstream
from datetime import datetime
from .constants import *

# Overlay constants
PYNQ_PATH = os.path.dirname(os.path.realpath(__file__))

BS_IS_PARTIAL = "/sys/devices/soc0/amba/f8007000.devcfg/is_partial_bitstream"
BS_XDEVCFG = "/dev/xdevcfg"


class PartialBitstream:
    """This class instantiates a programmable logic bitstream.

    Attributes
    ----------
    bitfile_name : str
        The absolute path of the bitstream.
    timestamp : str
        Timestamp when loading the bitstream. Format:
        year, month, day, hour, minute, second, microsecond

    """

    def __init__(self, bitfile_name):
        """Return a new Bitstream object.

        Users can either specify an absolute path to the bitstream file
        (e.g. '/home/xilinx/src/pynq/bitstream/base.bit'),
        or a relative path within an overlay folder.
        (e.g. 'base.bit' for base/base.bit).

        Note
        ----
        self.bitstream always stores the absolute path of the bitstream.

        Parameters
        ----------
        bitfile_name : str
            The bitstream absolute path or name as a string.
        """
        super().__init__()

        if not isinstance(bitfile_name, str):
            raise TypeError("Bitstream name has to be a string.")

        bitfile_abs = os.path.abspath(bitfile_name)
        bitfile_overlay_abs = os.path.join(PYNQ_PATH,
                                           bitfile_name)
        print(bitfile_overlay_abs)
        if os.path.isfile(bitfile_name):
            self.bitfile_name = bitfile_abs
        elif os.path.isfile(bitfile_overlay_abs):
            self.bitfile_name = bitfile_overlay_abs
        else:
            raise IOError('Bitstream file {} does not exist.'
                          .format(bitfile_name))

        self.timestamp = ''


    def download(self):
        """The method to download the bitstream onto PL.

        Note
        ----
        The class variables held by the singleton PL will also be updated. In
        addition, if this method is called on an unsupported architecture it
        will warn and return.

        Returns
        -------
        None

        """

        # Compose bitfile name, open bitfile
        with open(self.bitfile_name, 'rb') as f:
            buf = f.read()

        # Set is_partial_bitfile device attribute to 0
        with open(BS_IS_PARTIAL, 'w') as fd:
            fd.write('1')


        # Write bitfile to xdevcfg device
        with open(BS_XDEVCFG, 'wb') as f:
            f.write(buf)

        t = datetime.now()
        self.timestamp = "{}/{}/{} {}:{}:{} +{}".format(
                t.year, t.month, t.day,
                t.hour, t.minute, t.second, t.microsecond)

