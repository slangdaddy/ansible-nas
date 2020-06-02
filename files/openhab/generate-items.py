#!/usr/bin/env python3
#
# Parse an OpenHab things file and generate items for it. Currently only intended to be used for HomeMatic.
#
# TODO: 
# - How to inject pre-defined groups?

import argparse
import re
from jinja2 import Template


template_HG_HM_CC_RT_DN   =    Template("""
String                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_BatteryType             "BatteryType"             <battery>            ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#BATTERY_TYPE"}
String                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_CentralAddressSpoofed   "CentralAddressSpoofed"   <error>              ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#CENTRAL_ADDRESS_SPOOFED"}
Switch                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ConfigPending           "ConfigPending"           <settings>           ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#CONFIG_PENDING"}
Switch                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_DeleteDevice            "DeleteDevice"            <error>              ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#DELETE_DEVICE"}
String                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_DeleteDeviceMode        "DeleteDeviceMode"        <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#DELETE_DEVICE_MODE"}
Switch                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_DeviceInBootloader      "DeviceInBootloader"      <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#DEVICE_IN_BOOTLOADER"}
String                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Firmware                "Firmware"                <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#FIRMWARE"}
Switch                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Inhibit                 "Inhibit"                 <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#INHIBIT"}
Switch                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_LowBat                  "LowBat"                  <lowbattery>         ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#LOWBAT"}
Number                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Rssi                    "Rssi"                    <qualityofservice>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#RSSI"}
Number                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_RssiDevice              "RssiDevice"              <qualityofservice>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#RSSI_DEVICE"}
Number                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_RssiPeer                "RssiPeer"                <qualityofservice>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#RSSI_PEER"}
Number                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_SignalStrength          "SignalStrength"          <qualityofservice>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#SIGNAL_STRENGTH"}
Switch                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_StickyUnreach           "StickyUnreach"           <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#STICKY_UNREACH"}
Switch                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Unreach                 "Unreach"                 <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#UNREACH"}
Switch                    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_UpdatePending           "UpdatePending"           <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:0#UPDATE_PENDING"}

Switch   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_WindowState   "WindowState"   <window>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:3#WINDOW_STATE"}

{% if "Bath" in thing.location %}
Number:Temperature         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ActualTemperature   "ActualTemperature"   <temperature>   ({{ thing.mainGroup }}, g{{   thing.domain   }}_{{   thing.location   }}_Temperature)   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#ACTUAL_TEMPERATURE"}
Number:Temperature         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_SetTemperature      "SetTemperature"      <heating>       ({{ thing.mainGroup }}, g{{   thing.domain   }}_{{   thing.location   }}_TargetTemperature)   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#SET_TEMPERATURE"}
{% else %}
Number:Temperature         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ActualTemperature   "ActualTemperature"   <temperature>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#ACTUAL_TEMPERATURE"}
Number:Temperature         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_SetTemperature      "SetTemperature"      <heating>       ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#SET_TEMPERATURE"}
{% endif %}
Switch                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_AutoMode            "AutoMode"            <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#AUTO_MODE"}
Switch                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_BoostMode           "BoostMode"           <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#BOOST_MODE"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_BoostState          "BoostState"          <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#BOOST_STATE"}
Switch                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ComfortMode         "ComfortMode"         <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#COMFORT_MODE"}
String                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ControlMode         "ControlMode"         <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#CONTROL_MODE"}
String                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_FaultReporting      "FaultReporting"      <error>         ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#FAULT_REPORTING"}
Switch                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_LoweringMode        "LoweringMode"        <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#LOWERING_MODE"}
String                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyModeSubmit     "PartyModeSubmit"     <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#PARTY_MODE_SUBMIT"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStartDay       "PartyStartDay"       <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#PARTY_START_DAY"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStartMonth     "PartyStartMonth"     <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#PARTY_START_MONTH"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStartTime      "PartyStartTime"      <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#PARTY_START_TIME"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStartYear      "PartyStartYear"      <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#PARTY_START_YEAR"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStopDay        "PartyStopDay"        <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#PARTY_STOP_DAY"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStopMonth      "PartyStopMonth"      <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#PARTY_STOP_MONTH"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStopTime       "PartyStopTime"       <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#PARTY_STOP_TIME"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStopYear       "PartyStopYear"       <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#PARTY_STOP_YEAR"}
Number:ElectricPotential   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_BatteryState        "BatteryState"        <battery>       ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#BATTERY_STATE"}
Number:Dimensionless       {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ValveState          "ValveState"          <heating>       ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#VALVE_STATE"}
Number:Temperature         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ManuMode            "ManuMode"            <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#MANU_MODE"}
Number:Temperature         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyTemperature    "PartyTemperature"    <temperature>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-CC-RT-DN:ccu:{{   thing.id   }}:4#PARTY_TEMPERATURE"}
""")

