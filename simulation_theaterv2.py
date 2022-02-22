
import simpy
import random
import statistics

# This is creating an empty list called wait_times.
wait_times = []


# Theater is a class that has a name, a location, and a list of movies
# The Theater class is a class that contains a list of movies and a list of customers
class Theater(object):
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        """
        The function creates a simpy.Resource object for each of the three resources (cashier, server, usher) and assigns
        them to the attributes of the class

        :param env: The SimPy environment defined in the previous section
        :param num_cashiers: The number of cashiers that are available to serve customers
        :param num_servers: The number of servers at the movie theater
        :param num_ushers: The number of ushers at the movie theater
        """
        # This is creating a simpy environment object and assigning it to the attribute self.env.
        self.env = env
        # This is creating a simpy resource object and assigning it to the attribute self.cashier.
        self.cashier = simpy.Resource(env, num_cashiers)
        # This is creating a simpy resource object and assigning it to the attribute self.server.
        self.server = simpy.Resource(env, num_servers)
        # This is creating a simpy resource object and assigning it to the attribute self.usher.
        self.usher = simpy.Resource(env, num_ushers)

    def purchase_ticket(self, moviegoer):

        # This is a generator function that yields a random number of seconds between 1 and 3.
        yield self.env.timeout(random.randint(1, 3))

    def check_ticket(self, moviegoer):
        # This is a generator function that yields a random number of seconds between 1 and 3.
        yield self.env.timeout(3 / 60)

    def sell_food(self, moviegoer):
        # This is a generator function that yields a random number of seconds between 1 and 5.
        yield self.env.timeout(random.randint(1, 5))


def go_to_movies(env, moviegoer, theater):
    # Moviegoer arrives at the theater
    arrival_time = env.now

    # This is a context manager that is used to lock the resource.
    with theater.cashier.request() as request:
        # This is a context manager that is used to lock the resource.
        yield request
        # This is a generator function that yields a random number of seconds between 1 and 3.
        yield env.process(theater.purchase_ticket(moviegoer))

    # This is a context manager that is used to lock the resource.
    with theater.usher.request() as request:
        # This is a context manager that is used to lock the resource.
        # This is a generator function that yields a random number of seconds between 1 and 3.
        yield request
        yield env.process(theater.check_ticket(moviegoer))

    # This is a way to randomly select one of two options.
    if random.choice([True, False]):
        # This is a context manager that is used to lock the resource.
        with theater.server.request() as request:
            yield request
            # This is a way to call a process from within another process.
            yield env.process(theater.sell_food(moviegoer))

    # Moviegoer heads into the theater
    wait_times.append(env.now - arrival_time)


def run_theater(env, num_cashiers, num_servers, num_ushers):
    """
    Create a theater object, then create 3 moviegoers to use the theater

    :param env: The SimPy environment
    :param num_cashiers: The number of cashiers working the ticket counter
    :param num_servers: The number of servers in the service area
    :param num_ushers: The number of ushers working the theater
    """

    # It creates a theater object with the parameters passed in.
    theater = Theater(env, num_cashiers, num_servers, num_ushers)

    # Creating random number between 1-3 moviegoers.
    for moviegoer in range(30):
        # This is a way to call a process from within another process.
        env.process(go_to_movies(env, moviegoer, theater))

    while True:
        # This is a way to call a process from within another process.
        yield env.timeout(0.20)  # Wait a bit before generating a new person

        # This is incrementing the moviegoer variable by 1.
        moviegoer += 1
        # This is a way to call a process from within another process.
        env.process(go_to_movies(env, moviegoer, theater))


def calculate_average_wait_time(wait_times):
    """
    Calculate the average wait time

    :param wait_times: a list of wait times (in minutes)
    :return: The average wait time in minutes and seconds.
    """

    # This is calculating the average wait time by taking the mean of the wait times list.
    average_wait = statistics.mean(wait_times)

    # Dividing the average wait time by 1 minute and getting the remainder.
    minutes, frac_minutes = divmod(average_wait, 1)
    # This is converting the fraction of a minute into an actual number of seconds.
    seconds = frac_minutes * 60
    # This is returning the rounded minutes and seconds to the main function.
    return round(minutes), round(seconds)


def get_user_input():
    """
    Get user input and check if it's valid
    :return: A list of the number of cashiers, servers, and ushers.
    """

    # This is getting user input and checking if it's valid . If it's not valid, it will use the default value of 1.
    num_cashiers = input("Input the number of working cashiers: ")
    num_servers = input("Input the number of working servers: ")
    num_ushers = input("Input the number of working ushers: ")
    # This is getting the user input and checking if it's valid. If it's not valid, it will use the default value of 1.
    params = [num_cashiers, num_servers, num_ushers]
    # This is checking if the input is valid. If it's not valid, it will use the default value of 1.
    if all(str(i).isdigit() for i in params):  # Check input is valid
        # This is checking if the input is valid. If it's not valid, it will use the default value of 1.
        params = [int(x) for x in params]
    else:
        print(
            "Could not parse input. The simulation will use default values:",
            "\n1 cashier, 1 server, 1 usher.",
        )
        # This is setting the default values for the number of cashiers, servers, and ushers.
        params = [1, 1, 1]
    # This is returning the parameters to the main function.
    return params


def main():
    """
    Create an environment, run the simulation, and print the results
    """
    # Setup
    # This is setting the random seed to 42. This is so that the random number generator will generate the same
    #         random numbers each time the program is run.
    random.seed(42)
    # This is getting the user input and checking if it's valid. If it's not valid, it will use the default value of 1.
    num_cashiers, num_servers, num_ushers = get_user_input()

    # Run the simulation
    # This is creating a simpy environment object and assigning it to the attribute self.env.
    env = simpy.Environment()
    # This is creating a simpy environment object and assigning it to the attribute self.env.
    env.process(run_theater(env, num_cashiers, num_servers, num_ushers))
    # This is running the simulation for 90 minutes.
    env.run(until=90)

    # View the results
    # This is calculating the average wait time by taking the mean of the wait times list.
    mins, secs = calculate_average_wait_time(wait_times)
    print(
        "Running simulation...",
        f"\nThe average wait time is {mins} minutes and {secs} seconds.",
    )


if __name__ == '__main__':
    main()