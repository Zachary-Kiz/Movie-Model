
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
class reccommendMovie:

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
        checkYear = movieStuff[0][0:3] + "0s"
        if checkYear == customerPrefs["age"]:
            E.add_constraint(props[key]["age"])
        else:
            E.add_constraint(~props[key]["age"])
        run = movieStuff[1]
        run = run.split(" ")
        if int(run[0]) <= 120:
            checkRun = "short"
        else:
            checkRun = "long"
        if checkRun == customerPrefs["runtime"]:
            E.add_constraint(props[key]["runtime"])
        else:
            E.add_constraint(~props[key]["runtime"])
        genreList = movieStuff[2].split(",")
        if genreList[0].lower() == customerPrefs["genre(s)"]:
            E.add_constraint(props[key]["genre"])
        else:
            E.add_constraint(~props[key]["genre"])
        score = movieStuff[3]
        if float(score) <= 5:
            check = 'bad'
        else:
            check = 'good'
        if check == customerPrefs["rating"]:
            E.add_constraint(props[key]["rating"])
        else:
            E.add_constraint(~props[key]["rating"])

        E.add_constraint((props[key]["age"] & props[key]["runtime"] & props[key]["genre"] & props[key]["rating"]) >> props[key]["recommend"])
        

        

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
    
    return movies

def setUpProps(movies, customerNum):
    propsDict = {}
    for key in movies.keys():
        movieDict = movies[key]
        year = movieAge(movieDict[0][0:3] + "0s")
        run = movieDict[1]
        run = run.split(" ")
        if int(run[0]) <= 120:
            runtime = movieRun("short")
        else:
            runtime = movieRun("long")
        genreList = movieDict[2].split(",")
        genre = movieGenre(genreList[0].lower())
        if float(movieDict[3]) <= 5.0:
            rating = movieRating("bad")
        else:
            rating = movieRating("good")

        movieRec = reccommendMovie(key)
        propsDict[key] = {"recommend":movieRec, "age": year, "runtime": runtime, "genre": genre, "rating": rating }
    return propsDict
        

def getCustomers():
    '''
    This function is used to get the number of customers who wish to rent a movie
    '''
    customerNum = input("Please enter the number of customers that wish to rent a movie: ")
    while customerNum.isdigit() == False:
        print("Invalid input, please try agian.")
        customerNum = input("Please enter the number of customers that wish to rent a movie: ")
    return int(customerNum)

def getGenres(customerPrefs):
    genreList = ["action", "adventure", "animation", "biography", "comedy", "crime", "drama", 
    "fantasy", "history", "horror", "mystery", "romance", "sci-fi", "thriller", "western" ]

    customGenre = input("Please enter your prefered genre of movie. If you have no preference, enter 'np'. To view the list of genres, enter v.\n")

    while customGenre not in genreList and customGenre != "np" and customGenre != "v":
        print("Input invalid. Please try again.")
        customGenre = input("Please enter your prefered genre of movie. To view the list of genres, enter v:\n")

    if customGenre in genreList:
        customerPrefs["genre(s)"] = customGenre

    elif customGenre == "np":
        customerPrefs["genre(s)"] = "no preference"

    elif customGenre == "v":
        for genre in genreList:
            if genre != "western":
                print(genre + ", ", end="")
            else:
                print(genre)
        print()
        getGenres(customerPrefs)

def getQuality(customerPrefs):
    print("What quality of movie are you looking for? This program considers IMDB score 0 - 5 to be bad, 5.1 - 10.0 to be good")
    customerQual = input( "Enter 1 for a bad movie, 2 for a for a good movie. Enter np if you have no preference: ")

    check = ["1","2","3","np"]

    while customerQual not in check:
        print("Please enter a valid input")
        customerQual = input( "Enter 1 for a bad movie, 2 for an average movie, or 3 for a good movie: ")

    if customerQual == "1":
        customerPrefs["rating"] = "bad"
    elif customerQual == "2":
        customerPrefs["rating"] = "average"
    elif customerQual == "3":
        customerPrefs["rating"] = "good"
    elif customerQual == "np":
        customerPrefs["rating"] = "no preference"

def getRuntime(customerPrefs):
    print("How long do you want the movie to be?")
    customRun = input("Enter 1 for less than 120 mins, 2 for more than 120 mins ")

    check = ["1","2","3","4", "np"]
    while customRun not in check:
        print("Please enter a valid input")
        customRun = input("Enter 1 for less than 120 mins, 2 for more than 120 mins ")

    if customRun == "1":
        customerPrefs["runtime"] = "short"
    elif customRun == "2":
        customerPrefs["runtime"] = "long"
    elif customRun == "np":
        customerPrefs["runtime"] = "no preference"

def getPopularity(customerPrefs):

    print("How popular do you want the movie to be?")
    custPop = input("Enter N for niche, A for average, P for popular: ")

    check = ["N", "A", "P", "np"]
    while custPop not in check:
        print("Please enter a valid input.")
        custPop = input("Enter N for niche, A for average, P for popular: ")

    if custPop == "np":
        customerPrefs["popularity"] = "no preference"
    else:
        customerPrefs["popularity"] = custPop

def getAge(customerPrefs):

    print("How old do you want the movie to be?")
    custMil = input("Enter 1 for a movie made in the 1900s, 2 for a movie made in the 2000s")
    check = ["1","2","np"]

    while custMil not in check:
        print("Please enter a valid input")
        custMil = input("Enter 1 for a movie made in the 1900s, 2 for a movie made in the 2000s: ")

    if custMil == "np":
        customerPrefs["age"] = "no preference"
        return

    custDec = input("Enter 1 for a movie with decade 10s, 2 for 20s, etc. ")
    while int(custDec) < 0 or int(custDec) > 9:
        print("Please enter a valid input")
        custDec = input("Enter 1 for a movie with decade 10s, 2 for 20s, etc. ")

    while custMil == "2" and (int(custDec) < 0 or int(custDec) > 2):
        print("Decade does not exist")
        custDec = input("Enter 1 for a movie with decade 10s, 2 for 20s, etc. ")

    if custMil == "1":
        customerPrefs["age"] = custMil + "9" + custDec + "0s"
    else:
        customerPrefs["age"] = custMil + "0" + custDec + "0s"


def main():
    customerNum = 1

    movies = GetMovies()

    props = setUpProps(movies, customerNum)

    customerList = []

    print("Enter 'np' to any input to indicate no preference")

    for x in range(customerNum):
        customerPrefs = {"genre(s)": "", "rating": "", "runtime": "" , "popularity": "", "age" : ""}
        getGenres(customerPrefs)
        print()
        getQuality(customerPrefs)
        print()
        getRuntime(customerPrefs)
        print()
        #getPopularity(customerPrefs)
        #print()
        getAge(customerPrefs)
        print()
        customerList.append(customerPrefs)

    print(customerPrefs)

    T = example_theory(props, customerPrefs, movies)
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())
    

    


main()