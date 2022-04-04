$(document).ready(function () {
  var LINE_WIDTH = 60;
  var CANVAS_GRID_DIM = 100;
  var canvas = new fabric.Canvas('c');
  canvas_parent = $('#canvas-master-wrapper');
  drawing_line_width = $('#drawing-line-width');
  drawing_color = $('#drawing-color');

  active_brush = $('#Pointer');


  function RenderGridLines(canvas_width, canvas_height) {
    for (var y = 0; y < canvas_height; y += CANVAS_GRID_DIM){
      canvas.add(new fabric.Line([0, y, canvas_width, y], {
        stroke: "#000000",
        strokeWidth: 1,
        selectable: false
      }));
    }
    for (var x = 0; x < canvas_width; x += CANVAS_GRID_DIM) {
      canvas.add(new fabric.Line([x, 0, x, canvas_height], {
        stroke: "#000000",
        strokeWidth: 1,
        selectable: false
      }));
    }
  };

  function OnUserScroll(e){
    delta = (e.originalEvent.wheelDelta / 120)*2;
    LINE_WIDTH += delta;
    if (LINE_WIDTH < 0) LINE_WIDTH = 0
    console.log(LINE_WIDTH)
    AdjustLineWidth(LINE_WIDTH);
  }
  $('#canvas-wrapper').bind('mousewheel', function(e){OnUserScroll(e);});

  function AdjustCanvasDimensions() {
    let canvas_width = canvas_parent.width();
    let canvas_height = canvas_parent.height();

    canvas.setDimensions({
      width: canvas_width,
      height: canvas_height
    });
    // RenderGridLines(canvas_width, canvas_height);
  }
  
  function DeleteSelectedCanvasObjects(){
    var activeGroup = canvas.getActiveGroup();
    if (activeGroup) {
        var activeObjects = activeGroup.getObjects();
        for (let i in activeObjects) {
            canvas.remove(activeObjects[i]);
        }
        canvas.discardActiveGroup();
        canvas.renderAll();
    } else canvas.getActiveObject().remove();
  }

  function AdjustLineWidth(line_width){canvas.freeDrawingBrush.width = parseInt(line_width, 10) || 1;}
  function AdjustColor(color){canvas.freeDrawingBrush.color = color;}



  function __ChangeBrush(target){
    target_id = target.attr("id")
    active_brush = $('#' + target_id)
    if (active_brush.hasClass("not-fabric")){
      if (active_brush.attr("id") == "Eraser"){
        canvas.isDrawingMode = false;
      }
      return
    }
    canvas.isDrawingMode = (target_id != "Pointer")
    if(target_id != "Pointer"){
      canvas.freeDrawingBrush = new fabric[target_id + 'Brush'](canvas);
    }
    AdjustLineWidth(LINE_WIDTH)
    AdjustColor(drawing_color.get(0).value);
  }


  function __ChangeBrushHandleEvent(event){
    event.stopPropagation();
    event.stopImmediatePropagation();
  }

  function ChangeBrush(event){

    __ChangeBrushHandleEvent(event)
    __ChangeBrush($(event.target))
  }

  function CheckEraserEvent(){
    if (active_brush.attr("id") == "Eraser"){
      DeleteSelectedCanvasObjects()
    }
  }


  $('html').keyup(function(e){ if(e.keyCode == 46) DeleteSelectedCanvasObjects()});
  $('html').click(CheckEraserEvent)
  __ChangeBrush($('#Circle'))


  $(window).resize(function () {AdjustCanvasDimensions();})
  AdjustCanvasDimensions();
  $('.fa-solid.fa-spray-can.fa-lg').click(DeleteSelectedCanvasObjects)

  $(".brush").on('click', function(event){ChangeBrush(event);});

  drawing_color.on('change', function () {
    AdjustColor(this.value)
  });

})