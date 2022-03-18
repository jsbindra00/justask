// var jQueryScript = document.createElement('script');  
// jQueryScript.setAttribute('src','https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js');
// document.head.appendChild(jQueryScript);


function AdjustToolkit()
{
    toolbar = $('#toolkit')
    toolbarHeight = toolbar.css("height");
    toolbar.css("top", 60 / 2);

}

$(document).ready(function(){
    AdjustToolkit();
})
    
    
    var canvas, ctx, flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    dot_flag = false;




    const canvasColor = "rgb(250,250,250)";




    // function AdjustToolkit()
    // {
    //     toolbar = $('#toolkit');
    //     let toolbarHeight = css("height");
    //     toolbar.css("top", toolbarHeight / 2);


    // }


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
        // DrawGrid();
     
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
  

        ctx.fillStyle = canvasColor;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function color(obj) {
        x = obj.id;
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

 


