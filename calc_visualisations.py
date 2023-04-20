import sqlite3
import matplotlib.pyplot as plt

def avg_per_genre():
    #Calculate teh average cost of a movie per genre
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

avg_per_rating('imdb.db')