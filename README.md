🧾 Smart Expense Tracker (Serverless AWS + AI)
🚀 Overview

The Smart Expense Tracker is a fully serverless application built on AWS, allowing users to add, categorize, and manage their expenses efficiently.
It uses AI-based text classification (via Hugging Face) to automatically categorize expenses based on their descriptions.

🧩 Architecture

The project follows a serverless architecture powered by AWS:

Component	AWS Service	Description
💡 Frontend  Postman / API Client	Interacts with API Gateway
🧠 AI Categorization	Hugging Face API (BART-large-MNLI)	Classifies expenses into categories
⚙️ Backend Logic	AWS Lambda	Handles Add, Delete, Get, and Categorize Expense operations
🗄️ Database	Amazon DynamoDB	Stores expenses using UserId (Partition Key) and ExpenseDate (Sort Key)
☁️ Storage	Amazon S3	Stores receipts or related files
🔐 API Gateway	Amazon API Gateway	Provides RESTful endpoints for CRUD operations
🧱 Infrastructure as Code	AWS CloudFormation	Defines and deploys the complete stack
🧰 Features

✅ Add new expenses with amount, date, and description
✅ AI-based expense categorization
✅ Fetch all expenses for a user
✅ Delete expenses by UserId + ExpenseDate
✅ Upload and link receipts via pre-signed S3 URLs
✅ 100% serverless deployment with CloudFormation
✅ Environment-ready for CI/CD using GitHub Actions

🧱 Folder Structure
Smart_Expense_Tracker/
│
├── infra/
│   └── SMT.yaml                # CloudFormation template
│
├── lambda/
│   ├── add_expense.py
│   ├── delete_expense.py
│   ├── get_expenses.py
│   ├── categorize_expense.py
│   └── presign_url.py
│
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
│
└── README.md                   # You’re reading it :)

⚡ API Endpoints
Method	Endpoint	Description
POST	/expenses	Add a new expense
GET	/expenses Fetch all expenses for a user
DELETE	/expenses/{userId}/{expenseDate}	Delete an expense
POST	/categorize	Categorize an expense using AI
POST	/presign	Generate pre-signed S3 upload URL
🧠 AI Integration

The categorization logic uses the Hugging Face BART-large-MNLI model to classify expense descriptions into categories like:

Food, Travel, Shopping, Bills, Health, Entertainment, etc.

Example:

{
  "description": "Lunch at Subway"
}


➡️ Returns:

{
  "category": "Food"
}

⚙️ Deployment Steps

Clone the repo

git clone https://github.com/CODEAFSARA/Smart_AI_Expense_Tracker.git
cd smart-expense-tracker





Verify

Visit the API Gateway console → Find your deployed endpoints

Test each API in Postman or through frontend

🔐 Environment Variables

Each Lambda function requires:

TABLE_NAME 
HF_TOKEN   
BUCKET_NAME 

🧪 Example JSON Inputs

Add Expense

{
  "userId": "user123",
  "amount": 250.0,
  "description": "Lunch at Subway",
  "date": "2025-11-07",
  "receiptKey": "optional-s3-key"
}


Delete Expense

DELETE /expenses/user123/2025-11-07

💼 Tech Stack

Language: Python (AWS Lambda)

Infrastructure: AWS CloudFormation

Database: DynamoDB

Storage: S3

API Gateway: REST endpoints

CI/CD: GitHub Actions

AI: Hugging Face Transformers API

🌍 Future Enhancements

Add Cognito-based user authentication

Integrate a frontend (React or Next.js)

Add analytics dashboard using QuickSight

Implement budget alerts with SNS

✨ Author

Afsara Kainat
💼 Developer |  DevOps + AI Engineer