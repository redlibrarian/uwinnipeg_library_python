import os
import sys


def process_single_file(fname):
    proxy_logins = { "successes": 0, "users": 0, "failures": 0}
    if os.path.exists(fname):
        with open(fname) as f:
            for line in f:
                status = line.split("\t")[1]
                match status:
                    case "Login.Success": 
                        proxy_logins["successes"] += 1
                        proxy_logins["users"] += 1
                    case "Login.Success.Relogin":
                        proxy_logins["successes"] += 1
                    case "Login.Failure":
                        proxy_logins["failures"] += 1
    return proxy_logins

def test_equality(proxy_logins, test_fname):
    test_logins = {"successes": 870, "users": 739, "failures": 270}
    proxy_file = process_single_file(test_fname)
    return test_logins == proxy_file

#print(test_equality(proxy_data, "./test-data/20231101.txt")) # for testing
print(process_single_file(sys.argv[1]))
