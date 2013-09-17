
function createDiv(text,elementclass) {
  var div = document.createElement('div'); 
  div.className = elementclass;
  div.innerHTML = text;

  return div;
}

function createNewLine()
{
  var br = document.createElement('br');
  return br;
}
