#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import struct
import time
import logging
from emeter2 import emeterPacket
from speedwiredecoder import decode_speedwire

# Configuration
MAIN_METER_SN = 1900123456 # This is the SMA Energy Meter to copy all main values from (Your emulation master)
VIRTUAL_METER_SN = 1900999999 # should start with 1900 and have 10 digits in total
MULTICAST_GRP = '239.12.255.254'
MULTICAST_PORT = 9522

# Other meter serials (example setup)
SUPPLY_METERS = []  # Einspeisung auf "supply"
CONSUME_METERS = [1900555555] # Einspeisung auf "consume"

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def setup_multicast_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MULTICAST_PORT))
    mreq = struct.pack("=4sl", socket.inet_aton(MULTICAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock

def setup_sender_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

def merge_to_same_keys(master, other, keys):
    for key in keys:
        if key in other:
            master[key] = master.get(key, 0.0) + other[key]


def merge_consume_as_supply(master, other, mapping):
    for source, target in mapping.items():
        if source in other:
            master[target] = master.get(target, 0.0) + other[source]

def parse_and_emulate(data_dict, send_sock):
    timestamp = int(time.time() * 1000)
    packet = emeterPacket(int(VIRTUAL_METER_SN))
    packet.begin(timestamp)

    # Total power/energy consumption (positive) (Summierte Leistung/Energie Bezug (positiv))
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_ACTIVE_POWER, round(data_dict['pconsume'] * 10))
    packet.addCounterValue(emeterPacket.SMA_POSITIVE_ACTIVE_ENERGY, round(data_dict['pconsumecounter'] * 1000 * 3600))

    # Total power/energy feed-in (negative) (Summierte Leistung/Energie Einspeisung (negativ))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_ACTIVE_POWER, round(data_dict['psupply'] * 10))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_ACTIVE_ENERGY, round(data_dict['psupplycounter'] * 1000 * 3600))

    # Reactive power (Blindleistung)
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_REACTIVE_POWER, round(data_dict['qconsume'] * 10))
    packet.addCounterValue(emeterPacket.SMA_POSITIVE_REACTIVE_ENERGY, round(data_dict['qconsumecounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_REACTIVE_POWER, round(data_dict['qsupply'] * 10))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_REACTIVE_ENERGY, round(data_dict['qsupplycounter'] * 1000 * 3600))

    # Apparent power (Scheinleistung)
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_APPARENT_POWER, round(data_dict['sconsume'] * 10))
    packet.addCounterValue(emeterPacket.SMA_POSITIVE_APPARENT_ENERGY, round(data_dict['sconsumecounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_APPARENT_POWER, round(data_dict['ssupply'] * 10))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_APPARENT_ENERGY, round(data_dict['ssupplycounter'] * 1000 * 3600))

    # cos(phi)
    packet.addMeasurementValue(emeterPacket.SMA_POWER_FACTOR, round(data_dict['cosphi'] * 1000))

    # Phase 1
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_ACTIVE_POWER_L1, round(data_dict['p1consume'] * 10))
    packet.addCounterValue(emeterPacket.SMA_POSITIVE_ACTIVE_ENERGY_L1, round(data_dict['p1consumecounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_ACTIVE_POWER_L1, round(data_dict['p1supply'] * 10))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_ACTIVE_ENERGY_L1, round(data_dict['p1supplycounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_REACTIVE_POWER_L1, round(data_dict['q1consume'] * 10))
    packet.addCounterValue(emeterPacket.SMA_POSITIVE_REACTIVE_ENERGY_L1, round(data_dict['q1consumecounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_REACTIVE_POWER_L1, round(data_dict['q1supply'] * 10))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_REACTIVE_ENERGY_L1, round(data_dict['q1supplycounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_APPARENT_POWER_L1, round(data_dict['s1consume'] * 10))
    packet.addCounterValue(emeterPacket.SMA_POSITIVE_APPARENT_ENERGY_L1, round(data_dict['s1consumecounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_APPARENT_POWER_L1, round(data_dict['s1supply'] * 10))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_APPARENT_ENERGY_L1, round(data_dict['s1supplycounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_VOLTAGE_L1, round(data_dict['u1'] * 1000))
    packet.addMeasurementValue(emeterPacket.SMA_CURRENT_L1, round(data_dict['i1'] * 1000))
    packet.addMeasurementValue(emeterPacket.SMA_POWER_FACTOR_L1, round(data_dict['cosphi1'] * 1000))

    # Phase 2
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_ACTIVE_POWER_L2, round(data_dict['p2consume'] * 10))
    packet.addCounterValue(emeterPacket.SMA_POSITIVE_ACTIVE_ENERGY_L2, round(data_dict['p2consumecounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_ACTIVE_POWER_L2, round(data_dict['p2supply'] * 10))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_ACTIVE_ENERGY_L2, round(data_dict['p2supplycounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_REACTIVE_POWER_L2, round(data_dict['q2consume'] * 10))
    packet.addCounterValue(emeterPacket.SMA_POSITIVE_REACTIVE_ENERGY_L2, round(data_dict['q2consumecounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_REACTIVE_POWER_L2, round(data_dict['q2supply'] * 10))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_REACTIVE_ENERGY_L2, round(data_dict['q2supplycounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_APPARENT_POWER_L2, round(data_dict['s2consume'] * 10))
    packet.addCounterValue(emeterPacket.SMA_POSITIVE_APPARENT_ENERGY_L2, round(data_dict['s2consumecounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_APPARENT_POWER_L2, round(data_dict['s2supply'] * 10))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_APPARENT_ENERGY_L2, round(data_dict['s2supplycounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_VOLTAGE_L2, round(data_dict['u2'] * 1000))
    packet.addMeasurementValue(emeterPacket.SMA_CURRENT_L2, round(data_dict['i2'] * 1000))
    packet.addMeasurementValue(emeterPacket.SMA_POWER_FACTOR_L2, round(data_dict['cosphi2'] * 1000))

    # Phase 3
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_ACTIVE_POWER_L3, round(data_dict['p3consume'] * 10))
    packet.addCounterValue(emeterPacket.SMA_POSITIVE_ACTIVE_ENERGY_L3, round(data_dict['p3consumecounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_ACTIVE_POWER_L3, round(data_dict['p3supply'] * 10))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_ACTIVE_ENERGY_L3, round(data_dict['p3supplycounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_REACTIVE_POWER_L3, round(data_dict['q3consume'] * 10))
    packet.addCounterValue(emeterPacket.SMA_POSITIVE_REACTIVE_ENERGY_L3, round(data_dict['q3consumecounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_REACTIVE_POWER_L3, round(data_dict['q3supply'] * 10))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_REACTIVE_ENERGY_L3, round(data_dict['q3supplycounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_APPARENT_POWER_L3, round(data_dict['s3consume'] * 10))
    packet.addCounterValue(emeterPacket.SMA_POSITIVE_APPARENT_ENERGY_L3, round(data_dict['s3consumecounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_APPARENT_POWER_L3, round(data_dict['s3supply'] * 10))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_APPARENT_ENERGY_L3, round(data_dict['s3supplycounter'] * 1000 * 3600))
    packet.addMeasurementValue(emeterPacket.SMA_VOLTAGE_L3, round(data_dict['u3'] * 1000))
    packet.addMeasurementValue(emeterPacket.SMA_CURRENT_L3, round(data_dict['i3'] * 1000))
    packet.addMeasurementValue(emeterPacket.SMA_POWER_FACTOR_L3, round(data_dict['cosphi3'] * 1000))

    packet.end()

    send_sock.sendto(packet.getData()[:packet.getLength()], (MULTICAST_GRP, MULTICAST_PORT))
#    logging.info(f'Sent: Emulated SN {VIRTUAL_METER_SN} with {len(data_dict)} values')

def main():
    recv_sock = setup_multicast_listener()
    send_sock = setup_sender_socket()
    send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    meter_data = {}

    logging.info(f'Waiting for master SMA energy meter SN {MAIN_METER_SN}, emulating new energy meter SN {VIRTUAL_METER_SN}...')

    while True:
        try:
            data, _ = recv_sock.recvfrom(2048)
            decoded = decode_speedwire(data)
            if not decoded or "serial" not in decoded:
                continue

            sn = decoded["serial"]
            if sn not in [MAIN_METER_SN] + SUPPLY_METERS + CONSUME_METERS:
                continue

            meter_data[sn] = decoded

            if sn != MAIN_METER_SN:
                continue  # Warte auf Hauptzähler

            master = decoded.copy()

            supply_keys = [
                'psupply', 'psupplycounter', 'ssupply', 'ssupplycounter', 'qsupply', 'qsupplycounter',
                'p1supply', 'p1supplycounter', 's1supply', 's1supplycounter', 'q1supply', 'q1supplycounter',
                'p2supply', 'p2supplycounter', 's2supply', 's2supplycounter', 'q2supply', 'q2supplycounter',
                'p3supply', 'p3supplycounter', 's3supply', 's3supplycounter', 'q3supply', 'q3supplycounter',
                'i1', 'i2', 'i3'
            ]
            for sn2 in SUPPLY_METERS:
                if sn2 in meter_data:
                    merge_to_same_keys(master, meter_data[sn2], supply_keys)

            consume_to_supply = {
                'pconsume': 'psupply', 'pconsumecounter': 'psupplycounter',
                'sconsume': 'ssupply', 'sconsumecounter': 'ssupplycounter',
                'qconsume': 'qconsume', 'qconsumecounter': 'qconsumecounter',
                'p1consume': 'p1supply', 'p1consumecounter': 'p1supplycounter',
                's1consume': 's1supply', 's1consumecounter': 's1supplycounter',
                'q1consume': 'q1consume', 'q1consumecounter': 'q1consumecounter',
                'p2consume': 'p2supply', 'p2consumecounter': 'p2supplycounter',
                's2consume': 's2supply', 's2consumecounter': 's2supplycounter',
                'q2consume': 'q2consume', 'q2consumecounter': 'q2consumecounter',
                'p3consume': 'p3supply', 'p3consumecounter': 'p3supplycounter',
                's3consume': 's3supply', 's3consumecounter': 's3supplycounter',
                'q3consume': 'q3consume', 'q3consumecounter': 'q3consumecounter',
                'i1': 'i1', 'i2': 'i2', 'i3': 'i3'
            }
            for sn2 in CONSUME_METERS:
                if sn2 in meter_data:
                    merge_consume_as_supply(master, meter_data[sn2], consume_to_supply)

            parse_and_emulate(master, send_sock)
        except Exception as e:
            logging.error(f'Error while parsing or sending: {e}')

if __name__ == "__main__":
    main()
