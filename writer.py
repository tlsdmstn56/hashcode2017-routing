def write_output(filename, output: dict):
    """write output file 
    
    Args:
        filename(string): path of output filename
        output(dict): key(int)=cache_id value(list)=list of video
    """
    with open(filename, "w") as f:
        f.write(str(len(output)))
        f.write("\n")
        for cache_id in output:
            f.write(str(cache_id))
            f.write(" ")
            for video_id in output[cache_id]:
                f.write(str(video_id))
                f.write(" ")
            f.write("\n")
            
# test code
if __name__=="__main__":
    output ={}
    output[0] = [1,2,3]
    output[1] = [0,3,4]
    output[2] = [5,4,3]
    write_output("./test_output", output)
    print("Write should be:")
    print("3")
    print("0 1 2 3")
    print("1 0 3 4")
    print("2 5 4 3")
