from Dynkin import secretary_dynkin
import math
import random
import numpy 

def secretary_kleinberg(v: list[int], k: int) -> list[int]:
    if k == 0 :
        return []
    elif k == 1 :
        hired = secretary_dynkin(v)
        return [hired] if hired is not None else []
    elif k > 1 :
        n = len(v)
        l = math.floor(k/2)
        m = math.floor(numpy.random.binomial(n, 0.5))
        #m = math.floor(n/2)
        print ("m = {m}, n = {n}, l = {l}".format(m=m, n=n, l=l))

        s1 = v[:m]         
        s2 = v[m:]

        A = secretary_kleinberg(s1, l)

        Y = sorted(s1, reverse=True)
        if len(Y) >= l :
            threshold = Y[l-1]  # l-th largest value in s1
            print(f"Threshold for s2 is {threshold}")
        else :
            threshold = -float("inf")

        B = []
        for i in range(len(s2)):
            if len(A) + len(B) == k :
                break
            if s2[i] > threshold :
                B.append(i + m)  # Adjust index for s2
        
        return A + B
    
if __name__ == "__main__":
    n = int(input("Number of candidates: "))
    k = int(input("Number of hires (k): "))
    values = [random.randint(0, 100) for _ in range(n)] 

    print(f"Candidate values: {values}\n")
    hired_candidates = secretary_kleinberg(values, k)
    print(f"Hired candidates: {hired_candidates}, Values: {[values[i] for i in hired_candidates]}")