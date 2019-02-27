class Cache_server(object):
    def __init__(self, cache_capacity=0):
        self.connected_endpoint = []
        self.stored_videos = []
        self.size_of_stored_videos = {}
        self.added_score_of_video = {}
        self.current_capacity = 0
    
    def add_video(self, video_id, video_size):
        if video_id in self.stored_videos:
            return 
        self.stored_videos.append(video_id)
        self.size_of_stored_videos[video_id] = video_size
        self.current_capacity += video_size
        
    def can_add_video(self, video_size, cache_capacity):
        return ((self.current_capacity + video_size) <= cache_capacity)
    
# test codes
if __name__=="__main__":
    c = Cache_server()
    print("Expected True: {}".format(c.can_add_video(200,300)))
    print("Expected False: {}".format(c.can_add_video(200,150)))
    c.add_video(1,50)
    print("Expected [1]: {}".format(c.stored_videos))
    print("Expected {{1: 50}}: {}".format(c.size_of_stored_videos))
    print("Expected False: {}".format(c.can_add_video(50,80)))