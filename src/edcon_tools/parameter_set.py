"""CLI Tool to write whole paremeter set EDrive device using .pck file."""
from edcon_tools.generic_bus_argparser import GenericBusArgParser
from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_ethernetip import EDriveEthernetip
import logging


def main():
    """Parses command line arguments and reads PNU accordingly."""
    gparser = GenericBusArgParser('Write parameter set to an EDrive device.')
    gparser.add_argument("pnumap", help="PNU map (.csv) file")
    gparser.add_argument("file", help="Parameter set (.pck) file to write")

    args = gparser.create()

    # Initialize driver
    if args.com_type == 'modbus':
        edrive = EDriveModbus(args.ip_address, flavour=args.flavour)
    elif args.com_type == 'ethernetip':
        edrive = EDriveEthernetip(args.ip_address)

    pnumap = {}
    with open(args.pnumap) as f:
        lines = [line.split(';') for line in f.readlines()]
        for line in lines:
            try:
                pnumap[line[7].split('_')[0][:-2]] = int(line[0])
            except:
                pass

    # print(pnumap)

    pnuvalues = []
    with open(args.file, 'rb') as f:
        lines = f.readlines()
        start_idx = lines.index(b'----\r\n') + 1
        end_idx = lines[start_idx:].index(b'----\r\n') + start_idx
        for item in lines[start_idx:end_idx]:

            key = item.decode().split(';')[0]
            value = bytes.fromhex(item.decode().split(';')[1].split('x')[1])
            pnuvalues.append([key, value])

    counter = 0
    for pnuvalue in pnuvalues:
        status = edrive.write_pnu_raw(
            pnu=pnumap[pnuvalue[0].rsplit('.', 1)[0]], subindex=int(pnuvalue[0].split('.')[-1]), num_elements=1, value=pnuvalue[1][::-1])

        if status:
            counter += 1
        else:
            logging.error(f"Setting {pnuvalue[0]} to {pnuvalue[1]} failed")

    print(f"{counter} PNUs succesfully written!")


if __name__ == "__main__":
    main()
