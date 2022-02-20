import argparse
import asyncio
import sys
import time
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from bleak import BleakClient

# Nordic Semiconductor UART UUIDS; You shouldn't have to change these, unless you're modifying this to work on a device that uses a different chip.
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

# Bluetooth commands; These are the commands used on the GT101, and shouldn't need to be changed unless you're modifying this to work on a different device model.
CommandOpenHRM = bytes([0xAB, 0x00, 0x04, 0xFF, 0x84, 0x80, 0x01])
CommandShakeWatch = bytes([0xAB, 0x00, 0x03, 0xFF, 0x71, 0x80])

# Bluetooth MAC address of your smartwatch; If I'm not mistaken, you can find this in one of the watch's menus.
address = "00:00:00:00:00:00"


# VRChat OSC server parameters; You shouldn't have to change these unless you're using a custom OSC config.
OSCServerIP = "127.0.0.1"
OSCServerPort = 9000

# Name of the VRChat Avatar Parameter that you want your heartrate to drive.
HeartrateParameter = "Heartrate"

async def gthrm_server():

    OSCClient = udp_client.SimpleUDPClient(OSCServerIP, OSCServerPort)
    print("Initialized OSC Client on port", OSCServerPort,"!")

    def handle_disconnect(_: BleakClient):
        print("Watch Disconnected.")
        for task in asyncio.all_tasks():
            task.cancel()

    MessagesReceived = 0

    def handle_rx(_: int, data: bytearray):
        nonlocal MessagesReceived
        if MessagesReceived == 0:
            MessagesReceived += 1
        elif MessagesReceived == 1:
            print("Watch Successfully Connected!")
            if data[-2] == 0:
                print("Current Battery:", data[-1],", Currently Not Charging.")
            elif data[-2] == 3:
                print("Current Battery:", data[-1], ", Currently Charging.")
            print("Press any key to exit.")
            MessagesReceived += 1
        elif MessagesReceived == 2:
            print("Received Heartrate:", data[-1])
            OSCClient.send_message("/avatar/parameters/" + HeartrateParameter, float(data[-1]))

    async with BleakClient(address, disconnected_callback=handle_disconnect) as client:


        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)

        await client.write_gatt_char(UART_RX_CHAR_UUID, CommandOpenHRM)

        while True:
            await asyncio.get_running_loop().run_in_executor(None, sys.stdin.buffer.readline)
            return


try:
    asyncio.run(gthrm_server())
except asyncio.CancelledError:
    # task is cancelled on disconnect, so we ignore this error
    pass
