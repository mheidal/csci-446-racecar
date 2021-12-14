import multiprocessing
import turtle
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

class QLearnerMultiProcessedExperiments:

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

class ValueIteratorMultiProcessedExperiments:
    def __init__(self) -> None:
        self.lock: multiprocessing.Lock = multiprocessing.Lock()
        self.queue: Queue = Queue()
        self.output: List = []
        self.tracks: List = ["L-track"]
        self.default_epsilon = 0.5
        self.default_gamma = 1
        self.epsilon_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        self.gamma_values = [0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
        self.experiments_per_track: int = 10
        self.available_threads: int = 10

    def experiments(self) -> None:
        for track in self.tracks:
            processes: List[Process] = []
            self.lock.acquire()
            print(f"Track: {track}")
            self.lock.release()
            for i in range(len(self.epsilon_values)):
            # for i in range(1):
                processes.append(multiprocessing.Process(target=self._find_and_execute_policy, args=(deepcopy(track), i, self.epsilon_values[i], self.default_gamma, "epsilon",),
                                                         name=f"value_iter_epsilon_process_{track}_{i}"))

                processes.append(multiprocessing.Process(target=self._find_and_execute_policy, args=(deepcopy(track), i, self.default_epsilon, self.gamma_values[i], "gamma",),
                                                         name=f"value_iter_gamma_process_{track}_{i}"))


            for process in processes:
                process.start()
            self.lock.acquire()
            print(f"Processes 0-{len(self.epsilon_values) - 1} started for track: {track}")
            self.lock.release()
            for process in processes:
                self.output.append(self.queue.get())
                process.join()

            self.lock.acquire()
            print(f"Processes 0-{self.experiments_per_track - 1} joined for track: {track}")
            for out in self.output:
                print(f"Process {out[0]} reached the finish line in {out[1]} actions.\n\tE:{out[2]}\n\tG:{out[3]}")
            self.lock.release()
        return

    def _find_and_execute_policy(self, track_file: str, process_index: int, epsilon, gamma, test_param: str):
        vi: ValueIterator = ValueIterator(track_file=track_file, epsilon=epsilon, gamma=gamma)
        self.lock.acquire()
        print(f"Set up transition map for {process_index}_{test_param}")
        self.lock.release()
        best_action_by_state = vi.value_iteration()
        race_car = RaceCar(vi.model.start_state)
        actions_taken = 0
        self.lock.acquire()
        print(f"Process {process_index}_{test_param} is beginning execution of the racecar.")
        self.lock.release()
        i = 0
        while race_car.state != vi.model.special_state:
            i += 1
            if i % 2500 == 0:
                self.lock.acquire()
                print(f"Process {process_index}_{test_param} has transitioned {i} times.")
                self.lock.release()
            if i > 10000:
                self.lock.acquire()
                print(f"Process {process_index}_{test_param} has timed out.")
                self.queue.put((process_index, float('inf')))
                self.lock.release()
                return
            action = best_action_by_state[(race_car.state.x_pos, race_car.state.y_pos,
                                           race_car.state.x_vel, race_car.state.y_vel)]
            race_car.state = vi.model.transition(race_car.state, action[0], action[1])
            actions_taken += 1
        self.lock.acquire()
        print(f"Process {process_index}_{test_param} has finished execution of the racecar.")
        self.queue.put((process_index, actions_taken, epsilon, gamma))
        self.lock.release()


def execute_policy(track_file: str, epsilon, gamma):
    vi: ValueIterator = ValueIterator(track_file=track_file, epsilon=epsilon, gamma=gamma)
    best_action_by_state = vi.value_iteration()
    race_car = RaceCar(vi.model.start_state)
    actions_taken = 0
    i = 0
    vi.model.track.t = turtle.Turtle()
    vi.model.track.display_track_with_turtle()
    while race_car.state != vi.model.special_state:
        i += 1
        action = best_action_by_state[(race_car.state.x_pos, race_car.state.y_pos,
                                       race_car.state.x_vel, race_car.state.y_vel)]
        race_car.state = vi.model.transition(race_car.state, action[0], action[1])
        actions_taken += 1


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


    track_file = "L-track"
  #  vi: ValueIterator = ValueIterator(track_file=track_file, epsilon=0.5, gamma=1)
  #  best_action_by_state = vi.value_iteration()
    execute_policy(track_file, epsilon=0.5, gamma=1)
    x = 0
    while(True):
        x += 1


if __name__ == "__main__":
    main()
    # qlmpe: QLearnerMultiProcessedExperiments = QLearnerMultiProcessedExperiments()
    # qlmpe.experiments()
    # vimpe: ValueIteratorMultiProcessedExperiments = ValueIteratorMultiProcessedExperiments()
    # vimpe.experiments()

    # mpe.range_alpha()
    # mpe.range_gamma()
