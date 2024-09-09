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
            question = splitQuiz[0] #first index of split presenting the tQuiz (question)
            answer = splitQuiz[1].split(',') #starts from second index (potential answer) of splitQuiz and stops one before the last index (correct answer)
            correctAnswer = splitQuiz[-1]#Last index (answer)
            quizData.append((question, answer, correctAnswer))
    return quizData

def runQuiz(quizData): #Handles the formatting of questions for display, answer input, and scoring
    score = 0
    userAnswers = []

    for question, answers, correctAnswer in quizData:
        print ("\n" + question)

        for i, answer in enumerate(answers): #numbers each question
            print(f"{i+1}. {answer}")
        
        while True: #loop handles answer input, checking correct and incorrect answers, and handling numbers/characters outside of range
            userAnswer = input("Enter the number of your answer: ")

            if userAnswer.isdigit():
                if int(userAnswer) <= 0:
                    print("Invalid number, try again")
                    continue
                elif int(userAnswer) > len(answers):
                    print("Invalid number, try again")
                    continue
                userAnswers.append(userAnswer)
                if userAnswer.strip() == correctAnswer.strip(): #strips to make sure they're the same (takes into account formatting errors)
                    print("Correct!")
                    score += 1
                else:
                    print("Incorrect!")
                break
            else:
                print("Invalid input, please enter a number")
                continue
        

    return score, userAnswers

def writeResults(quizFile, userName, userID, score, totalQuestions, userAnswers, percentage): #Handles outputting to a text file located in /quizResults 
    quizName = quizFile.stem #removes .txt extension from the filename
    outputFilename = f"{quizName}_{userName}_results.txt" #sets the output filename to the Quiz Name + userName
    outputPath = resultsPath / outputFilename
    
    with open(outputPath, 'w') as file:
        file.write(f"\nQuiz {quizFile}")
        file.write(f"\nName: {userName}")                           #Generates the output file
        file.write(f"\nID: {userID}")
        file.write(f"\nCorrect Answers: {score}/{totalQuestions}")
        file.write(f"\nPercentage: {percentage}")
        file.write(f"\nUser Answers: {', '.join(map(str, userAnswers))}\n")

    print(f"\nResults saved to {outputPath}")



def main(): #handles literally everything else, userName/ID, calls all the other functions
    print ("Welcome to Quiz Program")
    userName = input(str("Please Type Your Name: "))
    userID = input(str("Please Type Your Student ID: ")) #grabs and assigns userName/ID to variables
    
    while True:
        quizzes = get_availableQuizzes() #calls the get_availableQuizzes function and assigns the returned quizList variable to quizzes

        if not quizzes:
            print("No quizzes available, add a properly formatted quiz to /quizFiles/ to get started! \nView correct format here: https://github.com/Vito-Scaletta00/QuizProgram/blob/main/README.md") #tells the user to add quizzes
            break

        print("\n Available quizzes:")
        for number, quiz in enumerate(quizzes, start=1): #counts through quizzes, assigning a number to each
            print (f"{number}. {quiz.name}")

        quizChoice = input("Choose a quiz by entering the number or enter q to quit: ")
        if quizChoice.lower() == "q":
            print("quitting")
            break

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
        print (f"\nQuiz completed! You scored {score}/{totalQuestions} You got {percentage} percent correct!")

        writeResults(quizFile,userName,userID,score,totalQuestions,userAnswers, percentage )

        retry = input("\nDo you want to quit or attempt another quiz? (q to quit, any key to continue): ")
        if retry.lower() == "q":
            print ("quitting")
            break


main()