
from curses.ascii import isdigit
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
import sys

sys.setrecursionlimit(10000)

# Encoding that will store all of your constraints
E = Encoding()

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

    def __init__(self, customer, name):
        self.data = customer
        self.name = name

    def __repr__(self):
        return f"{self.data} = {self.name}"

@proposition(E)
class customerPref:
    def __init__(self, num, pref):
        self.num = num
        self.pref = pref
    
    def __repr__(self):
        return f"Cust{self.num}.{self.pref}"



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
    x= 1
    for col in file:
        movies[col['Series_Title']] = col['Released_Year'], col['Certificate'], col['Runtime'], col['Genre'], col['IMDB_Rating'], col['Meta_score'], col['Gross']
        # Set x to however many movies you wish to include in the model
        # Using all 1000 with more than one customer can be slow
        if x == 100:
            break
        x+=1
        
    # Make movies easier to compare with customer preferences
    movieDict = {}
    count = 0
    for key in movies.keys():
        movieList = []
        movieList.append(movies[key][0][0:3] + "0s")
        certificate = movies[key][1]
        if certificate == "":
            certificate = "U"
        elif certificate == "TV-14" or certificate == "16":
            certificate = "AA-14"
        movieList.append(certificate)
        run = movies[key][2].split(" ")
        movieList.append(run[0])
        genreList = movies[key][3].split(",")
        if (len(genreList) > 3):
            movieList.append(genreList.lower())
        else:
            movieList.append(genreList[0].lower())
        movieList.append(movies[key][4])
        gross = movies[key][6]
        gross = gross.split(",")
        check = ""
        for val in gross:
            check += val
        gross = check
        if gross == "":
            gross = "N"
        elif int(gross) < 50000000:
            gross = "N"
        elif int(gross) < 100000000:
            gross = 'A'
        else:
            gross = 'P'
        movieList.append(gross)

        movieDict[key] = movieList


    return movieDict

def setUpProps(movies, customerNum):
    """
    This function is used to create the propositions for each movie
    Parameters: movies - dictionary represeting aspects of a list of movies
                customerNum - int value representing number of customers
    """
    
    # Iterate through movies and store propositions in dictionary
    allProps = {}
    for x in range(customerNum):
        # Create dictionary for propositions
        propsDict = {}
        for key in movies.keys():
            movieDict = movies[key]
            # Check if movie is short or long
            year = movieAge(movieDict[0])
            run = movieDict[2]
            # Create proposition
            if int(run) <= 120:
                runtime = movieRun("short")
            else:
                runtime = movieRun("long")

            # Get popularity from box office results
            pop = movieDict[5]
            pop = pop.split(",")
            check = ""
            for val in pop:
                check += str(val)
            
            pop = check
            popularity = moviePopularity(pop)

            # Create propositions for movie's genre, IMDB rating, rating, and whether movie is rented
            genreList = movieDict[3]
            genre = movieGenre(genreList)
            rating = movieRating(movieDict[4])
            certificate = movieCertificate(movieDict[1])
            movieRec = recommendMovie(x+1,key)
            propsDict[key] = {"recommend": movieRec, "age": year, "runtime": runtime, "genre": genre, "rating": rating, "certificate": certificate, "popularity": popularity }
        allProps[x+1] = propsDict
    

    return allProps

