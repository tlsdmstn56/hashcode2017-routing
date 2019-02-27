import numpy as np

from cache_server import Cache_server
from endpoint import Endpoint


class Solver2(object):
    def __init__(self, V, E, R, C, X):
        self.V = V
        self.E = E
        self.R = R
        self.C = C
        self.X = X
        self.video_size = []
        self.endpoints = []
        self.cache_servers = []
        self.request_list = []
        
    def solve(self, output_file_name):
        for request in request_list:
            for cache_candidate in self.endpoints[reqeust.end_point_id].connected_cache:
                if cache_servers[cache_candidate].can_add_video(video_size[reqeust.video_id])
        