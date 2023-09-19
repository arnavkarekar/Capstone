        with open('benchmark_times.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            if i == 0:
                csvwriter.writerow(['Iteration', 'Time Taken (seconds)'])
            csvwriter.writerow([i, f"{time_taken:.6f}"])