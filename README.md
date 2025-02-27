To run the app -

1. Make sure the root folder has .env file with OPENAI_API_KEY
2. docker-compose up -d --build for running the backend - FASTAPI
3. cd frontend
4. npm i for installation
5. npm run dev (Might have problem on platforms other than windows)

Choices of technology -
- Since I wanted to do fast prototyping I chose FastAPI in python with Vue for the frontend.
- I chose docker for fast setup although for frontend there were some minor roadblocks so we're directly using npm run dev
