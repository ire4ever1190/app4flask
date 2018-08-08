


function sendhttp(url){
    var xhttp = new XMLHttpRequest();
	xhttp.open("get", url);
	  // Not the best way of doing it but it works
	var username = document.getElementById("name").innerHTML;
	xhttp.setRequestHeader("student_num", username);
	xhttp.setRequestHeader("timezone", Intl.DateTimeFormat().resolvedOptions().timeZone);
	xhttp.send();
	xhttp.onload = function listener() {
	        console.log(xhttp.response)
            var response = JSON.parse(xhttp.response);
            var session;
            var classes = document.getElementsByTagName("Class");
            var times = document.getElementsByTagName("Time");
            var teachers = document.getElementsByTagName("Teacher");
            var rooms = document.getElementsByTagName("Room");
            var day = document.getElementById("day");

            day.innerHTML = response[0]['day'];
            for (session = 1; session < 10; session++) {
                var x = session - 1;
                classes[x].innerHTML = response[0]['session' + session]['Info']['Class'];
                times[x].innerHTML = response[0]['session' + session]['Info']['Time'];
                teachers[x].innerHTML = response[0]['session' + session]['Info']['Teacher'];
                rooms[x].innerHTML = response[0]['session' + session]['Info']['Room'];

            }

    }
    }



function nextday(){
        var day = document.getElementById("day").innerHTML;
        var newday = parseInt(day) + 1
        sendhttp("/list/" + newday)
    }
function prevday(){
        var day = document.getElementById("day").innerHTML;
        var newday = parseInt(day) - 1
        sendhttp("/list/" + newday)
    }

window.onload = sendhttp("/list");

