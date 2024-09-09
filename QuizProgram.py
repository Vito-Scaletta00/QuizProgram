from pathlib import Path
import os
import glob

quizFiles_path = Path('./quizFiles/') #assigns the path in the current working directory

def get_availableQuizzes():
    quizList = [quiz for quiz in quizFiles_path.glob('*.txt')] #creates a list for all the quizzes in the quizFiles directory, also handles non .txt files
    return quizList

def load_quizData(quizFile):
    quizData = []
    with open(quizFile) as file:
        for line in file:
            pass

def main():
    print ("Welcome to The Quiz Program")
    userName = input(str("Please Type Your Name: "))
    userID = input(str("Please Type Your Student ID: ")) #grabs and assigns usernName/ID to variables
    
    while True:
        quizzes = get_availableQuizzes() #calls the get_availableQuizzes function and assigns the returned quizList variable to quizzes

        if not quizzes:
            print("No quizzes available")
            break

        print("\n Available quizzes:")
        for number, quiz in enumerate(quizzes, start=1): #counts through quizzes, assigning a number to each
            print (f"{number}. {quiz.name}")

        quizChoice = input("Choose a quiz by entering the number: ")
    
    


    

main()