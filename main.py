import argparse
import asyncio
import sys
import time

import bleak
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
from bleak import BleakClient, BleakScanner

# Nordic Semiconductor UART UUIDS; You shouldn't have to change these, unless you're modifying this to work on a device that uses a different chip.
import main

UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

# Bluetooth commands; These are the commands used on the GT101, and shouldn't need to be changed unless you're modifying this to work on a different device model.
CommandOpenHRM = bytes([0xAB, 0x00, 0x04, 0xFF, 0x84, 0x80, 0x01])

# Doesn't work while HRM sensors are opened for some reason
CommandShakeWatch = bytes([0xAB, 0x00, 0x03, 0xFF, 0x71, 0x80])
CommandGetBatteryStatus = bytes([0xAB, 0x00, 0x04, 0xFF, 0x91, 0x80, 0x01])

# Bluetooth MAC address of your smartwatch; Leave this blank to use Auto-Discover Mode

# VRChat OSC server parameters; You shouldn't have to change these unless you're using a custom OSC config.
OSCClientIP = "127.0.0.1"
OSCClientPort = 9000

# Mac address of your smartwatch; Leave this blank to use auto-scan, unless that's giving you issues.
SmartwatchMac = "D5:0F:77:94:B1:1C"

# Property that determines whether the server will attempt to reconnect on failure
ReconnectOnFailure = True

# Name of the VRChat Avatar Parameter that you want your heartrate to drive.
HeartrateParameter = "Heartrate"
BatteryParameter = "SmartwatchBatteryLevel"

async def gthrm_server():

    OSCClient = udp_client.SimpleUDPClient(OSCClientIP, OSCClientPort)
    print("Initialized OSC Client on port " + str(OSCClientPort) + "!")

    async def DiscoverDevices():
        if main.SmartwatchMac == "":
            print("Searching For Watch...")
            devices = await BleakScanner.discover()
            for d in devices:
                if d.name == "GT101":
                    print("Watch Has Been Located! Mac Address:", d.address)
                    return d.address
        else:
            return main.SmartwatchMac

    def handle_disconnect(_: BleakClient):
        print("Watch Disconnected.")
        for task in asyncio.all_tasks():
            task.cancel()

    async def handle_rx(_: int, data: bytearray):
        if str(bytearray.hex(data)).startswith("ab0005ff9180"):
            print("Received Battery Status:", data[-1])
            OSCClient.send_message("/avatar/parameters/" + BatteryParameter, float(data[-1]))
        elif str(bytearray.hex(data)).startswith("ab0004ff8480"):
            print("Received Heartrate:", data[-1])
            OSCClient.send_message("/avatar/parameters/" + HeartrateParameter, float(data[-1]))
            await client.write_gatt_char(UART_RX_CHAR_UUID, CommandGetBatteryStatus)
        else:
            print("Recieved Unknown Data:", str(bytearray.hex(data)))

    async with BleakClient(await DiscoverDevices(), disconnected_callback=handle_disconnect) as client:

        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)

        loop = asyncio.get_running_loop()

        await client.write_gatt_char(UART_RX_CHAR_UUID, CommandOpenHRM)
        while True:
            await loop.run_in_executor(None, sys.stdin.buffer.readline)
            return

if ReconnectOnFailure:
    while True:
        try:
            asyncio.run(gthrm_server())
        except asyncio.CancelledError:
            # task is cancelled on disconnect, so we ignore this error
            pass
        except asyncio.TimeoutError:
            print("BLE Error: Connection Timed Out!")
        except bleak.exc.BleakError:
            print("BLE Error: Failed to connect to watch!")
        except AttributeError:
            print("BLE Error: Failed to locate watch!")
else:
    try:
        asyncio.run(gthrm_server())
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass
    except asyncio.TimeoutError:
        print("BLE Error: Connection Timed Out!")
    except bleak.exc.BleakError:
        print("BLE Error: Failed to connect to watch!")
    except AttributeError:
        print("BLE Error: Failed to locate watch!")