# Copyright 2014-present IntoRobot <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
IntoRobot

IntoRobot Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

www.intorobot.com
"""

from os.path import isdir, join

from SCons.Script import DefaultEnvironment


env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_NAME = "framework-intorobot-w67"
FRAMEWORK_DIR = platform.get_package_dir(FRAMEWORK_NAME)
FRAMEWORK_VERSION = platform.get_package_version(FRAMEWORK_NAME)
assert isdir(FRAMEWORK_DIR)

env.Append(
    ASFLAGS=[ "-c", "-g", "-MMD" ],
    CCFLAGS=[ "-g", "-w", "-Wfatal-errors" ],
    CXXFLAGS=[ "-fpermissive" ],
    LINKFLAGS=[
        "-u", "_scanf_float",
        "-u", "_printf_float",
        "-Wl,-wrap,system_restart_local",
        "-Wl,-wrap,spi_flash_read"
    ],

    CPPDEFINES=[
        ("INTOROBOT", 1),
        ("INTOYUN", 1),
        ("FIRMLIB_VERSION_STRING", FRAMEWORK_VERSION),
        ("PLATFORM_THREADING", 0),
        ("INTOROBOT_ARCH_XTENSA"),
        ("INTOROBOT_PLATFORM"),
        ("RELEASE_BUILD")
    ],

    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ],

    UPLOADERFLAGS=[
        "-ca", board.get("upload.address")
    ]
)

env.Prepend(
    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "hal", "inc"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "hal", "shared"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "platform", "MCU", "ESP8266-Arduino", "IntoRobot_Firmware_Driver", "inc"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "platform", "MCU", "ESP8266-Arduino", "sdk", "include"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "platform", "MCU", "ESP8266-Arduino", "sdk", "include", "json"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "platform", "MCU", "ESP8266-Arduino", "sdk", "lwip", "include"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "platform", "MCU", "ESP8266-Arduino", "sdk", "libc", "xtensa-lx106-elf", "include"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "platform", "shared", "inc"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "services", "inc"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "system", "inc"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "user", "inc"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "wiring", "inc"),
        join(FRAMEWORK_DIR, "variants", board.get("build.variant"), "hal", "inc"),
        join(FRAMEWORK_DIR, "variants", board.get("build.variant"), "wiring_ex", "inc"),
        join(FRAMEWORK_DIR, "variants", board.get("build.variant"), "communication", "mqtt", "inc")
    ],
    LIBPATH=[
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "platform", "MCU", "ESP8266-Arduino", "sdk", "lib"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"), "platform", "MCU", "ESP8266-Arduino", "sdk", "libc", "xtensa-lx106-elf", "lib"),
        join(FRAMEWORK_DIR, "variants", board.get("build.variant"), "lib"),
        join(FRAMEWORK_DIR, "variants", board.get("build.variant"), "build", "linker")
    ],
    LIBS=[
        "wiring","wiring_ex","hal", "system", "services", "communication", "platform",
        "m", "c", "gcc", "halhal", "phy", "pp", "net80211", "wpa", "crypto",
        "main", "wps", "axtls", "espnow", "smartconfig", "airkiss", "mesh",
        "wpa2", "lwip_gcc", "stdc++"
    ]
)

