
# fungsi untuk melaporkan progress bruteforce
# iternum : nomor iterasi saat ini
# total : total iterasi yang akan dilakukan

def report_progress(iternum, total):
    print(f'Progress: {"{:,}".format(iternum)}/{"{:,}".format(total)} ({iternum/total*100:.2f}%)')
