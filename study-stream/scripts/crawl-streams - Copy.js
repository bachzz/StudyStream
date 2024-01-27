var vids = document.querySelectorAll('video')

var canvas = document.createElement('canvas');
canvas.width = 640;
canvas.height = 480;
var ctx = canvas.getContext('2d');
ctx.drawImage(vids[0], 0, 0, canvas.width, canvas.height);

var image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");

var link = document.getElementById('link-0');
  link.setAttribute('download', '0.png');
  link.setAttribute('href', image);
  link.click();