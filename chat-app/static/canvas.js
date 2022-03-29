$(document).ready(function(){
  

  var canvas = new fabric.Canvas('c');
  canvas_parent = $('#canvas-master-wrapper');

  function RenderGridLines(canvas_width, canvas_height){
    var grid_size = 50;

    for(var y = 0; y < canvas_height; y+=grid_size){
      canvas.add(new fabric.Line([0, y, canvas_width, y], { stroke: "#000000", strokeWidth: 1, selectable:false}));
    }
    for(var x = 0; x < canvas_width; x+=grid_size){
      canvas.add(new fabric.Line([x, 0, x, canvas_height], { stroke: "#000000", strokeWidth: 1, selectable:false}));
    }


  };
  
  function AdjustCanvasDimensions(){
    let canvas_width = canvas_parent.width();
    let canvas_height = canvas_parent.height();

    canvas.setDimensions({width:canvas_width, height:canvas_height});
    RenderGridLines(canvas_width, canvas_height);
  

  }

  $(window).resize(function(){
    AdjustCanvasDimensions();
  })


  AdjustCanvasDimensions();


  var drawingModeEl = document.getElementById('drawing-mode'),
        drawingOptionsEl = document.getElementById('drawing-mode-options'),
        drawingColorEl = document.getElementById('drawing-color'),
        drawingLineWidthEl = document.getElementById('drawing-line-width')
    drawingModeEl.onclick = function() {
      canvas.isDrawingMode = !canvas.isDrawingMode;
      if (canvas.isDrawingMode) {
        drawingModeEl.innerHTML = 'Cancel drawing mode';
        drawingOptionsEl.style.display = '';
      }
      else {
        drawingModeEl.innerHTML = 'Enter drawing mode';
        drawingOptionsEl.style.display = 'none';
      }
    };

    if (fabric.PatternBrush) {
      var vLinePatternBrush = new fabric.PatternBrush(canvas);
      vLinePatternBrush.getPatternSrc = function() {
        var patternCanvas = fabric.document.createElement('canvas');
        patternCanvas.width = patternCanvas.height = 10;
        var ctx = patternCanvas.getContext('2d');
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 5;
        ctx.beginPath();
        ctx.moveTo(0, 5);
        ctx.lineTo(10, 5);
        ctx.closePath();
        ctx.stroke();
        return patternCanvas;
      };
      var hLinePatternBrush = new fabric.PatternBrush(canvas);
      hLinePatternBrush.getPatternSrc = function() {
        var patternCanvas = fabric.document.createElement('canvas');
        patternCanvas.width = patternCanvas.height = 10;
        var ctx = patternCanvas.getContext('2d');
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 5;
        ctx.beginPath();
        ctx.moveTo(5, 0);
        ctx.lineTo(5, 10);
        ctx.closePath();
        ctx.stroke();
        return patternCanvas;
      };
      var squarePatternBrush = new fabric.PatternBrush(canvas);
      squarePatternBrush.getPatternSrc = function() {
        var squareWidth = 10, squareDistance = 2;
        var patternCanvas = fabric.document.createElement('canvas');
        patternCanvas.width = patternCanvas.height = squareWidth + squareDistance;
        var ctx = patternCanvas.getContext('2d');
        ctx.fillStyle = this.color;
        ctx.fillRect(0, 0, squareWidth, squareWidth);
        return patternCanvas;
      };
      var diamondPatternBrush = new fabric.PatternBrush(canvas);
      diamondPatternBrush.getPatternSrc = function() {
        var squareWidth = 10, squareDistance = 5;
        var patternCanvas = fabric.document.createElement('canvas');
        var rect = new fabric.Rect({
          width: squareWidth,
          height: squareWidth,
          angle: 45,
          fill: this.color
        });
        var canvasWidth = rect.getBoundingRectWidth();
        patternCanvas.width = patternCanvas.height = canvasWidth + squareDistance;
        rect.set({ left: canvasWidth / 2, top: canvasWidth / 2 });
        var ctx = patternCanvas.getContext('2d');
        rect.render(ctx);
        return patternCanvas;
      };

    }
    document.getElementById('drawing-mode-selector').addEventListener('change', function() {
      if (this.value === 'hline') {
        canvas.freeDrawingBrush = vLinePatternBrush;
      }
      else if (this.value === 'vline') {
        canvas.freeDrawingBrush = hLinePatternBrush;
      }
      else if (this.value === 'square') {
        canvas.freeDrawingBrush = squarePatternBrush;
      }
      else if (this.value === 'diamond') {
        canvas.freeDrawingBrush = diamondPatternBrush;
      }
      else if (this.value === 'texture') {
        canvas.freeDrawingBrush = texturePatternBrush;
      }
      else {
        canvas.freeDrawingBrush = new fabric[this.value + 'Brush'](canvas);
      }
      if (canvas.freeDrawingBrush) {
        canvas.freeDrawingBrush.color = drawingColorEl.value;
        canvas.freeDrawingBrush.width = parseInt(drawingLineWidthEl.value, 10) || 1;
      }
    });


    drawingColorEl.onchange = function() {
      canvas.freeDrawingBrush.color = drawingColorEl.value;
    };
    drawingLineWidthEl.onchange = function() {
      canvas.freeDrawingBrush.width = parseInt(drawingLineWidthEl.value, 10) || 1;
    };

    
    if (canvas.freeDrawingBrush) {
      canvas.freeDrawingBrush.color = drawingColorEl.value;
      canvas.freeDrawingBrush.width = parseInt(drawingLineWidthEl.value, 10) || 1;
      canvas.freeDrawingBrush.shadowBlur = 0;
    }

    $('.canvas-container').css("overflow", "hidden");
    $('.canvas-container *').css({"overflow":"hidden"});


})