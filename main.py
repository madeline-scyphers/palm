import os
import subprocess

from job.run import main

summary = """
----------------- NEW JOB -----------------

Job Name {job_name}


"""


job_name = main(house_domain_fraction=4, plot_size_x=12, plot_size_y=8)

print(job_name)

os.chdir("current_version")

print("process running!")
result = subprocess.run(["sh", "start_job.sh", job_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# process = subprocess.Popen(["sh", "view_queue.sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# result = subprocess.run(["sh", "start_job.sh", job_name], stdout=subprocess.PIPE,  stderr=subprocess.PIPE, text=True)
# result = subprocess.run(["sh", "view_queue.sh"], stdout=subprocess.PIPE,  stderr=subprocess.PIPE, text=True)

print("stdout: ", result.stdout)
# print(process.stdout.read())
# while True:
#     # outs, errs = process.communicate()
#     # print(outs, errs)
#     # output = process.stdout.readline()
#     # output = process.stderr.readline()
#     # if output:
#     #     print("printing output")
#     #     print(output.strip())
#     result = process.poll()
#     if result is not None:
#         break
# print(result.stderr)
# print(result.stdout)
print(summary.format(job_name=job_name))

print("script done")


"""

20211202T181145 8 8
20211202T181512 4 4
20211202T181902 16 8
20211202T182327 16 4
20211202T182606 16 2
20211202T182802 8 2
20211202T183000 4 2
20211202T183222 6 4
20211202T183426 12 4
20211202T183638 12 12
20211202T183847 12 8

"""