// Firebase Configuration - Provided by User
const firebaseConfig = { 
   apiKey: "AIzaSyAnApUBw_8fB-WOKZpHfJildkECHDe0-xo", 
   authDomain: "codehub-966c6.firebaseapp.com", 
   projectId: "codehub-966c6", 
   storageBucket: "codehub-966c6.firebasestorage.app", 
   messagingSenderId: "890882130005", 
   appId: "1:890882130005:web:ed75089f9100b3a7a654dc", 
   measurementId: "G-BB8FP2LYN4" 
}; 

// Initialize Firebase (Compat Version)
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}

const db = firebase.firestore();
const auth = firebase.auth();
// Note: Analytics is usually initialized via firebase.analytics() in compat mode
const analytics = firebase.analytics ? firebase.analytics() : null;