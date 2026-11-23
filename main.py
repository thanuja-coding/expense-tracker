from fastapi import FastAPI, HTTPException, Header
import functions

app = FastAPI()


@app.post("/refresh")
def refresh_token(refresh_token: str = Header(...)):

    access_token = functions.refresh_access_token(refresh_token)

    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid or Expired Refresh Token")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }