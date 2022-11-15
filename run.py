
from curses.ascii import isdigit
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# Encoding that will store all of your constraints
E = Encoding()



# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding

@proposition(E)
class movieAge:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

@proposition(E)
class movieRun:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"R.{self.data}"

@proposition(E)
class movieGenre:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"G.{self.data}"

@proposition(E)
class movieRating:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"I.{self.data}"

@proposition(E)

class moviePopularity:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"P.{self.data}"

@proposition(E)

class movieCertificate:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"C.{self.data}"

@proposition(E)
class recommendMovie:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"{self.data}"



# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html

# Call your variables whatever you want

# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory(props, customerPrefs, movies):
    for key in movies.keys():
        movieStuff = movies[key]
        checkYear = movieStuff[0]
        if checkYear == customerPrefs["age"]:
            E.add_constraint(props[key]["age"])
        else:
            E.add_constraint(~props[key]["age"])

        run = movieStuff[2]
        if int(run) <= 120:
            checkRun = "short"
        else:
            checkRun = "long"

        if checkRun == customerPrefs["runtime"]:
            E.add_constraint(props[key]["runtime"])
        else:
            E.add_constraint(~props[key]["runtime"])
        genreList = movieStuff[3]
        print(genreList, customerPrefs["genre"])
        if genreList == customerPrefs["genre"]:
            E.add_constraint(props[key]["genre"])
        else:
            E.add_constraint(~props[key]["genre"])

        score = movieStuff[4]
        if float(score) >= float(customerPrefs["rating"]):
            E.add_constraint(props[key]["rating"])
        else:
            E.add_constraint(~props[key]["rating"])

        certificate = movieStuff[1]
        if certificate == customerPrefs["certificate"]:
            E.add_constraint(props[key]["certificate"])
        else:
            E.add_constraint(~props[key]["certificate"])
        
        E.add_constraint(~props[key]["age"] >> ~props[key]["recommend"])
        E.add_constraint(~props[key]["runtime"] >> ~props[key]["recommend"])
        E.add_constraint(~props[key]["genre"] >> ~props[key]["recommend"])
        E.add_constraint(~props[key]["rating"] >> ~props[key]["recommend"])
        E.add_constraint(~props[key]["certificate"] >> ~props[key]["recommend"])
        E.add_constraint((props[key]["age"] & props[key]["runtime"] & props[key]["genre"] & props[key]["rating"] & props[key]["certificate"]) >> props[key]["recommend"])
    
    return E


import csv

def GetMovies():
    """
    imports movie data from .csv file into python program
    ***NOTE*** .csv file should already be downloaded 

    movie data is organized in a dictionary

    movies = {Series_Title : ('Released_Year', 'Certificate', 'Runtime', 'Genre', 'IMDB_Rating', 'Meta_score', 'Gross')}
    """
    filename = open('imdb_top_1000.csv', encoding="utf8")
    file = csv.DictReader(filename)
    
    movies = {}
    
    for col in file:
        movies[col['Series_Title']] = col['Released_Year'], col['Certificate'], col['Runtime'], col['Genre'], col['IMDB_Rating'], col['Meta_score'], col['Gross']

    
    # Make movies easier to compare with customer preferences
    movieDict = {}
    for key in movies.keys():
        movieList = []
        movieList.append(movies[key][0][0:3] + "0s")
        movieList.append(movies[key][1])
        run = movies[key][2].split(" ")
        movieList.append(run[0])
        genreList = movies[key][3].split(",")
        if (len(genreList) > 3):
            movieList.append(genreList.lower())
        else:
            movieList.append(genreList[0].lower())
        movieList.append(movies[key][4])
        movieList.append(movies[key][6])
        movieDict[key] = movieList

    print(movieDict)
    return movieDict