template_HG_HM_TC_IT_WM_W_EU   =    Template("""
String                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_BatteryType             "BatteryType"             <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#BATTERY_TYPE"}
String                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_CentralAddressSpoofed   "CentralAddressSpoofed"   <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#CENTRAL_ADDRESS_SPOOFED"}
Switch                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ConfigPending           "ConfigPending"           <settings>           ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#CONFIG_PENDING"}
Switch                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_DeleteDevice            "DeleteDevice"            <error>              ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#DELETE_DEVICE"}
String                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_DeleteDeviceMode        "DeleteDeviceMode"        <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#DELETE_DEVICE_MODE"}
Switch                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_DeviceInBootloader      "DeviceInBootloader"      <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#DEVICE_IN_BOOTLOADER"}
String                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Firmware                "Firmware"                <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#FIRMWARE"}
Switch                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Inhibit                 "Inhibit"                 <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#INHIBIT"}
Switch                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_LowBat                  "LowBat"                  <lowbattery>         ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#LOWBAT"}
Number                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Rssi                    "Rssi"                    <qualityofservice>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#RSSI"}
Number                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_RssiDevice              "RssiDevice"              <qualityofservice>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#RSSI_DEVICE"}
Number                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_RssiPeer                "RssiPeer"                <qualityofservice>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#RSSI_PEER"}
Number                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_SignalStrength          "SignalStrength"          <qualityofservice>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#SIGNAL_STRENGTH"}
Switch                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_StickyUnreach           "StickyUnreach"           <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#STICKY_UNREACH"}
Switch                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Unreach                 "Unreach"                 <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#UNREACH"}
Switch                         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_UpdatePending           "UpdatePending"           <settings>           ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:0#UPDATE_PENDING"}

Number:Dimensionless   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Humidity      "Humidity"      <humidity>      ({{ thing.mainGroup }}, g{{   thing.domain   }}_{{   thing.location   }}_Humidity)   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:1#HUMIDITY"}
Number:Temperature     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Temperature   "Temperature"   <temperature>   ({{ thing.mainGroup }}, g{{   thing.domain   }}_{{   thing.location   }}_Temperature)   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:1#TEMPERATURE"}

Switch                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_AutoMode                 "AutoMode"                 <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#AUTO_MODE"}
Switch                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_BoostMode                "BoostMode"                <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#BOOST_MODE"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_BoostState               "BoostState"               <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#BOOST_STATE"}
Switch                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ComfortMode              "ComfortMode"              <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#COMFORT_MODE"}
Switch                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_CommunicationReporting   "CommunicationReporting"   <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#COMMUNICATION_REPORTING"}
String                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ControlMode              "ControlMode"              <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#CONTROL_MODE"}
Switch                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_LowBatReporting          "LowBatReporting"          <lowbattery>    ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#LOWBAT_REPORTING"}
Switch                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_LoweringMode             "LoweringMode"             <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#LOWERING_MODE"}
String                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyModeSubmit          "PartyModeSubmit"          <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#PARTY_MODE_SUBMIT"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStartDay            "PartyStartDay"            <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#PARTY_STOP_DAY"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStartMonth          "PartyStartMonth"          <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#PARTY_START_MONTH"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStartTime           "PartyStartTime"           <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#PARTY_START_TIME"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStartYear           "PartyStartYear"           <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#PARTY_START_YEAR"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStopDay             "PartyStopDay"             <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#PARTY_STOP_DAY"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStopMonth           "PartyStopMonth"           <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#PARTY_STOP_MONTH"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStopTime            "PartyStartTime"           <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#PARTY_STOP_TIME"}
Number                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyStopYear            "PartyStopYear"            <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#PARTY_STOP_YEAR"}
Switch                     {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_WindowOpenReporting      "WindowOpenReporting"      <window>        ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#WINDOW_OPEN_REPORTING"}
Number:ElectricPotential   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_BatteryState             "BatteryState"             <battery>       ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#BATTERY_STATE"}
Number:Dimensionless       {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ActualHumidity           "ActualHumidity"           <humidity>      ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#ACTUAL_HUMIDITY"}
Number:Temperature         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ActualTemperature        "ActualTemperature"        <temperature>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#ACTUAL_TEMPERATURE"}
Number:Temperature         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ManuMode                 "ManuMode"                 <none>          ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#MANU_MODE"}
Number:Temperature         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PartyTemperature         "PartyTemperature"         <temperature>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#PARTY_TEMPERATURE"}
Number:Temperature         {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_SetTemperature           "SetTemperature"           <heating>       ({{ thing.mainGroup }}, g{{   thing.domain   }}_{{   thing.location   }}_TargetTemperature)   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:2#SET_TEMPERATURE"}

Switch   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_WindowState   "WindowState"   <window>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:3#WINDOW_STATE"}

Number   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_DecisionVaule   "DecisionValue"   <none>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-TC-IT-WM-W-EU:ccu:{{   thing.id   }}:7#DECISION_VALUE"}
""")

