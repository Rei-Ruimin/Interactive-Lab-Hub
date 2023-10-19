from __future__ import print_function
import qwiic_button 
import time
import sys

def run_example():

    print("\nSparkFun Qwiic Button Example 1")
    # for i in range(1,10000):
    #     my_button = qwiic_button.QwiicButton(i)

    #     if my_button.begin() == False:
    #         print("\nThe Qwiic Button isn't connected to the system. Please check your connection", \
    #             file=sys.stderr)
    #         # return
    #     else:
    #         print(f"{i} passed")
    #         exit(1)

    # print(i)

    my_button = qwiic_button.QwiicButton(110)

    if my_button.begin() == False:
        print("\nThe Qwiic Button isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    print("\nButton ready!")
    
    while True:   
        
        if my_button.is_button_pressed() == True:
            print("\nThe button is pressed!")

        else:    
            print("\nThe button is not pressed!")
            
        time.sleep(0.02)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)