def setUpProps(movies, customerNum):
    propsDict = {}
    for key in movies.keys():
        movieDict = movies[key]
        year = movieAge(movieDict[0])
        run = movieDict[2]
        if int(run) <= 120:
            runtime = movieRun("short")
        else:
            runtime = movieRun("long")
        genreList = movieDict[3]
        genre = movieGenre(genreList)
        if float(movieDict[4]) <= 5.0:
            rating = movieRating("bad")
        else:
            rating = movieRating("good")
        certificate = movieCertificate(movieDict[1])

        movieRec = recommendMovie(key)
        propsDict[key] = {"recommend": movieRec, "age": year, "runtime": runtime, "genre": genre, "rating": rating, "certificate": certificate}
    return propsDict
        

def getCustomers():
    '''
    This function is used to get the number of customers who wish to rent a movie
    Returns an integer value representing the number of customers
    '''
    customerNum = input("Please enter the number of customers that wish to rent a movie: ")
    while customerNum.isdigit() == False or int(customerNum) <= 0:
        print("Invalid input, please try again.")
        customerNum = input("Please enter the number of customers that wish to rent a movie: ")
    return int(customerNum)

def getGenres(customerPrefs):
    """
    This function is used to get the customer's prefered genre of movie and add it to the
    customer dictionary
    Parameters: customerPrefs - dictionary of customer movie preferences
    """

    # Initialize list of movie genres
    genreList = ["action", "adventure", "animation", "biography", "comedy", "crime", "drama", 
    "fantasy", "history", "horror", "mystery", "romance", "sci-fi", "thriller", "western" ]

    # Get customer's prefered genre of movie
    customGenre = input("Please enter your prefered genre of movie. To view the list of genres, enter v.\n")

    # Check that input is valid
    while customGenre not in genreList and customGenre != "np" and customGenre != "v":
        print("Input invalid. Please try again.")
        customGenre = input("Please enter your prefered genre of movie. To view the list of genres, enter v:\n")

    # Add customers choice to customerPrefs
    if customGenre in genreList:
        customerPrefs["genre"] = customGenre

    elif customGenre == "np":
        customerPrefs["genre"] = "no preference"

    # Print list of genres if customer chooses this option
    elif customGenre == "v":
        for genre in genreList:
            if genre != "western":
                print(genre + ", ", end="")
            else:
                print(genre)
        print()
        getGenres(customerPrefs)



def getQuality(customerPrefs):
    """
    This function prompts the customer what quality of movie they want. Whether a movie is good or not is 
    determined by IMDB scores
    Parameters: customerPrefs - dictionary of the customer's movie preferences
    """
    # Prompt the customer on what quality of movie they are looking for
    print("What quality of movie are you looking for? This program uses IMDB scores to determine quality")
    customerQual = input( "Enter a number from 0-9 to indicate the minimum level of quality: ")

    check = ["0","1","2","3","4","5","6","7","8","9","np"]

    # Check that input is valid
    while customerQual not in check:
        print("Please enter a valid input")
        customerQual = input("Enter a number from 0-9 to indicate the minimum level of quality: ")

    # Add customer preference to dictionary customerPrefs
    if customerQual == "np":
        customerPrefs["rating"] = "no preference"
    else:
        customerPrefs["rating"] = customerQual

def getRuntime(customerPrefs):
    """
    This function prompts the user for their prefered movie runtime
    Parameters: customerPrefs - dictionary of the customer's movie preferences
    """
    # Prompt customer for prefered movie runtime
    print("How long do you want the movie to be?")
    customRun = input("Enter 1 for less than 120 mins, 2 for more than 120 mins ")

    # Check if input is valid
    check = ["1","2","3","4", "np"]
    while customRun not in check:
        print("Please enter a valid input")
        customRun = input("Enter 1 for less than 120 mins, 2 for more than 120 mins ")

    # Add customer preference to dictionary customerPrefs
    if customRun == "1":
        customerPrefs["runtime"] = "short"
    elif customRun == "2":
        customerPrefs["runtime"] = "long"
    elif customRun == "np":
        customerPrefs["runtime"] = "no preference"