template_HG_HM_Sec_SCo   =    Template("""
String                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_BatteryType             "BatteryType"             <battery>            ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#BATTERY_TYPE"}
String                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_CentralAddressSpoofed   "CentralAddressSpoofed"   <error>              ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#CENTRAL_ADDRESS_SPOOFED"}
Switch                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ConfigPending           "ConfigPending"           <settings>           ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#CONFIG_PENDING"}
Switch                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_DeleteDevice            "DeleteDevice"            <error>              ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#DELETE_DEVICE"}
String                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_DeleteDeviceMode        "DeleteDeviceMode"        <error>              ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#DELETE_DEVICE_MODE"}
Switch                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_DeviceInBootloader      "DeviceInBootloader"      <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#DEVICE_IN_BOOTLOADER"}
String                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Firmware                "Firmware"                <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#FIRMWARE"}
Switch                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_LowBat                  "LowBat"                  <lowbattery>         ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#LOWBAT"}
Number                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Rssi                    "Rssi"                    <qualityofservice>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#RSSI"}
Number                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_RssiDevice              "RssiDevice"              <qualityofservice>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#RSSI_DEVICE"}
Number                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_RssiPeer                "RssiPeer"                <qualityofservice>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#RSSI_PEER"}
Number                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_SignalStrength          "SignalStrength"          <qualityofservice>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#SIGNAL_STRENGTH"}
Switch                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_StickyUnreach           "StickyUnreach"           <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#STICKY_UNREACH"}
Switch                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Unreach                 "Unreach"                 <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#UNREACH"}
Switch                   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_UpdatePending           "UpdatePending"           <none>               ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:0#UPDATE_PENDING"}

String    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ShutterContact_Error         "ShutterContact   Error"         <error>        ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:1#ERROR"}
Switch    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ShutterContact_InstallTest   "ShutterContact   InstallTest"   <none>         ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:1#INSTALL_TEST"}
Switch    {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ShutterContact_LowBat        "ShutterContact   LowBat"        <lowbattery>   ({{ thing.mainGroup }})   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:1#LOWBAT"}
Contact   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_ShutterContact_State         "ShutterContact   State"         <window>       ({{ thing.mainGroup }}, g{{   thing.domain   }}_{{   thing.location   }}_WindowState)   {channel="homematic:HG-HM-Sec-SCo:ccu:{{   thing.id   }}:1#STATE"}
""")

template_kodi   =    Template("""
Player                 {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Control         "Control"         <none>               ({{ thing.mainGroup }})          {channel="{{   thing.id       }}:control"}
Switch                 {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Mute            "Mute"            <soundvolume_mute>   ({{ thing.mainGroup }})          {channel="{{   thing.id       }}:mute"}
Dimmer                 {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Volume          "Volume           [%d]"                <soundvolume>   ({{ thing.mainGroup }})            {channel="{{   thing.id             }}:volume"}
String                 {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Title           "Title            [%s]"                <none>          ({{ thing.mainGroup }})            {channel="{{   thing.id             }}:title"}
Switch                 {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_Stop            "Stop"            <none>               ({{ thing.mainGroup }})          {channel="{{   thing.id       }}:stop"}
String                 {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_SystemCommand   "SystemCommand"   <none>               ({{ thing.mainGroup }})          {channel="{{   thing.id       }}:systemcommand"}
String                 {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_MediaType       "MediaType"       <none>               ({{ thing.mainGroup }})          {channel="{{   thing.id       }}:mediatype"}
Number:Dimensionless   {{   thing.domain   }}_{{   thing.location   }}_{{   thing.name   }}_PlayingTime     "PlayingTime      [%d                  %%]"            <none>         ({{ thing.mainGroup }})            {channel="{{         thing.id      }}:currenttimepercentage"}
""")

class HMThing:
    def __init__(self, model, id, domain, location, name):
        self.model = model
        self.id = id
        self.domain = domain
        self.location = location
        self.name = name
        self.groups = []
        self.mainGroup = "g" + self.domain + "_" + self.location + "_" + self.name
        self.mainGroupDefinition = "Group " + self.mainGroup + " (g" + self.location + ")"

    def getModel(self):
        return self.model

    def getId(self):
        return self.id

    def getDomain(self):
        return self.domain

    def getLocation(self):
        return self.location

    def getName(self):
        return self.name

    def getGroups(self):
        return self.groups

    def getMainGroup(self):
        return self.mainGroup

    def getMainGroupDefinition(self):
        return self.mainGroup

