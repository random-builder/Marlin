
import serial
import math
import argparse
import sys


class BinaryStream:
    device = None
    max_block_size = 96
    port = None

    def __init__(self, device, baud):
        self.port = serial.Serial(device, baudrate=baud)

    def file_bytes(self, filename):
        return open(filename, "rb").read()

    def readline(self):
        line = self.port.readline()
        print("<<< ", line)
        return line

    def write(self, data):
        self.port.write(data.encode('utf8'))
        print(">>> ", data)

    def command_wait(self, cmd):
        self.write(cmd + '\n')
        while self.readline()[0:2] != b'ok':
            continue

    def send_int(self, value):
        self.port.write(value.to_bytes(4, byteorder='little'))

    def send_short(self, value):
        self.port.write(value.to_bytes(2, byteorder='little'))

    def send_array(self, value):
        self.port.write(bytearray(value))

    # checksum is simple 16bit xor
    def checksum(self, seed, value):
        return ((seed ^ value) ^ (seed << 8)) & 0xFFFF

    # build a checksum for an entire data buffer using an initial seed value
    def build_checksum(self, buffer):
        cs = 0x53A2
        for b in buffer:
            cs = self.checksum(cs, b)
        return cs

    # send a packet and await varification or error response
    def send_packet(self, id, packet):
        global max_block_size
        retries = 0
        while retries < 3:
            print("Transfering packet(" + str(id) + ") " + str(len(packet)) + "B")
            # transfer packet header
            self.send_int(id)
            self.send_short(len(packet))
            self.send_short(self.build_checksum(packet))
            # transfer the data block
            self.send_array(packet)

            # example control flow for stream protocol possible responses to packet transfer
            # so : the stream has been opened sucessfuly, 2 byte payload <uint16_t> maximum block size
            # ok : packet was transfered successfuly and validated
            # rs : something went wrong resend the last packet // 3 chances per packet before stream ends automaticaly
            # sf : something went really wrong the stream is closed
            # sc : all data transfered, validated and the stream has been closed

            # wait for a valid response
            code, value = self.read_response()

            # normal byte success response and stream complete
            if(code == b'ok' or code == b'sc'):
                return True

            # the stream was setup successfully and expects at most max_block_size blocks
            if(code == b'so'):
                max_block_size = int.from_bytes(value, byteorder='little', signed=False)
                print("max supported block size:", max_block_size)
                return True

            # the stream has encountered a fatal error and closed
            if(code == b'sf'):
                return False

            # last possible respose is a retry packet response
            retries += 1
        return False

    def read_response(self):
        valid_reponses = [ b'so', b'ok', b'rs', b'sf', b'sc' ]
        res = self.readline()
        while res[0:2] not in valid_reponses:  # todo: add response timeout
            res = self.readline()
        return res[0:2], res[2:4]

    def transfer_data_block(self, block_number, data, block_size):
        start = block_size * block_number
        end = start + block_size
        block = data[start:end]
        return self.send_packet(block_number + 1, block)

    def transfer_stream_header(self, file_size):
        stream_start_token = 0x1234
        packet = stream_start_token.to_bytes(2, byteorder='little') + file_size.to_bytes(4, byteorder='little')
        return self.send_packet(0, packet)

    def transfer_data(self, file):
        # actual packet size is block_size + header(8), needs to fit in Marlin RX buffer to avoid data loss on some platforms

        # Buffer the entire file
        data = self.file_bytes(file)

        if(len(data)):
            # initiate the file transfer, waite for standard ok response
            self.command_wait('M28B1 ' + file)
            # transfer the stream header in a standard packet that has a token and the filesize, returns false on error
            if not self.transfer_stream_header(len(data)):
                return False

            # In this example I do not allow this to scale but it doesnt need to be constant for flow control, failed packet could reduce block size ect
            blocks = math.floor((len(data) + max_block_size - 1) / max_block_size)
            for i in range(blocks):
                # transfer all the file data block packets, returns false on error
                if not self.transfer_data_block(i, data, max_block_size):
                    return False

        return True


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Send files over a serial port to Marlin')
    parser.add_argument('filename', help='The file to transfer')
    parser.add_argument("-p", "--port", default="/dev/ttyACM0", help="serial port to use")
    parser.add_argument("-b", "--baud", default="115200", help="baud rate of serial connection")
    args = parser.parse_args()

    try:
        stream = BinaryStream(args.port, args.baud)
        stream.command_wait('M21')
        try:
            if stream.transfer_data(args.filename):
                print("File Transfered")
            else:
                print("File Transfer Failed")
        except Exception as e:
            print(e)
        stream.command_wait('M22')
    except Exception as e:
        print(e)

