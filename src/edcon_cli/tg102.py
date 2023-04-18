"""CLI tool that performs a sequence on Telegram102 and EDrive classes."""
import sys
import time
import math

from profidrive.telegram102 import Telegram102


def add_tg102_args(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_tg102 = subparsers.add_parser('tg102')
    parser_tg102.set_defaults(func=tg102_func)
    parser_tg102.add_argument('-s', '--speed-setpoint',
                              default="1000000000", help='Speed setpoint to use')
    parser_tg102.add_argument('-m', '--moment-reduction',
                              default="0.0", help='Moment reduction to use in percent')
    parser_tg102.add_argument('--sinusoidal', action="store_true",
                              help='Apply sinusoidal setpoint')


def tg102_func(edrive, args):
    """Executes subcommand based on provided arguments"""
    if args.sinusoidal:
        def get_setpoint():
            return round(int(args.speed_setpoint) * math.sin(time.time()))
    else:
        def get_setpoint():
            return int(args.speed_setpoint)

    edrive.assert_selected_telegram(102)

    # Start process data
    edrive.start_io()

    tg102 = Telegram102()

    print("Enable plc control")
    tg102.stw1.control_by_plc = True
    edrive.send_io(tg102.output_bytes())
    time.sleep(0.1)

    print("Acknowledge any present faults")
    tg102.stw1.fault_ack = True
    edrive.send_io(tg102.output_bytes())
    time.sleep(0.1)

    print("Configure STW1 and MOMRED")
    tg102.stw1.no_coast_stop = True
    tg102.stw1.no_quick_stop = True
    tg102.stw1.enable_operation = True
    tg102.stw1.enable_ramp_generator = True
    tg102.stw1.unfreeze_ramp_generator = True
    tg102.stw1.fault_ack = False
    tg102.momred.value = round(16384.0 * float(args.moment_reduction) / 100.0)
    edrive.send_io(tg102.output_bytes())
    time.sleep(0.1)

    print("Check fault present bit", end='')
    tg102.input_bytes(edrive.recv_io())
    if tg102.zsw1.fault_present:
        print(" -> is present")
        edrive.stop_io()
        sys.exit(1)
    print(" -> cleared!")

    print("Enable Powerstage")
    tg102.stw1.on = True
    edrive.send_io(tg102.output_bytes())
    time.sleep(0.5)

    print("Enable Setpoint")
    tg102.stw1.setpoint_enable = True
    edrive.send_io(tg102.output_bytes())
    time.sleep(0.1)

    while True:
        try:
            tg102.nsoll_b.value = get_setpoint()
            edrive.send_io(tg102.output_bytes())
            tg102.input_bytes(edrive.recv_io())

            print(f"Setpoint:{tg102.nsoll_b}, Current:{tg102.nist_b}")

            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    edrive.stop_io()