class KodiThing:
    def __init__(self, id, domain, location, name):
        self.id = id
        self.domain = domain
        self.location = location
        self.name = name
        self.groups = []
        self.mainGroup = "g" + self.domain + "_" + self.location + "_" + self.name
        self.mainGroupDefinition = "Group " + self.mainGroup + " (g" + self.location + ")"

    def getId(self):
        return self.id

    def getDomain(self):
        return self.domain

    def getLocation(self):
        return self.location

    def getName(self):
        return self.name

    def getGroups(self):
        return self.groups

    def getMainGroup(self):
        return self.mainGroup

    def getMainGroupDefinition(self):
        return self.mainGroup

def processHM(ofh, line):
    # Assumption: things are defined in one line like this:
    ##    Thing HG-HM-CC-RT-DN          MEQ0182451  "Heating GF_LivingRoom device-01"
    ##    Thing DEVICE_MODEL          ID  "DOMAIN LOCATION DEVICE_NAME"
    prog = re.compile('\s*Thing\s+(?P<model>[a-zA-Z0-9\-]+)\s+(?P<id>[a-zA-Z0-9]+)\s+\"(?P<domain>[a-zA-Z0-9_\-]+)\s+(?P<location>[a-zA-Z0-9_\-]+)\s+(?P<name>[a-zA-Z0-9_\-]+)\"')
    result = prog.match(line)
    if result:
        t_model = result.group('model')
        t_id = result.group('id')
        t_domain = result.group('domain')
        t_location = result.group('location')
        t_name = result.group('name')
        thing = HMThing(t_model, t_id, t_domain, t_location, t_name)
        if t_model == 'HG-HM-CC-RT-DN':
            items = template_HG_HM_CC_RT_DN.render(thing=thing).strip()
            ofh.write(thing.mainGroupDefinition + "\n")
            ofh.write(items + "\n")
        elif t_model == 'HG-HM-TC-IT-WM-W-EU':
            items = template_HG_HM_TC_IT_WM_W_EU.render(thing=thing).strip()
            ofh.write(thing.mainGroupDefinition + "\n")
            ofh.write(items + "\n")
        elif t_model == 'HG-HM-Sec-SCo':
            items = template_HG_HM_Sec_SCo.render(thing=thing).strip()
            ofh.write(thing.mainGroupDefinition + "\n")
            ofh.write(items + "\n")
        else:
            print("Unknown thing type!")

def processKodi(ofh, line):
    # Assumption: things are defined in one line like this:
    ##Thing kodi:kodi:tv-wohnzimmer "Kodi TV Wohnzimmer"   @ "Netzwerk"    [ipAddress="tv-wohnzimmer"]
    ##Thing ID  "DOMAIN LOCATION DEVICE_NAME"
    prog = re.compile('\s*Thing\s+(?P<id>[a-zA-Z0-9\:\-_]+)\s+\"(?P<domain>[a-zA-Z0-9_\-]+)\s+(?P<location>[a-zA-Z0-9_\-]+)\s+(?P<name>[a-zA-Z0-9_\-]+)\"')
    result = prog.match(line)
    if result:
        t_id = result.group('id')
        t_domain = result.group('domain')
        t_location = result.group('location')
        t_name = result.group('name')
        thing = KodiThing(t_id, t_domain, t_location, t_name)
        items = template_kodi.render(thing=thing).strip()
        ofh.write(thing.mainGroupDefinition + "\n")
        ofh.write(items + "\n")

def main():
    print("Entering main")
    parser = argparse.ArgumentParser(prog = 'generate-items',
                description = 'Generate OpenHab items from things.')

    parser.add_argument('thingsfile', nargs='+')
    parser.add_argument('-o', '--output', type=str, default='generated.items')
    parser.add_argument('-t', '--type', type=str, default='homematic')

    args = parser.parse_args()

    for tf in args.thingsfile:
        print("Processing", tf)
        with open(tf) as tfh:
            print("Writing output to", args.output)
            with open(args.output, 'w') as ofh:
                ofh.write("// This file is generated. DO NOT MODIFY and expect changes to persist!\n\n")
                for line in tfh:
                    if args.type == 'homematic':
                        processHM(ofh, line)
                    elif args.type == 'kodi':
                        processKodi(ofh, line)
                    else:
                        print("Requested item type unkown!")

if __name__ == '__main__':
    print("Start")
    main()
    print("Stop")
