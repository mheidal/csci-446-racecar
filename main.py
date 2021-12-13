import multiprocessing
from copy import deepcopy
from datetime import datetime
from multiprocessing import Process, Queue
from typing import List


from q_learner import QLearner
from value_iterator import ValueIterator


class MultiProcessedExperiments:

    def __init__(self) -> None:
        self.lock = multiprocessing.Lock()
        self.queue: Queue = Queue()
        self.output: float = 0.0
        self.tracks: List = ["L-track", "O-track", "R-track"]
        self.experiments_per_track: int = 12

    def experiments(self) -> None:
        for track in self.tracks:
            processes: List[Process] = []
            self.lock.acquire()
            print(f"Track: {track}")
            self.lock.release()
            for i in range(0, self.experiments_per_track):
                processes.append(multiprocessing.Process(target=self._run_experiment, args=(deepcopy(track), i,),
                                                         name=f"experiment_process_{track}_{i}"))
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

    def _run_experiment(self, track: str, process_number: int) -> None:
        start_time = datetime.now()
        self.lock.acquire()
        q_learn: QLearner = QLearner(track=track)
        self.lock.release()
        results: List[int] = q_learn.q_learn(number_of_episodes=25000, viewable_episodes=5)
        end_time = datetime.now()

        sum: float = 0
        for result in results:
            sum += result
        sum = sum / len(results)

        self.lock.acquire()
        self.queue.put(sum)
        print(f"Finished track {track} on process {process_number} in {end_time - start_time}\nAverage actions taken: {sum}\n")
        self.lock.release()
        return


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

    vi: ValueIterator = ValueIterator()
    print(vi.model.track)
    x = vi.value_iteration()
    print(x)


if __name__ == "__main__":
    main()
    # mpe: MultiProcessedExperiments = MultiProcessedExperiments()
    # mpe.experiments()
