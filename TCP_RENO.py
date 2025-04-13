# IMPLEMENTATION OF THE TCP TAHOE CONGESTION CONTROL PROTOCOL

import random
import matplotlib.pyplot as plt

class TCPReno:
    def __init__(self, mss, initial_ssthresh, max_rtt, loss_interval, rtt=1):
        self.mss = mss
        self.ssthresh = initial_ssthresh
        self.cwnd = mss
        self.rtt = rtt
        self.max_rtt = max_rtt
        self.loss_interval = loss_interval

        self.cwnd_list = []
        self.ssthresh_list = []
        self.rtt_list = []
        self.phase_list = []
        self.in_fast_recovery = False

    def loss(self, rtt_count):
        """
        This function simulates a loss event (tiemout or triple duplicate ACK)
        """
        if rtt_count % self.loss_interval == 0 and rtt_count > 0:
            return True, random.choice(['timeout', 'triple_duplicate_ack'])
        return random.random() < 0.02, random.choice(['timeout', 'triple_duplicate_ack'])

    def update_window(self, rtt_count):
        """
        Updating the congestion window as per the rules of the protocol
        """
        phase = "Slow Start" if self.cwnd < self.ssthresh and not self.in_fast_recovery else "Congestion Avoidance"
        
        has_loss, effect = self.loss(rtt_count)
        
        if has_loss:
            self.ssthresh = max(self.cwnd / 2, 2 * self.mss)
            if effect == 'triple_duplicate_ack':
                self.cwnd /= 2
                self.in_fast_recovery = True
                phase = "Fast Recovery"
            else:  # timeout
                self.cwnd = self.mss
                self.in_fast_recovery = False
                phase = "Timeout"
        else:
            if self.in_fast_recovery:
                self.cwnd += self.mss
                if self.cwnd >= self.ssthresh:
                    self.in_fast_recovery = False
                    phase = "Congestion Avoidance"
            elif self.cwnd < self.ssthresh:
                self.cwnd *= 2
            else:
                self.cwnd += self.mss
        
        self.cwnd = max(self.cwnd, self.mss)
        
        self.cwnd_list.append(self.cwnd)
        self.ssthresh_list.append(self.ssthresh)
        self.rtt_list.append(rtt_count)
        self.phase_list.append(phase)

    def run(self):
        """
        This function runs the TCP RENO protocol
        """
        for rtt_count in range(self.max_rtt):
            self.update_window(rtt_count)

    def plot_result(self):
        """
        This function plots the congestion window size and threshold over time
        """
        plt.figure(figsize=(10,6))
        plt.plot(self.rtt_list, self.cwnd_list, label='Congestion window size (cwnd)', color='blue', marker='o')
        plt.plot(self.rtt_list, self.ssthresh_list, label='Threshold (ssthresh)', color='red', linestyle='--')
        for i, phase in enumerate(self.phase_list):
            if phase in ["Timeout", "Fast Recovery"]:
                plt.axvline(x=self.rtt_list[i], color='green' if phase == "Timeout" else 'orange', 
                           linestyle=':', alpha=0.5, label='Loss' if i == 0 else "")
        plt.xlabel('Transmission time in RTT')
        plt.ylabel('Congestion window (in segments)')
        plt.title('TCP Reno Congestion Control Simulation')
        plt.grid(True)
        plt.legend()
        plt.yscale('linear')
        plt.xticks(range(0, self.max_rtt + 1, 5)) 
        plt.yticks(range(0, 51, 2)) 
        plt.xlim(0, self.max_rtt)  
        plt.ylim(0, 50)              
        plt.show()

    def print_log(self, max_entries=15):
        """This function prints the logged values"""
        print("RTT | cwnd | ssthresh | Phase")
        print("-" * 40)
        for i in range(min(max_entries, len(self.rtt_list))):
            print(f"{self.rtt_list[i]:3d} | {self.cwnd_list[i]:4.1f} | "
                  f"{self.ssthresh_list[i]:4.1f} | {self.phase_list[i]}")

def main():
    sim = TCPReno(
        mss=int(input("mss: ")),
        initial_ssthresh=int(input("initial threshold: ")),
        rtt=1,
        max_rtt=int(input("max rtt: ")),         
        loss_interval=int(input("loss interval: ")) 
    )

    sim.run()

    sim.print_log(max_entries=15)

    sim.plot_result()

if __name__ == '__main__':
    main()