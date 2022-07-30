importScripts('https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js');
const firebaseConfig = {
    apiKey: "AIzaSyBUzBd7jlI4_xOOWk1Z21KGGeDmUogUL7s",
    authDomain: "tss-leave-15620.firebaseapp.com",
    projectId: "tss-leave-15620",
    storageBucket: "tss-leave-15620.appspot.com",
    messagingSenderId: "644297127885",
    appId: "1:644297127885:web:02256dc071fd129fb33684",
    measurementId: "G-8NFZMH0NY4"
  };


firebase.initializeApp(firebaseConfig);
const messaging=firebase.messaging();

messaging.setBackgroundMessageHandler(function (payload) {
    console.log(payload);
    const notification=JSON.parse(payload);
    const notificationOption={
        body:notification.body,
        icon:notification.icon
    };
    return self.registration.showNotification(payload.notification.title,notificationOption);
});