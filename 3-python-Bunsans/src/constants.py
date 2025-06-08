import re

DEBUG = True
LOG_PATTERN = re.compile(r'(\S+) - (\S+) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"')
ERROR_APPROX = 50
NUMBER_MOST_COMMON_HOURS = 5
PERCENTILE = 95

# from http.client import responses

# print(responses[404])


# def responses(status_code: int):

#     mapper_status_code_to_name = {
#         200: "OK",
#         404: "Not Found",
#         500: "Internal Server Error",
#     }
#     try:
#         return mapper_status_code_to_name[status_code]
#     except KeyError:
#         return "Unknown"
