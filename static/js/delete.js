var socket = io();

setInterval(function () {
    socket.emit("update", {sid: socket.id})
}, 1000)

socket.on("update_ctrl",

    function (data) {
        //default stuff
        console.log("update received")

        var table = document.getElementById("tablebody")
        table.innerHTML = '';
        var rows = data["times"]

        rows.forEach(function (row) {
            var domRow = document.createElement('tr')
            table.appendChild(domRow)
            var i = 0
            row.forEach(function (elem) {
                if (i !== 4) {
                    var domCell = document.createElement('td');
                    domRow.appendChild(domCell);
                    domCell.appendChild(document.createTextNode(elem));
                }
                i++
            });
            var domCell = document.createElement('td');
            domRow.appendChild(domCell);
            var domDelButton = document.createElement('button');
            domCell.appendChild(domDelButton);
            domDelButton.appendChild(document.createTextNode("Delete"));
            if (row[4] !== false) {
                domDelButton.setAttribute("class", "delete")
                domDelButton.addEventListener("click", function () {
                    socket.emit('delete', {identifier: row[4]})
                })
            } else {
                domDelButton.setAttribute("disabled", "disabled")

            }

        });


        var table = document.getElementById("tablebody2")
        table.innerHTML = '';
        var times_total = data["times_total"]
        var names = data["names"]
        for (i = 0; i < names.length; i++) {
            var domRow = document.createElement('tr')
            table.appendChild(domRow)
            var domCell = document.createElement('td');
            domRow.appendChild(domCell);
            domCell.appendChild(document.createTextNode(names[i]));
            var domCell = document.createElement('td');
            domRow.appendChild(domCell);
            var val = Math.floor(times_total[i] / 3600).toString().padStart(2, "0") + ':' + Math.floor((times_total[i] % 3600) / 60).toString().padStart(2, "0") + ':' + Math.floor((times_total[i] % 60)).toString().padStart(2, "0");
            domCell.appendChild(document.createTextNode(val));

            var domCell = document.createElement('td');
            domRow.appendChild(domCell);
            var domDelButton = document.createElement('button');
            domCell.appendChild(domDelButton);
            domDelButton.appendChild(document.createTextNode("Delete"));
            domDelButton.setAttribute("value", names[i])
            domDelButton.setAttribute("class", "delete")
            domDelButton.addEventListener("click", function (e) {
                socket.emit('delete', {identifier: [e.target.value]})
            })


        }


    });




