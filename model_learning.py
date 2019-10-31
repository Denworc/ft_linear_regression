import os
import sys
from math import sqrt
import matplotlib.pyplot as plt


def estimate(theta0, theta1, mileage):
    return theta0 + (theta1 * mileage)


def learn_model(price, mileage, m, rate):
    theta0, theta1 = 0.0, 0.0
    for c in range(500):
        sum_theta0, sum_theta1 = 0, 0
        for i in range(m):
            sum_theta0 += (estimate(theta0, theta1, mileage[i]) - price[i])
            sum_theta1 += ((estimate(theta0, theta1, mileage[i]) - price[i]) * mileage[i])
        theta0 -= sum_theta0 * rate / m
        theta1 -= sum_theta1 * rate / m
        l1, l2 = [], []
        l1.append(theta0)
        l2.append(theta1)
        plt.figure(3)
        plt.plot(l1, l2, 'o')
        plt.title("")
    return theta0, theta1


def get_mean(list):
    return sum(list) / len(list)


def get_std(list):
    res = 0
    mean = get_mean(list)
    for elem in list:
        res += (elem - mean) ** 2
    return sqrt(res / len(list))


def to_standart(list):
    res = []
    for elem in list:
        res.append((elem - get_mean(list)) / get_std(list))
    return res


def rev(li, norm):
    res = []
    for elem in li:
        res.append(elem * get_std(norm) + get_mean(norm))
    return res


def parse_file(l):
    price = []
    mileage = []
    rate = 0.4
    try:
        for line in l[1:]:
            price.append(float(line.split(',', 1)[1]))
            mileage.append(float(line.split(',', 1)[0]))
    except:
        print('Error: Incorrect "data.csv" file')
        sys.exit()
    m = len(price)
    if m < 2:
        print('Error: Need more examples for learning.')
        sys.exit()
    norm_price = to_standart(price)
    norm_mileage = to_standart(mileage)
    theta0, theta1 = learn_model(norm_price, norm_mileage, m, rate)
    calc_price = []
    for elem in norm_mileage:
        calc_price.append(estimate(theta0, theta1, elem))
    res_theta0 = (estimate(theta0, theta1, (0 - get_mean(mileage)) / get_std(mileage)) * get_std(price) + get_mean(price))
    res_theta1 = (price[0] - res_theta0) / mileage[0]
    f = open("theta.txt", 'w')
    f.write(str(res_theta0) + "\n" + str(res_theta1))
    f.close()
    res_price = rev(calc_price, price)
    res_sum = 0
    for i in range(len(price)):
        res_sum += (price[i] - res_price[i]) ** 2
    mse = sqrt(res_sum / len(price))
    print("Mean squared error =", mse)
    plt.figure(2)
    plt.plot(norm_mileage, norm_price, 'o')
    plt.title("Distribution of the standardized data")
    plt.figure(1)
    plt.plot(mileage, price, 'o')
    plt.plot(mileage, rev(calc_price, price))
    plt.ylabel("Price")
    plt.xlabel("Mileage, Km")
    plt.title("Distribution of the data + learning results")
    plt.show()


def main():
    if os.path.isfile("data.csv"):
        f = open("data.csv", 'r')
        if os.path.getsize("data.csv") > 0:
            l = [line.strip() for line in f]
        else:
            f.close()
            sys.exit()
        f.close()
        parse_file(l)
    else:
        print('Error: File "data.csv" not found, try again')
        sys.exit()


if __name__ == '__main__':
    main()
