import pandas as pd
from contacts.models import Contact

# reading the dummy contacts file
df = pd.read_csv('100-contacts.csv')

# converting to dictionary data type
contact_data = df.to_dict(orient="records")

print("starting entries")

# creating contacts
for row in contact_data:
    row["potential_name"] = f"{row.pop('first_name')} {row.pop('last_name')}"
    row["phone"] = "".join(row["phone"].split("-")) 
    contact = Contact.objects.create(**row)

print("contacts Added")