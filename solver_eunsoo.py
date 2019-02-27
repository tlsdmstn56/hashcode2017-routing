#!/usr/bin/env python3
import sys
from queue import PriorityQueue

import numpy as np

from writer import write_output
from endpoint import Endpoint
from cache_server import Cache_server


class ScoredInfo(object):
    """Class for elements in Solver.score_queue


    Attributes:
        score: R * (Ld - L)
        cache_id: id of cache server with the lowest latency given video_id and endpoint_id
        video_id: id of video
        endpoint_id: id of endpoint
    """

    def __init__(self, score, highest_cache_id, video_id, endpoint_id):
        self.score = score
        self.cache_id = highest_cache_id
        self.video_id = video_id
        self.endpoint_id = endpoint_id

    # comparison functions to keep descending order by ScoredInfo.score in Solver.score_queue(PriorityQueue)
    def __lt__(self, other):
        return self.score > other.score

    def __le__(self, other):
        return self.score >= other.score

    def __eq__(self, other):
        return self.score == other.score

    def __ne__(self, other):
        return self.score != other.score

    def __gt__(self, other):
        return self.score < other.score

    def __ge__(self, other):
        return self.score <= other.score


class Solver(object):
    def __init__(self):
        self.output = {}
        self.endpoints = {}
        self.score_queue = None
        self.cache_servers = None
        self.endpoints = None
        self.videos = None
        self.output = {}
        self.requests = []

    def read(self, filename):
        with open(filename, "r") as f:
            # read size parameters
            self.V, self.E, self.R, self.C, self.X = map(
                int, f.readline().split())
            self.score_queue = PriorityQueue()
            for cache_id in range(self.C):
                self.output[cache_id] = []
            # read videos
            self.videos = list(map(int, f.readline().split()))
            # read endpoints
            self.endpoints = [Endpoint() for i in range(self.E)]
            self.cache_servers = [Cache_server() for i in range(self.C)]
            for endpoint_id in range(self.E):
                latency, num_cache = map(int, f.readline().split())
                current_endpoint = self.endpoints[endpoint_id]
                current_endpoint.latency_from_data_center = latency
                for _ in range(num_cache):
                    cache_id, cache_latency = map(int, f.readline().split())
                    self.cache_servers[cache_id].connected_endpoint.append(
                        endpoint_id)
                    current_endpoint.connected_cache.append(cache_id)
                    current_endpoint.latency_of_connected_cache[cache_id] = cache_latency
            # read requests
            for request_id in range(self.R):
                video_id, endpoint_id, requests = map(
                    int, f.readline().split())
                # request: [video_id, endpoint_id, requests]
                self.requests.append([video_id, endpoint_id, requests])
                self.process_request(video_id, endpoint_id, requests)

    def get_score(self, endpoint_id, cache_id, requests):
        """ get_score calculate R*(Ld - L) from endpoint_id to cache_id, multiplied by the number of requests

        Args:
            endpoint_id(int)
            cache_id(int)
            requests(int): the number of requests

        Returns:
            score(int): caculated score given endpoint_id and cache_id
        """
        endpoint = self.endpoints[endpoint_id]
        if len(endpoint.connected_cache) == 0:
            return 0
        cache = self.cache_servers[cache_id]
        latency_to_cache = endpoint.latency_of_connected_cache[cache_id]
        return requests*(endpoint.latency_from_data_center - latency_to_cache)

    def process_request(self, video_id, endpoint_id, requests):
        """process request and put them into score_queue in the form of ScoredInfo type

        비디오 id, 엔드포인트 id, 리퀘스트 수를 읽은 후 
        가장 높은 엔드포인트와 연결된 모든 캐시에서의 점수를 계산합니다.
        계산된 점수 중 가장 높은 점수일 때의 정보를 score_queue에 넣습니다.
        """
        endpoint = self.endpoints[endpoint_id]
        if len(endpoint.connected_cache) == 0:
            return
        max_score = -1
        max_cache_id = -1
        for cache_id in endpoint.connected_cache:
            score = self.get_score(endpoint_id, cache_id, requests)
            if score > max_score:
                max_score = score
                max_cache_id = cache_id
        s = ScoredInfo(max_score, max_cache_id, video_id, endpoint_id)
        self.score_queue.put(s)

    def write(self, filename):
        write_output(filename, self.output)

    def solve(self):
        while not self.score_queue.empty():
            entry = self.score_queue.get()
            cache = self.cache_servers[entry.cache_id]
            if cache.can_add_video(self.videos[entry.video_id], self.X):
                # TODO: 용량이 넘어가는 경우 다른 캐시에 넣는 방법을 생각해야 함
                cache.add_video(entry.video_id, self.videos[entry.video_id])
            else:
                pass
        # TODO: 스코어 대로 비디오를 배치한 후 남은 공간에 대한 처리
        # making self.output
        for cache_id in range(self.C):
            cache = self.cache_servers[cache_id]
            if len(cache.stored_videos) == 0:
                continue
            self.output[cache_id] = cache.stored_videos

    def is_output_valid(self):
        for cache_id in self.output:
            sum_of_size = 0
            for video_id in self.output[cache_id]:
                sum_of_size += self.videos[video_id]
            if sum_of_size > self.X:
                return False
        return True

    def minimum_latency_cache_id(self, endpoint_id, video_id):
        """return cache_id which has most minimum latency given endpoint_id and video_id

        엔드포인트와 연결된 모든 캐시의 레이턴시를 확인한 후 가장 작은 레이턴시를 갖는 캐시의 id를 리턴        
        """
        endpoint = self.endpoints[endpoint_id]
        min_latency = endpoint.latency_from_data_center
        minimum_latency_cache_id = -1
        for cache_id in endpoint.connected_cache:
            cache = self.cache_servers[cache_id]
            if video_id not in cache.stored_videos:
                continue
            if min_latency > endpoint.latency_of_connected_cache[cache_id]:
                min_latency = endpoint.latency_of_connected_cache[cache_id]
                minimum_latency_cache_id = cache_id
        return minimum_latency_cache_id

    def solved_result_score(self):
        if not self.is_output_valid():
            print("Validation Error")
            return
        denominator = 0
        nominator = 0
        for request in self.requests:
            video_id, endpoint_id, requests = request
            denominator += requests
            cache_id = self.minimum_latency_cache_id(endpoint_id, video_id)
            if cache_id < 0:
                nominator += self.endpoints[endpoint_id].latency_from_data_center
            else:
                nominator += self.get_score(endpoint_id, cache_id, requests)

        return int(float(nominator) / float(denominator) * 1000.0)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERROR: need inputfile path and outputfile path")
        print("{} [inputfile path] [outputfile path]".format(argv[0]))
        exit(0)
    solver = Solver()
    solver.read(sys.argv[1])
    solver.solve()
    solver.write(sys.argv[2])
    print("Score: {}".format(solver.solved_result_score()))
