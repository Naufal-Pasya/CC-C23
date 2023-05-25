const express = require('express');
const admin = require('firebase-admin');
const api = express.Router();
const axios = require('axios');
const { initializeApp } = require('firebase/app');
const { getFirestore, Timestamp, FieldValue } = require('firebase-admin/firestore');
const { getAuth, signInWithEmailAndPassword } = require('firebase/auth');

const serviceAccount = require('./serviceaccount.json');
const firebaseConfig = {
  apiKey: "AIzaSyBYswVYe3WD_ZTXV5d13SWIHOJpML71Roo",
  authDomain: "capstone-project-c23.firebaseapp.com",
  projectId: "capstone-project-c23",
  storageBucket: "capstone-project-c23.appspot.com",
  messagingSenderId: "567330959158",
  appId: "1:567330959158:web:82c991ba8675382a384d97",
  measurementId: "G-ZWP0C9WTTT"
};

const firebaseApp = initializeApp(firebaseConfig);
const auth = getAuth(firebaseApp);
const apiKey = '9741b01d83634b94a2492237232505';

// Initialize the Firebase app
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
  });

const db = getFirestore();
  
  api.post('/signup', async (req, res) => {
    const { email, password, name, address } = req.body;
  
      try {
        // Create a new user using Firebase Admin SDK
        const userRecord = await admin.auth().createUser({
          email,
          password,
        });
    
        // Optional: Add additional user data to Firestore or perform other operations
        const newUser = await db.collection('users').doc(userRecord.uid).set({
          email: email || '',
          name: name || '',
          address: address || '',
        });
  
        console.log(newUser);
    
        res.status(200).json({ message: 'Sign-up successful' });
      } catch (error) {
        console.error('Sign-up error:', error);
        res.status(500).json({ error: 'Sign-up failed' });
      }
    });
  
    api.post('/signin', async (req, res) => {
      const { email, password } = req.body;
    
      try {
    
        // Verify the provided password
        signInWithEmailAndPassword(auth, email, password)
        .then(() => {
          // Sign-in successful
          const user = auth.currentUser;
          const { uid } = user;
          res.status(200).json({ message: 'Sign-in successful', uid });
        })        
        .catch((error) => {
          // Sign-in failed, handle the error
          console.error('Sign-in error:', error);
          res.status(401).json({ error: 'Invalid credentials' });
        });
    } catch (error) {
      console.error('Sign-in error:', error);
      res.status(500).json({ error: 'Sign-in failed' });
    }
    });
  
    api.get('/user', async (req, res) => {

      const user = auth.currentUser;
    
      try {
        if (!user) {
          res.status(401).json({ error: 'User not authenticated' });
        } else {
          const uid = user.uid;
          // Retrieve user data from Firestore
          const userDoc = await db.collection('users').doc(uid).get();
    
          if (!userDoc.exists) {
            res.status(404).json({ error: 'User not found' });
          } else {
            const userData = userDoc.data();
            res.status(200).json(userData);
          }
        }
      } catch (error) {
        console.error('User data retrieval error:', error);
        res.status(500).json({ error: 'Failed to retrieve user data' });
      }
    });
    

    api.get('/weather-forecast', async (req, res) => {
      // Check if the user is authenticated
      const user = auth.currentUser;
      if (!user) {
        return res.status(401).json({ error: 'User not authenticated' });
      }
    
      const { location } = req.body;
    
      try {
        // Make a request to WeatherAPI to fetch weather forecast
        const response = await axios.get(`https://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${location}`);
        const data = response.data;
    
        // Process the response and extract relevant information
        const forecastDays = data.forecast.forecastday.map((forecast) => ({
          date: forecast.date,
          temperature: forecast.day.avgtemp_c,
          humidity: forecast.day.avghumidity,
          windSpeed: forecast.day.maxwind_kph,
          text: forecast.day.condition.text
        }));
    
        const weatherForecast = {
          location: data.location.name,
          forecast: forecastDays
        };
    
        res.status(200).json(weatherForecast);
      } catch (error) {
        console.error('Weather retrieval error:', error);
        res.status(500).json({ error: 'Failed to retrieve weather data' });
      }
    });
  
  module.exports = api;