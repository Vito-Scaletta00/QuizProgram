from pathlib import Path
import os
import glob


quizFiles_path = Path('./quizFiles/') #defines paths for quiz files and results
resultsPath = Path('./quizResults/')

if not resultsPath.exists():
    resultsPath.mkdir()

if not quizFiles_path.exists():
    quizFiles_path.mkdir()
    print("No quizzes found! Add quizzes to /quizFiles!")

def get_availableQuizzes():
    quizList = [quiz for quiz in quizFiles_path.glob('*.txt')] #creates a list for all the quizzes in the quizFiles directory, also handles non .txt files
    return quizList


def load_quizData(quizFile): #handles line formatting and assigning the varibles in selected quiz
    quizData = []
    with open(quizFile) as file:
        for line in file:
            splitQuiz = line.strip().split(';') #strips whitespace and splits each line at the semi-colon
            question = splitQuiz[0] #first index of splipresenting the tQuiz (question)
            answer = splitQuiz[1:-1] #starts from second index (potential answer) of splitQuiz and stops one before the last index (correct answer)
            correctAnswer = splitQuiz[-1]#Last index (answer)
            quizData.append((question, answer, correctAnswer))
    return quizData

def runQuiz(quizData): #untested, should run the quiz
    score = 0
    userAnswers = []

    for question, answer, correctAnswer in quizData:
        print ("\n" + question)
        for i, answer in enumerate(answer):
            print(f"{i+1}. {answer}")
        userAnswer = input("Enter the number of your answer: ")

        if answer[int(userAnswer) - 1] == correctAnswer:
            print("Correct!")
            score += 1
        else:
            print("Incorrect!")
        
        userAnswers.append(userAnswer)
    return score, userAnswers

def writeResults(quizFile, userName, userID, score, totalQuestions, userAnswers, percentage):
    quizName = quizFile.stem #removes .txt extension from the filename
    outputFilename = f"{quizName}_{userName}_results.txt" #sets the output filename to the Quiz Name + userName
    outputPath = resultsPath / outputFilename
    
    with open(outputPath, 'w') as file:
        file.write(f"\nQuiz {quizFile}")
        file.write(f"\nName: {userName}")
        file.write(f"\nID: {userID}")
        file.write(f"\nCorrect Answers: {score}/{totalQuestions}")
        file.write(f"\nPercentage: {percentage}")
        file.write(f"\nUser Answers: {', '.join(map(str, userAnswers))}\n")

    print(f"\nResults saved to {outputPath}")



def main():
    print ("Welcome to Quiz Program")
    userName = input(str("Please Type Your Name: "))
    userID = input(str("Please Type Your Student ID: ")) #grabs and assigns userName/ID to variables
    
    while True:
        quizzes = get_availableQuizzes() #calls the get_availableQuizzes function and assigns the returned quizList variable to quizzes

        if not quizzes:
            print("No quizzes available")
            break

        print("\n Available quizzes:")
        for number, quiz in enumerate(quizzes, start=1): #counts through quizzes, assigning a number to each
            print (f"{number}. {quiz.name}")

        quizChoice = input("Choose a quiz by entering the number: ")

        try: # compares quizIndex to quizChoice and creates an exception for error handling if condition is not met
            quizIndex = int(quizChoice) - 1
            if quizIndex < 0 or quizIndex >= len(quizzes): #handles error conditions
                raise ValueError
            quizFile = quizzes[quizIndex]
        except ValueError: #gracefully acknowledges error and loops back to start
            print("Invalid choice, try again")
            continue

        quizData = load_quizData(quizFile)
        score, userAnswers = runQuiz(quizData)

        totalQuestions = len(quizData)
        percentage = (score / totalQuestions) * 100
        print (f"\nQuiz completed! You scored {score}/{totalQuestions}")

        writeResults(quizFile,userName,userID,score,totalQuestions,userAnswers, percentage)
    


    

main()