def customerProps():
    """
    This function is used to set up the set of propositions that represent the customer's preferences
    Return Value: custDict - a dictionary of propostions representing the customer's preferences
    """

    allDict = {}
    for n in range(customerNum):
        num = n + 1

        # Create dictionary
        custDict = {}

        # Create propositions for each genre
        genreList = ["action", "adventure", "animation", "biography", "comedy", "crime", "drama", 
        "fantasy", "history", "horror", "mystery", "romance", "sci-fi", "thriller", "western" ]
        custGenres = []
        for genre in genreList:
            custGen = customerPref(num,genre)
            custGenres.append(custGen)
        custDict["genre"] = custGenres

        # Create propositions for each IMDB score
        custScores = []
        for x in range(10):
            if x >= 7:
                custScore = customerPref(num,x)
                custScores.append(custScore)
        custDict["rating"] = custScores

        # Create propositions for each decade
        custAge = []
        for x in range(2):
            for y in range(10):
                mil = x+1
                if mil == 2 and y >= 3:
                    break
                if mil == 1:
                    custTime = customerPref(num, str(mil) + "9" + str(y) + "0s")
                    custAge.append(custTime)
                else:
                    custTime = customerPref(num, str(mil) + "0" + str(y) + "0s")
                    custAge.append(custTime)
        custDict["age"] = custAge

        # Create props for movie lengths
        short = customerPref(num, "short")
        long = customerPref(num, "long")
        custDict["runtime"] = [short,long]

        # Create props for each rating
        certList = ["U", "UA","G", "PG", "PG-13", "AA-14", "TV-14", "TV-MA", "Passed", "A", "R"]
        custCert = []
        for cert in certList:
            custProp = customerPref(num, str(cert))
            custCert.append(custProp)
        custDict["certificate"] = custCert
        N = customerPref(num, "N")
        A = customerPref(num, "A")
        P = customerPref(num, "P")

        custDict["popularity"] = [N,A,P]

        allDict[num] = custDict
    

    return allDict


        



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
    customerQual = input( "Enter a number from 7-9 to indicate the minimum level of quality: ")

    check = ["7","8","9","np"]

    # Check that input is valid
    while customerQual not in check:
        print("Please enter a valid input")
        customerQual = input("Enter a number from 7-9 to indicate the minimum level of quality: ")

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
    custMil = input("Enter 1 for a movie made in the 1900s, 2 for a movie made in the 2000s: ")
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
    "G - Appropriate for all ages",
    "PG - Parents Cautioned",
    "PG-13 - Parents Strongly Cautioned", 
    "AA-14 - Parents Strongly Cautioned",
    "TV-MA - Mature Audiences Only",
    "R - Restricted", 
    "Passed - Approved by the Code",
    "A - Restricted to adults"]

    # Initialize list of movie certificates
    check = ["U", "UA", "G", "PG", "PG-13", "AA-14", "TV-MA", "A", "Passed", "R", "np"]

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
        getCertificate(customerPrefs)




def example_theory(props,customerNum, movies,choices, customerList):

    # Test movie props by negating the ones the user specified
    if choices[0] == "m":
        for key in movies.keys():
            movieVer = []
            for x in range(customerNum):
                movieVer.append(props[x+1][key][choices[1]])
            constraint.add_none_of(E, movieVer)

    
    for x in range(customerNum):

        # Set up customer props
        num = x + 1
        allPrefs = ["genre",'rating','age','runtime','certificate', 'popularity']
        if customerList[0]["genre"] == "":
            for pref in allPrefs:
                # If user wants to test customer constraints they can set one type of preference to
                # always be false
                if pref == choices[1] and choices[0] == "c":
                    constraint.add_none_of(E, custProps[num][pref])
                else:
                    # Only one customer prop is true for each preference type (genre, rating, etc.)
                    constraint.add_exactly_one(E, custProps[num][pref])
        else:
            for pref in allPrefs:
                for custPref in custProps[num][pref]:
                    
                    if str(custPref.pref) == customerList[x][pref] or customerList[x][pref] == "no preference":
                        E.add_constraint(custPref)
                    else:
                        E.add_constraint(~custPref)

        for key in movies.keys():
            for prop in custProps[num]["genre"]:
                movie = movies[key][3]

                # Set up movie genre props
                if str(prop.pref) == movie:
                    E.add_constraint(prop >> props[num][key]["genre"])
                    E.add_constraint(~prop >> ~props[num][key]["genre"] )
    
            # Set up movie rating props
            if len(customerList) > 1:
                if customerList[x]["rating"] == "no preference":
                    E.add_constraint(props[num][key]["rating"])
                else:
                    for prop in custProps[num]["rating"]:
                        movie = movies[key][4]
                        if float(prop.pref) <= float(movie):
                            E.add_constraint(prop >> props[num][key]["rating"])
                        else:
                            E.add_constraint(prop >> ~props[num][key]["rating"])

            elif len(customerList) == 1 and customerList[0]["rating"] == "no preference":
                E.add_constraint(props[num][key]["rating"])
            else:
                for prop in custProps[num]["rating"]:
                    movie = movies[key][4]
                    if float(prop.pref) <= float(movie):
                        E.add_constraint(prop >> props[num][key]["rating"])
                    else:
                        E.add_constraint(prop >> ~props[num][key]["rating"])
                    
            # Set up movie age props
            for prop in custProps[num]["age"]:
                movie = movies[key][0]
                if str(prop.pref) == movie:
                    E.add_constraint(prop >> props[num][key]["age"])
                    E.add_constraint(~prop >> ~props[num][key]["age"])

            # Set up movie runtime props
            for prop in custProps[num]["runtime"]:
                movie = movies[key][2]
                if int(movie) < 120:
                    movie = "short"
                else:
                    movie = "long"
                if str(prop.pref) == movie:
                    E.add_constraint(prop >> props[num][key]["runtime"])
                    E.add_constraint(~prop >> ~props[num][key]["runtime"])

            # Set up movie certificate props
            for prop in custProps[num]["certificate"]:
                movie = movies[key][1]
                if str(prop.pref) == movie:
                    E.add_constraint(prop >> props[num][key]["certificate"] )
                    E.add_constraint(~prop >> ~props[num][key]["certificate"] )

            for prop in custProps[num]["popularity"]:
                movie = movies[key][5]
                if str(prop.pref) == movie:
                    E.add_constraint(prop >> props[num][key]["popularity"] )
                    E.add_constraint(~prop >> ~props[num][key]["popularity"] )

        

        allRecs = []
        for key in movies.keys():
            
            # Movies with any false props do not fit user preferences and are not recommended
            E.add_constraint(~props[num][key]["age"] >> ~props[num][key]["recommend"])
            E.add_constraint(~props[num][key]["rating"] >> ~props[num][key]["recommend"])
            E.add_constraint(~props[num][key]["genre"] >> ~props[num][key]["recommend"])
            E.add_constraint(~props[num][key]["runtime"] >> ~props[num][key]["recommend"])
            E.add_constraint(~props[num][key]["certificate"] >> ~props[num][key]["recommend"])
            E.add_constraint(~props[num][key]["popularity"] >> ~props[num][key]["recommend"])
            allRecs.append(props[num][key]["recommend"])
        
        # Customer can only rent one movie
        constraint.add_exactly_one(E, allRecs)

        # Only one customer can rent a movie
        if customerNum > 1:
            for key in movies.keys():
                movieVer = []
                for x in range(customerNum):
                    movieVer.append(props[x+1][key]["recommend"])
                constraint.add_at_most_one(E,movieVer)
    
    return E

