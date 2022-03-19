// var jQueryScript = document.createElement('script');  
// jQueryScript.setAttribute('src','https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js');
// document.head.appendChild(jQueryScript);

var cursorCanvas, ccctx;


var x = "black",
strokeWidth = 50,
y = 2;
lastScroll = 0;
currentScroll = 0;



function AdjustStrokeWidth(amount)
{
    strokeWidth += amount;
}




function PrintSlider()
{
    console.log("CHANGING");

}

function UpdateStrokeWidth(newWidth)
{
    let p = document.getElementById("val")
    p.textContent = newWidth;
    strokeWidth = newWidth;
    // RenderBrushCursor(ccctx, e)

    

}
function RenderBrushCursor(context, e)
{

    context.strokeStyle = x;
    context.strokeWidth = 2;
    context.clearRect(0,0, cursorCanvas.width, cursorCanvas.height);
    context.fillStyle = x;
    context.beginPath();
    context.arc(e.pageX , e.pageY, strokeWidth, 0, 2 * Math.PI);
    context.stroke(); 
}
function AdjustToolkit()
{
    toolbar = $('#toolkit')
    toolbarHeight = toolbar.css("height");
    toolbar.css("top", 60 / 2);
    colorPicker = document.getElementById('colorPicker');

    colorPicker.onchange = function()
    {
        x = colorPicker.value;
    }

    UpdateStrokeWidth(3);
    let range = document.getElementById("slide")
    range.oninput = function(){
            UpdateStrokeWidth(range.value);
    }
}

$(document).ready(function(){
    AdjustToolkit();

    cursorCanvas = $('#cursorcanvas').get(0);
    ccctx = cursorCanvas.getContext('2d');

    const onMouseMove = (e) =>
    {
        RenderBrushCursor(ccctx, e)
   
    }


document.addEventListener('mousemove', onMouseMove);



cursorCanvas.addEventListener("wheel", function(evnt){
    console.log("SCROLL");
    RAD_INCREASE = 5;
    if(evnt.deltaY > 0)
    {
        UpdateStrokeWidth(strokeWidth - RAD_INCREASE);
    }
    else{
        UpdateStrokeWidth(strokeWidth + RAD_INCREASE);
    }
})

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


        console.log("WINDOW RESIZING");
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        cursorCanvas = $('#cursorcanvas').get(0);
        cursorCanvas.width = window.innerWidth;
        cursorCanvas.height = window.innerHeight;
        ccctx = cursorCanvas.getContext('2d');
     
    }
    





    function init() {
        canvas = document.getElementById('can');
        ctx = canvas.getContext("2d");
        cursorCanvas = $('#cursorcanvas').get(0);

        OnWindowResize();
        window.onresize = OnWindowResize

        w = canvas.width;
        h = canvas.height;
    
        cursorCanvas.addEventListener("mousemove", function (e) {
            findxy('move', e)
        }, false);
        cursorCanvas.addEventListener("mousedown", function (e) {
            findxy('down', e)
        }, false);
        cursorCanvas.addEventListener("mouseup", function (e) {
            findxy('up', e)
        }, false);
        cursorCanvas.addEventListener("mouseout", function (e) {
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
        console.log("drawing at " + prevX +  " : " + prevY)
        ctx.lineWidth = strokeWidth;
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
        ctx.lineTo(currX, currY);
        ctx.strokeStyle = x;
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
            console.log("MOUSE DOWN");
    
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

 


