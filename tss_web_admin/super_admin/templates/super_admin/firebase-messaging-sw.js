importScripts('https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js');

const firebaseConfig = {
        apiKey: "AIzaSyAoGTaeBjBPPiJFtTLt9LZ4rtbEKYWyH9Y",
        authDomain: "tss-leave.firebaseapp.com",
        projectId: "tss-leave",
        storageBucket: "tss-leave.appspot.com",
        messagingSenderId: "462968925453",
        appId: "1:462968925453:web:1d4792e45170fb1b5a9444",
        measurementId: "G-C21S9MZJSR"
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