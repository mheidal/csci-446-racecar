from track import Track
from simulator import Simulator
def main():

    track: Track = Track()
    simulator: Simulator = Simulator()
    print("Welcome to the RaceTrack")
    pressed_key = input("Press Spacebar then Enter to Start")
    if(pressed_key == " "):
        print(track)
    print("W = Up, A = Left, S = Down, D = Right ")
    #call simulator
    simulator.manual_control()



if __name__ == "__main__":
    main()
