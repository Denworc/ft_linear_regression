import os
import sys


def get_theta(l):
    return float(l[0]), float(l[1])


def estimate(theta0, theta1, mileage):
    return int(theta0 + (theta1 * mileage))


def main():
    try:
        mileage = float(input("Enter a mileage: "))
    except:
        print("Error: Invalid mileage!")
        sys.exit()
    if os.path.isfile("theta.txt"):
        f = open("theta.txt", 'r')
        if os.path.getsize("theta.txt") > 0:
            l = [line.strip() for line in f]
        else:
            f.close()
            print('Error: File "theta.txt" is empty.')
            sys.exit()
        f.close()
        try:
            theta0, theta1 = get_theta(l)
        except:
            print('Error: File "theta.txt" is invalid.')
            sys.exit()
    else:
        theta0, theta1 = 0, 0
    estimate(theta0, theta1, mileage)
    print("Price:", estimate(theta0, theta1, mileage))


if __name__ == '__main__':
    main()
