def read_for_scoring(filename):
    with open("score_data/" + filename, "r") as file_input:    
            N = file_input.readline()
            N = int(N)
            lineNum = 0
            cacheIDs = []
            videos_in_c = []
            for line in range(0,N):
                lineInfo = file_input.readline().rstrip().split(" ")
                cacheIDs.append(lineInfo[0])
                videos_in_c.append((lineInfo[1:]))
                print(cacheID,videos_in_c)
    return(cacheIDs, videos_in_c)     

def validation(sizes, capacities, cacheIDs, videos_in_c):
    valid = True
    for cacheID in cacheIDs:
        video_bytes = 0
        for video_in_c in videos_in_c[cacheID]:
            video_bytes += sizes[video_in_c]
        if(capacities[cacheID]<video_bytes):
            valid = False
    #TODO: sizes에 비디오번호대로 용량 넣기/ capcacitis에 cacheID 맞춰서 용량넣기
    
def main(filename):
    cacheIDs, videos_in_c = read_for_scoring(filename)
    if(validation(,,cacheIDs, videos_in_c)==False):
        print("your answer include an error: saved videos in cache server more than its capacity")
        return 0
    
    
print(scoring('test.txt'))