# -*- coding=utf-8 -*-

import re
import requests

import ipaddr
from naivepool import ThreadPool

def scan_one(func, ip, port):
    response = func(ip, port)
    return response

def scan_all(func, init_ip, number, ports):
    """use `func` to scan ip range from `init_ip` to `init_ip+number`

    Args:
        def func(ip, port):
            if success:
                return response string
            else:
                return None
        
        func: function to ssrf, take two argument:
          ip(ipaddr.IPAddress) and port(int),
          if port is open, return response string, else return None
        
        init_ip: a string means start ip
        number: number of ip to scan
        port: a list of int number

    Returns:
        response of func
       
    """
    try:
        init_ip = ipaddr.IPAddress(init_ip)    
    except ValueError, e:
        print(e)
        return False

    inputs = []
    for i in range(number):
        for j in range(len(ports)):
            ip = init_ip + i
            inputs.append((func, ip, ports[j]))

    p = ThreadPool(scan_one, inputs, 20, True)
    p.start()
    
    for i in range(len(inputs)):
        if p.outputs[i] != None:
            print("%s:%s is valid: %s" % (str(inputs[i][1]), str(inputs[i][2]), p.outputs[i]))

if __name__ == "__main__":
    pass
