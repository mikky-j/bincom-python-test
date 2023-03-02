import re
import random
from typing import Dict, List
import functools

raw_colors = []
color_count: Dict[str, int] = dict()
with open("python_class_question.html", 'r') as file:
    for line in file:
        x = re.search(r"<td>.+</td>", line)
        if x:
            (start, stop) = x.span()

            # To remove the <td> and </td> respectively
            start += 4
            stop -= 5

            # Check it's a day that is stored
            if stop - start < 20:
                continue

            for value in line[start:stop].split(", "):
                raw_colors.append(value)
                if value in color_count:
                    color_count[value] += 1
                else:
                    color_count[value] = 1


def find_mean():
    values = color_count.values()
    return sum([index * value for index, value in enumerate(values)]) / sum(values)


def find_max():
    maximum = ("", 0)
    for key in color_count:
        value = color_count[key]
        if value > maximum[1]:
            maximum = (key, value)
    return maximum[0]


def find_median():
    return raw_colors[int(len(raw_colors)/2)]


def find_variance():
    mean = find_mean()
    return 1/len(raw_colors) * sum([value * ((index - mean)**2) for index, value in enumerate(color_count.values())])


def prob_red():
    print(color_count["RED"]/len(raw_colors))


def get_connection():
    from os.path import exists
    if not exists(".env"):
        print("Please create a .env file with the following variables")
        print("DATABASE, USER, PASSWORD, HOST and PORT")
        return False

    from dotenv import load_dotenv, find_dotenv
    import os
    import psycopg2

    load_dotenv(find_dotenv())

    databse = os.environ.get("DATABASE")
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")

    try:
        return psycopg2.connect(
            databse=databse,
            user=user,
            password=password,
            host=host,
            port=port
        )
    except:
        print("Check if the following variables are defined in the .env file")
        print("DATABASE, USER, PASSWORD, HOST and PORT")
        return False


def load_into_postgres():
    connection = get_connection()
    if not connection:
        print("could not create the connection")
        return
    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS color_count (
                color TEXT PRIMARY KEY,
                frequency INT
            );
        """)

        sql = "INSERT INTO color_count (color, frequency) VALUES (%s, %s)"
        cursor.execute(sql, color_count.items())

        cursor.commit()

        cursor.close()
    except e:
        print("Error Occured:", e)
    finally:
        connection.close()


def linear_search(array, target, index=0):
    if index >= len(array):
        return -1
    if array[index] != target:
        return linear_search(array, target, index + 1)
    return index


def list_of_numbers():
    numbers = []
    length = int(input("Enter how many numbers you want: "))
    for i in range(length):
        number = int(input(f"Enter number {i + 1}: "))
        numbers.append(number)
    print()
    target = int(input("Enter the number that you want to search for: "))
    index = linear_search(numbers, target)
    print(f"The index of {target} is {index}")


def random_1_or_0():
    result = 0
    for power in range(3, -1, -1):
        result += random.choice([0, 1]) * (10 ** power)
    return result


def fib(n, cache):
    if n in cache:
        return cache[n]
    cache[n] = fib(n-1, cache) + fib(n-2, cache)
    return cache[n]


def sum_of_fib():
    cache = {0: 0, 1: 1}
    # To fill the cache up with 50 values
    fib(50, cache)
    return sum(cache.values())


def main():
    print("Welcome to the challenge solution for the Bincom Test\n")
    while True:
        user_input = input(
            "Enter the question that you want to solve (type \"exit\" to quit): ")
        if user_input.lower() == "exit":
            print("Thank you for using this tool")
            break
        question_number = int(user_input)
        match question_number:
            case 1:
                mean = find_mean()
                print("The mean color is", list(
                    color_count.values())[int(mean)])
            case 2:
                print("The color that was worn the most is", find_max())
            case 3:
                print("The median color is", find_median())
            case 4:
                print("The variance of the colors is", find_variance())
            case 5:
                print("The probability of choosing the red color is", prob_red())
            case 6:
                print("Loading data into the postgres database")
                load_into_postgres()
            case 7:
                list_of_numbers()
            case 8:
                print("The random number is", random_1_or_0())
            case 9:
                print("The sum of the first 50 fibbonaci number is", sum_of_fib())
            case _:
                print("Unrecognized question number:", question_number)
                print("Please choose a number between 1 to 9")


main()
