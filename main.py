import re
import random
from typing import Dict, List
import functools

# This stores the raw colors
raw_colors = []
color_count: Dict[str, int] = dict()
with open("python_class_question.html", 'r') as file:
    # We go line by line
    for line in file:
        # We use regular expression to get where the table data (<td>) is stored on the line
        table_data = re.search(r"<td>.+</td>", line)
        if table_data:
            # Find the span of the match
            (start, stop) = table_data.span()

            # To remove the <td> and </td> respectively
            start += 4
            stop -= 5

            # Check it's a day that is stored
            # If it is, we skip it
            if stop - start < 20:
                continue

            # Split all the colors and then add them to the `color_count` dictionary
            # and then update the count if it repeats
            for color in line[start:stop].split(", "):
                raw_colors.append(color)
                if color in color_count:
                    color_count[color] += 1
                else:
                    color_count[color] = 1


# Since the data is categorical and not numerical
# The mean should be the color that is worn the most on average
# So in that case, it can be seen as the color that has the highest probabilty of being worn
# So we calculate that probability for every color and then return the color with the highest one
def find_mean():
    values = color_count.values()
    # Calculate the probabiltiy of a person wearing the color in a week
    prob_colors = [value / len(raw_colors) for value in values]

    # Get the index of the maximum probability
    max_index = prob_colors.index(max(prob_colors))

    # Get the color that corresponds to the maximum probability
    result = list(color_count.keys())[max_index]

    # Return that as the mean
    return result


# This function finds the color that was worn the maximum number of times
def find_max():
    maximum = ("", 0)
    for key in color_count:
        value = color_count[key]
        if value > maximum[1]:
            maximum = (key, value)
    return maximum[0]


# This finds the middle element to the sorted array of raw_colors
def find_median():
    sorted_array = sorted(raw_colors)
    return sorted_array[int(len(sorted_array) / 2)]


# To find the varaiance we have to calculate how far each color is from the mean,
# square it and then divide it by the total number of colors
# Since the colors don't have numerical values, we try to sort the color_count dictionary
# and then try to find the how far the index of the mean is from the index of a particular color
def find_variance():
    # Sort the map and create a new map
    sorted_colors = {color: frequency for color, frequency in sorted(
        color_count.items(), key=lambda x: x[0])}

    # Get the mean
    mean = find_mean()

    # Get a list of all the keys in the map
    keys = list(sorted_colors.keys())
    # Find which index the mean is in
    mean_index = keys.index(mean)

    # Create an accumulator
    sum_distance = 0
    for index, key in enumerate(keys):
        # Calculate the distance from the mean, square it and then multiply it by frequency
        sum_distance += ((index - mean_index)**2) * sorted_colors[key]

    # Calculate the variance and then return it
    return sum_distance/len(raw_colors)


# To find the probability that someone would wear red would be
# just taking the frequency of red shirts and dividing it by the total frequncy of all shirts
def prob_red():
    return color_count["RED"]/len(raw_colors)


# This function gets a connection to the Postgres database and then returns it
# It loads the information needed from the a .env file
def get_connection():
    from dotenv import load_dotenv, find_dotenv
    from os.path import exists
    dotenv_path = find_dotenv()
    if not exists(dotenv_path):
        print("Please create a .env file with the following variables")
        print("DATABASE, USER, PASSWORD, HOST and PORT")
        return False

    import os
    import psycopg2

    load_dotenv(dotenv_path)

    databse = os.environ.get("DATABASE")
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")
    try:
        return psycopg2.connect(
            database=databse,
            user=user,
            password=password,
            host=host,
            port=port
        )
    except Exception as e:
        print("Error occured", e)
        print("Check if the following variables are defined in the .env file")
        print("DATABASE, USER, PASSWORD, HOST and PORT")
        return False


# This loads the color data into a Postgres database
# It saves it in a table called `color_count`
def load_into_postgres():
    connection = get_connection()
    if not connection:
        print("could not create the connection")
        return
    try:
        # Get a cursor
        cursor = connection.cursor()

        # Create the table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS color_count (
                color TEXT PRIMARY KEY,
                frequency INT
            );
        """)

        # Insert all the colors in the color_count dictionary into the table
        sql = "INSERT INTO color_count (color, frequency) VALUES (%s, %s);"
        colors = list(map(lambda x: (x[0], str(x[1])), color_count.items()))
        for color, frequency in colors:
            cursor.execute(sql, (color, frequency,),)

        connection.commit()

        cursor.close()
    except Exception as e:
        print("Error Occured:", e)
    finally:
        connection.close()


# This is a recursive implementation of linear search
# Linear search just goes from index to index checking if the target value is that
# If it is, it then returns the index
def linear_search(array, target, index=0):
    if index >= len(array):
        return -1
    if array[index] != target:
        return linear_search(array, target, index + 1)
    return index


# This function asks the user for the numbers that are meant to be in a list and then
# performs linear search on it
def list_of_numbers():
    numbers = []
    length = int(input("Enter how many numbers you want: "))

    # Get all the numbers from the user
    for i in range(length):
        number = int(input(f"Enter number {i + 1}: "))
        numbers.append(number)
    print()

    target = int(input("Enter the number that you want to search for: "))
    index = linear_search(numbers, target)
    print(f"The index of {target} is {index}")


# This function generates a number that have 4 digits that have a random number of 1s and 0s
def random_1_or_0():
    result_str = ""
    for _ in range(4):
        result_str += random.choice(["0", "1"])

    print("The resulting string is", result_str)

    return int(result_str)


# Recursive implementation of the Fibonnacci function
# We use a cache so that we don't have to recompute any values that we have already calculated
def fib(n, cache):
    if n in cache:
        return cache[n]
    cache[n] = fib(n-1, cache) + fib(n-2, cache)
    return cache[n]


# This finds the sum of the first 50 fibonnaci numbers
# The plan is to fill up the cache with those numbers and then find the sum of the values
def sum_of_fib():
    cache = {0: 0, 1: 1}
    # To fill the cache up with 50 values
    fib(50, cache)
    return sum(cache.values())


# Simple UI for selecting a question to solve
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
                print("The mean color is", mean)
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
                print("Done loading datat into the postgres database")
            case 7:
                list_of_numbers()
            case 8:
                print("So therefore the random number is", random_1_or_0())
            case 9:
                print("The sum of the first 50 fibbonaci number is", sum_of_fib())
            case _:
                print("Unrecognized question number:", question_number)
                print("Please choose a number between 1 to 9")


main()
