from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import post, user, auth, vote

# do not need this line if we are going to use alembic to upgrade database changes
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# domain origins that we allow to make requests to our API (wildcard will allow all domains)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # can restrict which HTTP methods are allowed
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}


