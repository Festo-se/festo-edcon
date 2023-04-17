"""CLI tool that performs a sequence on Telegram111 and EDrive classes."""
import time
import sys

from profidrive.telegram111 import Telegram111


def add_tg111_args(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_tg111 = subparsers.add_parser('tg111')
    parser_tg111.set_defaults(func=tg111_func)


def tg111_func(edrive, args):
    """Executes subcommand based on provided arguments"""
    edrive.assert_selected_telegram(111)
    # Start process data
    edrive.start_io()

    tg111 = Telegram111()

    print("Enable plc control")
    tg111.stw1.control_by_plc = True
    edrive.send_io(tg111.output_bytes())
    time.sleep(0.1)

    print("Acknowledge any present faults")
    tg111.stw1.fault_ack = True
    edrive.send_io(tg111.output_bytes())
    time.sleep(0.1)

    print("Configure STW1 and OVERRIDE")
    tg111.stw1.no_coast_stop = True
    tg111.stw1.no_quick_stop = True
    tg111.stw1.enable_operation = True
    tg111.stw1.do_not_reject_traversing_task = True
    tg111.stw1.no_intermediate_stop = True
    tg111.stw1.fault_ack = False
    tg111.override.value = 16384
    edrive.send_io(tg111.output_bytes())
    time.sleep(0.1)

    print("Check fault present bit", end='')
    tg111.input_bytes(edrive.recv_io())
    if tg111.zsw1.fault_present:
        print(f" -> is present ({int(tg111.fault_code)})")
        edrive.stop_io()
        sys.exit(1)
    print(" -> cleared!")

    print("Enable Powerstage")
    tg111.stw1.on = True
    edrive.send_io(tg111.output_bytes())
    time.sleep(0.5)

    print("Start homing procedure")
    tg111.stw1.start_homing_procedure = True
    edrive.send_io(tg111.output_bytes())
    time.sleep(0.1)

    while tg111.zsw1.home_position_set:
        try:
            tg111.input_bytes(edrive.recv_io())
            time.sleep(0.1)

        except KeyboardInterrupt:
            print("Killed by user!")
            edrive.stop_io()
            sys.exit(1)

    while not tg111.zsw1.home_position_set:
        try:
            tg111.input_bytes(edrive.recv_io())
            time.sleep(0.1)

        except KeyboardInterrupt:
            print("Killed by user!")
            edrive.stop_io()
            sys.exit(1)

    print("Finished homing")

    tg111.stw1.start_homing_procedure = False
    edrive.send_io(tg111.output_bytes())
    time.sleep(0.1)

    print("Start traversing task")
    tg111.mdi_tarpos.value = 10000
    tg111.mdi_velocity.value = 1200000
    tg111.mdi_acc.value = 16384
    tg111.mdi_dec.value = 16384
    tg111.pos_stw1.activate_mdi = True
    tg111.stw1.activate_traversing_task = True
    edrive.send_io(tg111.output_bytes())
    time.sleep(0.1)

    while tg111.zsw1.target_position_reached:
        try:
            tg111.input_bytes(edrive.recv_io())
            time.sleep(0.1)

        except KeyboardInterrupt:
            print("Killed by user!")
            edrive.stop_io()
            sys.exit(1)

    while not tg111.zsw1.target_position_reached:
        try:
            tg111.input_bytes(edrive.recv_io())
            print(
                f"Target: {int(tg111.mdi_tarpos)}, Current: {int(tg111.xist_a)}")
            time.sleep(0.1)

        except KeyboardInterrupt:
            print("Killed by user!")
            edrive.stop_io()
            sys.exit(1)

    print("Target position reached")

    tg111.stw1.enable_operation = False
    edrive.send_io(tg111.output_bytes())
    time.sleep(0.1)

    edrive.stop_io()
