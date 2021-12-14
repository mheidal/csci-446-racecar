import multiprocessing
from copy import deepcopy
from datetime import datetime
from multiprocessing import Process, Queue
from typing import List


from model import Model
from track import Track
from race_car import RaceCar
from state import State
from q_learner import QLearner
from value_iterator import ValueIterator
from turtle import Turtle

class MultiProcessedExperiments:

    def __init__(self) -> None:
        self.lock = multiprocessing.Lock()
        self.queue: Queue = Queue()
        self.output: float = 0.0
        self.tracks: List = ["L-track", "O-track", "R-track"]
        # self.episodes: List[int] = [300, 750, 1000, 2500, 5000, 10000, 20000, 30000, 25000, 50000]
        self.episodes: List[int] = [15000, 40000, 75000, 100000]
        # self.episodes: List[int] = [35000]
        # self.tracks: List = ["R-track"]
        self.experiments_per_track: int = 10
        self.available_threads: int = 20  # actually 24 but 20 allows for other tasks such as os, temp monitoring, etc

    def experiments(self) -> None:
        for track in self.tracks:
            processes: List[Process] = []
            self.lock.acquire()
            print(f"Track: {track}")
            self.lock.release()
            for i, episode in enumerate(self.episodes):
                processes.append(multiprocessing.Process(target=self._run_experiment, args=(deepcopy(track), i, episode, True,),
                                                         name=f"experiment_process_restart_{track}_{i}"))
                processes.append(multiprocessing.Process(target=self._run_experiment, args=(deepcopy(track), i, episode, False,),
                                                         name=f"experiment_process_stop_{track}_{i}"))
                processes.append(
                    multiprocessing.Process(target=self._run_experiment, args=(deepcopy(track), i, episode, True,),
                                            name=f"experiment_process_restart_{track}_{i}"))
                processes.append(
                    multiprocessing.Process(target=self._run_experiment, args=(deepcopy(track), i, episode, False,),
                                            name=f"experiment_process_stop_{track}_{i}"))

            for process in processes:
                process.start()
            self.lock.acquire()
            print(f"Processes 0-{self.experiments_per_track - 1} started for track: {track}")
            self.lock.release()
            for process in processes:
                self.output += self.queue.get()
                process.join()

            self.lock.acquire()
            print(f"Processes 0-{self.experiments_per_track - 1} joined for track: {track}\nAverage actions taken: {self.output/self.experiments_per_track}")
            self.lock.release()
        return

    def range_alpha(self) -> None:
        for track in self.tracks:
            processes: List[Process] = []
            self.lock.acquire()
            print(f"Track: {track}")
            self.lock.release()
            alpha: float = 1
            episodes: int = 25000
            decrement: float = 0.1/(self.available_threads + 1)
            for i in range(0, self.available_threads):
                processes.append(multiprocessing.Process(target=self._run_alpha_experiment, args=(deepcopy(track), i, episodes, alpha,),
                                                         name=f"alpha_experiment_process_{track}_{i}_alpha_{alpha}"))
                alpha -= decrement
            for process in processes:
                process.start()
            self.lock.acquire()
            print(f"Processes 0-{self.available_threads - 1} started for track: {track}")
            self.lock.release()
            for process in processes:
                self.output += self.queue.get()
                process.join()

            self.lock.acquire()
            print(f"Processes 0-{self.available_threads - 1} joined for track: {track}\nAverage actions taken: {self.output/self.available_threads}")
            self.lock.release()
        return

    def range_gamma(self) -> None:
        for track in self.tracks:
            processes: List[Process] = []
            self.lock.acquire()
            print(f"Track: {track}")
            self.lock.release()
            gamma: float = 1
            episodes: int = 25000
            decrement: float = 0.2 / (self.available_threads + 1)
            for i in range(0, self.available_threads):
                processes.append(multiprocessing.Process(target=self._run_gamma_experiment, args=(deepcopy(track), i, episodes, gamma,),
                                                         name=f"gamma_experiment_process_{track}_{i}_gamma_{gamma}"))
                gamma -= decrement
            for process in processes:
                process.start()
            self.lock.acquire()
            print(f"Processes 0-{self.available_threads - 1} started for track: {track}")
            self.lock.release()
            for process in processes:
                self.output += self.queue.get()
                process.join()

            self.lock.acquire()
            print(f"Processes 0-{self.available_threads - 1} joined for track: {track}\nAverage actions taken: {self.output/self.available_threads}")
            self.lock.release()
        return

    def _run_experiment(self, track: str, process_number: int, episodes: int = 25000, crash_type_restart: bool = True) -> None:
        start_time = datetime.now()
        q_learn: QLearner = QLearner(track=track, crash_type_restart=crash_type_restart)
        results: List[int] = q_learn.q_learn(number_of_episodes=episodes, viewable_episodes=1)
        end_time = datetime.now()

        sum: float = 0
        for result in results:
            sum += result
        sum = sum / len(results)

        self.lock.acquire()
        self.queue.put(sum)
        print(f"Finished track {track}-{'restart' if crash_type_restart else 'stop'} on process {process_number} in {end_time - start_time}\nEpisodes: {episodes}\nAverage actions taken: {sum}\n")
        self.lock.release()
        return

    def _run_alpha_experiment(self, track: str, process_number: int, episodes: int, alpha: float) -> None:
        start_time = datetime.now()
        self.lock.acquire()
        q_learn: QLearner = QLearner(track=track)
        self.lock.release()
        results: List[int] = q_learn.q_learn(number_of_episodes=episodes, viewable_episodes=5, alpha_rate=alpha)
        end_time = datetime.now()

        sum: float = 0
        for result in results:
            sum += result
        sum = sum / len(results)

        self.lock.acquire()
        self.queue.put(sum)
        print(f"Finished track {track} on process {process_number} in {end_time - start_time}\nAlpha: {alpha}\nAverage actions taken: {sum}\n")
        self.lock.release()
        return

    def _run_gamma_experiment(self, track: str, process_number: int, episodes: int, gamma: float) -> None:
        start_time = datetime.now()
        self.lock.acquire()
        q_learn: QLearner = QLearner(track=track, gamma=gamma)
        self.lock.release()
        results: List[int] = q_learn.q_learn(number_of_episodes=episodes, viewable_episodes=5)
        end_time = datetime.now()

        sum: float = 0
        for result in results:
            sum += result
        sum = sum / len(results)

        self.lock.acquire()
        self.queue.put(sum)
        print(f"Finished track {track} on process {process_number} in {end_time - start_time}\nGamma: {gamma}\nAverage actions taken: {sum}\n")
        self.lock.release()
        return

def execute_policy(best_action_by_state, track_file: str):
    model = Model(Track(track_file=track_file, turt=Turtle()))
    race_car = RaceCar(model.start_state)
    while race_car.state != model.special_state:

        action = best_action_by_state[(race_car.state.x_pos, race_car.state.y_pos,
                                       race_car.state.x_vel, race_car.state.y_vel)]
        race_car.state = model.transition(race_car.state, action[0], action[1])
    print('yahoo')



def main():
    # track: Track = Track()
    # simulator: Simulator = Simulator()
    # print("Welcome to the RaceTrack")
    # pressed_key = input("Press Spacebar then Enter to Start")
    # if(pressed_key == " "):
    #     print(track)
    # print("w = Up, a = Left, s = Down, d = Right ")
    # #call simulator
    # simulator.manual_control()
    track_file = "R-track"
    vi: ValueIterator = ValueIterator(track_file=track_file)
    best_action_by_state = vi.value_iteration()
    execute_policy(best_action_by_state, track_file)
    x = 0
    while(True):
        x += 1


if __name__ == "__main__":
    main()
    # mpe: MultiProcessedExperiments = MultiProcessedExperiments()
    # mpe.experiments()
    # mpe.range_alpha()
    # mpe.range_gamma()