def testProps():
    """
    This function allows the user to test a set of propositions by negating all
    of them
    """


    prefList = ["genre",'rating','age','runtime','certificate', 'popularity']

    # Test customer props or movie props
    choice = input("Enter c to test customer props, m to test movie props: ")

    while choice != "c" and choice != "m":
        print("Invalid input. Please try again")
        choice = input("Enter c to test customer props, m to test movie props: ")

    # Choose prop to test
    choice2 = input("Enter the name of the proposition you'd like to test: ")

    while choice2 not in prefList:
        print("Invalid input. Please try again")
        choice2 = input("Enter the name of the proposition you'd like to test: ")
        

    return [choice, choice2]



def main():


    # Put movies in dictionary
    movies = GetMovies()

    
    global getAll
    # Initialize list of customer decisions
    customerList = []

    getChoice = input("Enter 1 for regular model, 2 for user input version, 3 for all recommendations: ")
    choiceOpts = ["1","2","3"]
    while getChoice not in choiceOpts:
        print("invalid input. Please try again")
        getChoice = input("Enter 1 for regular model, 2 for user input version, 3 for all recommendations: ")
    
    global custProps
    if getChoice == "1":
        
        global customerNum
        customerNum = getCustomers()

        getAll = False

        custProps = customerProps()

        #Set up movie propositions
        props = setUpProps(movies, customerNum)

        test = input("Do you want to test the constraints? (Y/N) ")
        while test != "Y" and test != "N":
            print("Invalid input. Please try again")
            test = input("Do you want to test the constraints? (Y/N) ")
        
        if test == "Y":
            choices = testProps()
        else: 
            choices = ['','']

        customerList.append({"genre": "", "rating": "", "runtime": "" , "popularity": "", "age" : "", "certificate": ""})

        T = example_theory(props, customerNum, movies,choices, customerList)

    elif getChoice == "2" or getChoice == "3":

        if getChoice == "2":
            customerNum = getCustomers()
        else: 
            customerNum = 1


        custProps = customerProps()

        props = setUpProps(movies, customerNum)

        print("Enter 'np' to any input to indicate no preference")

    # For each customer create a dictionary of their preferences and add it to customerList
        for x in range(customerNum):
            num = x + 1
            print("Customer", num)
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
        
        
        T = example_theory(props,customerNum, movies,['',''], customerList)
        
        if getChoice == "3":
            
            getAll = True
        else:
            getAll = False



    
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    solDict = {}
    if getAll == False:
        solution = T.solve()
        
        if solution != None:
            for key,value in solution.items():
                key = str(key)
                if key[1] != "." and value and str(key[0:4]) != "Cust" :
                    solDict[key] = value
            print(solDict) 
        else:
            print("No solution")
    else:
        allSols = T.models()
        for x in range(count_solutions(T)):
            solution = next(allSols)
            for key, value in solution.items():
                key = str(key)
                if key[1] != "." and value and str(key[0:4]) != "Cust" :
                    solDict[key] = value
            
        print(solDict)
               
    
    
    

    
# Get number of customers


main()

