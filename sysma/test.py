from datetime import datetime

date = datetime.strptime("17/05/2023", "%d/%m/%Y")

print(date.date())