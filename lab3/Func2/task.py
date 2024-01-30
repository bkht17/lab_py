def imdb_score(movie):
    if movie["imdb"] > 5.5:
        return True
    else:
        return False
    
def imdb_score_list(movies):
    bestmovies = []
    for x in movies:
        if imdb_score(x):
            bestmovies.append(x)

    return bestmovies

def movies_by_category(movies, category):
    movies_out = []
    for x in movies:
        if x["category"] == category:
            movies_out.append(x)
    
    return movies_out
            
def avg_score(movies,number):
    sum = 0
    for x in movies:
        sum += x["imdb"]
    
    return sum/number

def avg_score_by_category(movies, category):
    return avg_score(movies_by_category(movies, category),len(movies_by_category(movies, category)))
    

movies = [
{
"name": "Usual Suspects", 
"imdb": 7.0,
"category": "Thriller"
},
{
"name": "Hitman",
"imdb": 6.3,
"category": "Action"
},
{
"name": "Dark Knight",
"imdb": 9.0,
"category": "Adventure"
},
{
"name": "The Help",
"imdb": 8.0,
"category": "Drama"
},
{
"name": "The Choice",
"imdb": 6.2,
"category": "Romance"
},
{
"name": "Colonia",
"imdb": 7.4,
"category": "Romance"
},
{
"name": "Love",
"imdb": 6.0,
"category": "Romance"
},
{
"name": "Bride Wars",
"imdb": 5.4,
"category": "Romance"
},
{
"name": "AlphaJet",
"imdb": 3.2,
"category": "War"
},
{
"name": "Ringing Crime",
"imdb": 4.0,
"category": "Crime"
},
{
"name": "Joking muck",
"imdb": 7.2,
"category": "Comedy"
},
{
"name": "What is the name",
"imdb": 9.2,
"category": "Suspense"
},
{
"name": "Detective",
"imdb": 7.0,
"category": "Suspense"
},
{
"name": "Exam",
"imdb": 4.2,
"category": "Thriller"
},
{
"name": "We Two",
"imdb": 7.2,
"category": "Romance"
}
]

print(imdb_score(movies[0]))
print(imdb_score_list(movies))
print(movies_by_category(movies, "Thriller"))
print(avg_score(movies, len(movies)))
print(avg_score_by_category(movies, "Thriller"))
