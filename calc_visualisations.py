import sqlite3
import matplotlib.pyplot as plt

def avg_per_genre(imdb):
    #Calculate the average cost of a movie per genre
    conn = sqlite3.connect(imdb)
    c = conn.cursor()

    c.execute('''
    SELECT budget.budget, movie_genre.title, itunes.genre
    FROM budget
    JOIN movie_genre
    ON budget.title = movie_genre.title
    JOIN itunes
    ON movie_genre.genre_id = itunes.id
    ''')
    
    rows = c.fetchall()
    data = []
    budget = []
    genre = []
    for row in rows:
        data.append((row[0], row[1], row[2]))
        budget.append(row[0])
        genre.append(row[2])

    print(rows)
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    count7 = 0
    count8 = 0
    count9 = 0
    count10 = 0
    count11 = 0
    count12 = 0
    count13 = 0


    b1 = 0
    b2 = 0
    b3 = 0
    b4 = 0
    b5 = 0
    b6 = 0
    b7 = 0
    b8 = 0
    b9 = 0
    b10 = 0
    b11 = 0
    b12 = 0
    b13 = 0


    for row in rows:
        if row[2] == 'Drama':
            b1 += row[0]
            count1 += 1
        elif row[2] == 'Anime':
            b2 += row[0]
            count2 += 1
        elif row[2] == 'Documentary':
            b3 += row[0]
            count3 += 1
        elif row[2] == 'Thriller':
            b4 += row[0]
            count4 += 1
        elif row[2] == 'Action & Adventure':
            b5 += row[0]
            count5 += 1
        elif row[2] == 'Foreign':
            b6 += row[0]
            count6 += 1
        elif row[2] == 'Music Feature Films':
            b7 += row[0]
            count7 += 1
        elif row[2] == 'Comedy':
            b8 += row[0]
            count8 += 1
        elif row[2] == 'Horror':
            b9 += row[0]
            count9 += 1
        elif row[2] == 'Sci-Fi & Fantasy':
            b10 += row[0]
            count10 += 1
        elif row[2] == 'Kids & Family':
            b11 += row[0]
            count11 += 1
        elif row[2] == 'Musicals':
            b12 += row[0]
            count12 += 1
        elif row[2] == 'Romance':
            b13 += row[0]
            count13 += 1


    b1 /= count1
    b2 /= count2
    b3 /= count3
    b4 /= count4
    b5 /= count5
    b6 /= count6
    b7 /= count7
    b8 /= count8
    b9 /= count9
    b10 /= count10
    b11 /= count11
    b12 /= count12
    b13 /= count13
   

    # Create a bar graph of the results
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(genre, budget)
    ax.set_xlabel('Genre')
    ax.set_ylabel('Average Budget')
    ax.set_title('Average Budget by Genre')
    plt.xticks(rotation=90)
    plt.show()

    pass

def avg_per_rating(imdb):
    #calculate the average price for every .3 stars

    conn = sqlite3.connect(imdb)
    c = conn.cursor()

    c.execute('''
    SELECT budget.budget, imdb.title, imdb.rating
    FROM budget
    JOIN imdb
    ON budget.title = imdb.title
    ''')
    
    rows = c.fetchall()
    data = []
    budget = []
    rating = []
    for row in rows:
        data.append((row[0], row[1], row[2]))
        budget.append(row[0])
        rating.append(row[2])


    avg_six = 0
    count_six = 0
    avg_four = 0
    count_four = 0
    avg_last = 0
    count_last = 0

    for row in rows:
        if row[2] >= 8.6:
            avg_six += row[0]
            count_six += 1
        elif row[2] <= 8.5 and row[2] >= 8.4:
            avg_four += row[0]
            count_four += 1
        else:
            avg_last += row[0]
            count_last += 1  


    avg_six /= count_six
    avg_four /= count_four
    avg_last /= count_last

    figure, graph = plt.subplots()
    graph.bar([1,2,3], [avg_six, avg_four, avg_last], width=0.5)
    graph.set_title('Average Cost by Rating Range')
    graph.set_xlabel('Rating Range')
    graph.set_ylabel('Average Cost')
    graph.set_xticks([1,2,3])
    graph.set_xticklabels(['9.3 - 8.6', '8.5 - 8.4', '8.3 - 8.2'])
    plt.show()

    
    plt.scatter(budget, rating)
    plt.title('Movie Budget vs. Rating')
    plt.xlabel('Budget in millions')
    plt.ylabel('Rating (out of 10)')
    plt.show()
    
    pass


def rating_per_genre():
    #calculate the average rating per genre
    pass


avg_per_genre('imdb.db')
avg_per_rating('imdb.db')