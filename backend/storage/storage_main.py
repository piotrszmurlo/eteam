from fastapi import FastAPI

storage_app = FastAPI()


import csv

path_to_csv = "C:/Users/oem/OneDrive/Documents/I3/ERSMS/PROJEKT/eteam/backend/storage/data.csv"

def save_to_csv(name, sub, filename=path_to_csv):

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, sub])


from pydantic import BaseModel

class User(BaseModel):
    name: str
    sub: int

@storage_app.post("/add_user")
def add_user(new_user: User):

    save_to_csv(new_user.name, new_user.sub)
    print("data saved")

    return {"message": "User added successfully"}

    












@storage_app.get("/hello")
def root():
    
    return {"message": "hello storage"}

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"


# @storage_app.get("/hello")
# async def root(token):

#     decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
#     print(decoded_token)

#     return {"message": "hello storage"}


fake_db = {
    1: {"user_id": 1, "name": "John", "surname": "Cena", "company": "Facebook"},
    2: {"user_id": 2, "name": "Peter", "surname": "Smith", "company": "Google"},
    3: {"user_id": 3, "name": "Emily", "surname": "Johnson", "company": "Amazon"},
    4: {"user_id": 4, "name": "Michael", "surname": "Brown", "company": "Apple"},
    5: {"user_id": 5, "name": "Jessica", "surname": "Davis", "company": "Microsoft"}
}






@storage_app.get("/users/{user_id}")
async def give_user(user_id: int):
    if user_id in fake_db:
        return fake_db[user_id]["surname"]
    else:
        return {"error": "User not found"}