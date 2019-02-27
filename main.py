 #!/usr/bin/env python3
    
import sys    

if __name__=="__main__":
    if len(sys.argv) < 3:
        print("ERROR: need inputfile path and outputfile path")
        print("{} [inputfile path] [outputfile path]".format(argv[0]))
        exit(0)
    solver = Solver()
    solver.read(sys.argv[1])
    solver.solve()
    solver.write(sys.argv[2])