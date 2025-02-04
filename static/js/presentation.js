var socket = io();


socket.on('connect',
    function () {
        console.log("connected")
        const time = document.getElementById("time");


    });

socket.on("update_pres",

    function (data) {
        //default stuff
        console.log("update received")
        console.log(data)


        chart.data.labels = data["labels"]

        chart.data.datasets[0].data = data["data"]
        chart.data.datasets[0].backgroundColor = data["colors"]

        chart.update();
    });




