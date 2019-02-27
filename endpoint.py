class Endpoint(object):

    def __init__(self):
        self.latency_from_data_center = 0
        self.connected_cache = []
        self.latency_of_connected_cache = {}
