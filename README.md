# Confessions Page Using Prince Cipher 

## Introduction
Confessions App is a web application that allows users to submit and view confessions anonymously. It provides a secure and private platform for users to share their thoughts without revealing their identities.

## Features
- User Registration: Users can create an account with a secure password using bcrypt for hashing and storing.
- Anonymous Confessions: Users can submit confessions without revealing their identities.
- Prince Cipher Encryption: Confessions are encrypted using the Prince cipher before storage, ensuring confidentiality.
- Decryption for Viewing: Decrypted confessions are shown to users when they request to see their confessions.

## Technologies Used
- Node.js
- Express.js
- EJS (Embedded JavaScript)
- Hashing
- Prince Cipher (for encryption)
- MongoDB (or any suitable database)

## Getting Started
1. Clone the repository: `git clone https://github.com/your_username/confessions-app.git`
2. Install dependencies: `npm install`
3. Set up the database (e.g., MongoDB).
4. Configure environment variables (if necessary).
5. Start the server: `npm start`

