'''
Created on Mar 21, 2012

@author: moloch

    Copyright [2012] [Redacted Labs]

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''


import socket
import logging


class HostNetworkConfig():

    @classmethod
    def get_ip_address(self, uri="rootthebox.com", port=80):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((uri, port))
        ip_address = sock.getsockname()[0]
        sock.close()
        return ip_address
