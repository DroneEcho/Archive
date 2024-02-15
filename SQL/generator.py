import csv, random, datetime
from faker import Faker

import csv

museums = ['Luvr', 'British Museum', 'Metropolitan Museum of Art', 'Orsay Museum', 'Hermitage', 'Museum of Modern Art', 'Prado']

art_type = ['Picture','Sculpture','Book','Graphics']

damage = ['Theft','Spoilage', 'arson', 'stab wound']

Validation = ['OK', 'FAKE']
fake = Faker(['en_US'])

art_cnt = 1000
vand_cnt = 500
author_cnt = 800
art_and_end_museum = []
id_and_date = []
with open('Art.csv', 'w', newline='') as angar:
    field_names = ['id', 'Title', 'Year', 'Price', 'Current_place', 'Art_type']
    writer = csv.DictWriter(angar, fieldnames=field_names)
    writer.writeheader()
    row_cnt = 0
    for row_cnt in range(art_cnt):
        numb = random.randrange(1, 4)
        year = fake.date_between_dates(datetime.date(1930,1, 1), datetime.date(2000, 1, 1))
        museum = museums[random.randint(0,len(museums)-1)]
        writer.writerow({'id' : row_cnt,
                         'Title': fake.sentence(nb_words = numb), 
                         'Year': year, 
                         'Price': random.randint(100000, 6000000),
                         'Current_place': museum,
                         'Art_type': art_type[random.randint(0,len(art_type)-1)]})
        art_and_end_museum.append(museum)
        id_and_date.append([row_cnt, year])


with open('Author.csv', 'w', newline='') as angar:
    field_names = ['Id', 'FullName', 'Birthday', 'City']
    writer = csv.DictWriter(angar, fieldnames=field_names)
    writer.writeheader()
    row_cnt = 0
    for row_cnt in range(author_cnt):
        date = fake.date_between_dates(datetime.date(1890,1, 1), datetime.date(1920, 1, 1))
        writer.writerow({'Id' : row_cnt,
                         'FullName': fake.name(), 
                         'Birthday': date, 
                         'City': fake.city()})

with open('Owner.csv', 'w', newline='') as angar:
    field_names = ['Id', 'FullName', 'PricePaid', 'PurchaceDate']
    writer = csv.DictWriter(angar, fieldnames=field_names)
    writer.writeheader()
    row_cnt = 0
    for row_cnt in range(art_cnt):
        writer.writerow({'Id' : row_cnt,
                         'FullName': fake.name(), 
                         'PricePaid':  random.randint(100000, 6000000), 
                         'PurchaceDate': fake.date_between_dates(datetime.date(2000,1, 1), datetime.date(2022, 1, 1))})
        
with open('Museum.csv', 'w', newline='') as angar:
    field_names = ['id', 'Name']
    writer = csv.DictWriter(angar, fieldnames=field_names)
    writer.writeheader()
    row_cnt = 0
    for row_cnt in range(len(museums)):
        writer.writerow({'id' : row_cnt,
                         'Name' : museums[row_cnt]})

M_history = []
with open('MuseumHistory.csv', 'w', newline='') as angar:
    field_names = ['MuseumId','ArtId','StartDate','EndDate','Hall']
    writer = csv.DictWriter(angar, fieldnames=field_names)
    writer.writeheader()
    row_cnt = 0
    
    for row_cnt in range(art_cnt):
        end_mus = art_and_end_museum[row_cnt]
        numb = random.randrange(1, 3)
        prevdate = fake.date_between_dates(datetime.date(1900,1, 1), datetime.date(2000, 1, 1))
        prev_museum = end_mus
        for i in range(numb):
            if i == numb - 1:
                newdate = 'now'
                cur_museum = end_mus
            else:
                newdate = fake.date_between_dates(prevdate, datetime.date(2000, 1, 1))
                cur_museum = random.choice(museums)
                while (cur_museum == prev_museum or (i == numb - 2 and cur_museum == end_mus)):
                    cur_museum = random.choice(museums)
            writer.writerow({'MuseumId' : museums.index(cur_museum),
                            'ArtId' : row_cnt,
                            'StartDate': prevdate,
                            'EndDate': newdate,
                            'Hall': random.randrange(1, 20)})
            prev_museum = cur_museum
            prevdate = newdate
            if i == numb - 1:
                M_history.append([row_cnt, cur_museum, prevdate, newdate])
        
with open('VandalismCase.csv', 'w', newline='') as angar:
    field_names = ['MuseumId', 'ArtId', 'AcidentDate', 'DamageType', 'FullName']
    writer = csv.DictWriter(angar, fieldnames=field_names)
    writer.writeheader()
    row_cnt = 0
    
    l = list(range(0, art_cnt))
    random.shuffle(l)
    for row_cnt in range(vand_cnt):
        list_art = []
        for i in M_history:
            if i[0] == l[row_cnt]:
                list_art.append(i)
        chosen_period = random.choice(list_art)
        writer.writerow({'MuseumId': museums.index(chosen_period[1]), 
                         'ArtId': l[row_cnt], 
                         'AcidentDate': fake.date(chosen_period[2], chosen_period[3]), 
                         'DamageType': damage[random.randint(0,len(damage)-1)], 
                         'FullName': fake.name()})

"""
with open('Author_And_Art.csv', 'w', newline='') as angar:
    field_names = ['AuthorId', 'PaintingId']
    writer = csv.DictWriter(angar, fieldnames=field_names)
    writer.writeheader()
    row_cnt = 0
    
    l = list(range(0, art_cnt))
    l_iter = 0
    random.shuffle(l)
    to_choose_works = art_cnt - author_cnt
    for row_cnt in range(author_cnt):
        paintings = random.randint(1, 5)
        if (paintings > 1):
            to_choose_works -= paintings - 1
        if (row_cnt == author_cnt - 1):
            paintings = to_choose_works
        for i in range(paintings):
            writer.writerow({'AuthorId': row_cnt,  
                         'PaintingId' : l[l_iter]})
            l_iter += 1
        
with open('Owner_And_Art.csv', 'w', newline='') as angar:
    field_names = ['OwnerId', 'PaintingId']
    writer = csv.DictWriter(angar, fieldnames=field_names)
    writer.writeheader()
    row_cnt = 0
    
    l = list(range(0, art_cnt))
    random.shuffle(l)
    
    l_o = list(range(0, art_cnt))
    random.shuffle(l_o)
    
    for row_cnt in range(art_cnt):
        writer.writerow({'OwnerId': l_o[row_cnt],
                        'PaintingId' : l[row_cnt]})

"""
with open('Val.csv', 'w', newline='') as angar:
    field_names = ['ArtId','Date_check','Validation_p']
    writer = csv.DictWriter(angar, fieldnames=field_names)
    writer.writeheader()
    row_cnt = 0
    
    l = list(range(0, art_cnt))
    random.shuffle(l)
    
    for row_cnt in range(100):
        writer.writerow({'ArtId': l[row_cnt],
                        'Date_check' : fake.date_between_dates(datetime.date(1900,1, 1), datetime.date(2000, 1, 1)),
                        'Validation_p': random.choice(Validation)})

