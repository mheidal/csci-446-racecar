from track import Track
from simulator import Simulator
def main():

    track: Track = Track()
    simulator: Simulator = Simulator()
    print("Welcome to the RaceTrack")
    pressed_key = input("Press Spacebar then Enter to Start")
    if(pressed_key == " "):
        print(track)
    print("w = Up, a = Left, s = Down, d = Right ")
    #call simulator
    simulator.manual_control()



if __name__ == "__main__":
    main()
