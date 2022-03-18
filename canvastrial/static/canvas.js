
    var canvas, ctx, flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    dot_flag = false;


    var gridLineWidth = 1;
    var gridSpacing = 30;
    function DrawGrid()
    {
        p = 0;
        // grid = document.getElementById('grid');
        // gridctx = grid.getContext('2d');
        ctx.lineWidth = 1

        bw = canvas.width;
        bh = canvas.height;

        for (var x = 0; x <= canvas.width; x += 40) {
            ctx.moveTo(0.5 + x + p, p);
            ctx.lineTo(0.5 + x + p, bh + p);
        }
    
        for (var x = 0; x <= canvas.height; x += 40) {
            ctx.moveTo(p, 0.5 + x + p);
            ctx.lineTo(bw + p, 0.5 + x + p);
        }
        ctx.strokeStyle = "black";
        ctx.stroke();
    }


    function OnWindowResize()
    {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        console.log(canvas.width)
        DrawGrid();
    }
    
    var x = "black",
        y = 2;




    function init() {
        canvas = document.getElementById('can');
        ctx = canvas.getContext("2d");

        OnWindowResize();
        window.onresize = OnWindowResize

        w = canvas.width;
        h = canvas.height;
    
        canvas.addEventListener("mousemove", function (e) {
            findxy('move', e)
        }, false);
        canvas.addEventListener("mousedown", function (e) {
            findxy('down', e)
        }, false);
        canvas.addEventListener("mouseup", function (e) {
            findxy('up', e)
        }, false);
        canvas.addEventListener("mouseout", function (e) {
            findxy('out', e)
        }, false);
  

    }




    function color(obj) {
        switch (obj.id) {
            case "green":
                x = "green";
                break;
            case "blue":
                x = "blue";
                break;
            case "red":
                x = "red";
                break;
            case "yellow":
                x = "yellow";
                break;
            case "orange":
                x = "orange";
                break;
            case "black":
                x = "black";
                break;
            case "white":
                x = "white";
                break;
        }
        if (x == "white") y = 14;
        else y = 2;
    
    }
    
    function draw() {
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
        ctx.lineTo(currX, currY);
        ctx.strokeStyle = x;
        ctx.lineWidth = y;
        ctx.stroke();
        ctx.closePath();
    }

    
    function erase() {
        var m = confirm("Want to clear");
        if (m) {
            ctx.clearRect(0, 0, w, h);
        }
    }


    
    function findxy(res, e) {
        if (res == 'down') {
            prevX = currX;
            prevY = currY;
            currX = e.pageX - canvas.offsetLeft;
            currY = e.pageY - canvas.offsetTop;
    
            flag = true;
            dot_flag= true;
            if (dot_flag) {
                console.log("drawing");
                    // we need to get every single coordinate when the mouse was down and store it in an array.
    
                    ctx.beginPath();
                    ctx.fillStyle = x;
                    ctx.fillRect(currX, currY, 2, 2);
                    ctx.closePath();
                    dot_flag = false;
                }
            }

        if (res == 'up' || res == "out") {
            flag = false;
        }
        if (res == 'move') {
            if (flag) {
                prevX = currX;
                prevY = currY;
                currX = e.pageX - canvas.offsetLeft;
                currY = e.pageY - canvas.offsetTop ;
                draw();
            }
        }
    }

 


