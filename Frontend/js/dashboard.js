var email;
var userId;
var savedRef;
var prefRef;
var linkTreeRef;
var starredUrls = [];
var crawledUrlsData;
var darkMode = true;
var db;

$.getJSON("./config.json", function(data) {
  var config = data;

  firebase.initializeApp(config);
  db = firebase.database();
  linkTreeRef = firebase.database().ref("linkTree");

  firebase.auth().onAuthStateChanged(function(user) {
    {
      if (user) {
        email = user.email;
        photoURL = user.photoURL;

        console.log(photoURL)

        document.getElementById("profile-img").src = photoURL;
        document.getElementById("user-name").innerHTML = user.displayName;

        userId = email.split("@")[0];

        savedRef = firebase.database().ref("users/" + userId + "/starred");
        prefRef = firebase.database().ref("users/" + userId + "/pref");

        savedRef.once("value").then(function(snapshot) {
          if (snapshot.val() === null) {
            starredUrls = [];
          } else {
            starredUrls = snapshot.val();
          }
          document.getElementById("savedCount").innerHTML = starredUrls.length;
        });

        prefRef
          .child("darkMode")
          .once("value")
          .then(function(snapshot) {
            if (snapshot.val() != null) {
              darkMode = snapshot.val();
            }
          });

        loadData(renderData);
      } else {
        window.location = "index.html";
      }
    }
  });
});

function signout() {
  firebase
    .auth()
    .signOut()
    .then(function() {})
    .catch(function(error) {});
}

function loadData(callback) {
  ref = db.ref("linkTree");

  ref.on("value", function(snapshot) {
    crawledUrlsData = snapshot.val();
    sortLinks();
    callback();
  });
}

function toggleDarkMode() {
  darkMode = !darkMode;
  prefRef.child("/darkMode").set(darkMode);
  renderData();
}
function renderData() {
  document.getElementById("saved-opp-container").innerHTML = "";
  document.getElementById("opp-container").innerHTML = "";

  const darkModeBtn = document.getElementById("dark-mode-btn");
  const nav = document.getElementById("nav-bar");
  const logoutBtn = document.getElementById("logout-btn");
  const userName = document.getElementById("user-name");

  if (darkMode) {
    darkModeBtn.setAttribute(
      "class",
      "fa fa-lightbulb dark-mode-btn dark-mode-btn-on"
    );
    nav.setAttribute("class", "dark-nav");
    logoutBtn.setAttribute("class", "logout-btn-dark");
    userName.setAttribute("class", "user-name-dark");
    document.body.style.backgroundImage = "url('./images/dark-bg.jpg')";
    document.body.style.color = "white";
  } else {
    darkModeBtn.setAttribute(
      "class",
      "fa fa-lightbulb dark-mode-btn dark-mode-btn-off"
    );
    nav.setAttribute("class", "light-nav");
    logoutBtn.setAttribute("class", "logout-btn-light");
    userName.setAttribute("class", "user-name-light");
    document.body.style.backgroundImage = "url('./images/light-bg.jpg')";
    document.body.style.color = "black";
  }

  for (data of crawledUrlsData) {
    if (typeof data === "object") {
      var cell = makeCell(data);
      var container;

      if (starredUrls.indexOf(data["url"]) > -1) {
        container = document.getElementById("saved-opp-container");
      } else {
        container = document.getElementById("opp-container");
      }
      container.appendChild(cell);
    }
  }
}

