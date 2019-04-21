var provider;

$.getJSON("./config.json", function(data) {
  var config = data;
  firebase.initializeApp(config);
  
  provider = new firebase.auth.GoogleAuthProvider();

  firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
      var displayName = user.displayName;
      var displayUrl = user.displayUrl
      var uid = user.email.split("@")[0];
      storeUser([uid, displayUrl]);

      document.getElementById("status").innerText = "Welcome " + displayName;
    } else {
    }
  });
});

document
  .getElementById("login-btn")
  .addEventListener("click", openGLogin, false);

function openGLogin() {
  provider.setCustomParameters({
    prompt: "select_account"
  });
  firebase.auth().signInWithRedirect(provider);
}

function storeUser(details) {
  var db = firebase.database();
  ref = db.ref("users/" + details[0]);

  ref.once("value").then(function(snapshot) {
    if (snapshot.val() === null) {
      ref.set(
        {
          createdOn: getDate(),
          name: details[1]
        },
        function(error) {
          if (error) {
            firebase.auth().signOut();
          } else {
            window.location = "dashboard.html";
          }
        }
      );
    } else {
      window.location = "dashboard.html";
    }
  });
}

function getDate() {
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth() + 1; //January is 0!
  var yyyy = today.getFullYear();

  if (dd < 10) {
    dd = "0" + dd;
  }

  if (mm < 10) {
    mm = "0" + mm;
  }

  today = mm + "/" + dd + "/" + yyyy;
  return today;
}
