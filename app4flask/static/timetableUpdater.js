var xhttp = new XMLHttpRequest();

xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var session;
        var response = JSON.parse(xhttp.responseText);
        var classes = document.getElementsByTagName("Class");
        var times = document.getElementsByTagName("Time");
        var teachers = document.getElementsByTagName("Teacher");
        var rooms = document.getElementsByTagName("Room");
        var day = document.getElementById("day");

        day.innerHTML = "Day " + response[0]['day'];
        for (session = 1; session < 10; session++) {
            var x = session - 1;
            classes[x].innerHTML = response[0]['session' + session]['Info']['Class'];
            times[x].innerHTML = response[0]['session' + session]['Info']['Time'];
            teachers[x].innerHTML = response[0]['session' + session]['Info']['Teacher'];
            rooms[x].innerHTML = response[0]['session' + session]['Info']['Room'];

        }

    }
}
function sendhttp(url = '/list'){
    xhttp.open("POST", url, true);
      // Not the best way of doing it but it works
    var username = document.getElementById("name");
    xhttp.setRequestHeader("student_num", username);
    xhttp.setRequestHeader("timezone", Intl.DateTimeFormat().resolvedOptions().timeZone);
    xhttp.send();
}
sendhttp()
