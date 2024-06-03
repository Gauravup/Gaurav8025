letters = [['h','o','l','i','d','a','y'],

           ['p', 'r', 'o', 'g', 'r', 'a', 'm', 'm','i','n','g'],

           ['b','o','o','t','c','a','m','p'],

           ['f','l','o','w','c','h','a','r','t'],

           ['w', 'o', 'r', 'd', 's', 'c', 'a','p','e','s']]

words = [["hi","hay","day","had","lay","dal","lad","lid","hold","lady","hail"],

         ["go","an","in","no","on","map","mom","gap","gag","pig","man","ping",

          "pong","pram","prom","ramp"],

         ["am","at","to","cab","cap","cob","cop","map","mop","act","bat","camp",

          "comb","boom","pact","atom"],

         ["of","at","or","to","caw","cow","how","who","calf","claw","flaw","flow",

          "fowl","wolf","crow","half"],

         ["we","do","as","cap","caw","cop","cow","paw","cod","dew","pad","cape",

          "cope","crap","crew","crop","pace"]]
score=0
life=3
level=0

while level<5:
    print('level 1',level+1)
    print('given word is :',letters[level])
    print('create 3 word')
    

    count=0
    oldword=''
    word=''

    while count<3:
        word = input('Enter the word: ').lower()
        if(word != oldword):
            if(word in words[level]):
                print('well done------------------')
                score+=1
                count+=1
            # if count==3:
            #  break
            
                
            else:
                life-=1
                print('wrong guess word')
                
        else:
            print('same word does not count')
        
        if count==3:
         break
        
        if life ==0:
            print('game is over')
            print('your score is :',score)
            break
    count=0
    if level==4:
        print('game end')
        print('your score is',score)
        break
    else:
        print('do you want to play again :')
        play_again = input('enter yes or no :').lower()
        if (play_again == 'y'):
            level+=1
            
        else:
            print("Game is Over !")
            print("Your Score is :",score)
            print('if you want to play again plz restart the game')
            break

