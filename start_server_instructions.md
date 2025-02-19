# in backend folder
uvicorn app.main:app --reload 

# In the frontend directory
npm run dev

# Once both servers are running:

Visit http://localhost:3000 in your browser
You should see:

A list of courses (including "Fundamentals of Apache Spark", "PySpark Programming", etc.)
Each course should show its title, description, and premium status
The navigation should work when clicking on courses

# Also, as a quick API check, you can test the backend directly by visiting:

http://localhost:8000/courses
http://localhost:8000/lessons

Note: Frontend server takes a few minutes, but is ready after Compiling step completed

<!-- client id -->
451335044929-lvkt6krc0vo36h0108pj15l9aac80kdn.apps.googleusercontent.com

<!-- client secret -->
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
<!-- creation date -->
18 February 2025 at 00:53:51 GMT-5
