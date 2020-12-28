import sqlite3
import os
import sys
import time
import matplotlib.pyplot as p
import numpy as np


class DB_Class:  # Create DB And Load DB
    def __init__(self):
        self.Create_DB()

    def Create_DB(self):
        try:
            self.conn = sqlite3.connect('CovidData.db')
            print("Database Loading.. ")
            time.sleep(0.8)
            print("Database Loaded Successfully.. ")
            time.sleep(0.8)
            os.system('cls')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS PDATA 
            (NAME TEXT NOT NULL,
            AGE INT NOT NULL,
            CITY CHAR(50) NOT NULL,
            MOBILE INT PRIMARY KEY NOT NULL,
            STATUS TEXT)''')
        except sqlite3.Error as error:
            print("Error Occured while connecting with Database..!!", error)


class Patient_Data(DB_Class):
    def __init__(self):
        super().__init__()      # Call Parent Class
        self.Patient_Details()

    def Patient_Details(self):
        p_name = input("Enter Your Name : ")
        p_age = int(input("Enter Your Age : "))
        p_city = input("Enter Your City : ").lower()
        self.p_mobile = input("Enter Mobile Number : ")
        self.cursor.execute("""
        INSERT INTO PDATA(NAME, AGE, CITY, MOBILE, STATUS)
        VALUES(?,?,?,?,?)
        """, (p_name, p_age, p_city, self.p_mobile, None))


class Symptoms_Report(Patient_Data):
    def __init__(self):
        super().__init__()      # Call DB_Class
        self.Symptoms()

    def Symptoms(self):         # Check Symptoms
        yes, no = 0, 0

        symptoms = ['fever', 'cough', 'tiredness',
                    'headache', 'Difficulty in Breathing']

        for i in symptoms:
            uinput = input(f"\n Do You Have {i} Enter (y/n) : ")
            if uinput.lower() == 'y':
                yes += 1
            elif uinput.lower() == 'n':
                no += 1
            else:
                print("You Entered Wrong Choice ..!!")
                time.sleep(1)
                print("Please try Again..")
                time.sleep(1)
                self.conn.close()
                Main()

        if yes >= 3:

            self.cursor.execute(f'''
                UPDATE PDATA SET STATUS="POSITIVE" WHERE MOBILE={self.p_mobile} 
            ''')
            print("-------------- You Are Corona Positive --------------")
            time.sleep(1)
            print()
            print("------------ Thank you For Registration -------------")
            time.sleep(1)

        else:

            self.cursor.execute(f'''
                UPDATE PDATA SET STATUS="NEGATIVE" WHERE MOBILE={self.p_mobile} 
            ''')

            print("-------------- You Are Corona Negative --------------")
            time.sleep(1.2)
        self.conn.commit()
        self.conn.close()
        Main()


class Covid_Update(DB_Class):  # Covid Data Analysis Class

    def __init__(self):
        self.Area = []
        super().__init__()  # Call DB_Class Class
        print(""" 
            
                    [ 1] Specific City Data
                    [ 2] All City Data
                    [99] Exit
        """)
        self.choice = int(input("Enter Choice : "))
        if self.choice == 1:
            self.Specific_City_Data()
        elif self.choice == 2:
            self.All_data()
        elif self.choice == 99:
            Main()
        else:
            print("Please Enter Valid Choice..")
            sys.exit()

    def Specific_City_Data(self):  # Specific City Report
        positive, negative = [], []
        cityname = input("Enter City Name : ").lower()
        # query = self.cursor.execute(
        #     f"SELECT * FROM PDATA WHERE CITY= '{cityname}' AND STATUS = 'POSITIVE' ")
        # record = query.fetchall()
        # total = len(record)
        # print(f"Cases in {cityname} is {total}")

        query = self.cursor.execute(
            f"SELECT * FROM PDATA WHERE CITY= '{cityname}'")
        record = query.fetchall()
        for i in record:
            if i[4] == "POSITIVE":
                positive.append(i[4])
            else:
                negative.append(i[4])
        total_positive = len(positive)
        total_negative = len(negative)
        self.city_graph(total_positive, total_negative, cityname)
        Main()
    def city_graph(self, total_positive, total_negative, cityname):
        labels = 'Positive', 'Negative'
        sizes = [total_positive, total_negative]
        explode = (0, 0)
        fig1, ax1 = p.subplots()
        p.title(cityname)
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')
        p.show()

    def All_data(self):  # ALL City Report
        area, positive, color, negative = [], [], [], []

        query = self.cursor.execute(
            f"SELECT DISTINCT CITY,COUNT(STATUS) FROM PDATA WHERE STATUS='POSITIVE' GROUP BY CITY ")

        for j in query:
            area.append(j[0])
            positive.append(j[1])

        d = dict(zip(area, positive))
        for key, value in d.items():
            if key and value >= 6:
                color.append('red')
            elif key and value <= 2:
                color.append('green')
            elif key and value >= 3:
                color.append('orange')

        n_query = self.cursor.execute(
            f"SELECT DISTINCT CITY,COUNT(STATUS) FROM PDATA WHERE STATUS='NEGATIVE' GROUP BY CITY ")
        for a in n_query:
            negative.append(a[1])

        self.graph(area, positive, color)  # Graph1 Print
        print("Please Wait One More Report Loading..!!")
        time.sleep(1)

        self.graph_2(area, positive, negative)  # Graph2 Print
        Main()
    ######       Simple Graph    ########

    def graph(self, area, positive, color):
        p.bar(area, positive, color=color)
        p.title("Covid-19 Positive Area Report")
        p.xlabel("Area")
        p.ylabel("No. of Positive Patient")
        p.show()

    ###############     Added New One  ############
    def graph_2(self, area, positive, negative):

        p.bar(area, positive, label="Positive", color='red')

        p.bar(area, negative, label="Negative", color='green')
        p.legend()
        p.xlabel('City')
        p.ylabel('No. of cases')
        p.title('Covid-19 Analysis Report')
        p.show()


                   
def Main():          ## Start From Here

    try:
        print("""

                [ 1] Registration 
                [ 2] Check Corona Update
                [99] Exit
        """)
        choice = int(input(" \n Enter Your Choice : "))
        if choice == 1:
            Symptoms_Report()
        elif choice == 2:
            Covid_Update()
        elif choice == 99:
            sys.exit()
    except KeyboardInterrupt:
        print("\n Invalid Choice")


Main()
