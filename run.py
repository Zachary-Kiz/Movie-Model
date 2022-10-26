
from curses.ascii import isdigit
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# Encoding that will store all of your constraints
E = Encoding()



# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"


# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

# Call your variables whatever you want
a = BasicPropositions("a")
b = BasicPropositions("b")   
c = BasicPropositions("c")
d = BasicPropositions("d")
e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    # Add custom constraints by creating formulas with the variables you created. 
    E.add_constraint((a | b) & ~x)
    # Implication
    E.add_constraint(y >> z)
    # Negate a formula
    E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    constraint.add_exactly_one(E, a, b, c)

    return E


import csv

def GetMovies():
    """
    imports movie data from .csv file into python program
    ***NOTE*** .csv file should already be downloaded 

    movie data is organized in a dictionary

    movies = {Series_Title : ('Released_Year', 'Runtime', 'Genre', 'IMDB_Rating', 'Meta_score', 'Gross')}
    """
    filename = open('imdb_top_1000.csv', encoding="utf8")
    file = csv.DictReader(filename)
    
    movies = {}
    
    for col in file:
        movies[col['Series_Title']] = col['Released_Year'], col['Runtime'], col['Genre'], col['IMDB_Rating'], col['Meta_score'], col['Gross']
    
    return movies

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
    print("What quality of movie are you looking for? This program considers IMDB score 0 - 3.9 to be bad, 4 - 6.9 to be average and 7 - 10 to be good")
    customerQual = input( "Enter 1 for a bad movie, 2 for an average movie, or 3 for a good movie. Enter np if you have no preference: ")

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
    customRun = input("Enter 1 for less than 90 mins, 2 for less than 120 mins, 3 for less than 150 mins, 4 for more than 150 mins: ")

    check = ["1","2","3","4", "np"]
    while customRun not in check:
        print("Please enter a valid input")
        customRun = input("Enter 1 for less than 90 mins, 2 for less than 120 mins, 3 for less than 150 mins, 4 for more than 150 mins: ")

    if customRun == "1":
        customerPrefs["runtime"] = "short"
    elif customRun == "2":
        customerPrefs["runtime"] = "average"
    elif customRun == "3":
        customerPrefs["runtime"] = "long"
    elif customRun == "4":
        customerPrefs["runtime"] = "very long"
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
    customerNum = getCustomers()

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
        getPopularity(customerPrefs)
        print()
        getAge(customerPrefs)
        print()
        customerList.append(customerPrefs)
    print(customerList)


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:

    main()

    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
