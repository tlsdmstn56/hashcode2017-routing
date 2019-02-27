import sys
import numpy as np

from cache_server import Cache_server
from endpoint import Endpoint
from request_list import Request_list

def return_input_arguments(filename):

	with open("input_data/" + filename, "r") as file_input:
		
		video_size = []
		endpoint = []
		endpoint_id = 0
        connected_cache = []
        V, E, R, C, X = file_input.readline().split(" ")
		V = int(V)
		E = int(E)
		R = int(R)
		C = int(C)
		X = int(X)
		video_size = file_input.readline().split(" ")
		            
        for line in file_input.readlines().split(" "):
            chache_number[endpoint_id] = line[1]:
            datacenter_to_endpoint = line[0]
            
            for number in range (0,chache_number):
                line = file_input.readlines().split(" ")
			    cache_id = line[0]
			    cache_latency[endpoint_id] = {line[0] : line[1]}
                connected_cache[endpoint_id].append(line[0])
                if(number == chache_number-1):
                    endpoint_id += 1