function makeCell(content) {
  var url = content["url"];
  var cell = document.createElement("div");
  var cellClass = document.createAttribute("class");
  cellClass.value = "cell";
  cell.setAttributeNode(cellClass);

  if ("img" in content) {
    var img = document.createElement("img");
    var src = document.createAttribute("src");
    src.value = content["img"];
    var imgClass = document.createAttribute("class");
    imgClass.value = "oppImg";
    img.setAttributeNode(imgClass);
    img.setAttributeNode(src);
    cell.appendChild(img);
  }

  var abstractContainer = document.createElement("div");
  var abstractContainerClass = document.createAttribute("class");
  abstractContainerClass.value = "abstract-container";
  abstractContainer.setAttributeNode(abstractContainerClass);

  if ("img" in content) {
  } else {
    abstractContainer.style.width = "95%";
  }

  var abstract = document.createElement("p");
  var abstractClass = document.createAttribute("class");
  abstractClass.value = "abstract-text";
  abstract.setAttributeNode(abstractClass);
  var abstractTxt = document.createTextNode(content["abstract"]);
  abstract.appendChild(abstractTxt);

  abstractContainer.appendChild(abstract);

  //Abstract buttons container
  var abstractButtonsContainer = document.createElement("div");
  var abstractButtonsContainerClass = document.createAttribute("class");
  abstractButtonsContainerClass.value = "abstract-buttons-container";
  abstractButtonsContainer.setAttributeNode(abstractButtonsContainerClass);

  //like btn
  var likeBtnContainer = document.createElement("div");

  var likeBtnIcon = document.createElement("span");
  var likeBtnIconClass = document.createAttribute("class");
  likeBtnIconClass.value = "far fa-thumbs-up like-dislike-btns";
  likeBtnIcon.setAttributeNode(likeBtnIconClass);

  var likesCountLbl = document.createElement("span");
  var likesCountLblClass = document.createAttribute("class");
  likesCountLblClass.value = "likes-dislikes-lbl";
  likesCountLbl.setAttributeNode(likesCountLblClass);

  if ("likes" in content) {
    likesCountLbl.innerHTML = content["likes"].length;
    if (content["likes"].includes(userId)) {
      likeBtnIconClass.value = "fas fa-thumbs-up like-dislike-btns";
      likeBtnIcon.setAttributeNode(likeBtnIconClass);
    }
  } else {
    likesCountLbl.innerHTML = 0;
  }

  likeBtnContainer.appendChild(likeBtnIcon);
  likeBtnContainer.appendChild(likesCountLbl);

  likeBtnIcon.onclick = function() {
    saveLikeDislike(url, "like");
  };
  abstractButtonsContainer.appendChild(likeBtnContainer);

  //dislike btn

  var dislikeBtnContainer = document.createElement("div");

  var dislikeBtnIcon = document.createElement("span");
  var dislikeBtnIconClass = document.createAttribute("class");
  dislikeBtnIconClass.value = "far fa-thumbs-down like-dislike-btns";
  dislikeBtnIcon.setAttributeNode(dislikeBtnIconClass);

  var dislikesCountLbl = document.createElement("span");
  var dislikesCountLblClass = document.createAttribute("class");
  dislikesCountLblClass.value = "likes-dislikes-lbl";
  dislikesCountLbl.setAttributeNode(dislikesCountLblClass);

  if ("dislikes" in content) {
    dislikesCountLbl.innerHTML = content["dislikes"].length;

    if (content["dislikes"].includes(userId)) {
      dislikeBtnIconClass.value = "fas fa-thumbs-down like-dislike-btns";
    }
  } else {
    dislikesCountLbl.innerHTML = 0;
  }

  dislikeBtnContainer.appendChild(dislikeBtnIcon);
  dislikeBtnContainer.appendChild(dislikesCountLbl);

  dislikeBtnIcon.onclick = function() {
    saveLikeDislike(url, "dislike");
  };

  abstractButtonsContainer.appendChild(dislikeBtnContainer);

  //Star button
  var starButton = document.createElement("div");

  var i = document.createElement("i");
  starButton.appendChild(i);

  if (starredUrls.indexOf(url) > -1) {
    var filledStarClass = document.createAttribute("class");
    filledStarClass.value = "fa fa-star star-icon";
    i.setAttributeNode(filledStarClass);
  } else {
    var emptyStarClass = document.createAttribute("class");
    emptyStarClass.value = "far fa-star star-icon";
    i.setAttributeNode(emptyStarClass);
  }

  starButton.onclick = function() {
    if (starredUrls.indexOf(url) > -1) {
      var emptyStarClass = document.createAttribute("class");
      emptyStarClass.value = "far fa-star star-icon";
      i.setAttributeNode(emptyStarClass);

      starredUrls = starredUrls.filter(item => item !== url);
      savedRef.set(starredUrls);
      renderData()
    } else {
      var filledStarClass = document.createAttribute("class");
      filledStarClass.value = "fa fa-star star-icon";
      i.setAttributeNode(filledStarClass);

      starredUrls.push(url);

      savedRef.set(starredUrls);
      renderData()
    }

    document.getElementById("savedCount").innerHTML = starredUrls.length;
  };

  abstractButtonsContainer.appendChild(starButton);

  abstractContainer.appendChild(abstractButtonsContainer);

  var keyWords = content["keywords"];

  var keywordsContainer = document.createElement("div");
  var kewordsContainerClass = document.createAttribute("class");
  kewordsContainerClass.value = "keywords-container";
  keywordsContainer.setAttributeNode(kewordsContainerClass);

  for (keyword of keyWords) {
    var keywordCell = document.createElement("p");
    var keywordCellClass = document.createAttribute("class");
    keywordCellClass.value = "keyword";
    keywordCell.setAttributeNode(keywordCellClass);
    var text = document.createTextNode(keyword);

    keywordCell.appendChild(text);

    keywordsContainer.appendChild(keywordCell);
  }

  cell.appendChild(abstractContainer);

  cell.appendChild(keywordsContainer);

  abstract.onclick = function() {
    window.open(url);
  };

  return cell;
}

function saveLikeDislike(url, action) {
  for (i = 0; i < crawledUrlsData.length; i += 1) {
    if (
      typeof crawledUrlsData[i] === "object" &&
      crawledUrlsData[i]["url"] == url
    ) {
      var obj = crawledUrlsData[i];

      if (url === obj["url"]) {
        if (action === "like") {
          if ("likes" in obj) {
            likes = obj["likes"];
            if (likes.includes(userId)) {
              likes = likes.filter(id => id != userId);
            } else {
              likes.push(userId);
            }
            obj["likes"] = likes;
          } else {
            obj.likes = [userId];
          }

          if ("dislikes" in obj) {
            var dislikes = obj["dislikes"];

            if (dislikes.includes(userId)) {
              dislikes = dislikes.filter(id => id != userId);
              obj["dislikes"] = dislikes;
            }
          }
        } else if (action === "dislike") {
          if ("dislikes" in obj) {
            dislikes = obj["dislikes"];
            if (dislikes.includes(userId)) {
              dislikes = dislikes.filter(id => id != userId);
            } else {
              dislikes.push(userId);
            }
            obj["dislikes"] = dislikes;
          } else {
            obj["dislikes"] = [userId];
          }
          if ("likes" in obj) {
            var likes = obj["likes"];

            if (likes.includes(userId)) {
              likes = likes.filter(id => id != userId);
              obj["likes"] = likes;
            }
          }
        }
      }

      crawledUrlsData[i] = obj;

      linkTreeRef.set(crawledUrlsData);
    }
  }
}

function sortLinks() {
  const n = crawledUrlsData.length;
  for (i = 0; i < n; i++) {
    for (j = 0; j < n - i - 1; j++) {
      if (crawledUrlsData[j]["rank"] < crawledUrlsData[j + 1]["rank"]) {
        var temp = crawledUrlsData[j];
        crawledUrlsData[j] = crawledUrlsData[j + 1];
        crawledUrlsData[j + 1] = temp;
      }
    }
  }
}
