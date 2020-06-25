from retrying import retry
@retry(stop_max_attempt_number=2, wait_random_min=300, wait_random_max=1500, stop_max_delay=3000)
def stop_after_10_s():
    print("Stopping after 10 seconds")
    raise NameError('HiThere')


stop_after_10_s()
