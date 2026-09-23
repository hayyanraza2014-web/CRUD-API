from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel, EmailStr, field_validator


# Create FastAPI application
app = FastAPI(
    title="CRUD API",
    description="User CRUD operations using FastAPI and JSON",
    version="1.0.0"
)

# Load users from JSON file
with open("database/users.json", "r") as f:
    users = json.load(f)


# Save users to JSON file
def save_users():
    with open("database/users.json", "w") as f:
        json.dump(users, f, indent=4)


# GET - Get all users
@app.get("/user")
def read_users():
    return users


# GET - Get one user
@app.get("/user/{user_id}")
def read_user(user_id: int):

    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

# Model for creating and replacing a user
class UserModel(BaseModel):
    name: str
    age: int
    email: EmailStr

    # Allow only Gmail addresses
    @field_validator("email")
    @classmethod
    def only_gmail_allowed(cls, value: EmailStr):
        if not str(value).lower().endswith("@gmail.com"):
            raise ValueError("Email must be a Gmail address")
        return value

# POST - Create a new user
@app.post("/create")
def create(user: UserModel):

    # Create a new user
    new_user = {
        "id": len(users) + 1,
        "name": user.name,
        "age": user.age,
        "email": str(user.email)
    }

    # Add user to the list
    users.append(new_user)

    # Save changes to JSON
    save_users()

    return new_user


# PUT - Update the complete user
@app.put("/user/{user_id}")
def update(user_id: int, user: UserModel):

    for old_user in users:

        # Find user by ID
        if old_user["id"] == user_id:

            # Update all user information
            old_user["name"] = user.name
            old_user["age"] = user.age
            old_user["email"] = str(user.email)

            # Save changes
            save_users()

            return old_user

    # User was not found
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# DELETE - Delete a user
@app.delete("/user/{user_id}")
def delete_user(user_id: int):

    for user in users:

        # Find user by ID
        if user["id"] == user_id:

            # Remove user
            users.remove(user)

            # Save changes
            save_users()

            return {
                "message": "User deleted successfully"
            }

    # User was not found
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

# Model for PATCH
# Only the field we want to partially update
class UserAgeUpdate(BaseModel):
    age: int
# PATCH - Update only part of a user
@app.patch("/user/{user_id}")
def update_user(user_id: int, user: UserAgeUpdate):

    for old_user in users:

        # Find user by ID
        if old_user["id"] == user_id:

            # Update only the age
            old_user["age"] = user.age

            # Save changes
            save_users()

            return old_user

    # User was not found
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )