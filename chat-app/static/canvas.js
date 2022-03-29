$(document).ready(function () {


  var canvas = new fabric.Canvas('c');
  canvas_parent = $('#canvas-master-wrapper');

  function RenderGridLines(canvas_width, canvas_height) {
    var grid_size = 50;

    for (var y = 0; y < canvas_height; y += grid_size) {
      canvas.add(new fabric.Line([0, y, canvas_width, y], {
        stroke: "#000000",
        strokeWidth: 1,
        selectable: false
      }));
    }
    for (var x = 0; x < canvas_width; x += grid_size) {
      canvas.add(new fabric.Line([x, 0, x, canvas_height], {
        stroke: "#000000",
        strokeWidth: 1,
        selectable: false
      }));
    }
  };

  function AdjustCanvasDimensions() {
    let canvas_width = canvas_parent.width();
    let canvas_height = canvas_parent.height();

    canvas.setDimensions({
      width: canvas_width,
      height: canvas_height
    });
    RenderGridLines(canvas_width, canvas_height);

  }

  $(window).resize(function () {
    AdjustCanvasDimensions();
  })


  AdjustCanvasDimensions();

  drawing_line_width = $('#drawing-line-width');
  drawing_color = $('#drawing-color');

  function AdjustLineWidth(line_width){

    canvas.freeDrawingBrush.width = parseInt(line_width, 10) || 1;
  }
  function AdjustColor(color){
    canvas.freeDrawingBrush.color = color;

  }


  $(".brush").on('click', function(event){
    event.stopPropagation();
    event.stopImmediatePropagation();
    canvas.isDrawingMode = (this.id != "Pointer")
    if(this.id != "Pointer"){
      canvas.freeDrawingBrush = new fabric[this.id + 'Brush'](canvas);

        // if (canvas.freeDrawingBrush) {
        //   canvas.freeDrawingBrush.color = drawing_color.value;
        //   canvas.freeDrawingBrush.width = parseInt(drawing_line_width.value, 10) || 1;
        // }
    }
    AdjustLineWidth(drawing_line_width.get(0).value);
    AdjustColor(drawing_color.get(0).value);
  });

 drawing_line_width.on('change', function(){
      AdjustLineWidth(this.value);
  })

  drawing_color.on('change', function () {
    AdjustColor(this.value)
  });



  $('.canvas-container').css("overflow", "hidden");
  $('.canvas-container *').css({
    "overflow": "hidden"
  });
})