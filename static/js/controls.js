var socket = io();

setInterval(function(){socket.emit("update",{sid:socket.id})}, 1000)

socket.on("update_ctrl",

    function (data) {
        //default stuff
        console.log("update received")

        var table = document.getElementById("tablebody")
        table.innerHTML = '';
        var rows = data["times"]
        rows.forEach(function (row) {
            domRow = document.createElement('tr')
            table.appendChild(domRow)
            i = 0
            row.forEach(function (elem) {
                if (i !== 4) {
                    var domCell = document.createElement('td');
                    domRow.appendChild(domCell);
                    domCell.appendChild(document.createTextNode(elem));
                }
                i++
            });
        });

        const zip = (a, b) => a.map((k, i) => [k, b[i]]);
        var active = zip(Array.from(document.getElementById("buttons").children), data["active"])
        active.forEach(function (elem) {
            elem[0].children[0].disabled = elem[1]
            elem[0].children[1].disabled = !elem[1]
        })
    });




