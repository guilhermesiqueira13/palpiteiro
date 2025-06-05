{
  "version": 2,
  "builds": [
    {
      "src": "api/*.py",
      "use": "@vercel/python",
      "config": { "runtime": "python3.10" }
    },
    { "src": "public/**/*", "use": "@vercel/static" }
  ],
  "routes": [
    {
      "src": "/teams",
      "dest": "/api/teams.py",
      "methods": ["GET"]
    },
    {
      "src": "/predict",
      "dest": "/api/predict.py",
      "methods": ["POST"]
    },
    {
      "src": "/(.*)",
      "dest": "/public/$1"
    }
  ]
}
