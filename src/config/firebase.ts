import { initializeApp, getApps } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyBjef8xlGrD7dyHtIJ6aytPztQ3S91pe9o",
  authDomain: "finisbank.firebaseapp.com",
  projectId: "finisbank",
  storageBucket: "finisbank.firebasestorage.app",
  messagingSenderId: "669819713979",
  appId: "1:669819713979:web:019e8f3d22442818e2ec9e",
};

const fireApp =
  getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
export const auth = getAuth(fireApp);
export const db = getFirestore(fireApp);
