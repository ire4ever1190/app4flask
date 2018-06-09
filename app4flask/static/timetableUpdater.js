var xhttp = new XMLHttpRequest();

  function getCookie(name)
  {
    let re = new RegExp(name + "=([^;]+)");
    let value = re.exec(document.cookie);
    return (value != null) ? unescape(value[1]) : null;
  }

xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let session;
        let response = JSON.parse(xhttp.responseText);
        let classes = document.getElementsByTagName("Class");
        let times = document.getElementsByTagName("Time");
        let teachers = document.getElementsByTagName("Teacher");
        let rooms = document.getElementsByTagName("Room");
        let day = document.getElementsByTagName("day");
        day[0].innerHTML = response[0]['day'];
        for (session=1; session < 10; session++) {
             let  x = session - 1;
            classes[x].innerHTML = response[0]['session' + session]['Info']['Class'];
            times[x].innerHTML = response[0]['session' + session]['Info']['Time'];
            teachers[x].innerHTML = response[0]['session' + session]['Info']['Teacher'];
            rooms[x].innerHTML = response[0]['session' + session]['Info']['Room'];

        }

    }
};
xhttp.open("POST", "/list", true);
    // Not the best way of doing it but it works
let username = document.getElementById("name");
xhttp.setRequestHeader("username", document.getElementById("name").innerHTML);
    //xhttp.setRequestHeader("username", getCookie("student_num"));

xhttp.send();