def getPopularity(customerPrefs):
    """
    This movie prompts the user for how popular they want the movie to be
    Popularity is decided based on box office results
    Parameters: customerPrefs - dictionary of the customer's movie preferences
    """

    # Prompt customer for their preference
    print("How popular do you want the movie to be?")
    custPop = input("Enter N for niche, A for average, P for popular: ")

    # Check if input is valid
    check = ["N", "A", "P", "np"]
    while custPop not in check:
        print("Please enter a valid input.")
        custPop = input("Enter N for niche, A for average, P for popular: ")

    # Add preference to dictionary customerPrefs
    if custPop == "np":
        customerPrefs["popularity"] = "no preference"
    else:
        customerPrefs["popularity"] = custPop

def getAge(customerPrefs):
    """
    This function prompts the user for their prefered decade of movie
    Parameters: customerPrefs - dictionary of the customer's movie preferences
    """
    # Prompt user for their prefered millenium of movie
    print("How old do you want the movie to be?")
    custMil = input("Enter 1 for a movie made in the 1900s, 2 for a movie made in the 2000s")
    check = ["1","2","np"]

    # Check if input is valid
    while custMil not in check:
        print("Please enter a valid input")
        custMil = input("Enter 1 for a movie made in the 1900s, 2 for a movie made in the 2000s: ")

    # If customer has no preference, add it to dictionary and end function
    if custMil == "np":
        customerPrefs["age"] = "no preference"
        return

    # Prompt user for prefered decade of movie
    custDec = input("Enter 1 for a movie with decade 10s, 2 for 20s, etc. ")

    # Check that inputs are valid
    while int(custDec) < 0 or int(custDec) > 9:
        print("Please enter a valid input")
        custDec = input("Enter 1 for a movie with decade 10s, 2 for 20s, etc. ")

    while custMil == "2" and (int(custDec) < 0 or int(custDec) > 2):
        print("Decade does not exist")
        custDec = input("Enter 1 for a movie with decade 10s, 2 for 20s, etc. ")

    # Add customer preference to dictionary customerPrefs
    if custMil == "1":
        customerPrefs["age"] = custMil + "9" + custDec + "0s"
    else:
        customerPrefs["age"] = custMil + "0" + custDec + "0s"

def getCertificate(customerPrefs):

    #Create a list of certificate details
    certificateList = ["U - Unrestricted Public Exhibition", 
    "U/A - Parental Guidance Suggested", 
    "PG-13 - Parents Strongly Cautioned", 
    "R - Restricted", 
    "A - Restricted to adults"]

    # Initialize list of movie certificates
    check = ["U", "U/A", "PG-13", "A", "R", "np"]

    # Get customer's prefered movie certificate
    custCer = input("Please enter your prefered movie certificate. To view the list of certificates, enter v.\n")

    # Check that input is valid
    while custCer not in check and custCer != "np" and custCer != "v":
        print("Please enter a valid input.")
        custCer = input("Please enter your prefered movie certificate. To view the list of certificates, enter v.\n")

    # Add customers choice to customerPrefs
    if custCer == "np":
        customerPrefs["certificate"] = "no preference"
    elif custCer in check:
        customerPrefs["certificate"] = custCer

    # Print certificate details if customer chooses this option
    elif custCer == "v":
        for certificate in certificateList:
                print(certificate)
                print()
        getCertificate()


def main():
    # Get number of customers
    customerNum = getCustomers()

    # Put movies in dictionary
    movies = GetMovies()

    #Set up movie propositions
    props = setUpProps(movies, customerNum)

    # Initialize list of customer decisions
    customerList = []

    print("Enter 'np' to any input to indicate no preference")

    # For each customer create a dictionary of their preferences and add it to customerList
    for x in range(customerNum):
        customerPrefs = {"genre": "", "rating": "", "runtime": "" , "popularity": "", "age" : "", "certificate": ""}
        getGenres(customerPrefs)
        print()
        getQuality(customerPrefs)
        print()
        getRuntime(customerPrefs)
        print()
        getPopularity(customerPrefs)
        print()
        getAge(customerPrefs)
        print()
        getCertificate(customerPrefs)
        print()
        customerList.append(customerPrefs)

    print(customerPrefs)

    T = example_theory(props, customerPrefs, movies)
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    # print("\nSatisfiable: %s" % T.is_satisfiable())
    #print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())
    
    

    


main()
